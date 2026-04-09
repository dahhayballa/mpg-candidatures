#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════
  MPG Candidatures — Enrichissement (Phase 2)
  Lit le contenu COMPLET de chaque e-mail +
  extrait le texte des pièces jointes PDF et DOCX.
  Usage : python enrich_emails.py
  ⚠ Lancez APRÈS process_emails.py
════════════════════════════════════════════════════════
"""

import imaplib, email, sqlite3, os, re, json, sys, io
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime
import unicodedata
import config

# ─────────────────────────────────────────────────────────────
#  Extraction de texte depuis les pièces jointes
# ─────────────────────────────────────────────────────────────

def extract_pdf_text(data: bytes) -> str:
    """Extrait le texte d'un PDF (pypdf)."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(data))
        pages = []
        for page in reader.pages[:8]:      # max 8 pages
            t = page.extract_text() or ""
            pages.append(t)
        return " ".join(pages)[:4000]
    except Exception as e:
        return f"[PDF non lisible: {e}]"


def extract_docx_text(data: bytes) -> str:
    """Extrait le texte d'un fichier Word (python-docx)."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(data))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return " ".join(paragraphs)[:4000]
    except Exception as e:
        return f"[DOCX non lisible: {e}]"


# ─────────────────────────────────────────────────────────────
#  OCR — extraction de texte depuis les images
#  (captures d'écran de CV, lettres de motivation, scans…)
# ─────────────────────────────────────────────────────────────

_ocr_reader = None   # chargé une seule fois

def get_ocr_reader():
    """Charge EasyOCR une seule fois (arabe + français + anglais)."""
    global _ocr_reader
    if _ocr_reader is None:
        try:
            import easyocr
            print("\n   🔍 Chargement du moteur OCR (EasyOCR)…")
            _ocr_reader = easyocr.Reader(
                ["ar","en"],   # ← 2 langues simultanées
                gpu=False,            # CPU uniquement (compatible tous PCs)
                verbose=False,
            )
            print("   ✅ OCR prêt (arabe + français + anglais)")
        except ImportError:
            print("\n   ⚠  EasyOCR non installé. Lancez : pip install easyocr pillow")
            _ocr_reader = "unavailable"
        except Exception as e:
            print(f"\n   ⚠  OCR erreur d'initialisation : {e}")
            _ocr_reader = "unavailable"
    return _ocr_reader


def extract_image_text(data: bytes) -> str:
    """
    Extrait le texte d'une image (JPG, PNG, BMP, TIFF…)
    via OCR multilingue (arabe / français / anglais).
    Gère les captures d'écran de CV et lettres de motivation.
    """
    reader = get_ocr_reader()
    if reader == "unavailable":
        return "[OCR non disponible]"
    try:
        import numpy as np
        from PIL import Image
        img = Image.open(io.BytesIO(data))

        # Convertir en RGB si nécessaire (RGBA, P, L…)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        # Amélioration légère : augmenter la résolution si petite
        w, h = img.size
        if w < 800:
            factor = 800 / w
            img = img.resize((int(w*factor), int(h*factor)), Image.LANCZOS)

        img_array = np.array(img)
        results = reader.readtext(img_array, detail=0, paragraph=True)
        text = " ".join(results)
        return text[:4000]
    except ImportError:
        return "[PIL/numpy manquant — pip install pillow numpy]"
    except Exception as e:
        return f"[Erreur OCR image: {e}]"


IMAGE_TYPES = {
    "image/jpeg", "image/jpg", "image/png",
    "image/bmp", "image/tiff", "image/gif",
    "image/webp",
}


def extract_text_from_part(part) -> str:
    """
    Extrait le texte depuis n'importe quelle partie de l'e-mail.
    PDF → pypdf | DOCX → python-docx | Images → OCR EasyOCR
    """
    ct   = part.get_content_type()
    data = part.get_payload(decode=True)
    if not data:
        return ""

    if ct == "application/pdf":
        return extract_pdf_text(data)

    elif ct in ("application/vnd.openxmlformats-officedocument"
                ".wordprocessingml.document",
                "application/msword"):
        return extract_docx_text(data)

    elif ct in IMAGE_TYPES:
        return extract_image_text(data)

    elif ct == "text/plain":
        charset = part.get_content_charset() or "utf-8"
        return data.decode(charset, errors="replace")[:2000]

    return ""


# ─────────────────────────────────────────────────────────────
#  Analyse du contenu enrichi
# ─────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Minuscules + suppression diacritiques."""
    return unicodedata.normalize("NFKD", text.lower())


