import os
import pytest
from llm_security_evals.loader import (
    SecurityTestCase,
    get_default_dataset_path,
    load_attack_dataset,
)


def test_dataset_file_exists():
    path = get_default_dataset_path()
    assert os.path.exists(path), f"Expected dataset file to exist at {path}"


def test_dataset_cases_count():
    cases = load_attack_dataset()
    assert len(cases) >= 20, f"Expected at least 20 cases, got {len(cases)}"


def test_required_fields_present():
    cases = load_attack_dataset()
    for case in cases:
        assert isinstance(case.id, str) and case.id
        assert isinstance(case.category, str) and case.category
        assert isinstance(case.title, str) and case.title
        assert isinstance(case.prompt, str) and case.prompt
        assert (
            isinstance(case.expected_safe_behavior, str)
            and case.expected_safe_behavior
        )
        assert isinstance(case.severity, str) and case.severity


def test_loader_returns_expected_instances():
    cases = load_attack_dataset()
    assert all(isinstance(case, SecurityTestCase) for case in cases)


def test_loader_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        load_attack_dataset("non_existent_file.json")


def test_loader_invalid_json_raises_error(tmp_path):
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("invalid json content")
    with pytest.raises(ValueError, match="Invalid JSON format"):
        load_attack_dataset(str(invalid_file))


def test_loader_invalid_fields_raises_error(tmp_path):
    invalid_file = tmp_path / "invalid_fields.json"
    invalid_file.write_text('[{"id": "inj-001", "category": "prompt injection"}]')
    with pytest.raises(ValueError, match="Missing required field"):
        load_attack_dataset(str(invalid_file))
