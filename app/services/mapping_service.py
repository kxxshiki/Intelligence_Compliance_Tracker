from __future__ import annotations

from app.models.control import Control
from app.models.evidence import Evidence
from app.models.mapping import EvidenceControlMapping
from app.services.embedding_service import EmbeddingService


class MappingService:
    def __init__(self, db, embedding_service: EmbeddingService | None = None):
        self.db = db
        self.embedding_service = embedding_service or EmbeddingService()

    def rank_controls_for_evidence(self, evidence: Evidence, controls: list[Control]) -> list[dict]:
        if not evidence.embedding or not controls:
            return []
        ranked = []
        for control in controls:
            control_embedding = control.embedding or []
            score = self.embedding_service.cosine_similarity(evidence.embedding, control_embedding)
            ranked.append({
                "control": control,
                "score": score,
                "status": "AUTO_MAPPED" if score >= 0.85 else "REVIEW_REQUIRED" if score >= 0.65 else "UNMAPPED",
            })
        ranked.sort(key=lambda item: item["score"], reverse=True)
        return ranked

    def persist_mappings(self, evidence: Evidence, controls: list[Control]) -> list[EvidenceControlMapping]:
        mappings: list[EvidenceControlMapping] = []
        for ranked in self.rank_controls_for_evidence(evidence, controls):
            control = ranked["control"]
            mapping = EvidenceControlMapping(
                evidence_id=evidence.id,
                control_id=control.id,
                similarity_score=ranked["score"],
                mapping_status=ranked["status"],
            )
            self.db.add(mapping)
            self.db.commit()
            self.db.refresh(mapping)
            mappings.append(mapping)
        return mappings

    def get_mapped_controls(self, evidence_id: str) -> list[Control]:
        rows = (
            self.db.query(EvidenceControlMapping)
            .filter(EvidenceControlMapping.evidence_id == evidence_id)
            .order_by(EvidenceControlMapping.similarity_score.desc())
            .all()
        )
        controls = []
        for row in rows:
            control = self.db.query(Control).filter(Control.id == row.control_id).first()
            if control:
                controls.append(control)
        return controls
