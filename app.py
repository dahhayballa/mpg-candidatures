from __future__ import annotations
import os
import sys
import io
import csv
import json
from typing import List, Optional, Tuple, Dict, Any, Union
from flask import Flask, render_template, jsonify, request, send_from_directory, Response

# Fix path for root imports
sys.path.append(os.path.dirname(__file__))

import config
from core.domain.entities import Candidate
from infrastructure.persistence.sqlite_repository import SqliteCandidateRepository, SqliteAuditLogRepository
from core.use_cases.get_stats import GetStatsUseCase
from core.use_cases.evaluate_candidate import EvaluateCandidateUseCase
from core.use_cases.retenir_candidate import RetenirCandidateUseCase

app = Flask(__name__)
DEADLINE = "2026-03-31 14:00"

# --- Dependency Injection ---
candidate_repo = SqliteCandidateRepository(config.DB_PATH)
audit_repo = SqliteAuditLogRepository(config.DB_PATH)

get_stats_uc = GetStatsUseCase(candidate_repo, audit_repo, DEADLINE)
evaluate_uc = EvaluateCandidateUseCase(candidate_repo, audit_repo)
retenir_uc = RetenirCandidateUseCase(candidate_repo, audit_repo)

# --- Routes ---

@app.route("/")
def index() -> str:
    return render_template("dashboard.html")

@app.route("/pieces_jointes/<path:f>")
def attachments(f: str) -> Response:
    return send_from_directory(config.ATTACHMENTS_DIR, f)

@app.route("/api/stats")
def api_stats() -> Response:
    return jsonify(get_stats_uc.execute())

@app.route("/api/candidates")
def api_candidates() -> Response:
    filters: Dict[str, Any] = {
        "q": str(request.args.get("q", "")).strip(),
        "status": str(request.args.get("status", "")),
        "specialty": str(request.args.get("specialty", "")),
        "mention": str(request.args.get("mention", "")),
        "verification_required": request.args.get("verification_required", ""),
        "contenu_manquant": request.args.get("contenu_manquant", ""),
        "retenu": request.args.get("retenu", "")
    }
    page = max(1, int(request.args.get("page", 1)))
    per_page = min(100, int(request.args.get("per_page", 50)))
    sort = str(request.args.get("sort", "last_date"))
    
    candidates, total = candidate_repo.list_candidates(filters, sort, page, per_page)
    
    return jsonify({
        "total": total,
        "page": page,
        "pages": (total + per_page - 1) // per_page,
        "data": [vars(c) for c in candidates]
    })

@app.route("/api/candidate/<int:cid>")
def api_candidate(cid: int) -> Union[Response, Tuple[Response, int]]:
    candidate = candidate_repo.get_by_id(cid)
    if not candidate:
        return jsonify({"error": "Introuvable"}), 404
    
    res = vars(candidate)
    res['evaluations'] = [vars(e) for e in candidate.evaluations]
    return jsonify(res)

@app.route("/api/candidate/<int:cid>/evaluate", methods=["POST"])
def api_evaluate(cid: int) -> Union[Response, Tuple[Response, int]]:
    data = request.get_json()
    if not data: return jsonify({"error": "No data"}), 400
    res = evaluate_uc.execute(cid, data)
    if not res:
        return jsonify({"error": "Erreur"}), 400
    return jsonify(res)

@app.route("/api/candidate/<int:cid>/retenir", methods=["POST"])
def api_retenir(cid: int) -> Union[Response, Tuple[Response, int]]:
    data = request.get_json()
    if not data: return jsonify({"error": "No data"}), 400
    retenu = bool(data.get("retenu", False))
    evaluateur = str(data.get("evaluateur", "Admin"))
    res = retenir_uc.execute(cid, retenu, evaluateur)
    if not res:
        return jsonify({"error": "Introuvable"}), 404
    return jsonify(res)

@app.route("/api/candidate/<int:cid>/open-folder", methods=["GET", "POST"])
def api_open_folder(cid: int) -> Union[Response, Tuple[Response, int]]:
    candidate = candidate_repo.get_by_id(cid)
    if not candidate or not candidate.folder_path:
        return jsonify({"error": "Dossier introuvable"}), 404
    
    path = os.path.abspath(os.path.join(config.ATTACHMENTS_DIR, candidate.folder_path))
    if os.path.exists(path):
        import subprocess
        if sys.platform == 'win32':
            subprocess.Popen(['explorer', path])
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])
        return jsonify({"success": True, "path": path})
    return jsonify({"error": "Chemin invalide", "path": path}), 400

@app.route("/api/quotas")
def api_quotas() -> Response:
    return jsonify(candidate_repo.get_quotas())

@app.route("/api/export/csv")
def export_csv() -> Response:
    candidates, _ = candidate_repo.list_candidates(per_page=10000)
    
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["ID", "Nom", "E-mail", "Filière", "Statut", "Score", "Mention"])
    for c in candidates:
        w.writerow([c.id, c.name, c.email_addr, c.specialty, c.status, c.score_total, c.mention])
    
    return Response("\ufeff" + out.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=candidatures_final.csv"})

if __name__ == "__main__":
    print(f"🌐 Running Clean Arch Server : http://localhost:{config.FLASK_PORT}")
    app.run(host="0.0.0.0", port=config.FLASK_PORT, debug=config.FLASK_DEBUG)
