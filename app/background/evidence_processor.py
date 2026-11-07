from __future__ import annotations

from app.db.session import SessionLocal
from app.models.control import Control
from app.models.evidence import Evidence
from app.services.audit_service import AuditService
from app.services.drift_service import DriftService
from app.services.embedding_service import EmbeddingService
from app.services.evaluation_service import EvaluationService
from app.services.finding_service import FindingService
from app.services.mapping_service import MappingService
from app.services.normalization_service import NormalizationService


async def process_evidence(evidence_id: str):
    db = SessionLocal()
    try:
        evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
        if not evidence:
            return
        evidence.processing_status = "PROCESSING"
        db.commit()
        AuditService(db).log_event("EVIDENCE_PROCESSING_STARTED", "EVIDENCE", evidence.id, {"source_name": evidence.source_name})

        normalized = NormalizationService().normalize(evidence.evidence_type, evidence.raw_data)
        evidence.normalized_data = normalized
        evidence.embedding = EmbeddingService().embed_text(str(normalized))
        db.commit()

        controls = db.query(Control).filter(Control.active.is_(True)).all()
        mapping_service = MappingService(db)
        mapping_service.persist_mappings(evidence, controls)

        evaluations = EvaluationService(db).evaluate_evidence(evidence.id)
        for evaluation in evaluations:
            finding = FindingService(db).create_or_update_for_evaluation(evaluation)
            if finding:
                AuditService(db).log_event("FINDING_CREATED", "FINDING", finding.id, {"control_id": finding.control_id})
            drift = DriftService(db).detect(evaluation)
            if drift:
                AuditService(db).log_event("DRIFT_DETECTED", "DRIFT", drift.id, {"status": drift.current_status})

        evidence.processing_status = "PROCESSED"
        AuditService(db).log_event("EVIDENCE_PROCESSED", "EVIDENCE", evidence.id, {"status": "PROCESSED"})
        db.commit()
    finally:
        db.close()
