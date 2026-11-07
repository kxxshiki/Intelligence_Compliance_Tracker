from __future__ import annotations

from datetime import datetime

from app.models.evidence import Evidence
from app.models.evaluation import Evaluation
from app.services.mapping_service import MappingService
from app.services.rule_engine import RuleEngine


class EvaluationService:
    def __init__(self, db):
        self.db = db
        self.mapping_service = MappingService(db)
        self.rule_engine = RuleEngine()

    def evaluate_evidence(self, evidence_id: str) -> list[Evaluation]:
        evidence = self.db.query(Evidence).filter(Evidence.id == evidence_id).first()
        if evidence is None:
            return []
        controls = self.mapping_service.get_mapped_controls(evidence_id)
        if not controls:
            return []
        evaluations: list[Evaluation] = []
        for control in controls:
            facts = evidence.normalized_data or {}
            if isinstance(facts, dict):
                facts = facts.get("attributes", {})
            result = self.rule_engine.evaluate(control.rule_definition, facts)
            eval_record = Evaluation(
                control_id=control.control_id,
                evidence_id=evidence.id,
                asset_identifier=evidence.asset_identifier,
                status=result.get("status", "UNKNOWN"),
                reason=result.get("reason", "No reason provided."),
                evaluation_snapshot={
                    "control_id": control.control_id,
                    "asset_identifier": evidence.asset_identifier,
                    "status": result.get("status", "UNKNOWN"),
                    "reason": result.get("reason", "No reason provided."),
                    "rule_definition": control.rule_definition,
                },
                evaluated_at=datetime.utcnow(),
            )
            self.db.add(eval_record)
            self.db.commit()
            self.db.refresh(eval_record)
            evaluations.append(eval_record)
        return evaluations
