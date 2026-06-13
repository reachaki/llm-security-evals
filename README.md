# LLM Security Evaluations

This Python framework tests Large Language Models (LLMs) against security risks including prompt injection, jailbreak-style prompts, data leakage, and unsafe tool-use patterns.

## Why LLM Security Evaluation Matters

As large language models are integrated into production applications, they interact with untrusted inputs and external systems. Unlike traditional software, LLMs process instructions and data in a single text stream. This design opens up vulnerabilities like prompt injection, where an attacker can override system prompts to hijack model behavior. Evaluators must verify that applications remain secure against prompt manipulation, prevent leakage of sensitive system instructions or user data, and invoke external tools safely.

## Current Release

This release contains the sample attack dataset, local mock model, scoring logic, evaluation runner, local prompt detectors, and data leakage validators. The framework now provides tools to load security prompts, scan inputs for prompt injection and jailbreak patterns locally before execution, simulate model responses, validate outputs for sensitive data leaks, and generate summary reports.

### Project Structure

- `src/llm_security_evals/`: Core source directory for loaders, models, scorers, detectors, leakage validators, and runners.
- `tests/`: Project test suite.
- `data/prompts/`: Standardized prompt templates for security testing.
- `docs/`: Framework documentation.

## Attack Dataset

The repository includes a sample attack prompt dataset under `data/prompts/sample_attacks.json`. This dataset contains 20 local security evaluation test cases.

Each test case consists of:
- `id`: A unique identifier for the test case.
- `category`: The security category of the attack.
- `title`: A short descriptive title.
- `prompt`: The specific input text sent to the model.
- `expected_safe_behavior`: Description of how a secure model should respond.
- `severity`: The potential risk impact (low, medium, high, or critical).

### Security Categories

The test cases cover the following core areas:
- **Prompt Injection**: Attempts to hijack model execution or override original system instructions using direct or indirect commands.
- **Secret Extraction**: Social engineering or direct queries attempting to retrieve confidential variables, system prompts, or API credentials.
- **Policy Override**: Jailbreak attempts (such as roleplaying) designed to bypass safety guidelines and content restrictions.
- **Tool Misuse**: Input payloads crafted to exploit external interfaces, database search tools, or system execution tools (such as SQL injections or path traversal).
- **Data Leakage**: Queries designed to extract personally identifiable information (PII) or proprietary user data across active session context boundaries.

### Loading the Dataset Locally

You can load and validate the dataset using the built-in loader:

```python
from llm_security_evals import load_attack_dataset

# Load the default sample dataset
test_cases = load_attack_dataset()

# Print details of the first test case
first_case = test_cases[0]
print(f"ID: {first_case.id}")
print(f"Category: {first_case.category}")
print(f"Prompt: {first_case.prompt}")
```

## Prompt and Jailbreak Detection

This framework includes local detectors to analyze incoming prompts for potential exploits before they reach the model.

### Available Detectors
- **Prompt Injection Detector**: Identifies phrases designed to override original instructions (e.g. "ignore all instructions" or "system override").
- **Jailbreak Detector**: Identifies roleplay or guideline bypass patterns (e.g. "act as dan" or "unrestricted mode").

### Why Pre-execution Detection Matters
Detecting malicious prompts before they reach the model allows applications to block attacks at the boundary. This approach saves token processing costs and prevents models from generating unsafe content in response to adversarial inputs.

### Limitations of Pattern-based Detection
- **Evasion**: Attackers can easily bypass exact string matching by using character substitutions, translation, or obfuscation.
- **False Positives**: General prompts discussing safety or containing similar strings may be incorrectly flagged.
- **Context Ignorance**: Pattern matching does not evaluate the semantic context of the prompt, meaning complex injections might go unnoticed.

## Running Local Evaluations

You can simulate security evaluations using the mock model adapter and the evaluation runner.

The `MockModel` supports four execution modes:
- `safe`: The model refuses to comply with malicious instructions, generating safe outputs.
- `unsafe`: The model complies with adversarial overrides, leaking credentials or executing payloads.
- `mixed`: The model generates safe responses for some prompts and complies with others.
- `leakage`: The model outputs responses containing fake sensitive data (API keys, passwords, emails) designed to trigger leakage detection.

### Code Example

```python
from llm_security_evals import MockModel, EvaluationRunner

# Initialize a mock model in mixed mode
model = MockModel(mode="mixed")

# Create a runner for the model
runner = EvaluationRunner(model)

# Run the local security evaluation
report = runner.run_eval()

# Print the final score summary
print(f"Total Runs: {report['total']}")
print(f"Passed: {report['passed']}")
print(f"Failed: {report['failed']}")

# Print detailed results
for result in report["results"]:
    print(f"[{result['id']}] {result['category']} - {result['result']}")

    # Check leakage validation
    lv = result["leakage_validation"]
    if lv["detected"]:
        print(f"  Leakage detected: {', '.join(lv['matched_pattern_labels'])}")
```

## Data Leakage Detection

The framework includes a response validator that scans model outputs for sensitive data patterns. This catches cases where a model leaks credentials, private contact information, or system instructions in its responses.

### Detected Patterns

| Label | What it catches | Example match |
|-------|----------------|---------------|
| `api_key` | Fake API key strings | `api_key_99999` |
| `password` | Fake passwords and credentials | `password_12345`, `confidential_pwd_abc` |
| `email` | Email addresses | `user@example.com` |
| `phone_number` | Phone numbers | `+1-555-0199` |
| `access_token` | Bearer tokens and access tokens | `token_abc12345`, `bearer eyJhbGci...` |
| `system_prompt` | System prompt leakage | `System setup: You are a helpful assistant` |

### Using the Leakage Detector Directly

```python
from llm_security_evals import ResponseLeakageDetector

detector = ResponseLeakageDetector()

# Check a response for sensitive data
result = detector.validate("The API key is api_key_99999")
print(result.detected)               # True
print(result.matched_pattern_labels)  # ['api_key']
print(result.risk_level)              # 'high'
print(result.explanation)             # 'Sensitive patterns leaked: api_key.'

# Clean responses are not flagged
result = detector.validate("I cannot share that information.")
print(result.detected)  # False
print(result.risk_level) # 'none'
```

### Integration with the Evaluation Runner

The leakage detector runs automatically as part of the evaluation pipeline. Every result in the report includes a `leakage_validation` field with the following structure:

```json
{
  "detected": true,
  "detector_name": "Response Leakage Detector",
  "matched_pattern_labels": ["api_key", "email"],
  "risk_level": "high",
  "explanation": "Sensitive patterns leaked: api_key, email."
}
```

### Limitations of Pattern-based Leakage Detection

- **Synthetic patterns only**: The current rules target fake or templated credentials. Real-world API keys and tokens come in many formats that may not match these patterns.
- **False positives**: Legitimate discussion of security topics or example code snippets may trigger matches.
- **No semantic analysis**: The detector uses regex matching and does not understand whether the detected data is genuinely sensitive in context.

## Installation and Testing

### Prerequisites

- Python 3.9 or higher

### Running Tests

This project uses `pytest` for testing. Run the tests with the following command:

```bash
python -m pytest
```

## Planned Milestones

1. **Milestone 1**: Project setup, package configuration, and README.
2. **Milestone 2**: Attack dataset and loader implementation.
3. **Milestone 3**: Mock model, scoring logic, and evaluation runner.
4. **Milestone 4**: Local prompt injection and jailbreak detectors.
5. **Milestone 5 (Current)**: Data leakage detection rules and validators.
6. **Milestone 6**: Interactive tool-use simulation and sandboxed environment tests.
