import sqlite3, config

conn = sqlite3.connect(config.DB_PATH)
c = conn.cursor()

print("=== STATISTIQUES COMPLETES MPG FQ2026 ===")
print()
print("--- EMAILS ---")
print("Total emails recus       :", c.execute("SELECT SUM(num_emails) FROM candidates").fetchone()[0])
print("Candidats uniques        :", c.execute("SELECT COUNT(*) FROM candidates").fetchone()[0])
print("Dans les delais          :", c.execute("SELECT COUNT(*) FROM candidates WHERE hors_delai=0").fetchone()[0])
print("Hors delai               :", c.execute("SELECT COUNT(*) FROM candidates WHERE hors_delai=1").fetchone()[0])
print()
print("--- DOSSIERS ---")
print("Complets  (4/4)          :", c.execute("SELECT COUNT(*) FROM candidates WHERE status='Complet' AND hors_delai=0").fetchone()[0])
print("Partiels  (2-3/4)        :", c.execute("SELECT COUNT(*) FROM candidates WHERE status='Partiel' AND hors_delai=0").fetchone()[0])
print("Incomplets (1/4)         :", c.execute("SELECT COUNT(*) FROM candidates WHERE status='Incomplet' AND hors_delai=0").fetchone()[0])
print("Vides     (0/4)          :", c.execute("SELECT COUNT(*) FROM candidates WHERE status='Vide' AND hors_delai=0").fetchone()[0])
print()
print("--- RESULTATS IA ---")
print("Excellent  (>=80)        :", c.execute("SELECT COUNT(*) FROM candidates WHERE mention='Excellent' AND hors_delai=0").fetchone()[0])
print("Bon        (65-79)       :", c.execute("SELECT COUNT(*) FROM candidates WHERE mention='Bon' AND hors_delai=0").fetchone()[0])
print("Moyen      (50-64)       :", c.execute("SELECT COUNT(*) FROM candidates WHERE mention='Moyen' AND hors_delai=0").fetchone()[0])
print("Non retenu (<50)         :", c.execute("SELECT COUNT(*) FROM candidates WHERE mention='Non retenu' AND hors_delai=0").fetchone()[0])
print("Non evalue               :", c.execute("SELECT COUNT(*) FROM candidates WHERE mention IS NULL AND hors_delai=0").fetchone()[0])
print()
print("--- DATES ---")
print("Premier email            :", c.execute("SELECT MIN(first_date) FROM candidates").fetchone()[0])
print("Dernier email            :", c.execute("SELECT MAX(last_date) FROM candidates").fetchone()[0])
print()
print("--- TOP 5 PLUS D'ENVOIS ---")
for r in c.execute("SELECT name, email_addr, num_emails FROM candidates ORDER BY num_emails DESC LIMIT 5").fetchall():
    print(f"  {r[0][:30]:<30} {r[1][:30]:<30} {r[2]} emails")
print()
print("--- PAR SPECIALITE ---")
for r in c.execute("SELECT specialty, COUNT(*) as n FROM candidates WHERE hors_delai=0 GROUP BY specialty ORDER BY n DESC").fetchall():
    print(f"  {str(r[0])[:45]:<45} : {r[1]}")
print()
print("--- SCORE MOYEN PAR SPECIALITE ---")
for r in c.execute("""
    SELECT specialty, COUNT(*) as n,
           ROUND(AVG(score_total),1) as avg,
           MAX(score_total) as max_score
    FROM candidates
    WHERE hors_delai=0 AND score_total IS NOT NULL
    GROUP BY specialty ORDER BY avg DESC
""").fetchall():
    print(f"  {str(r[0])[:40]:<40} n={r[1]:>4}  moy={r[2]:>5}  max={r[3]:>5}")

conn.close()