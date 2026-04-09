from __future__ import annotations
from typing import Dict, Any, TYPE_CHECKING
from core.interfaces.repositories import ICandidateRepository, IAuditLogRepository

class GetStatsUseCase:
    def __init__(self, candidate_repo: ICandidateRepository, audit_log: IAuditLogRepository, deadline: str):
        self.candidate_repo = candidate_repo
        self.audit_log = audit_log
        self.deadline = deadline

    def execute(self) -> Dict[str, Any]:
        stats = self.candidate_repo.get_stats()
        stats["audit"] = self.audit_log.get_recent(20)
        stats["deadline"] = self.deadline
        return stats
