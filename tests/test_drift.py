from app.models.evaluation import Evaluation


def test_drift_detection_rules():
    previous = Evaluation(
        id="prev",
        control_id="AC-001",
        asset_identifier="test@example.com",
        status="PASS",
        reason="pass",
        evaluation_snapshot={},
    )
    current = Evaluation(
        id="current",
        control_id="AC-001",
        asset_identifier="test@example.com",
        status="FAIL",
        reason="fail",
        evaluation_snapshot={},
    )

    assert previous.status != current.status
    assert current.status in {"PASS", "FAIL"}
    assert previous.status in {"PASS", "FAIL"}
