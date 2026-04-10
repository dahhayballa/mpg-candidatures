#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════
  MPG — Correction des scores suspects (Phase 4b)
  Ré-évalue les candidats avec score ≤ 10 ou
  "Non spécifié" pour corriger les faux 0.
  Usage : python fix_scores.py
════════════════════════════════════════════════════════
"""

import sqlite3, json, time, os, sys
from datetime import datetime
import urllib.request, urllib.error
import config

EVALUATEUR_IA = "IA — Claude (Anthropic)"
CHECKPOINT_FILE = "fix_scores_checkpoint.json"

# ─────────────────────────────────────────────────────
#  Appel Claude
# ─────────────────────────────────────────────────────

def call_claude(prompt: str, max_retries: int = 3) -> str:
    url = "https://api.anthropic.com/v1/messages"
    body = json.dumps({
        "model": "claude-sonnet-4-5",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")
    headers = {
        "x-api-key":         config.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type":      "application/json",
    }
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=body, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["content"][0]["text"]
        except urllib.error.HTTPError as e:
            err = e.read().decode()
            if e.code == 429:
                wait = 20 * (attempt + 1)
                print(f"\n   ⏳ Rate limit — attente {wait}s…", flush=True)
                time.sleep(wait)
            else:
                print(f"\n   ⚠ HTTP {e.code}: {err[:150]}")
                time.sleep(10)
        except Exception as e:
            print(f"\n   ⚠ Réseau (tentative {attempt+1}): {e}")
            time.sleep(15)
    return ""


# ─────────────────────────────────────────────────────
#  Prompt amélioré — plus clément sur le contenu manquant
# ─────────────────────────────────────────────────────

SPECIALTIES_CONTEXT = {
    "Maintenance industrielle":           "mécanique industrielle, maintenance préventive/corrective",
    "Électricité industrielle":           "électricité industrielle, automatismes, câblage",
    "Tuyauterie industrielle":            "tuyauterie, robinetterie, soudure de tuyaux",
    "Construction métallique et soudure": "soudure MIG/TIG, charpente métallique",
    "HSE":                                "hygiène sécurité environnement, prévention des risques",
    "Opérations pétrolières et gazières": "pétrole et gaz, opérations pétrolières",
    "Techniques minières":                "exploitation minière, géologie, traitement des minerais",
    "Non spécifié":                       "secteur industriel, minier ou pétrolier",
}


def build_prompt_v2(candidate: dict) -> str:
    """
    Prompt amélioré :
    - Si contenu absent → ne pas pénaliser, évaluer la disponibilité et le dossier
    - Détecter la spécialité depuis le contenu même si non déclarée
    - Être juste : un dossier vide ≠ candidat nul
    """
    specialty = candidate.get("specialty", "Non spécifié")
    context   = SPECIALTIES_CONTEXT.get(specialty, SPECIALTIES_CONTEXT["Non spécifié"])

    body  = (candidate.get("email_body_full") or "")[:1500]
    att   = (candidate.get("att_text") or "")[:2000]

    subjs = candidate.get("subjects", "")
    if isinstance(subjs, str):
        try: subjs = json.loads(subjs)
        except: subjs = [subjs]
    subj_str = " | ".join(subjs[:3]) if subjs else ""

    docs = []
    if candidate.get("has_cv"):         docs.append("CV")
    if candidate.get("has_motivation"): docs.append("Lettre de motivation")
    if candidate.get("has_id"):         docs.append("Pièce d'identité")
    if candidate.get("has_diplomas"):   docs.append("Diplômes/Attestations")
    docs_str = ", ".join(docs) if docs else "Aucune pièce identifiée"

    contenu_disponible = bool(body.strip()) or bool(att.strip())

    return f"""Tu es un évaluateur expert pour l'EETFP-MPG en Mauritanie.

Évalue ce dossier de candidature pour la filière : **{specialty}**
Contexte : {context}

--- DONNÉES ---
Nom : {candidate.get("name", "Inconnu")}
Filière déclarée : {specialty}
Pièces présentes : {docs_str}
Sujet(s) e-mail : {subj_str}

Corps de l'e-mail :
{body if body.strip() else "[Aucun texte extrait — le candidat a peut-être envoyé uniquement des fichiers joints]"}

Contenu des pièces jointes :
{att if att.strip() else "[Contenu non extractible — scan, image ou PDF protégé]"}
--- FIN ---

RÈGLES IMPORTANTES :
1. Si le contenu est vide ou illisible, ce n'est PAS la faute du candidat.
   → Évalue sur la BASE des pièces présentes et du sujet de l'e-mail.
   → Ne mets PAS 0 juste parce que le texte est vide.
