import sqlite3, config
conn = sqlite3.connect(config.DB_PATH)
c = conn.cursor()
print('Complets:', c.execute("SELECT COUNT(*) FROM candidates WHERE status='Complet' AND hors_delai=0").fetchone()[0])
print('Partiels:', c.execute("SELECT COUNT(*) FROM candidates WHERE status='Partiel' AND hors_delai=0").fetchone()[0])
print('Evalues:', c.execute("SELECT COUNT(*) FROM candidates WHERE ia_scored=1 AND hors_delai=0").fetchone()[0])
print('Score moyen:', c.execute("SELECT AVG(score_total) FROM candidates WHERE hors_delai=0 AND score_total IS NOT NULL").fetchone()[0])
conn.close()