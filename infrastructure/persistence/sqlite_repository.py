from __future__ import annotations
import sqlite3
import json
from typing import List, Optional, Tuple, Any, Dict, TYPE_CHECKING
from datetime import datetime

# Root absolute imports
from core.domain.entities import Candidate, Evaluation
from core.interfaces.repositories import ICandidateRepository, IAuditLogRepository

class SqliteCandidateRepository(ICandidateRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def save(self, candidate: Candidate) -> Candidate:
        conn = self._get_connection()
        c = conn.cursor()
        
        # Check if exists
        c.execute("SELECT id FROM candidates WHERE email_addr = ?", (candidate.email_addr,))
        row = c.fetchone()
        
        if row:
            # Update
            c.execute("""
                UPDATE candidates SET
                    name=?, num_emails=?, first_date=?, last_date=?, specialty=?,
                    num_attachments=?, attachment_names=?, has_cv=?, has_motivation=?,
                    has_id=?, has_diplomas=?, status=?, subjects=?, body_preview=?,
                    folder_path=?, score_total=?, mention=?, retenu=?, enriched=?, hors_delai=?
                WHERE email_addr=?
            """, (
                candidate.name, candidate.num_emails, candidate.first_date, candidate.last_date,
                candidate.specialty, len(candidate.attachment_names), json.dumps(candidate.attachment_names),
                int(candidate.has_cv), int(candidate.has_motivation), int(candidate.has_id),
                int(candidate.has_diplomas), candidate.status, json.dumps(candidate.subjects),
                candidate.body_preview, candidate.folder_path, candidate.score_total,
                candidate.mention, int(candidate.retenu), int(candidate.enriched),
                int(candidate.hors_delai), candidate.email_addr
            ))
            candidate.id = row['id']
        else:
            # Insert
            c.execute("""
                INSERT INTO candidates (
                    email_addr, name, num_emails, first_date, last_date, specialty,
                    num_attachments, attachment_names, has_cv, has_motivation,
                    has_id, has_diplomas, status, subjects, body_preview,
                    folder_path, score_total, mention, retenu, enriched, hors_delai
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                candidate.email_addr, candidate.name, candidate.num_emails,
                candidate.first_date, candidate.last_date, candidate.specialty,
                len(candidate.attachment_names), json.dumps(candidate.attachment_names),
                int(candidate.has_cv), int(candidate.has_motivation),
                int(candidate.has_id), int(candidate.has_diplomas),
                candidate.status, json.dumps(candidate.subjects),
                candidate.body_preview, candidate.folder_path,
                candidate.score_total, candidate.mention,
                int(candidate.retenu), int(candidate.enriched), int(candidate.hors_delai)
            ))
            candidate.id = c.lastrowid
        
        conn.commit()
        conn.close()
        return candidate

    def get_by_id(self, candidate_id: int) -> Optional[Candidate]:
        conn = self._get_connection()
        row = conn.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,)).fetchone()
        if not row:
            conn.close()
            return None
        
        candidate = self._row_to_entity(row)
        
        # Load evaluations
        evals_rows = conn.execute("SELECT * FROM evaluations WHERE candidate_id = ?", (candidate_id,)).fetchall()
        candidate.evaluations = [self._row_to_evaluation(e) for e in evals_rows]
        
        conn.close()
        return candidate

    def get_by_email(self, email: str) -> Optional[Candidate]:
        conn = self._get_connection()
        row = conn.execute("SELECT * FROM candidates WHERE email_addr = ?", (email,)).fetchone()
        if not row:
            conn.close()
            return None
        
        candidate = self._row_to_entity(row)
        conn.close()
        return candidate

    def list_candidates(self, filters: Optional[Dict[str, Any]] = None, sort: Optional[str] = None, page: int = 1, per_page: int = 50) -> Tuple[List[Candidate], int]:
        conn = self._get_connection()
        where = ["hors_delai=0"]
        params: List[Any] = []
        
        if filters:
            if filters.get('q'):
                where.append("(name LIKE ? OR email_addr LIKE ? OR specialty LIKE ?)")
                params.extend([f"%{filters['q']}%"]*3)
            if filters.get('status'):
                where.append("status = ?")
                params.append(filters['status'])
            if filters.get('specialty'):
                where.append("specialty = ?")
                params.append(filters['specialty'])
            if filters.get('mention'):
                where.append("mention = ?")
                params.append(filters['mention'])
        
        wsql = "WHERE " + " AND ".join(where) if where else ""
        total_row = conn.execute(f"SELECT COUNT(*) FROM candidates {wsql}", params).fetchone()
        total = total_row[0] if total_row else 0
        
        order_sql = f"ORDER BY {sort} DESC" if sort else "ORDER BY last_date DESC"
        
        rows = conn.execute(f"""
            SELECT * FROM candidates {wsql} {order_sql}
            LIMIT ? OFFSET ?
        """, params + [per_page, (page-1)*per_page]).fetchall()
        
        candidates = [self._row_to_entity(r) for r in rows]
        conn.close()
        return candidates, total

    def get_stats(self) -> Dict[str, Any]:
        conn = self._get_connection()
        c = conn.cursor()
        def q(sql: str, p: List[Any] = []) -> Any: 
            row = c.execute(sql, p).fetchone()
            return row[0] if row else 0

        stats = {
            "total": q("SELECT COUNT(*) FROM candidates WHERE hors_delai=0"),
            "hors_delai": q("SELECT COUNT(*) FROM candidates WHERE hors_delai=1"),
            "complet": q("SELECT COUNT(*) FROM candidates WHERE status='Complet' AND hors_delai=0"),
            "partiel": q("SELECT COUNT(*) FROM candidates WHERE status='Partiel' AND hors_delai=0"),
            "vide": q("SELECT COUNT(*) FROM candidates WHERE status='Vide' AND hors_delai=0"),
            "evalues": q("SELECT COUNT(DISTINCT candidate_id) FROM evaluations"),
            "excellent": q("SELECT COUNT(*) FROM candidates WHERE hors_delai=0 AND mention='Excellent'"),
            "bon": q("SELECT COUNT(*) FROM candidates WHERE hors_delai=0 AND mention='Bon'"),
            "moyen": q("SELECT COUNT(*) FROM candidates WHERE hors_delai=0 AND mention='Moyen'"),
            "non_retenu": q("SELECT COUNT(*) FROM candidates WHERE hors_delai=0 AND mention='Non retenu'"),
            "by_specialty": [dict(r) for r in c.execute("SELECT specialty, COUNT(*) as cnt FROM candidates WHERE hors_delai=0 GROUP BY specialty").fetchall()]
        }
        conn.close()
        return stats

    def _row_to_entity(self, row: sqlite3.Row) -> Candidate:
        d = dict(row)
        
        def safe_json_load(val: Any) -> List[str]:
            if not val: return []
            try: return json.loads(str(val))
            except: return []

        return Candidate(
            id=d['id'],
            email_addr=str(d.get('email_addr', '')),
            name=str(d.get('name', '')),
            specialty=str(d.get('specialty', 'Non spécifié')),
            status=str(d.get('status', 'Incomplet')),
            num_emails=int(d.get('num_emails', 0)),
            first_date=d.get('first_date'),
            last_date=d.get('last_date'),
            has_cv=bool(d.get('has_cv', 0)),
            has_motivation=bool(d.get('has_motivation', 0)),
            has_id=bool(d.get('has_id', 0)),
            has_diplomas=bool(d.get('has_diplomas', 0)),
            score_total=d.get('score_total'),
            mention=d.get('mention'),
            retenu=bool(d.get('retenu', 0)),
            enriched=bool(d.get('enriched', 0)),
            hors_delai=bool(d.get('hors_delai', 0)),
            attachment_names=safe_json_load(d.get('attachment_names')),
            subjects=safe_json_load(d.get('subjects')),
            body_preview=str(d.get('body_preview', '')),
            folder_path=str(d.get('folder_path', ''))
        )

    def _row_to_evaluation(self, row: sqlite3.Row) -> Evaluation:
        d = dict(row)
        return Evaluation(
            evaluateur=str(d.get('evaluateur', '')),
            score_niveau=float(d.get('score_niveau', 0)),
            score_experience=float(d.get('score_experience', 0)),
            score_motivation=float(d.get('score_motivation', 0)),
            score_adequation=float(d.get('score_adequation', 0)),
            score_dossier=float(d.get('score_dossier', 0)),
            score_disponibilite=float(d.get('score_disponibilite', 0)),
            score_total=float(d.get('score_total', 0)),
            mention=d.get('mention'),
            note=str(d.get('note', '')),
            created_at=str(d.get('created_at', ''))
        )

class SqliteAuditLogRepository(IAuditLogRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def log(self, action: str, evaluateur: str, detail: str) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO audit_log (action, evaluateur, detail, created_at) VALUES (?,?,?,?)",
            (action, evaluateur, detail, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()

    def get_recent(self, limit: int = 100) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
