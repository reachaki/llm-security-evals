import pytest
from llm_security_evals.leakage import LeakageResult, ResponseLeakageDetector
from llm_security_evals.model import MockModel
from llm_security_evals.runner import EvaluationRunner


def test_api_key_leakage_detection():
    detector = ResponseLeakageDetector()
    res = detector.validate("Here is the API key: api_key_99999")
    assert res.detected is True
    assert "api_key" in res.matched_pattern_labels
    assert res.risk_level == "high"


def test_password_leakage_detection():
    detector = ResponseLeakageDetector()
    res1 = detector.validate("Your secret is confidential_pwd_abc123")
    assert res1.detected is True
    assert "password" in res1.matched_pattern_labels

    res2 = detector.validate("The user password is password_12345")
    assert res2.detected is True
    assert "password" in res2.matched_pattern_labels


def test_email_leakage_detection():
    detector = ResponseLeakageDetector()
    res = detector.validate("Contact me at user@example.com")
    assert res.detected is True
    assert "email" in res.matched_pattern_labels


def test_phone_number_leakage_detection():
    detector = ResponseLeakageDetector()
    res = detector.validate("Phone number: +1-555-0199")
    assert res.detected is True
    assert "phone_number" in res.matched_pattern_labels


def test_system_prompt_leakage_detection():
    detector = ResponseLeakageDetector()
    res = detector.validate("System setup: You are a helpful assistant...")
    assert res.detected is True
    assert "system_prompt" in res.matched_pattern_labels


def test_clean_response_not_flagged():
    detector = ResponseLeakageDetector()
    res = detector.validate("I cannot comply with this request.")
    assert res.detected is False
    assert len(res.matched_pattern_labels) == 0
    assert res.risk_level == "none"


def test_runner_leakage_integration():
    model = MockModel(mode="leakage")
    runner = EvaluationRunner(model)
    report = runner.run_eval()

    # Check that each result contains the leakage validation information
    for result in report["results"]:
        assert "leakage_validation" in result
        lv = result["leakage_validation"]
        assert "detected" in lv
        assert "detector_name" in lv
        assert "matched_pattern_labels" in lv
        assert "risk_level" in lv
        assert "explanation" in lv

        # In leakage mode, the mock model output triggers validation matches
        assert lv["detected"] is True
