from __future__ import annotations

import json

from app.core.constants import ALLOWLISTED_REMEDIATION_ACTIONS
from app.demo.simulated_environment import SimulatedEnvironment
from app.models.finding import Finding
from app.models.remediation import Remediation
from app.services.llm.fallback_provider import FallbackProvider
from app.services.llm.ollama_provider import OllamaProvider


class RemediationService:
    def __init__(self, db):
        self.db = db
        self.environment = SimulatedEnvironment()

    def format_context(self, finding: Finding, control: object, evidence: object | None = None) -> str:
        evidence_payload = evidence.raw_data if evidence else {}
        return "\n".join([
            "CONTROL:",
            getattr(control, "name", "Unknown"),
            "CONTROL REQUIREMENT:",
            getattr(control, "description", "Unknown requirement") + " Rule: " + str(getattr(control, "rule_definition", {})),
            "EVIDENCE:",
            json.dumps(evidence_payload, sort_keys=True),
            "DETERMINISTIC RESULT:",
            "FAIL",
            "FINDING:",
            f"Title: {finding.title}",
            f"Description: {finding.description}",
            "The compliance status has already been determined by a deterministic rule engine. Do not change or reassess the compliance status.",
        ])

    def generate_grounded_remediation(self, finding: Finding, control: object, evidence: object | None = None) -> dict:
        context = self.format_context(finding, control, evidence)
        provider = OllamaProvider()
        try:
            llm_output = provider.generate_remediation(context)
        except Exception:
            llm_output = FallbackProvider().generate_remediation(context)
        lines = [line.strip() for line in llm_output.splitlines() if line.strip()]
        explanation = lines[0] if lines else "The compliance status has been determined by the rule engine and the issue requires remediation."
        root_cause = lines[1] if len(lines) > 1 else "The control failed against the evaluated evidence."
        recommended_steps = "\n".join(lines[2:]) if len(lines) > 2 else "1. Apply the approved remediation 2. Re-collect evidence 3. Re-evaluate compliance."
        payload = {
            "explanation": explanation,
            "root_cause": root_cause,
            "recommended_steps": recommended_steps,
        }
        self.db.add(Remediation(
            finding_id=finding.id,
            control_id=getattr(control, "control_id", "UNKNOWN"),
            asset_identifier=finding.asset_identifier,
            action="MANUAL_REVIEW",
            explanation=payload["explanation"],
            root_cause=payload["root_cause"],
            recommended_steps=payload["recommended_steps"],
            payload=payload,
        ))
        self.db.commit()
        return payload

    def execute_allowlisted_action(self, finding: Finding, action: str) -> dict:
        action_name = action.strip().upper()
        if action_name not in ALLOWLISTED_REMEDIATION_ACTIONS:
            raise ValueError(f"Action '{action_name}' is not allowlisted.")
        self.environment.apply_action(action_name, finding.asset_identifier)
        return {
            "action": action_name,
            "asset_identifier": finding.asset_identifier,
            "message": "Allowlisted remediation action applied to simulated environment.",
            "status": "APPLIED",
        }
