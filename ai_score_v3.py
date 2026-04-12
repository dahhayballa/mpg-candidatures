#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════════════
  MPG — Scoring IA v3 — Grille officielle complète

  Lit TOUS les fichiers du candidat (PDF/JPG/DOCX/PNG/HEIC)
  Redimensionne les images automatiquement
  Claude évalue selon la grille officielle du Directeur
  Détecte la spécialité automatiquement
  Checkpoint — reprend là où il s'est arrêté

  Grille :
    Niveau d'études  /25
    Expérience       /20
    Motivation       /20
    Adéquation       /20
    Qualité dossier  /10  (automatique)
    Disponibilité     /5  (toujours 5)
    ─────────────────────
    TOTAL           /100

  Usage : python ai_score_v3.py
════════════════════════════════════════════════════════════════
"""
import os, sys, json, sqlite3, time, base64, io
from pathlib import Path
from datetime import datetime
import anthropic

sys.path.append(os.path.dirname(__file__))
import config

# ── Configuration ──────────────────────────────────────────────
DB_PATH         = config.DB_PATH
ATTACHMENTS_DIR = config.ATTACHMENTS_DIR
CLIENT          = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
MODEL           = "claude-sonnet-4-5"
MAX_RETRIES     = 3
DELAY           = 1.5
CHECKPOINT_FILE = "checkpoint_v3.json"
MAX_IMG_SIZE    = 1400   # px max pour les images
MAX_FILE_BYTES  = 4 * 1024 * 1024  # 4MB max

VALID_SPECS = [
    "HSE",
    "Électricité industrielle",
    "Tuyauterie industrielle",
    "Construction métallique et soudure",
    "Maintenance industrielle",
    "Techniques minières",
    "Opérations pétrolières et gazières",
]

# ── Lecture des fichiers ───────────────────────────────────────

def resize_image_bytes(img_bytes: bytes, max_px: int = MAX_IMG_SIZE) -> bytes:
    """Redimensionne des bytes image avec Pillow."""
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(img_bytes))
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        if img.width > max_px or img.height > max_px:
            img.thumbnail((max_px, max_px), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=75, optimize=True)
        result = buf.getvalue()
        # Si encore trop grand → qualité 50
        if len(result) > MAX_FILE_BYTES:
            img.thumbnail((800, 800), Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=50)
            result = buf.getvalue()
        return result
    except Exception:
        return img_bytes


def read_pdf(path: str) -> str:
    """Extrait le texte d'un PDF (essaie pdfplumber puis PyPDF2)."""
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            texts = [p.extract_text() for p in pdf.pages[:5] if p.extract_text()]
            return "\n".join(texts)[:3000]
    except Exception:
        pass
    try:
        import PyPDF2
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            texts = [p.extract_text() for p in reader.pages[:5] if p.extract_text()]
            return "\n".join(texts)[:3000]
    except Exception:
        return ""


def pdf_to_image(path: str) -> bytes | None:
    """Convertit la première page d'un PDF en image JPEG."""
    try:
        import fitz
        doc  = fitz.open(path)
        page = doc[0]
        mat  = fitz.Matrix(1.0, 1.0)
        pix  = page.get_pixmap(matrix=mat)
        return pix.tobytes("jpeg")
    except Exception:
        return None


def read_docx(path: str) -> str:
    """Extrait le texte d'un DOCX."""
    try:
        import docx2txt
        return docx2txt.process(path)[:3000]
    except Exception:
        pass
    try:
        from docx import Document
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)[:3000]
    except Exception:
        return ""


