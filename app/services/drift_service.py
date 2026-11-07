from __future__ import annotations

from datetime import datetime

from app.models.drift import Drift
from app.models.evaluation import Evaluation


class DriftService:
    def __init__(self, db):
        self.db = db

    def detect(self, evaluation: Evaluation) -> Drift | None:
        previous = (
            self.db.query(Evaluation)
            .filter(
                Evaluation.control_id == evaluation.control_id,
                Evaluation.asset_identifier == evaluation.asset_identifier,
                Evaluation.id != evaluation.id,
            )
            .order_by(Evaluation.evaluated_at.desc())
            .first()
        )
        if previous is None or previous.status == evaluation.status:
            return None
        if previous.status not in {"PASS", "FAIL"} or evaluation.status not in {"PASS", "FAIL"}:
            return None
        drift = Drift(
            control_id=evaluation.control_id,
            asset_identifier=evaluation.asset_identifier,
            previous_evaluation_id=previous.id,
            current_evaluation_id=evaluation.id,
            previous_status=previous.status,
            current_status=evaluation.status,
            description=f"Compliance drift detected: {previous.status} -> {evaluation.status} for {evaluation.asset_identifier} on control {evaluation.control_id}.",
            detected_at=datetime.utcnow(),
        )
        self.db.add(drift)
        self.db.commit()
        self.db.refresh(drift)
        return drift
