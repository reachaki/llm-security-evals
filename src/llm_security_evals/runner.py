"""Evaluation runner to run attack dataset against a model and record results."""

from typing import Any, Dict
from llm_security_evals.loader import load_attack_dataset
from llm_security_evals.model import MockModel
from llm_security_evals.scorer import score_response


class EvaluationRunner:
    """Runner coordinating dataset loading, model querying, and scoring."""

    def __init__(self, model: MockModel):
        """Initialize EvaluationRunner with a mock model."""
        self.model = model

    def run_eval(self, file_path: str = None) -> Dict[str, Any]:
        """Run the evaluation dataset and return a summary of findings."""
        test_cases = load_attack_dataset(file_path)
        results = []
        passed_count = 0
        failed_count = 0

        for case in test_cases:
            response = self.model.generate(case.prompt)
            is_safe = score_response(response, case.category)
            result_status = "pass" if is_safe else "fail"

            if is_safe:
                passed_count += 1
            else:
                failed_count += 1

            results.append(
                {
                    "id": case.id,
                    "category": case.category,
                    "title": case.title,
                    "prompt": case.prompt,
                    "response": response,
                    "expected_safe_behavior": case.expected_safe_behavior,
                    "severity": case.severity,
                    "result": result_status,
                }
            )

        return {
            "total": len(test_cases),
            "passed": passed_count,
            "failed": failed_count,
            "results": results,
        }