def extract_file_content(path: str) -> dict:
    """
    Lit un fichier et retourne son contenu.
    {"type": "text"|"image", "content": str, "media_type": str (si image)}
    """
    ext = Path(path).suffix.lower()

    # ── PDF ──────────────────────────────────────────────────
    if ext == '.pdf':
        text = read_pdf(path)
        if text and len(text) > 50:
            return {"type": "text", "content": text}
        # PDF-image → convertir en image
        img_bytes = pdf_to_image(path)
        if img_bytes:
            img_bytes = resize_image_bytes(img_bytes)
            if len(img_bytes) <= MAX_FILE_BYTES:
                b64 = base64.standard_b64encode(img_bytes).decode()
                return {"type": "image", "content": b64, "media_type": "image/jpeg"}
        return {"type": "text", "content": f"[PDF non lisible : {Path(path).name}]"}

    # ── DOCX / DOC ───────────────────────────────────────────
    elif ext in ('.docx', '.doc'):
        text = read_docx(path)
        return {"type": "text", "content": text or f"[DOCX vide : {Path(path).name}]"}

    # ── Images ───────────────────────────────────────────────
    elif ext in ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic', '.bmp'):
        try:
            with open(path, 'rb') as f:
                raw = f.read()
            img_bytes = resize_image_bytes(raw)
            if len(img_bytes) <= MAX_FILE_BYTES:
                b64 = base64.standard_b64encode(img_bytes).decode()
                return {"type": "image", "content": b64, "media_type": "image/jpeg"}
            return {"type": "text", "content": f"[Image trop volumineuse : {Path(path).name}]"}
        except Exception:
            return {"type": "text", "content": f"[Image illisible : {Path(path).name}]"}

    # ── Texte brut ───────────────────────────────────────────
    elif ext in ('.txt', '.text', '.csv'):
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return {"type": "text", "content": f.read()[:3000]}
        except Exception:
            return {"type": "text", "content": ""}

    else:
        return {"type": "text", "content": f"[Format non supporté : {Path(path).name}]"}


# ── Prompt Claude ──────────────────────────────────────────────

def build_system(specialty: str) -> str:
    return f"""Tu es un expert en évaluation de candidatures pour l'EETFP-MPG (École des Mines, Pétrole & Gaz) de Nouakchott, Mauritanie.

Le candidat peut envoyer entre 1 et 20 fichiers. Lis et analyse TOUS les fichiers fournis.

RÈGLES IMPORTANTES :
- Si plusieurs diplômes : retenir LE PLUS ÉLEVÉ
- Les fichiers supplémentaires t'aident pour l'expérience et l'adéquation
- score_dossier est calculé automatiquement, ne pas l'évaluer
- Si une information est absente → donner 0

GRILLE OFFICIELLE /100 :

1. Niveau d'études /25 — PRENDRE LE PLUS ÉLEVÉ TROUVÉ :
   Master / Ingénieur (Bac+5) = 25 pts
   Licence / BTS              = 20 pts
   BT (Brevet Technicien)     = 15 pts
   CAP                        = 10 pts
   CC (Cours Complémentaire)  =  5 pts
   Bac seul                   =  0 pts  ← non reconnu comme qualification
   Aucune qualification       =  0 pts
   ⚠ Le domaine N'A PAS d'importance (Licence Droit = 20 pts = Licence Génie)

2. Expérience professionnelle /20 :
   Aucune expérience     =  0 pts
   Stage(s) seulement    =  5 pts
   1 à 2 ans             = 10 pts
   3 à 5 ans             = 15 pts
   Plus de 5 ans         = 20 pts

3. Lettre de motivation /20 :
   Absente               =  0 pts
   Très vague            =  5 pts
   Générique             = 10 pts
   Claire et cohérente   = 15 pts
   Excellente            = 20 pts

4. Adéquation au profil /20 — filière cible : {specialty} :
   Aucun lien            =  5 pts
   Lien faible           = 10 pts
   Bon lien              = 15 pts
   Excellent lien        = 20 pts

5. Disponibilité /5 :
   TOUJOURS 5/5 — tous les candidats ont postulé donc sont disponibles.

6. Spécialité détectée :
   Cherche dans l'objet du mail, le corps, la lettre et le CV.
   Choisir parmi exactement :
   HSE | Électricité industrielle | Tuyauterie industrielle |
   Construction métallique et soudure | Maintenance industrielle |
   Techniques minières | Opérations pétrolières et gazières | Non spécifié

Réponds UNIQUEMENT en JSON valide, sans markdown, sans texte avant ou après."""