def detect_specialty_enriched(full_text: str) -> str:
    """Détection de spécialité depuis le texte complet (3 langues)."""
    txt = normalize(full_text)
    best, best_score = "Non spécifié", 0
    for specialty, keywords in config.SPECIALTIES.items():
        score = sum(len(kw) for kw in keywords if normalize(kw) in txt)
        if score > best_score:
            best_score, best = score, specialty
    return best


def classify_docs_enriched(filenames: list, full_text: str) -> dict:
    """
    Classifie les documents depuis noms de fichiers + contenu textuel.
    Beaucoup plus précis que les noms seuls.
    """
    combined = normalize(" ".join(filenames) + " " + full_text)

    def has(keywords):
        return any(normalize(k) in combined for k in keywords)

    return {
        "has_cv":         has(config.CV_KEYWORDS),
        "has_motivation": has(config.MOTIVATION_KEYWORDS),
        "has_id":         has(config.ID_KEYWORDS),
        "has_diplomas":   has(config.DIPLOMA_KEYWORDS),
    }


def compute_status(docs: dict) -> str:
    score = sum(docs.values())
    if score == 4:   return "Complet"
    if score >= 2:   return "Partiel"
    if score == 1:   return "Incomplet"
    return "Vide"


def compute_score_dossier(docs: dict) -> float:
    return sum(docs.values()) * 2.5   # /10


# ─────────────────────────────────────────────────────────────
#  Helpers IMAP
# ─────────────────────────────────────────────────────────────

def decode_str(s) -> str:
    if not s:
        return ""
    try:
        parts = decode_header(s)
        out = ""
        for part, enc in parts:
            if isinstance(part, bytes):
                out += part.decode(enc or "utf-8", errors="replace")
            else:
                out += str(part)
        return out.strip()
    except Exception:
        return str(s).strip()


def connect_imap():
    print(f"📡 Connexion à {config.IMAP_SERVER}:{config.IMAP_PORT} …")
    if config.USE_SSL:
        mail = imaplib.IMAP4_SSL(config.IMAP_SERVER, config.IMAP_PORT)
    else:
        mail = imaplib.IMAP4(config.IMAP_SERVER, config.IMAP_PORT)
    mail.login(config.EMAIL_ADDRESS, config.PASSWORD)
    mail.socket().settimeout(60)
    print("✅ Connecté.")
    return mail


# ─────────────────────────────────────────────────────────────
#  Base de données — colonnes supplémentaires
# ─────────────────────────────────────────────────────────────

def ensure_enrich_columns(conn):
    c = conn.cursor()
    existing = [r[1] for r in c.execute("PRAGMA table_info(candidates)").fetchall()]
    new_cols = [
        ("enriched",       "INTEGER DEFAULT 0"),
        ("email_body_full","TEXT DEFAULT ''"),
        ("att_text",       "TEXT DEFAULT ''"),
    ]
    for col, typedef in new_cols:
        if col not in existing:
            c.execute(f"ALTER TABLE candidates ADD COLUMN {col} {typedef}")
    conn.commit()


# ─────────────────────────────────────────────────────────────
#  Traitement principal
# ─────────────────────────────────────────────────────────────

