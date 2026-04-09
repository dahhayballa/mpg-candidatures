#!/usr/bin/env python3
"""Migration : ajoute les tables et colonnes manquantes."""
import sqlite3, config

conn = sqlite3.connect(config.DB_PATH)
c = conn.cursor()

# Colonnes manquantes dans candidates
existing = [r[1] for r in c.execute("PRAGMA table_info(candidates)").fetchall()]
for col, typedef in [
    ("retenu",  "INTEGER DEFAULT 0"),
]:
    if col not in existing:
        c.execute(f"ALTER TABLE candidates ADD COLUMN {col} {typedef}")
        print(f"  ✅ Colonne ajoutée : {col}")
    else:
        print(f"  ✓  Colonne existante : {col}")

# Table evaluations
c.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id        INTEGER NOT NULL,
        evaluateur          TEXT    NOT NULL,
        score_niveau        REAL    DEFAULT 0,
        score_experience    REAL    DEFAULT 0,
        score_motivation    REAL    DEFAULT 0,
        score_adequation    REAL    DEFAULT 0,
        score_dossier       REAL    DEFAULT 0,
        score_disponibilite REAL    DEFAULT 0,
        score_total         REAL    DEFAULT 0,
        mention             TEXT,
        note                TEXT    DEFAULT '',
        created_at          TEXT,
        UNIQUE(candidate_id, evaluateur)
    )
""")
print("  ✅ Table evaluations : OK")

# Table audit_log
c.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        action     TEXT,
        evaluateur TEXT,
        detail     TEXT,
        created_at TEXT
    )
""")
print("  ✅ Table audit_log : OK")

# Marquer hors délai
c.execute("UPDATE candidates SET hors_delai=1 WHERE last_date > '2026-03-31 14:00' AND hors_delai=0")
print(f"  ✅ Hors délai marqués : {c.rowcount}")

# Score dossier automatique
c.execute("""
    UPDATE candidates SET score_dossier=(
        CAST(has_cv AS REAL)*2.5 + CAST(has_motivation AS REAL)*2.5 +
        CAST(has_id AS REAL)*2.5  + CAST(has_diplomas AS REAL)*2.5
    ) WHERE score_dossier IS NULL
""")
print(f"  ✅ Scores dossier calculés : {c.rowcount}")

conn.commit()
conn.close()
print("\n  🎉 Migration terminée — lancez maintenant : python app.py")