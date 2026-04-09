#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════
  MPG Candidatures — Détection des doublons (Phase 3)
  Identifie les candidats ayant utilisé plusieurs
  adresses e-mail (même personne, noms similaires).
  Usage : python detect_duplicates.py
  ⚠ Lancez APRÈS enrich_emails.py
════════════════════════════════════════════════════════
"""

import sqlite3, re, json, unicodedata
from difflib import SequenceMatcher
from itertools import combinations
import config

SEUIL_SIMILARITE = 0.78   # ratio minimum pour signaler une paire


def normalize_name(name: str) -> str:
    """
    Normalise un nom pour la comparaison :
    - Minuscules
    - Suppression des diacritiques
    - Suppression des titres courants
    - Suppression des espaces multiples
    """
    if not name:
        return ""
    # Minuscules
    name = name.lower()
    # Supprimer diacritiques
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    # Titres et mots parasites
    stops = r"\b(mr|mme|dr|prof|ould|wld|mint|bint|m\.|mme\.|el|al|ben|bou|ould|dit)\b"
    name = re.sub(stops, " ", name)
    # Retirer les caractères non alphabétiques sauf espace
    name = re.sub(r"[^a-z\s]", " ", name)
    # Espaces multiples
    name = re.sub(r"\s+", " ", name).strip()
    return name


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def ensure_duplicate_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS duplicate_pairs (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_a  INTEGER NOT NULL,
            candidate_b  INTEGER NOT NULL,
            similarity   REAL    NOT NULL,
            status       TEXT    DEFAULT 'pending',  -- pending | confirmed | dismissed
            created_at   TEXT
        )
    """)
    conn.commit()


def detect_duplicates():
    print("=" * 60)
    print("  MPG — Détection des doublons potentiels")
    print("=" * 60)

    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    ensure_duplicate_table(conn)

    # Vider les paires pending (on recalcule)
    conn.execute("DELETE FROM duplicate_pairs WHERE status = 'pending'")
    conn.commit()

    candidates = conn.execute("""
        SELECT id, name, email_addr, specialty
        FROM candidates
        WHERE hors_delai = 0
        ORDER BY id
    """).fetchall()

    print(f"   {len(candidates)} candidats à analyser…")

    # Préparer les noms normalisés
    data = []
    for c in candidates:
        norm = normalize_name(c["name"])
        if norm:
            data.append({
                "id":       c["id"],
                "name":     c["name"],
                "email":    c["email_addr"],
                "specialty":c["specialty"],
                "norm":     norm,
            })

    pairs_found = 0
    pairs_to_insert = []

    # Comparer toutes les paires (O(n²) mais n=1639, ok pour une seule exécution)
    for a, b in combinations(data, 2):
        # Optimisation rapide : si longueur très différente, skip
        la, lb = len(a["norm"]), len(b["norm"])
        if la == 0 or lb == 0:
            continue
        if abs(la - lb) / max(la, lb) > 0.5:
            continue

        ratio = similarity(a["norm"], b["norm"])
        if ratio >= SEUIL_SIMILARITE:
            # Bonus si même spécialité
            if a["specialty"] == b["specialty"] and a["specialty"] != "Non spécifié":
                ratio = min(1.0, ratio + 0.05)

            pairs_to_insert.append((
                a["id"], b["id"],
                round(ratio, 3),
                "pending",
                __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
            ))
            pairs_found += 1

    # Insérer les paires
    conn.executemany("""
        INSERT INTO duplicate_pairs (candidate_a, candidate_b, similarity, status, created_at)
        VALUES (?,?,?,?,?)
    """, pairs_to_insert)
    conn.commit()

    # Résumé
    high   = sum(1 for p in pairs_to_insert if p[2] >= 0.92)
    medium = sum(1 for p in pairs_to_insert if 0.78 <= p[2] < 0.92)

    print(f"\n  🔴 Très probable (≥92%) : {high} paire(s)")
    print(f"  🟡 Probable (78-91%)    : {medium} paire(s)")
    print(f"  Total à vérifier       : {pairs_found} paire(s)")
    print("\n  → Consultez la page 'Doublons' dans le dashboard pour les examiner.")
    print("=" * 60)

    conn.close()


if __name__ == "__main__":
    detect_duplicates()
