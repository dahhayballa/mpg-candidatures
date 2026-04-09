from __future__ import annotations
from typing import List, Dict, Any, TYPE_CHECKING, Optional, cast
import json
import re

# Root absolute imports
from core.domain.entities import Candidate
from core.interfaces.repositories import ICandidateRepository
from core.interfaces.gateways import IEmailService, IAttachmentProvider

class IngestEmailsUseCase:
    def __init__(self, 
                 email_service: IEmailService, 
                 candidate_repo: ICandidateRepository,
                 attachment_provider: IAttachmentProvider,
                 config: Dict[str, Any]):
        self.email_service = email_service
        self.candidate_repo = candidate_repo
        self.attachment_provider = attachment_provider
        self.config = config

    def execute(self, batch_size: int = 10) -> int:
        emails = self.email_service.fetch_emails(batch_size)
        processed: int = 0
        
        for email_data in emails:
            email_addr = str(email_data.get('email_addr', '')).lower().strip()
            if not email_addr: continue
            
            candidate = self.candidate_repo.get_by_email(email_addr)
            
            if not candidate:
                candidate = Candidate(
                    email_addr=email_addr,
                    name=str(email_data.get('name', '')),
                    first_date=str(email_data.get('date', '')),
                    last_date=str(email_data.get('date', '')),
                    folder_path=self.attachment_provider.get_candidate_folder(email_addr)
                )
            
            # Update dates
            email_date = str(email_data.get('date', ''))
            if email_date:
                if not candidate.first_date or email_date < candidate.first_date: 
                    candidate.first_date = email_date
                if not candidate.last_date or email_date > candidate.last_date:  
                    candidate.last_date = email_date
            
            # Merge subjects
            subj = str(email_data.get('subject', ''))
            if subj and subj not in candidate.subjects:
                candidate.subjects = list(set(candidate.subjects + [subj]))
            
            candidate.num_emails += 1
            
            # Merge body preview
            body_text = str(email_data.get('body', ''))
            if not candidate.body_preview:
                candidate.body_preview = body_text[:600]
            
            # Specialty detection
            if candidate.specialty == "Non spécifié":
                candidate.specialty = self._detect_specialty(subj + " " + body_text)
            
            # Attachments
            new_attachments: List[str] = []
            parts = email_data.get('parts', [])
            if isinstance(parts, list):
                for part in parts:
                    filename = self.attachment_provider.save_attachment(part, candidate.folder_path)
                    if filename:
                        new_attachments.append(filename)
            
            candidate.attachment_names = list(set(candidate.attachment_names + new_attachments))
            candidate.num_attachments = len(candidate.attachment_names)
            
            # Classification
            self._classify_attachments(candidate)
            
            # Status and deadline
            candidate.update_status()
            deadline = str(self.config.get('DEADLINE', '2026-03-31 14:00'))
            if candidate.last_date:
                candidate.hors_delai = candidate.last_date > deadline
            
            self.candidate_repo.save(candidate)
            processed += 1
            
        return processed

    def _detect_specialty(self, text: str) -> str:
        text_clean = text.lower()
        best_specialty = "Non spécifié"
        best_score = 0

        specialties_raw = self.config.get('SPECIALTIES', {})
        if isinstance(specialties_raw, dict):
            for specialty, keywords in specialties_raw.items():
                if not isinstance(keywords, list): continue
                score = 0
                for kw in keywords:
                    if str(kw).lower() in text_clean:
                        score += len(str(kw))
                if score > best_score:
                    best_score = score
                    best_specialty = str(specialty)
        return best_specialty

    def _classify_attachments(self, candidate: Candidate) -> None:
        body_p = str(candidate.body_preview or "")
        combined = (" ".join(candidate.attachment_names)).lower() + " " + body_p.lower()
        
        def has_any(key: str) -> bool:
            keywords = self.config.get(key, [])
            if not isinstance(keywords, list): return False
            return any(str(k).lower() in combined for k in keywords)

        candidate.has_cv    = candidate.has_cv or has_any('CV_KEYWORDS')
        candidate.has_motivation = candidate.has_motivation or has_any('MOTIVATION_KEYWORDS')
        candidate.has_id    = candidate.has_id or has_any('ID_KEYWORDS')
        candidate.has_diplomas = candidate.has_diplomas or has_any('DIPLOMA_KEYWORDS')
