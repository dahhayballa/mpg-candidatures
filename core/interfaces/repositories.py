from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from core.domain.entities import Candidate

class ICandidateRepository(ABC):
    @abstractmethod
    def save(self, candidate: Candidate) -> Candidate:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, candidate_id: int) -> Optional[Candidate]:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Candidate]:
        raise NotImplementedError

    @abstractmethod
    def list_candidates(self, filters: Optional[Dict[str, Any]] = None, sort: Optional[str] = None, page: int = 1, per_page: int = 50) -> Tuple[List[Candidate], int]:
        raise NotImplementedError

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def mark_retenu(self, candidate_id: int, retenu: bool) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_quotas(self) -> List[Dict[str, Any]]:
        """Return per-specialty quota stats for the Quotas & Sélection page."""
        raise NotImplementedError

class IAuditLogRepository(ABC):
    @abstractmethod
    def log(self, action: str, evaluateur: str, detail: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_recent(self, limit: int = 100) -> List[Dict[str, Any]]:
        raise NotImplementedError
