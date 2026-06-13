"""Multi-mode experiment runner for running evaluations across all model modes."""

from typing import Any, Dict, List, Optional
from llm_security_evals.model import MockModel
from llm_security_evals.runner import EvaluationRunner


# Default set of mock model modes to test against
DEFAULT_MODES = ["safe", "unsafe", "mixed", "leakage"]


class ExperimentRunner:
    """Runs the evaluation pipeline across multiple mock model modes.

    This provides a higher-level interface than EvaluationRunner. Instead of
    running a single mode at a time, it loops through all configured modes
    and collects per-mode summaries into one experiment result.
    """

    def __init__(self, modes: Optional[List[str]] = None):
        """Initialize with a list of mock model modes to test.

        Args:
            modes: List of mode strings. Defaults to all available modes.
        """
        self.modes = modes or list(DEFAULT_MODES)

    def run(self, dataset_path: Optional[str] = None) -> Dict[str, Any]:
        """Run the full experiment across all configured modes.

        Args:
            dataset_path: Optional path to a custom dataset file.

        Returns:
            Dictionary with per-mode results and an overall summary.
        """
        mode_results = {}

        for mode in self.modes:
            model = MockModel(mode=mode)
            runner = EvaluationRunner(model)
            report = runner.run_eval(dataset_path)
            mode_results[mode] = report

        return {
            "modes_tested": list(self.modes),
            "mode_results": mode_results,
            "summary": self._build_summary(mode_results),
        }

    def _build_summary(self, mode_results: Dict[str, Any]) -> Dict[str, Any]:
        """Build an aggregate summary across all modes."""
        total_tests = 0
        total_passed = 0
        total_failed = 0

        per_mode = {}
        for mode, report in mode_results.items():
            total_tests += report["total"]
            total_passed += report["passed"]
            total_failed += report["failed"]
            per_mode[mode] = {
                "total": report["total"],
                "passed": report["passed"],
                "failed": report["failed"],
                "pass_rate": report["passed"] / report["total"] if report["total"] > 0 else 0.0,
            }

        return {
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "overall_pass_rate": total_passed / total_tests if total_tests > 0 else 0.0,
            "per_mode": per_mode,
        }
