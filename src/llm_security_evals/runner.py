"""Evaluation runner to run attack dataset against a model and record results."""

from typing import Any, Dict
from llm_security_evals.loader import load_attack_dataset
from llm_security_evals.model import MockModel
from llm_security_evals.scorer import score_response
from llm_security_evals.detectors import PromptInjectionDetector, JailbreakDetector
from llm_security_evals.leakage import ResponseLeakageDetector


class EvaluationRunner:
    """Runner coordinating dataset loading, model querying, and scoring."""

    def __init__(self, model: MockModel):
        """Initialize EvaluationRunner with a mock model."""
        self.model = model

    def run_eval(self, file_path: str = None) -> Dict[str, Any]:
        """Run the evaluation dataset and return a summary of findings."""
        injection_detector = PromptInjectionDetector()
        jailbreak_detector = JailbreakDetector()
        leakage_detector = ResponseLeakageDetector()

        test_cases = load_attack_dataset(file_path)
        results = []
        passed_count = 0
        failed_count = 0

        for case in test_cases:
            # Run detectors on the prompt
            injection_res = injection_detector.detect(case.prompt)
            jailbreak_res = jailbreak_detector.detect(case.prompt)

            response = self.model.generate(case.prompt)
            is_safe = score_response(response, case.category)
            result_status = "pass" if is_safe else "fail"

            # Validate the response for data leakage
            leakage_res = leakage_detector.validate(response)

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
                    "detection": {
                        "prompt_injection": {
                            "detected": injection_res.detected,
                            "detector_name": injection_res.detector_name,
                            "matched_patterns": injection_res.matched_patterns,
                            "risk_level": injection_res.risk_level,
                            "explanation": injection_res.explanation,
                        },
                        "jailbreak": {
                            "detected": jailbreak_res.detected,
                            "detector_name": jailbreak_res.detector_name,
                            "matched_patterns": jailbreak_res.matched_patterns,
                            "risk_level": jailbreak_res.risk_level,
                            "explanation": jailbreak_res.explanation,
                        },
                    },
                    "leakage_validation": leakage_res.to_dict(),
                }
            )

        return {
            "total": len(test_cases),
            "passed": passed_count,
            "failed": failed_count,
            "results": results,
        }
