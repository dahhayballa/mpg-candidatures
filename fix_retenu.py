#!/usr/bin/env python3
"""Fix retenu field - correct specialty matching with accents"""
import sqlite3, sys, os
sys.path.append(os.path.dirname(__file__))
import config

conn = sqlite3.connect(config.DB_PATH)
c = conn.cursor()

# Voir toutes les spécialités exactes en DB
print("=== Spécialités exactes dans DB ===")
specs = c.execute("""
    SELECT specialty, COUNT(*) as n
    FROM candidates
    WHERE hors_delai=0
    GROUP BY specialty
    ORDER BY n DESC
""").fetchall()
for s, n in specs[:15]:
    print(f"  [{s}] : {n}")

print()

# Reset
c.execute("UPDATE candidates SET retenu=0")

QUOTAS = [
    ("HSE",                                40),
    ("Électricité industrielle",           30),
    ("Tuyauterie industrielle",            30),
    ("Construction métallique et soudure", 40),
    ("Maintenance industrielle",           20),
    ("Techniques minières",                20),
    ("Opérations pétrolières et gazières", 20),
]

total = 0
for specialty, quota in QUOTAS:
    # Récupérer tous les candidats de cette spécialité
    # Utiliser = exact + variantes connues
    ids = c.execute("""
        SELECT id, name, score_total, specialty FROM candidates
        WHERE hors_delai=0
        AND (
            specialty = ?
            OR specialty = REPLACE(?, 'é', 'e')
            OR specialty = REPLACE(REPLACE(?, 'é', 'e'), 'è', 'e')
            OR specialty = REPLACE(?, 'è', 'e')
        )
        ORDER BY score_total DESC, first_date ASC
        LIMIT ?
    """, (specialty, specialty, specialty, specialty, quota)).fetchall()

    for (cid, name, score, spec) in ids:
        c.execute("UPDATE candidates SET retenu=1 WHERE id=?", (cid,))

    print(f"{specialty[:40]:<40} : {len(ids):>3} retenus")
    total += len(ids)

conn.commit()
print(f"\nTOTAL retenu=1 : {total}")
conn.close()
print("\n→ Lancez : python liste_attente.py")