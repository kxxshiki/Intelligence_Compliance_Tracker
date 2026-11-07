from __future__ import annotations

from datetime import datetime
from typing import Any


class RuleEngine:
    def _get_value(self, data: dict, field: str) -> Any:
        return data.get(field)

    def _matches_operator(self, actual: Any, operator: str, expected: Any) -> bool:
        if operator == "equals":
            return actual == expected
        if operator == "not_equals":
            return actual != expected
        if operator == "greater_than":
            return actual is not None and expected is not None and actual > expected
        if operator == "less_than":
            return actual is not None and expected is not None and actual < expected
        if operator == "exists":
            return actual is not None
        if operator == "contains":
            return actual is not None and expected in str(actual)
        return False

    def _evaluate_rule(self, rule: dict, facts: dict) -> tuple[str, str]:
        field = rule.get("field")
        operator = rule.get("operator")
        expected = rule.get("expected")
        if field is None or operator is None:
            return "UNKNOWN", "Rule is not structured correctly."
        actual = self._get_value(facts, field)
        if operator == "exists":
            return ("PASS", "Field exists.") if actual is not None else ("FAIL", f"Field '{field}' is missing.")
        if self._matches_operator(actual, operator, expected):
            return "PASS", f"Condition '{field} {operator} {expected}' passed."
        return "FAIL", f"Condition '{field} {operator} {expected}' failed (actual: {actual})."

    def evaluate(self, rule_definition: dict, facts: dict) -> dict:
        if not isinstance(rule_definition, dict):
            return {"status": "UNKNOWN", "reason": "No rule definition available."}
        if "if" in rule_definition and "then" in rule_definition:
            condition = rule_definition["if"]
            then_rule = rule_definition["then"]
            condition_status, _ = self._evaluate_rule(condition, facts)
            if condition_status != "PASS":
                return {
                    "status": "PASS",
                    "reason": "Conditional rule did not apply because required condition was not met.",
                    "evaluated_at": datetime.utcnow().isoformat(),
                }
            then_status, then_reason = self._evaluate_rule(then_rule, facts)
            return {"status": then_status, "reason": then_reason, "evaluated_at": datetime.utcnow().isoformat()}
        if "field" in rule_definition:
            status, reason = self._evaluate_rule(rule_definition, facts)
            return {"status": status, "reason": reason, "evaluated_at": datetime.utcnow().isoformat()}
        if "all_of" in rule_definition:
            results = [self.evaluate(item, facts) for item in rule_definition["all_of"]]
            if all(item["status"] == "PASS" for item in results):
                return {"status": "PASS", "reason": "All sub-rules passed.", "evaluated_at": datetime.utcnow().isoformat()}
            failed_reason = "; ".join(item["reason"] for item in results if item["status"] != "PASS")
            return {"status": "FAIL", "reason": failed_reason, "evaluated_at": datetime.utcnow().isoformat()}
        return {"status": "UNKNOWN", "reason": "Unsupported rule structure.", "evaluated_at": datetime.utcnow().isoformat()}
