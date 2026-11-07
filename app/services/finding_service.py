from __future__ import annotations

from datetime import datetime

from app.models.evaluation import Evaluation
from app.repositories.finding_repository import FindingRepository


class FindingService:
    def __init__(self, db):
        self.db = db
        self.repo = FindingRepository(db)

    def create_or_update_for_evaluation(self, evaluation: Evaluation):
        if evaluation.status != "FAIL":
            return None
        existing = self.repo.find_open_for_asset_control(evaluation.control_id, evaluation.asset_identifier)
        if existing:
            existing.description = evaluation.reason
            existing.last_detected_at = datetime.utcnow()
            self.db.commit()
            return existing
        return self.repo.create({
            "control_id": evaluation.control_id,
            "evidence_id": evaluation.evidence_id,
            "asset_identifier": evaluation.asset_identifier,
            "title": f"{evaluation.control_id} failed for {evaluation.asset_identifier}",
            "description": evaluation.reason,
            "severity": "high",
            "status": "OPEN",
            "first_detected_at": datetime.utcnow(),
            "last_detected_at": datetime.utcnow(),
            "resolved_at": None,
        })
