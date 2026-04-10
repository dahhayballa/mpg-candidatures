from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Evaluation:
    evaluateur: str
    score_niveau: float = 0.0
    score_experience: float = 0.0
    score_motivation: float = 0.0
    score_adequation: float = 0.0
    score_dossier: float = 0.0
    score_disponibilite: float = 0.0
    score_total: float = 0.0
    mention: Optional[str] = None
    note: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))
    # AI justifications per criterion
    justif_niveau: str = ""
    justif_experience: str = ""
    justif_motivation: str = ""
    justif_adequation: str = ""
    justif_dossier: str = ""
    justif_disponibilite: str = ""
    note_globale: str = ""  # AI global summary

    def calculate_total(self) -> None:
        val = (
            float(self.score_niveau) + float(self.score_experience) + float(self.score_motivation) +
            float(self.score_adequation) + float(self.score_dossier) + float(self.score_disponibilite)
        )
        self.score_total = round(val, 1)
        self.mention = self._get_mention(self.score_total)

    @staticmethod
    def _get_mention(total: float) -> str:
        if total >= 80: return "Excellent"
        if total >= 65: return "Bon"
        if total >= 50: return "Moyen"
        return "Non retenu"

@dataclass
class Candidate:
    id: Optional[int] = None
    email_addr: str = ""
    name: str = ""
    specialty: str = "Non spécifié"
    status: str = "Incomplet"
    num_emails: int = 0
    first_date: Optional[str] = None
    last_date: Optional[str] = None
    has_cv: bool = False
    has_motivation: bool = False
    has_id: bool = False
    has_diplomas: bool = False
    score_total: Optional[float] = None
    mention: Optional[str] = None
    retenu: bool = False
    verification_required: bool = False
    enriched: bool = False
    hors_delai: bool = False
    attachment_names: List[str] = field(default_factory=list)
    subjects: List[str] = field(default_factory=list)
    body_preview: str = ""
    folder_path: str = ""
    evaluations: List[Evaluation] = field(default_factory=list)

    def update_status(self) -> None:
        if not self.attachment_names and not self.body_preview:
            self.status = "Vide"
            return
        
        score = sum([int(self.has_cv), int(self.has_motivation), int(self.has_id), int(self.has_diplomas)])
        if score == 4:
            self.status = "Complet"
        elif score >= 2:
            self.status = "Partiel"
        else:
            self.status = "Incomplet"

    def calculate_aggregate_score(self) -> None:
        if not self.evaluations:
            self.score_total = None
            self.mention = None
            return
        
        # Priority: 1. Latest Human, 2. Latest AI
        human_evals = [e for e in self.evaluations if not e.evaluateur.startswith('IA')]
        ai_evals = [e for e in self.evaluations if e.evaluateur.startswith('IA')]
        
        target = None
        if human_evals:
            # Sort by date if available, or just take the last one
            target = human_evals[-1]
        elif ai_evals:
            target = ai_evals[-1]
            
        if target:
            self.score_total = target.score_total
            self.mention = target.mention
        else:
            self.score_total = None
            self.mention = None
