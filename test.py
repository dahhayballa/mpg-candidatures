import sqlite3, config
conn = sqlite3.connect(config.DB_PATH)
c = conn.cursor()
tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print('Tables:', [t[0] for t in tables])
cols = [r[1] for r in c.execute("PRAGMA table_info(candidates)").fetchall()]
print('Colonnes:', cols)
conn.close()