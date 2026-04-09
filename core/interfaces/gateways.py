from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class IEmailService(ABC):
    @abstractmethod
    def fetch_emails(self, batch_size: int = 10) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def logout(self) -> None:
        raise NotImplementedError

class IAttachmentProvider(ABC):
    @abstractmethod
    def save_attachment(self, part: Any, folder: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_candidate_folder(self, email: str) -> str:
        raise NotImplementedError