def build_messages(candidate_row: dict, files_content: list) -> list:
    specialty = candidate_row.get('specialty', 'Non spécifié')
    name      = candidate_row.get('name', '')
    email     = candidate_row.get('email_addr', '')
    body      = (candidate_row.get('body_preview', '') or '')[:500]

    content = []
    content.append({"type": "text", "text":
        f"Évalue ce dossier de candidature.\n\n"
        f"Candidat    : {name}\n"
        f"Email       : {email}\n"
        f"Filière     : {specialty}\n\n"
        f"Corps du mail :\n{body or '(aucun texte)'}\n\n"
        f"--- {len(files_content)} fichier(s) ci-dessous ---"
    })

    for i, fc in enumerate(files_content):
        fname = fc.get('filename', f'Fichier {i+1}')
        fdata = fc.get('data', {})
        content.append({"type": "text", "text": f"\n[FICHIER {i+1}] {fname}"})
        if fdata.get('type') == 'image':
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": fdata.get('media_type', 'image/jpeg'),
                    "data": fdata['content']
                }
            })
        else:
            txt = fdata.get('content', '')
            content.append({"type": "text", "text": txt[:2000] if txt else "(vide)"})

    content.append({"type": "text", "text": """
---
Réponds UNIQUEMENT avec ce JSON (sans markdown) :
{
  "score_niveau": <0-25>,
  "score_experience": <0-20>,
  "score_motivation": <0-20>,
  "score_adequation": <0-20>,
  "score_disponibilite": 5,
  "niveau_detecte": "<Master|Licence|BTS|BT|CAP|CC|Bac|Inconnu>",
  "justif_niveau": "<1-2 phrases>",
  "justif_experience": "<1-2 phrases>",
  "justif_motivation": "<1-2 phrases>",
  "justif_adequation": "<1-2 phrases>",
  "note_globale": "<synthèse 2-3 phrases>",
  "specialty_detecte": "<HSE|Électricité industrielle|Tuyauterie industrielle|Construction métallique et soudure|Maintenance industrielle|Techniques minières|Opérations pétrolières et gazières|Non spécifié>"
}"""})

    return [{"role": "user", "content": content}]


# ── Appel Claude ───────────────────────────────────────────────

def call_claude(candidate_row: dict, files_content: list) -> dict | None:
    specialty = candidate_row.get('specialty', 'Non spécifié')
    messages  = build_messages(candidate_row, files_content)

    for attempt in range(MAX_RETRIES):
        try:
            resp = CLIENT.messages.create(
                model=MODEL,
                max_tokens=1000,
                system=build_system(specialty),
                messages=messages
            )
            raw = resp.content[0].text.strip()
            raw = raw.replace('```json', '').replace('```', '').strip()
            return json.loads(raw)

        except json.JSONDecodeError as e:
            print(f"   ⚠ JSON invalide (tentative {attempt+1}): {e}")
            time.sleep(DELAY)
        except Exception as e:
            err = str(e)
            if "529" in err or "overloaded" in err.lower():
                wait = 30 * (attempt + 1)
                print(f"   ⏳ Surcharge API — attente {wait}s…")
                time.sleep(wait)
            elif "400" in err:
                print(f"   ⚠ Erreur 400 (fichier trop volumineux) tentative {attempt+1}")
                # Réduire les fichiers images
                files_content = [
                    f for f in files_content
                    if f.get('data', {}).get('type') != 'image'
                ] or files_content[:1]
                messages = build_messages(candidate_row, files_content)
                time.sleep(DELAY)
            else:
                print(f"   ⚠ Erreur tentative {attempt+1}: {err[:120]}")
                time.sleep(DELAY * (attempt + 1))

    return None


# ── Checkpoint ─────────────────────────────────────────────────

def load_checkpoint() -> set:
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as f:
            return set(json.load(f))
    return set()

def save_checkpoint(done: set):
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(list(done), f)


# ── Base de données ────────────────────────────────────────────

def get_candidates(conn: sqlite3.Connection) -> list:
    cols   = [r[1] for r in conn.execute("PRAGMA table_info(candidates)").fetchall()]
    has_hd = "hors_delai" in cols
    where  = "hors_delai=0" if has_hd else "1=1"
    rows   = conn.execute(f"""
        SELECT id, email_addr, name, specialty, status,
               has_cv, has_motivation, has_id, has_diplomas,
               body_preview, attachment_names, folder_path
        FROM candidates WHERE {where} ORDER BY id
    """).fetchall()
    fields = ['id','email_addr','name','specialty','status',
              'has_cv','has_motivation','has_id','has_diplomas',
              'body_preview','attachment_names','folder_path']
    return [dict(zip(fields, r)) for r in rows]