2. La présence des 4 pièces = dossier complet = 10/10 sur la qualité du dossier.
3. Si la spécialité est "Non spécifié", essaie de la déduire du contenu disponible.
4. Sois JUSTE : un candidat avec dossier complet mais contenu illisible mérite au moins :
   - Disponibilité : 4/5 (a pris le temps d'envoyer un dossier complet)
   - Qualité dossier : selon les pièces présentes
   - Les autres critères : 8-12 sur leur max si aucune info contraire

GRILLE :
1. Niveau d'études       : /25
2. Expérience            : /20
3. Lettre de motivation  : /20
4. Adéquation au profil  : /20
5. Qualité du dossier    : /10 (CV=2.5, Lettre=2.5, CIN=2.5, Diplômes=2.5)
6. Disponibilité         : /5

Réponds UNIQUEMENT avec ce JSON valide :
{{
  "score_niveau": <0-25>,
  "justif_niveau": "<1 phrase>",
  "score_experience": <0-20>,
  "justif_experience": "<1 phrase>",
  "score_motivation": <0-20>,
  "justif_motivation": "<1 phrase>",
  "score_adequation": <0-20>,
  "justif_adequation": "<1 phrase>",
  "score_dossier": <0-10>,
  "justif_dossier": "<1 phrase>",
  "score_disponibilite": <0-5>,
  "justif_disponibilite": "<1 phrase>",
  "specialty_detected": "<filière détectée ou 'Non spécifié'>",
  "note_globale": "<2-3 phrases résumant le profil>",
  "contenu_manquant": <true|false>
}}"""


# ─────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────

def mention(total):
    if total >= 80: return "Excellent"
    if total >= 65: return "Bon"
    if total >= 50: return "Moyen"
    return "Non retenu"


def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE) as f:
                return set(json.load(f).get("done_ids", []))
        except: pass
    return set()


def save_checkpoint(done_ids):
    try:
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump({"done_ids": list(done_ids)}, f)
    except: pass


def ensure_columns(conn):
    existing = [r[1] for r in conn.execute("PRAGMA table_info(candidates)").fetchall()]
    for col, td in [
        ("justif_niveau",        "TEXT DEFAULT ''"),
        ("justif_experience",    "TEXT DEFAULT ''"),
        ("justif_motivation",    "TEXT DEFAULT ''"),
        ("justif_adequation",    "TEXT DEFAULT ''"),
        ("justif_dossier",       "TEXT DEFAULT ''"),
        ("justif_disponibilite", "TEXT DEFAULT ''"),
        ("note_globale",         "TEXT DEFAULT ''"),
        ("ia_scored",            "INTEGER DEFAULT 0"),
        ("contenu_manquant",     "INTEGER DEFAULT 0"),
    ]:
        if col not in existing:
            conn.execute(f"ALTER TABLE candidates ADD COLUMN {col} {td}")
    conn.commit()


# ─────────────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────────────

def run():
    start = datetime.now()
    print("=" * 62)
    print("  MPG — Correction des scores suspects")
    print("  Cible : score ≤ 10 OU spécialité non identifiée")
    print("=" * 62)

    if not hasattr(config, "ANTHROPIC_API_KEY") or not config.ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY manquante dans config.py")
        sys.exit(1)

    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    ensure_columns(conn)

    # Candidats suspects : score très bas OU spécialité inconnue
    candidates = conn.execute("""
        SELECT * FROM candidates
        WHERE hors_delai = 0
          AND (
            score_total <= 10
            OR specialty = 'Non spécifié'
          )
        ORDER BY
          CASE WHEN score_total IS NULL THEN 0 ELSE score_total END ASC,
          last_date DESC
    """).fetchall()

    total = len(candidates)
    done_ids = load_checkpoint()
    todo = [c for c in candidates if c["id"] not in done_ids]

    print(f"\n  📋 Candidats suspects     : {total}")
    print(f"  ✅ Déjà retraités         : {len(done_ids)}")
    print(f"  ⏳ Reste à corriger       : {len(todo)}")
    print(f"  💰 Coût estimé            : ~${len(todo)*0.004:.2f}\n")

    if not todo:
        print("  ✅ Tous déjà corrigés !")
        conn.close()
        return

    errors = 0
    improved = 0

    for i, cand in enumerate(todo):
        cid  = cand["id"]
        name = cand["name"] or cand["email_addr"]
        old_score = cand["score_total"] or 0
        print(f"  🔄 [{i+1}/{len(todo)}] {name[:40]}… (était {old_score}/100)", end=" ", flush=True)

        prompt   = build_prompt_v2(dict(cand))
        response = call_claude(prompt)

        if not response:
            print("⚠ Pas de réponse")
            errors += 1
            continue

        try:
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            result = json.loads(clean.strip())
        except json.JSONDecodeError:
            print("⚠ JSON invalide")
            errors += 1
            continue

        sn = min(float(result.get("score_niveau",        0)), 25)
        se = min(float(result.get("score_experience",    0)), 20)
        sm = min(float(result.get("score_motivation",    0)), 20)
        sa = min(float(result.get("score_adequation",    0)), 20)
        sd = min(float(result.get("score_dossier",       0)), 10)
        sv = min(float(result.get("score_disponibilite", 0)),  5)
        total_score  = round(sn+se+sm+sa+sd+sv, 1)
        mention_str  = mention(total_score)
        contenu_manq = 1 if result.get("contenu_manquant") else 0

        # Mettre à jour la spécialité si détectée
        new_specialty = result.get("specialty_detected", "")
        if new_specialty and new_specialty != "Non spécifié":
            update_specialty = new_specialty
        else:
            update_specialty = cand["specialty"]

        conn.execute("""
            UPDATE candidates SET
                score_niveau        = ?,
                score_experience    = ?,
                score_motivation    = ?,
                score_adequation    = ?,
                score_dossier       = ?,
                score_disponibilite = ?,
                score_total         = ?,
                mention             = ?,
                justif_niveau       = ?,
                justif_experience   = ?,
                justif_motivation   = ?,
                justif_adequation   = ?,
                justif_dossier      = ?,
                justif_disponibilite= ?,
                note_globale        = ?,
                note_evaluateur     = ?,
                evalue_le           = ?,
                ia_scored           = 1,
                contenu_manquant    = ?,
                specialty           = ?
            WHERE id = ?
        """, (
            sn, se, sm, sa, sd, sv,
            total_score, mention_str,
            result.get("justif_niveau",""),
            result.get("justif_experience",""),
            result.get("justif_motivation",""),
            result.get("justif_adequation",""),
            result.get("justif_dossier",""),
            result.get("justif_disponibilite",""),
            result.get("note_globale",""),
            EVALUATEUR_IA,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            contenu_manq,
            update_specialty,
            cid
        ))

        # Mise à jour table evaluations
        conn.execute("""
            INSERT INTO evaluations
                (candidate_id, evaluateur, score_niveau, score_experience,
                 score_motivation, score_adequation, score_dossier,
                 score_disponibilite, score_total, mention, note, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(candidate_id, evaluateur) DO UPDATE SET
                score_total=excluded.score_total,
                mention=excluded.mention,
                created_at=excluded.created_at
        """, (
            cid, EVALUATEUR_IA, sn, se, sm, sa, sd, sv,
            total_score, mention_str,
            result.get("note_globale",""),
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))

        conn.commit()
        done_ids.add(cid)
        save_checkpoint(done_ids)

        delta = total_score - old_score
        arrow = f"↑ +{delta:.1f}" if delta > 0 else f"→ {delta:.1f}"
        if delta > 0: improved += 1
        print(f"→ {total_score}/100 {arrow} — {mention_str}")

        time.sleep(1.2)

    # Résumé final
    duration = (datetime.now() - start).total_seconds()

    c = conn.cursor()
    excellent = c.execute("SELECT COUNT(*) FROM candidates WHERE mention='Excellent' AND hors_delai=0").fetchone()[0]
    bon       = c.execute("SELECT COUNT(*) FROM candidates WHERE mention='Bon'       AND hors_delai=0").fetchone()[0]
    moyen     = c.execute("SELECT COUNT(*) FROM candidates WHERE mention='Moyen'     AND hors_delai=0").fetchone()[0]
    non_ret   = c.execute("SELECT COUNT(*) FROM candidates WHERE mention='Non retenu' AND hors_delai=0").fetchone()[0]
    manquant  = c.execute("SELECT COUNT(*) FROM candidates WHERE contenu_manquant=1  AND hors_delai=0").fetchone()[0]
    conn.close()

    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)

    print()
    print("=" * 62)
    print(f"  ✅ Correction terminée en {duration/60:.1f} min")
    print(f"  📈 Scores améliorés       : {improved}")
    print(f"  ⚠  Erreurs               : {errors}")
    print()
    print(f"  🏆 Excellent (≥80)        : {excellent}")
    print(f"  ✅ Bon      (65-79)       : {bon}")
    print(f"  🟡 Moyen    (50-64)       : {moyen}")
    print(f"  ❌ Non retenu (<50)       : {non_ret}")
    print()
    print(f"  📭 Contenu illisible      : {manquant}")
    print(f"     (à réviser manuellement — dossier peut être bon)")
    print("=" * 62)
    print()
    print("  → Lancez maintenant : python app.py")


if __name__ == "__main__":
    run()