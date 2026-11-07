from app.services.rule_engine import RuleEngine


def test_rule_engine_equals_and_operators():
    engine = RuleEngine()
    equality = engine.evaluate({"field": "mfa_enabled", "operator": "equals", "expected": True}, {"mfa_enabled": True})
    assert equality["status"] == "PASS"

    not_equal = engine.evaluate({"field": "mfa_enabled", "operator": "not_equals", "expected": True}, {"mfa_enabled": False})
    assert not_equal["status"] == "PASS"

    greater_than = engine.evaluate({"field": "days_since_last_login", "operator": "greater_than", "expected": 90}, {"days_since_last_login": 120})
    assert greater_than["status"] == "PASS"

    less_than = engine.evaluate({"field": "backup_age_hours", "operator": "less_than", "expected": 24}, {"backup_age_hours": 12})
    assert less_than["status"] == "PASS"

    conditional = engine.evaluate({
        "if": {"field": "days_since_last_login", "operator": "greater_than", "expected": 90},
        "then": {"field": "active", "operator": "equals", "expected": False},
    }, {"days_since_last_login": 120, "active": True})
    assert conditional["status"] == "FAIL"
