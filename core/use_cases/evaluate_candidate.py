from __future__ import annotations
from typing import Dict, Any, Optional

# Root absolute imports
from core.domain.entities import Candidate, Evaluation
from core.interfaces.repositories import ICandidateRepository, IAuditLogRepository

class EvaluateCandidateUseCase:
    def __init__(self, candidate_repo: ICandidateRepository, audit_log: IAuditLogRepository):
        self.candidate_repo = candidate_repo
        self.audit_log = audit_log

    def execute(self, candidate_id: int, evaluation_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        candidate = self.candidate_repo.get_by_id(candidate_id)
        if not candidate:
            return None
        
        # Create evaluation entity
        ev = Evaluation(
            evaluateur=str(evaluation_data.get('evaluateur', '')),
            score_niveau=float(evaluation_data.get('score_niveau', 0)),
            score_experience=float(evaluation_data.get('score_experience', 0)),
            score_motivation=float(evaluation_data.get('score_motivation', 0)),
            score_adequation=float(evaluation_data.get('score_adequation', 0)),
            score_dossier=float(evaluation_data.get('score_dossier', 0)),
            score_disponibilite=float(evaluation_data.get('score_disponibilite', 0)),
            note=str(evaluation_data.get('note', ''))
        )
        ev.calculate_total()
        
        # Replace or add evaluation
        found = False
        for i, existing in enumerate(candidate.evaluations):
            if existing.evaluateur == ev.evaluateur:
                candidate.evaluations[i] = ev
                found = True
                break
        if not found:
            candidate.evaluations.append(ev)
            
        candidate.calculate_aggregate_score()
        self.candidate_repo.save(candidate)
        
        self.audit_log.log(
            "EVALUATION", 
            ev.evaluateur, 
            f"Candidat #{candidate_id} — {ev.score_total}/100 ({ev.mention})"
        )
        
        return {
            "success": True,
            "score_final": candidate.score_total,
            "mention": candidate.mention
        }
