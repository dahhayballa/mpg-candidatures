#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════
  MPG Candidatures — Notation automatique par IA (Phase 4)
  Utilise Claude pour évaluer chaque candidat selon
  la grille officielle /100 avec justification écrite.
  Usage : python ai_score.py
  ⚠ Lancez APRÈS enrich_emails.py
════════════════════════════════════════════════════════
"""

import sqlite3, json, time, os, sys
from datetime import datetime
import urllib.request, urllib.error
import config

EVALUATEUR_IA = "IA — Claude (Anthropic)"
CHECKPOINT_FILE = "ai_score_checkpoint.json"

# ─────────────────────────────────────────────────────
#  Appel à l'API Claude
# ─────────────────────────────────────────────────────

def call_claude(prompt: str, max_retries: int = 3) -> str:
    """Appelle Claude Haiku (économique) et retourne la réponse texte."""
    url = "https://api.anthropic.com/v1/messages"
    body = json.dumps({
        "model": "claude-3-haiku-20240307",
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
            if e.code == 429:   # Rate limit
                wait = 20 * (attempt + 1)
                print(f"\n   ⏳ Rate limit — attente {wait}s…", flush=True)
                time.sleep(wait)
            elif e.code == 401:
                print("\n❌ Clé API invalide. Vérifiez ANTHROPIC_API_KEY dans config.py")
                sys.exit(1)
            else:
                print(f"\n   ⚠ HTTP {e.code}: {err[:200]}")
                time.sleep(10)
        except Exception as e:
            print(f"\n   ⚠ Erreur réseau (tentative {attempt+1}): {e}")
            time.sleep(15)
    return ""


# ─────────────────────────────────────────────────────
#  Construction du prompt d'évaluation
# ─────────────────────────────────────────────────────

SPECIALTIES_CONTEXT = {
    "Maintenance industrielle":           "mécanique industrielle, maintenance préventive et corrective, machines industrielles",
    "Électricité industrielle":           "électricité industrielle, automatismes, câblage, tableaux électriques",
    "Tuyauterie industrielle":            "tuyauterie, robinetterie, lecture de plans isométriques, soudure de tuyaux",
    "Construction métallique et soudure": "soudure MIG/TIG/électrode, charpente métallique, lecture de plans",
    "HSE":                                "hygiène sécurité environnement, réglementation, audits, plans de prévention",
    "Opérations pétrolières et gazières": "pétrole et gaz, opérations offshore/onshore, process pétrolier",
    "Techniques minières":                "exploitation minière, géologie, abattage, traitement des minerais",
    "Non spécifié":                       "secteur industriel, minier ou pétrolier",
}


def build_prompt(candidate: dict) -> str:
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

    return f"""Tu es un évaluateur expert pour l'EETFP-MPG (École d'Enseignement Technique et de Formation Professionnelle — Mines, Pétrole & Gaz) en Mauritanie.

Tu dois évaluer ce dossier de candidature pour la filière : **{specialty}**
Contexte de la filière : {context}

--- DONNÉES DU CANDIDAT ---
Nom : {candidate.get("name", "Inconnu")}
E-mail : {candidate.get("email_addr", "")}
Filière demandée : {specialty}
Pièces présentes : {docs_str}
Sujet(s) de l'e-mail : {subj_str}

Contenu de l'e-mail :
{body if body else "[Aucun texte extrait]"}

Contenu des pièces jointes (OCR) :
{att if att else "[Aucun contenu extrait des pièces jointes]"}
--- FIN DES DONNÉES ---

Évalue ce candidat selon la GRILLE OFFICIELLE ci-dessous.
Attribue une note à chaque critère en te basant UNIQUEMENT sur les informations disponibles.
RÈGLES LOGIQUES STRICTES (IMPÉRATIF) :
1. PREUVE PAR DOCUMENT : Toute information déclarée dans l'E-MAIL mais non supportée par une PIÈCE JOINTE (CV, Diplôme, CID) doit être ignorée ou notée à 0. Une déclaration écrite ne remplace pas une preuve documentaire.
2. ABSENCE DE CV => Note "Expérience" = 0. (Interdiction de déduire l'expérience du texte de l'e-mail).
3. ABSENCE DE LETTRE => Note "Motivation" = 0.
4. ABSENCE DE DIPLÔME => Note "Niveau d'études" = 0.
5. AUCUN DOCUMENT => La note globale doit être proche de 0, avec une observation invitant le candidat à compléter son dossier.

