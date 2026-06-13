"""LLM Security Evals package."""

__version__ = "0.1.0"

from llm_security_evals.loader import SecurityTestCase, load_attack_dataset
from llm_security_evals.model import MockModel
from llm_security_evals.runner import EvaluationRunner
from llm_security_evals.scorer import score_response
from llm_security_evals.detectors import DetectorResult, PromptInjectionDetector, JailbreakDetector
from llm_security_evals.leakage import LeakageResult, ResponseLeakageDetector

__all__ = [
    "SecurityTestCase",
    "load_attack_dataset",
    "MockModel",
    "EvaluationRunner",
    "score_response",
    "DetectorResult",
    "PromptInjectionDetector",
    "JailbreakDetector",
    "LeakageResult",
    "ResponseLeakageDetector",
]


