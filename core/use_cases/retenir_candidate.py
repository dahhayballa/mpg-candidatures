from __future__ import annotations
from typing import Dict, Any, Optional

from core.domain.entities import Candidate
from core.interfaces.repositories import ICandidateRepository, IAuditLogRepository


class RetenirCandidateUseCase:
    """Mark a candidate as retenu (accepted) or non-retenu by the committee."""

    def __init__(self, candidate_repo: ICandidateRepository, audit_log: IAuditLogRepository):
        self.candidate_repo = candidate_repo
        self.audit_log = audit_log

    def execute(self, candidate_id: int, retenu: bool, evaluateur: str) -> Optional[Dict[str, Any]]:
        candidate = self.candidate_repo.get_by_id(candidate_id)
        if not candidate:
            return None

        candidate.retenu = retenu
        self.candidate_repo.save(candidate)

        action_label = "RETENU" if retenu else "NON_RETENU"
        self.audit_log.log(
            action_label,
            evaluateur,
            f"Candidat #{candidate_id} ({candidate.name}) marqué {'✅ Retenu' if retenu else '❌ Non retenu'} par {evaluateur}"
        )

        return {
            "success": True,
            "candidate_id": candidate_id,
            "retenu": retenu,
        }
