# LLM Security Evaluations

This Python framework tests Large Language Models (LLMs) against security risks including prompt injection, jailbreak-style prompts, data leakage, and unsafe tool-use patterns.

## Why LLM Security Evaluation Matters

As large language models are integrated into production applications, they interact with untrusted inputs and external systems. Unlike traditional software, LLMs process instructions and data in a single text stream. This design opens up vulnerabilities like prompt injection, where an attacker can override system prompts to hijack model behavior. Evaluators must verify that applications remain secure against prompt manipulation, prevent leakage of sensitive system instructions or user data, and invoke external tools safely.

## Current Release

This release contains the sample attack dataset and local loader configuration. The framework now provides a baseline of security prompts and validation tools to verify incoming test sets.

### Project Structure

- `src/llm_security_evals/`: Core source directory for testing logic, loaders, and runners.
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
2. **Milestone 2 (Current)**: Attack dataset and loader implementation.
3. **Milestone 3**: Core evaluation engine and template runners.
4. **Milestone 4**: Detection mechanisms for prompt injection and jailbreak attacks.
5. **Milestone 5**: Data leakage detection rules and validators.
6. **Milestone 6**: Interactive tool-use simulation and sandboxed environment tests.
