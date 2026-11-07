from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.evidence import Evidence


class EvidenceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, evidence_id: str) -> Evidence | None:
        return self.db.query(Evidence).filter(Evidence.id == evidence_id).first()

    def list(self, source_type: str | None = None) -> list[Evidence]:
        query = self.db.query(Evidence)
        if source_type:
            query = query.filter(Evidence.source_type == source_type)
        return query.order_by(Evidence.collected_at.desc()).all()

    def create(self, payload: dict) -> Evidence:
        evidence = Evidence(**payload)
        self.db.add(evidence)
        self.db.commit()
        self.db.refresh(evidence)
        return evidence

    def update(self, evidence: Evidence, payload: dict) -> Evidence:
        for field, value in payload.items():
            setattr(evidence, field, value)
        self.db.commit()
        self.db.refresh(evidence)
        return evidence
