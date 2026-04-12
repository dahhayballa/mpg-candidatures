import sqlite3
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

# SQLite
sqlite_conn = sqlite3.connect("candidates.db")
cursor = sqlite_conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]

    if table_name == "sqlite_sequence":
        continue

    print(f"🚀 Migrating: {table_name}")

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    if not rows:
        continue

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [c[1] for c in cursor.fetchall()]

    for row in rows:
        data = dict(zip(columns, row))

        try:
            # مهم: upsert لتجنب duplicate errors
            supabase.table(table_name).upsert(data).execute()

        except Exception as e:
            print(f"❌ {table_name}: {e}")

print("✅ Migration completed!")