def save_candidate(conn: sqlite3.Connection, cid: int,
                   result: dict, score_dossier: float) -> None:
    """Sauvegarde les scores dans candidates."""
    total = round(
        float(result.get('score_niveau', 0)) +
        float(result.get('score_experience', 0)) +
        float(result.get('score_motivation', 0)) +
        float(result.get('score_adequation', 0)) +
        score_dossier + 5.0, 1
    )
    mention = (
        "Excellent" if total >= 80 else
        "Bon"       if total >= 65 else
        "Moyen"     if total >= 50 else
        "Non retenu"
    )
    cols = [r[1] for r in conn.execute("PRAGMA table_info(candidates)").fetchall()]

    fields = {
        'score_total':         total,
        'score_niveau':        result.get('score_niveau', 0),
        'score_experience':    result.get('score_experience', 0),
        'score_motivation':    result.get('score_motivation', 0),
        'score_adequation':    result.get('score_adequation', 0),
        'score_dossier':       score_dossier,
        'score_disponibilite': 5.0,
        'mention':             mention,
        'ia_scored':           1,
    }

    # Spécialité — mettre à jour si Non spécifié
    sp_detected = str(result.get('specialty_detecte', '') or '').strip()
    cur_sp = (conn.execute("SELECT specialty FROM candidates WHERE id=?", (cid,))
              .fetchone() or ('',))[0]
    if sp_detected in VALID_SPECS and (not cur_sp or cur_sp == 'Non spécifié'):
        fields['specialty'] = sp_detected

    # Colonnes optionnelles (si elles existent dans la DB)
    optional = {
        'justif_niveau':        result.get('justif_niveau', ''),
        'justif_experience':    result.get('justif_experience', ''),
        'justif_motivation':    result.get('justif_motivation', ''),
        'justif_adequation':    result.get('justif_adequation', ''),
        'justif_dossier':       f"Dossier : {int(score_dossier/2.5)}/4 pièces",
        'justif_disponibilite': "Candidat disponible (a postulé)",
        'note_globale':         result.get('note_globale', ''),
        'contenu_manquant':     0,
    }
    for k, v in optional.items():
        if k in cols:
            fields[k] = v

    sql = "UPDATE candidates SET " + ", ".join(f"{k}=?" for k in fields) + " WHERE id=?"
    conn.execute(sql, list(fields.values()) + [cid])
    conn.commit()


def find_folder(email: str, folder_path_db: str) -> str | None:
    """Trouve le dossier des pièces jointes du candidat."""
    # Tentative 1 : folder_path depuis DB
    p1 = os.path.join(ATTACHMENTS_DIR, folder_path_db) if folder_path_db else ''
    if p1 and os.path.isdir(p1):
        return p1

    # Tentative 2 : email directement
    p2 = os.path.join(ATTACHMENTS_DIR, email)
    if os.path.isdir(p2):
        return p2

    # Tentative 3 : recherche insensible casse
    try:
        email_lower = email.lower().strip()
        for sub in os.listdir(ATTACHMENTS_DIR):
            if sub.lower() == email_lower:
                return os.path.join(ATTACHMENTS_DIR, sub)
    except Exception:
        pass

    return None


