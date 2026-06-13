"""Dataset loader and validator for attack prompts."""

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SecurityTestCase:
    id: str
    category: str
    title: str
    prompt: str
    expected_safe_behavior: str
    severity: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SecurityTestCase":
        """Create a SecurityTestCase from a dictionary, validating all required fields."""
        required_fields = [
            "id",
            "category",
            "title",
            "prompt",
            "expected_safe_behavior",
            "severity",
        ]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: '{field}'")
            if not isinstance(data[field], str):
                raise ValueError(f"Field '{field}' must be a string")
        return cls(
            id=data["id"],
            category=data["category"],
            title=data["title"],
            prompt=data["prompt"],
            expected_safe_behavior=data["expected_safe_behavior"],
            severity=data["severity"],
        )


def get_default_dataset_path() -> str:
    """Resolve the default path to the sample attacks dataset."""
    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    return os.path.join(base_dir, "data", "prompts", "sample_attacks.json")


def load_attack_dataset(file_path: str = None) -> List[SecurityTestCase]:
    """Load, parse, and validate the attack prompts dataset."""
    if file_path is None:
        file_path = get_default_dataset_path()

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in dataset: {e}")

    if not isinstance(raw_data, list):
        raise ValueError("Dataset must be a JSON list of test cases")

    test_cases = []
    for index, item in enumerate(raw_data):
        if not isinstance(item, dict):
            raise ValueError(
                f"Test case at index {index} must be a JSON object"
            )
        test_cases.append(SecurityTestCase.from_dict(item))

    return test_cases
