# Observations

## Current system

The framework now has a full local evaluation loop:

1. Load adversarial prompts.
2. Detect prompt injection and jailbreak patterns before model execution.
3. Run a mock model response.
4. Score whether the response follows safe behaviour.
5. Check the response for simulated sensitive data leakage.
6. Return structured results.

## What this proves

The project shows that prompt injection and leakage risks can be turned into testable evaluation cases rather than vague concerns.

It also shows that security checks can be split into two stages:

- input-side detection before the model responds
- output-side validation after the model responds

This is useful because some attacks are visible in the prompt, while others only become visible in the model output.

## What worked well

The dataset loader, mock model, detectors, scorer, and leakage validator all work together under test.

The test suite gives confidence that the framework is stable enough to extend.

The mock model makes the framework safe to develop without API keys, paid providers, or real secrets.

## Limitations

The detectors are mostly rule-based.

This means they are likely to miss:
- obfuscated instructions
- paraphrased attacks
- unicode tricks
- indirect prompt injections
- attacks hidden inside long context

The mock model does not prove how real models behave. It only proves that the evaluation framework can run.

## Research value

The project is useful as a starting point for AI security evaluation research. It can be extended to compare real models, test different prompt injection styles, and measure how often attack categories cause unsafe responses.

The next research step is to generate experiment reports and compare different mock or real model behaviours across the same dataset.