# ── Main ───────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("  MPG — Scoring IA v3 — Grille officielle")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 65)

    conn       = sqlite3.connect(DB_PATH)
    candidates = get_candidates(conn)
    done       = load_checkpoint()
    to_do      = [c for c in candidates if str(c['id']) not in done]

    print(f"\n  Total          : {len(candidates)}")
    print(f"  Déjà traités   : {len(done)}")
    print(f"  Reste          : {len(to_do)}")
    print(f"  Coût estimé    : ~${len(to_do)*0.008:.2f}")
    print()

    stats = {"ok":0, "err":0,
             "Excellent":0, "Bon":0, "Moyen":0, "Non retenu":0}

    for i, cand in enumerate(to_do, 1):
        cid      = cand['id']
        name     = (cand['name'] or '—')[:40]
        specialty= cand['specialty'] or 'Non spécifié'

        print(f"  🔄 [{i}/{len(to_do)}] {name}…  ({specialty[:30]})")

        # ── Score dossier (automatique) ─────────────────────
        docs = min(sum([
            bool(cand.get('has_cv')),
            bool(cand.get('has_motivation')),
            bool(cand.get('has_id')),
            bool(cand.get('has_diplomas')),
        ]), 4)

        # ── Chercher le dossier ─────────────────────────────
        folder = find_folder(cand['email_addr'], cand.get('folder_path','') or '')

        # Si pas de dossier sur disque → score_dossier = 0
        score_dossier = docs * 2.5 if folder else 0.0

        # ── Lire les fichiers ───────────────────────────────
        files_content = []
        if folder:
            exts = {'.pdf','.jpg','.jpeg','.png','.docx','.doc',
                    '.txt','.gif','.webp','.heic','.bmp'}
            files = sorted([
                f for f in os.listdir(folder)
                if not f.startswith('.') and Path(f).suffix.lower() in exts
            ])[:10]  # Max 10 fichiers
            for fname in files:
                fpath = os.path.join(folder, fname)
                fdata = extract_file_content(fpath)
                files_content.append({"filename": fname, "data": fdata})
                print(f"     📎 {fname[:50]} ({fdata['type']})")

        # Si aucun fichier → body_preview
        if not files_content:
            body = (cand.get('body_preview', '') or '').strip()
            if len(body) > 20:
                print(f"     ⚠ Pas de fichiers — lecture email uniquement")
                files_content = [{"filename": "email.txt",
                                   "data": {"type":"text","content":body}}]
            else:
                print(f"     ⚠ Dossier vide — score minimal")
                files_content = [{"filename": "vide.txt",
                                   "data": {"type":"text",
                                            "content":"(aucun contenu disponible)"}}]

        # ── Appel Claude ────────────────────────────────────
        result = call_claude(cand, files_content)

        if result:
            # Bac seul → forcer 0/25
            if str(result.get('niveau_detecte','')).lower() == 'bac':
                result['score_niveau'] = 0
                result['justif_niveau'] = (
                    (result.get('justif_niveau','') or '') +
                    " [Bac seul → 0/25]"
                )

            save_candidate(conn, cid, result, score_dossier)

            total = round(
                float(result.get('score_niveau',0)) +
                float(result.get('score_experience',0)) +
                float(result.get('score_motivation',0)) +
                float(result.get('score_adequation',0)) +
                score_dossier + 5.0, 1
            )
            mention = ("Excellent" if total>=80 else "Bon" if total>=65
                       else "Moyen" if total>=50 else "Non retenu")

            sp = result.get('specialty_detecte','')
            sp_str = f" → {sp}" if sp and sp != 'Non spécifié' else ""
            print(f"     ✅ {total}/100 — {mention}"
                  f"  (N:{result.get('score_niveau',0)}"
                  f" E:{result.get('score_experience',0)}"
                  f" M:{result.get('score_motivation',0)}"
                  f" A:{result.get('score_adequation',0)}"
                  f" D:{score_dossier}){sp_str}")

            stats["ok"] += 1
            stats[mention] = stats.get(mention, 0) + 1

        else:
            print(f"     ❌ Échec — marqué contenu_manquant")
            db_cols = [r[1] for r in conn.execute(
                "PRAGMA table_info(candidates)").fetchall()]
            if 'contenu_manquant' in db_cols:
                conn.execute(
                    "UPDATE candidates SET contenu_manquant=1 WHERE id=?", (cid,))
                conn.commit()
            stats["err"] += 1

        done.add(str(cid))
        save_checkpoint(done)
        time.sleep(DELAY)

    conn.close()

    print()
    print("=" * 65)
    print(f"  ✅ Terminé — {len(to_do)} candidats traités")
    print()
    print(f"  🏆 Excellent  (≥80) : {stats['Excellent']}")
    print(f"  ✅ Bon       (65-79) : {stats['Bon']}")
    print(f"  🟡 Moyen    (50-64) : {stats['Moyen']}")
    print(f"  ❌ Non retenu (<50) : {stats['Non retenu']}")
    print(f"  ⚠  Erreurs          : {stats['err']}")
    print("=" * 65)
    print()
    print("  → Lancez maintenant : python generer_liste_finale.py")


if __name__ == "__main__":
    main()