GRILLE D'ÉVALUATION :
1. Niveau d'études       : /25 (correspondance avec la filière, niveau minimum requis)
2. Expérience            : /20 (stages, expériences professionnelles liées au domaine)
3. Lettre de motivation  : /20 (clarté, cohérence, motivation réelle, projet professionnel)
4. Adéquation au profil  : /20 (compatibilité avec la formation, aptitudes, logique)
5. Qualité du dossier    : /10 (complétude : CV=2.5, Lettre=2.5, CIN=2.5, Diplômes=2.5)
6. Disponibilité         : /5  (capacité à suivre 3 à 6 mois à temps plein)

Réponds UNIQUEMENT avec ce JSON valide, sans texte avant ni après :
{{
  "score_niveau": <0-25>,
  "justif_niveau": "<1 phrase en français>",
  "score_experience": <0-20>,
  "justif_experience": "<1 phrase en français>",
  "score_motivation": <0-20>,
  "justif_motivation": "<1 phrase en français>",
  "score_adequation": <0-20>,
  "justif_adequation": "<1 phrase en français>",
  "score_dossier": <0-10>,
  "justif_dossier": "<1 phrase en français>",
  "score_disponibilite": <0-5>,
  "justif_disponibilite": "<1 phrase en français>",
  "note_globale": "<2-3 phrases résumant le profil du candidat>"
}}"""


# ─────────────────────────────────────────────────────
#  Traitement
# ─────────────────────────────────────────────────────

def ensure_columns(conn):
    existing = [r[1] for r in conn.execute("PRAGMA table_info(candidates)").fetchall()]
    cols = [
        ("justif_niveau",       "TEXT DEFAULT ''"),
        ("justif_experience",   "TEXT DEFAULT ''"),
        ("justif_motivation",   "TEXT DEFAULT ''"),
        ("justif_adequation",   "TEXT DEFAULT ''"),
        ("justif_dossier",      "TEXT DEFAULT ''"),
        ("justif_disponibilite","TEXT DEFAULT ''"),
        ("note_globale",        "TEXT DEFAULT ''"),
        ("ia_scored",           "INTEGER DEFAULT 0"),
    ]
    for col, typedef in cols:
        if col not in existing:
            conn.execute(f"ALTER TABLE candidates ADD COLUMN {col} {typedef}")
    conn.commit()


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
        except Exception:
            pass
    return set()


def save_checkpoint(done_ids):
    try:
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump({"done_ids": list(done_ids)}, f)
    except Exception:
        pass


def run():
    start = datetime.now()
    print("=" * 62)
    print("  MPG — Notation automatique par IA (Claude)")
    print("  Grille officielle /100 avec justifications")
    print("=" * 62)

    if not hasattr(config, "ANTHROPIC_API_KEY") or not config.ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY manquante dans config.py")
        sys.exit(1)

    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    ensure_columns(conn)

    # Candidats à évaluer (pas encore notés par l'IA)
    candidates = conn.execute("""
        SELECT * FROM candidates
        WHERE hors_delai = 0 AND ia_scored = 0
        ORDER BY
            CASE specialty
                WHEN 'Non spécifié' THEN 1 ELSE 0
            END,
            last_date DESC
    """).fetchall()

    total = len(candidates)
    if total == 0:
        print("  ✅ Tous les candidats sont déjà notés !")
        conn.close()
        return

    done_ids = load_checkpoint()
    todo = [c for c in candidates if c["id"] not in done_ids]

    print(f"  📋 Total à noter      : {total}")
    print(f"  ✅ Déjà traités       : {len(done_ids)}")
    print(f"  ⏳ Reste              : {len(todo)}")
    print(f"  💰 Coût estimé        : ~${len(todo)*0.004:.2f}")
    print()

    errors = 0
    for i, cand in enumerate(todo):
        cid  = cand["id"]
        name = cand["name"] or cand["email_addr"]
        print(f"  🤖 [{i+1}/{len(todo)}] {name[:45]}…", end=" ", flush=True)

        prompt = build_prompt(dict(cand))
        response = call_claude(prompt)

        if not response:
            print("⚠ Pas de réponse")
            errors += 1
            continue

        # Parser le JSON
        try:
            # Nettoyer si Claude ajoute des backticks
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

        # ─────────────────────────────────────────────────────
        # IRON LOGIC : On force les scores à 0 si les documents sont absents
        # (L'humain a toujours le dernier mot via les flags has_xxx)
        # ─────────────────────────────────────────────────────
        has_cv    = candidate.get("has_cv", 0)
        has_mot   = candidate.get("has_motivation", 0)
        has_dipl  = candidate.get("has_diplomas", 0)

        sn = min(float(result.get("score_niveau", 0)),      25)
        se = min(float(result.get("score_experience", 0)),  20)
        sm = min(float(result.get("score_motivation", 0)),  20)
        sa = min(float(result.get("score_adequation", 0)),  20)
        sd = min(float(result.get("score_dossier", 0)),     10)
        sv = min(float(result.get("score_disponibilite",0)), 5)

        # Sanitaires (Enforcement)
        if not has_cv: 
            se = 0
            reason_se = "[FORCÉ 0: CV absents]"
        if not has_mot:
            sm = 0
            reason_sm = "[FORCÉ 0: Lettre absente]"
        if not has_dipl:
            sn = min(sn, 5) # Plafond à 5 points pour les dires dans l'email sans preuve

        total_score = round(sn + se + sm + sa + sd + sv, 1)
        mention_str = mention(total_score)

        # Enregistrer en base
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
                ia_scored           = 1
            WHERE id = ?
        """, (
            sn, se, sm, sa, sd, sv,
            total_score, mention_str,
            result.get("justif_niveau", ""),
            result.get("justif_experience", ""),
            result.get("justif_motivation", ""),
            result.get("justif_adequation", ""),
            result.get("justif_dossier", ""),
            result.get("justif_disponibilite", ""),
            result.get("note_globale", ""),
            EVALUATEUR_IA,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            cid
        ))

        # Insérer dans la table evaluations aussi
        conn.execute("""
            INSERT INTO evaluations
                (candidate_id, evaluateur, score_niveau, score_experience,
                score_motivation, score_adequation, score_dossier,
                
                    score_disponibilite, score_total, mention, note, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(candidate_id, evaluateur) DO UPDATE SET
                score_niveau=excluded.score_niveau,
                score_experience=excluded.score_experience,
                score_motivation=excluded.score_motivation,
                score_adequation=excluded.score_adequation,
                score_dossier=excluded.score_dossier,
                score_disponibilite=excluded.score_disponibilite,
                score_total=excluded.score_total,
                mention=excluded.mention,
                note=excluded.note,
                created_at=excluded.created_at
        """, (
            cid, EVALUATEUR_IA, sn, se, sm, sa, sd, sv,
            total_score, mention_str,
            result.get("note_globale", ""),
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))

        conn.commit()
        done_ids.add(cid)
        save_checkpoint(done_ids)

        print(f"{total_score}/100 — {mention_str}")
        # Pause pour éviter le rate limit (5 req/min sur tier gratuit)
        time.sleep(1.2)

    # Résumé final
    duration = (datetime.now() - start).total_seconds()
    scored = conn.execute(
        "SELECT COUNT(*) FROM candidates WHERE ia_scored=1 AND hors_delai=0"
    ).fetchone()[0]

    excellent = conn.execute(
        "SELECT COUNT(*) FROM candidates WHERE mention='Excellent' AND hors_delai=0"
    ).fetchone()[0]
    bon = conn.execute(
        "SELECT COUNT(*) FROM candidates WHERE mention='Bon' AND hors_delai=0"
    ).fetchone()[0]
    moyen = conn.execute(
        "SELECT COUNT(*) FROM candidates WHERE mention='Moyen' AND hors_delai=0"
    ).fetchone()[0]
    non_ret = conn.execute(
        "SELECT COUNT(*) FROM candidates WHERE mention='Non retenu' AND hors_delai=0"
    ).fetchone()[0]

    conn.close()

    # Supprimer checkpoint si tout est fini
    if not todo or errors == 0:
        if os.path.exists(CHECKPOINT_FILE):
            os.remove(CHECKPOINT_FILE)

    print()
    print("=" * 62)
    print(f"  ✅ Notation terminée en {duration/60:.1f} min")
    print(f"  📊 Candidats notés     : {scored}/{scored+errors}")
    print(f"  ⚠  Erreurs             : {errors}")
    print()
    print(f"  🏆 Excellent (≥80)     : {excellent}")
    print(f"  ✅ Bon      (65-79)    : {bon}")
    print(f"  🟡 Moyen    (50-64)    : {moyen}")
    print(f"  ❌ Non retenu (<50)    : {non_ret}")
    print("=" * 62)
    print()
    print("  → Lancez maintenant : python app.py")
    print("  → Le dashboard affiche les résultats classés")


if __name__ == "__main__":
    run()