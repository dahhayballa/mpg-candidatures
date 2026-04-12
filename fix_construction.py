#!/usr/bin/env python3
"""Fix import Construction métallique — Diplôme col 5"""
import sqlite3, sys, os, openpyxl
sys.path.append(os.path.dirname(__file__))
import config

DB_PATH    = config.DB_PATH
EXCEL_FILE = "Liste_FQ2026__1_.xlsx"
SPECIALTY  = "Construction métallique et soudure"

def get_score_niveau(d):
    d = str(d).lower().strip()
    if any(k in d for k in ["master","ingénieur","ingenieur"]): return 25, "Master"
    if any(k in d for k in ["licence","bac+3"]): return 20, "Licence"
    if any(k in d for k in ["bts","bac+2"]): return 20, "BTS"
    if "bt" in d: return 15, "BT"
    if "cap" in d: return 10, "CAP"
    if d.startswith("cc"): return 5, "CC"
    if "bac" in d: return 0, "Bac"
    if any(k in d for k in ["soudure","soudeur"]): return 10, "CAP/Soudure"
    return 0, "Inconnu"

conn = sqlite3.connect(DB_PATH)
wb   = openpyxl.load_workbook(EXCEL_FILE, data_only=True)
ws   = wb["Construction métallique et Soud"]
rows = list(ws.iter_rows(values_only=True))

imported = 0
for row in rows:
    if not any(v is not None for v in row): continue
    if row[1] is None or not isinstance(row[1], (int, float)): continue

    try:
        nom     = str(row[2] or "").strip()
        nni     = str(row[3] or "").strip()
        tel     = str(row[4] or "").strip()
        diplome = str(row[5] or "").strip()  # ← col 5

        if not nom or len(nom) < 3: continue

        score_exp  = min(20, max(0, float(row[7]  or 0)))
        score_mot  = min(20, max(0, float(row[8]  or 0)))
        score_adeq = min(20, max(0, float(row[9]  or 0)))
        score_dos  = min(10, max(0, float(row[10] or 0)))

        score_niveau, label = get_score_niveau(diplome)
        total = round(score_niveau + score_exp + score_mot + score_adeq + score_dos + 5.0, 1)
        mention = ("Excellent" if total>=80 else "Bon" if total>=65
                   else "Moyen" if total>=50 else "Non retenu")

        safe  = nom.lower().replace(' ','_').replace("'","")[:30]
        email = f"papier_{nni or safe}@papier.eetfp-mpg.mr"

        if conn.execute("SELECT id FROM candidates WHERE email_addr=?", (email,)).fetchone():
            print(f"   = {nom[:40]} (déjà importé)")
            continue

        conn.execute("""
            INSERT INTO candidates (
                email_addr, name, specialty, source, nni, telephone,
                score_total, score_niveau, score_experience,
                score_motivation, score_adequation, score_dossier,
                score_disponibilite, mention, ia_scored,
                has_cv, has_motivation, has_id, has_diplomas,
                status, hors_delai, num_emails,
                justif_niveau, note_globale, first_date, last_date
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (email, nom, SPECIALTY, "papier", nni, tel,
              total, score_niveau, score_exp, score_mot, score_adeq, score_dos,
              5.0, mention, 1, 1, 1, 1, 1,
              "Complet", 0, 1,
              f"{diplome} → {label} = {score_niveau}/25",
              f"Dossier papier. Diplôme: {diplome}",
              "2026-03-31", "2026-03-31"))

        print(f"   ✅ {nom[:35]:<35} | {diplome:<12} → {label:<15} | {total}/100 — {mention}")
        imported += 1

    except Exception as e:
        print(f"   ⚠ {e} — {str(row[:6])}")

conn.commit()
n = conn.execute("SELECT COUNT(*) FROM candidates WHERE source='papier'").fetchone()[0]
print(f"\n✅ {imported} candidats Construction métallique importés")
print(f"📊 Total papier en DB : {n}")
conn.close()
print("\n→ Lancez maintenant : python generer_liste_finale.py")