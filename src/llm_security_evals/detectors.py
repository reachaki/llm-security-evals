"""Detectors for identifying malicious inputs like prompt injection and jailbreaks."""

from dataclasses import dataclass
from typing import List


@dataclass
class DetectorResult:
    """Structured result containing evaluation from a security detector."""

    detected: bool
    detector_name: str
    matched_patterns: List[str]
    risk_level: str
    explanation: str


class PromptInjectionDetector:
    """Detector for identifying obvious prompt injection phrases and patterns."""

    def __init__(self):
        """Initialize detector with standard injection trigger patterns."""
        self.name = "Prompt Injection Detector"
        self.patterns = [
            "ignore all previous instructions",
            "ignore instructions",
            "ignore translation",
            "system override",
            "developer debugging",
            "override instructions",
            "bypass guidelines",
            "developer mode",
        ]

    def detect(self, prompt: str) -> DetectorResult:
        """Scan the prompt input for known injection patterns."""
        matched = []
        for pattern in self.patterns:
            if pattern in prompt.lower():
                matched.append(pattern)

        if matched:
            return DetectorResult(
                detected=True,
                detector_name=self.name,
                matched_patterns=matched,
                risk_level="high",
                explanation=f"Potential prompt injection detected. Matched: {', '.join(matched)}",
            )
        return DetectorResult(
            detected=False,
            detector_name=self.name,
            matched_patterns=[],
            risk_level="none",
            explanation="No prompt injection patterns matched.",
        )


class JailbreakDetector:
    """Detector for identifying jailbreak-style phrases and policy overrides."""

    def __init__(self):
        """Initialize detector with standard jailbreak trigger patterns."""
        self.name = "Jailbreak Detector"
        self.patterns = [
            "act as dan",
            "do anything now",
            "freed from your guidelines",
            "bypass safety filters",
            "ignore safety",
            "evil mastermind",
            "unrestricted mode",
            "hidden instruction",
            "academic research",
        ]

    def detect(self, prompt: str) -> DetectorResult:
        """Scan the prompt input for known jailbreak patterns."""
        matched = []
        for pattern in self.patterns:
            if pattern in prompt.lower():
                matched.append(pattern)

        if matched:
            return DetectorResult(
                detected=True,
                detector_name=self.name,
                matched_patterns=matched,
                risk_level="high",
                explanation=f"Potential jailbreak pattern detected. Matched: {', '.join(matched)}",
            )
        return DetectorResult(
            detected=False,
            detector_name=self.name,
            matched_patterns=[],
            risk_level="none",
            explanation="No jailbreak patterns matched.",
        )

