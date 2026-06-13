# LLM Security Evaluations

This Python framework tests Large Language Models (LLMs) against security risks including prompt injection, jailbreak-style prompts, data leakage, and unsafe tool-use patterns.

## Why LLM Security Evaluation Matters

As large language models are integrated into production applications, they interact with untrusted inputs and external systems. Unlike traditional software, LLMs process instructions and data in a single text stream. This design opens up vulnerabilities like prompt injection, where an attacker can override system prompts to hijack model behavior. Evaluators must verify that applications remain secure against prompt manipulation, prevent leakage of sensitive system instructions or user data, and invoke external tools safely.

## Current Release

This initial version provides the foundational repository layout, dependencies, packaging configuration, and test suite setup. Future logic and evaluation suites will build upon this structure.

### Project Structure

- `src/llm_security_evals/`: Core source directory for testing logic, validators, and runners.
- `tests/`: Project test suite.
- `data/prompts/`: Standardized prompt templates for security testing.
- `docs/`: Framework documentation.

## Installation and Testing

### Prerequisites

- Python 3.9 or higher

### Running Tests

This project uses `pytest` for testing. Run the tests with the following command:

```bash
python -m pytest
```

## Planned Milestones

1. **Milestone 1 (Current)**: Project setup, package configuration, and README.
2. **Milestone 2**: Core evaluation engine and prompt template loaders.
3. **Milestone 3**: Detection mechanisms for prompt injection and jailbreak attacks.
4. **Milestone 4**: Data leakage detection rules and validators.
5. **Milestone 5**: Interactive tool-use simulation and sandboxed environment tests.
