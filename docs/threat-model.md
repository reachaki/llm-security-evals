# Threat Model

The main threat is adversarial text being placed inside a document, prompt, brief, support ticket, web page, or tool output.

The attacker wants the model to:
- ignore the real user instruction
- reveal hidden or sensitive information
- follow a malicious instruction
- misuse a tool
- leak data from context
- override safety or policy constraints

This project does not currently test real production systems. It starts with local datasets and mock evaluation so the framework can be developed safely before adding real model providers.
