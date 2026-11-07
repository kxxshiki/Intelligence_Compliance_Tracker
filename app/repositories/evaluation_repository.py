from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.evaluation import Evaluation


class EvaluationRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, asset_identifier: str | None = None, control_id: str | None = None) -> list[Evaluation]:
        query = self.db.query(Evaluation)
        if asset_identifier:
            query = query.filter(Evaluation.asset_identifier == asset_identifier)
        if control_id:
            query = query.filter(Evaluation.control_id == control_id)
        return query.order_by(Evaluation.evaluated_at.desc()).all()

    def create(self, payload: dict) -> Evaluation:
        evaluation = Evaluation(**payload)
        self.db.add(evaluation)
        self.db.commit()
        self.db.refresh(evaluation)
        return evaluation

    def get_latest_for_control_asset(self, control_id: str, asset_identifier: str) -> Evaluation | None:
        return (
            self.db.query(Evaluation)
            .filter(Evaluation.control_id == control_id, Evaluation.asset_identifier == asset_identifier)
            .order_by(Evaluation.evaluated_at.desc())
            .first()
        )
