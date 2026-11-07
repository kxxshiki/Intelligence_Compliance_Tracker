from __future__ import annotations

from datetime import datetime

from app.models.control import Control
from app.models.drift import Drift
from app.models.evaluation import Evaluation
from app.models.finding import Finding
from app.models.remediation import Remediation


class AnalyticsService:
    def __init__(self, db):
        self.db = db

    def _status_counts(self, records, status_field: str = "status") -> dict[str, int]:
        counts: dict[str, int] = {}
        for row in records:
            status_value = getattr(row, status_field)
            counts[status_value] = counts.get(status_value, 0) + 1
        return counts

    def dashboard(self) -> dict:
        controls = self.db.query(Control).all()
        evaluations = self.db.query(Evaluation).all()
        findings = self.db.query(Finding).all()
        drifts = self.db.query(Drift).all()
        remediations = self.db.query(Remediation).all()

        evaluation_counts = self._status_counts(evaluations)
        finding_counts = self._status_counts(findings)
        finding_severity = self._status_counts(findings, "severity")

        remediation_counts = self._status_counts(remediations, "action")
        drift_counts = self._status_counts(drifts, "current_status")

        pass_count = evaluation_counts.get("PASS", 0)
        fail_count = evaluation_counts.get("FAIL", 0)
        unknown_count = evaluation_counts.get("UNKNOWN", 0)
        total = pass_count + fail_count + unknown_count
        score = round((pass_count / total) * 100, 2) if total else 0.0

        return {
            "overall_compliance_score": score,
            "total_controls": len(controls),
            "total_evaluations": total,
            "passed_controls": pass_count,
            "failed_controls": fail_count,
            "unknown_controls": unknown_count,
            "open_findings": finding_counts.get("OPEN", 0),
            "findings_by_severity": finding_severity,
            "remediation_status": remediation_counts,
            "drift_summary": {
                "total": len(drifts),
                "by_status": drift_counts,
            },
            "evaluation_status_summary": evaluation_counts,
            "compliance_trends": self.compliance_trends(),
            "finding_trends": self.finding_trends(),
        }

    def compliance_score(self) -> dict:
        evaluations = self.db.query(Evaluation).all()
        pass_count = sum(1 for item in evaluations if item.status == "PASS")
        fail_count = sum(1 for item in evaluations if item.status == "FAIL")
        unknown_count = sum(1 for item in evaluations if item.status == "UNKNOWN")
        total = pass_count + fail_count + unknown_count
        score = round((pass_count / total) * 100, 2) if total else 0.0
        return {
            "overall_compliance_score": score,
            "total_controls": total,
            "passed_controls": pass_count,
            "failed_controls": fail_count,
            "unknown_controls": unknown_count,
            "generated_at": datetime.utcnow().isoformat(),
        }

    def control_summary(self) -> dict:
        evaluations = self.db.query(Evaluation).all()
        return {
            "passed": sum(1 for item in evaluations if item.status == "PASS"),
            "failed": sum(1 for item in evaluations if item.status == "FAIL"),
            "unknown": sum(1 for item in evaluations if item.status == "UNKNOWN"),
            "total": len(evaluations),
        }

    def finding_summary(self) -> dict:
        findings = self.db.query(Finding).all()
        return {
            "total": len(findings),
            "open": sum(1 for item in findings if item.status == "OPEN"),
            "resolved": sum(1 for item in findings if item.status == "RESOLVED"),
            "by_severity": self._status_counts(findings, "severity"),
        }

    def drift_summary(self) -> dict:
        drifts = self.db.query(Drift).all()
        return {
            "total": len(drifts),
            "by_status": self._status_counts(drifts, "current_status"),
        }

    def compliance_trends(self) -> list[dict]:
        evaluations = self.db.query(Evaluation).all()
        buckets: dict[str, dict] = {}
        for item in evaluations:
            key = item.evaluated_at.date().isoformat() if item.evaluated_at else datetime.utcnow().date().isoformat()
            bucket = buckets.setdefault(key, {"date": key, "PASS": 0, "FAIL": 0, "UNKNOWN": 0})
            bucket[item.status] = bucket.get(item.status, 0) + 1
        return [
            {"date": value["date"], "PASS": value.get("PASS", 0), "FAIL": value.get("FAIL", 0), "UNKNOWN": value.get("UNKNOWN", 0)}
            for _, value in sorted(buckets.items())
        ]

    def finding_trends(self) -> list[dict]:
        findings = self.db.query(Finding).all()
        buckets: dict[str, int] = {}
        for item in findings:
            key = item.first_detected_at.date().isoformat() if item.first_detected_at else datetime.utcnow().date().isoformat()
            buckets[key] = buckets.get(key, 0) + 1
        return [{"date": key, "count": value} for key, value in sorted(buckets.items())]