def enrich():
    start = datetime.now()
    print("=" * 60)
    print("  MPG — Enrichissement des candidatures (Phase 2)")
    print("  Lecture complète : corps + pièces jointes (PDF/DOCX)")
    print("  Version OPTIMISÉE (Targeted Search)")
    print("=" * 60)

    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    ensure_enrich_columns(conn)

    # Candidats à enrichir (uniquement ceux qui ne sont pas encore enrichis)
    candidates = [dict(r) for r in
                  conn.execute("SELECT * FROM candidates WHERE hors_delai=0 AND enriched=0").fetchall()]
    
    total_to_enrich = len(candidates)
    if total_to_enrich == 0:
        print("✅ Tous les candidats sont déjà enrichis.")
        conn.close()
        return

    print(f"   🔍 {total_to_enrich} nouveaux candidats à enrichir.\n")

    mail = connect_imap()
    mail.select("INBOX")

    processed = 0
    errors = 0

    for idx, cand in enumerate(candidates):
        email_addr = cand["email_addr"].lower().strip()
        pct = int(((idx + 1) / total_to_enrich) * 100)
        print(f"\r🚀 [{idx+1}/{total_to_enrich}] {pct}% | Traitement : {email_addr} ...", end="", flush=True)

        # Accumulateur pour ce candidat
        acc = { "body_texts": [], "att_texts": [], "filenames": [] }

        # Recherche ciblée par expéditeur
        try:
            # Utilisation de SEARCH FROM pour trouver uniquement les mails de cette personne
            _, data = mail.search(None, f'FROM "{email_addr}"')
            ids = data[0].split()
            
            if not ids:
                # Marquer comme enrichi même si pas de mail trouvé (pour ne pas boucler indéfiniment)
                conn.execute("UPDATE candidates SET enriched=1 WHERE email_addr=?", (email_addr,))
                conn.commit()
                continue

            # Fetch uniquement les mails trouvés
            for msg_id in ids:
                _, msg_data = mail.fetch(msg_id, "(RFC822)")
                if not msg_data or not isinstance(msg_data[0], tuple):
                    continue
                
                msg = email.message_from_bytes(msg_data[0][1])
                
                # Extraction identique à la version originale
                for msg_part in msg.walk():
                    ct   = msg_part.get_content_type()
                    cd   = str(msg_part.get("Content-Disposition", ""))
                    fname = msg_part.get_filename()
                    if fname: fname = decode_str(fname).strip()

                    if "attachment" not in cd and ct == "text/plain":
                        try:
                            charset = msg_part.get_content_charset() or "utf-8"
                            body = msg_part.get_payload(decode=True).decode(charset, errors="replace")
                            acc["body_texts"].append(body[:2000])
                        except: pass

                    elif "attachment" in cd and fname:
                        acc["filenames"].append(fname)
                        payload = msg_part.get_payload(decode=True) or b""
                        if len(payload) > 10 * 1024 * 1024: # Skip > 10MB
                             acc["att_texts"].append(f"[{fname}: trop grand]")
                             continue
                             
                        att_text = extract_text_from_part(msg_part)
                        if att_text: acc["att_texts"].append(f"[{fname}] {att_text}")

                        # Sauvegarde physique
                        folder = os.path.join(config.ATTACHMENTS_DIR, re.sub(r'[^\w@.-]', '_', email_addr))
                        os.makedirs(folder, exist_ok=True)
                        safe_name = re.sub(r'[\r\n\t<>:"/\\|?*]', '_', fname)
                        try:
                            with open(os.path.join(folder, safe_name), "wb") as f:
                                f.write(payload)
                        except: pass

            # Analyse et mise à jour
            full_body = " ".join(acc["body_texts"])
            full_att  = " ".join(acc["att_texts"])
            full_text = full_body + " " + full_att

            docs     = classify_docs_enriched(acc["filenames"], full_text)
            specialty = detect_specialty_enriched(full_text)
            status   = compute_status(docs)
            score_d  = compute_score_dossier(docs)

            # Préserver spécialité si déjà détectée
            if specialty == "Non spécifié" and cand["specialty"] != "Non spécifié":
                specialty = cand["specialty"]

            conn.execute("""
                UPDATE candidates SET
                    email_body_full = ?, att_text = ?,
                    has_cv = ?, has_motivation = ?, has_id = ?, has_diplomas = ?,
                    status = ?, score_dossier = ?, specialty = ?, enriched = 1
                WHERE email_addr = ?
            """, (
                full_body[:8000], full_att[:8000],
                int(docs["has_cv"]), int(docs["has_motivation"]), 
                int(docs["has_id"]), int(docs["has_diplomas"]),
                status, score_d, specialty, email_addr
            ))
            conn.commit()
            processed += 1

        except Exception as e:
            print(f"\n  ⚠ Erreur pour {email_addr}: {e}")
            errors += 1
            # Reconnexion si nécessaire
            try: mail = connect_imap(); mail.select("INBOX")
            except: pass

    # Statistiques finales
    c = conn.cursor()
    enriched_total = c.execute("SELECT COUNT(*) FROM candidates WHERE enriched=1").fetchone()[0]
    specialty_fixed = c.execute(
        "SELECT COUNT(*) FROM candidates WHERE specialty != 'Non spécifié' AND enriched=1"
    ).fetchone()[0]

    conn.close()
    mail.logout()

    duration = (datetime.now() - start).total_seconds()
    print("\n" + "=" * 60)
    print(f"  ✅ Enrichissement terminé en {duration/60:.1f} min")
    print(f"  📋 Candidats traités (nouveaux) : {processed}")
    print(f"  🔍 Total enrichis en DB  : {enriched_total}")
    print(f"  🎯 Spécialité identifiée : {specialty_fixed}")
    print(f"  ⚠  Erreurs rencontrées : {errors}")
    print("=" * 60)
    print("\n  Lancez ensuite : python detect_duplicates.py")


if __name__ == "__main__":
    if not os.path.exists(config.DB_PATH):
        print("❌ Base de données introuvable. Lancez d'abord process_emails.py")
        sys.exit(1)
    enrich()
