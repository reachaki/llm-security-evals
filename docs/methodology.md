# Methodology

The project will use a small local dataset of adversarial prompts grouped by category.

Each test case includes:
- id
- category
- title
- prompt
- expected safe behaviour
- severity

The framework will load the dataset, validate the structure, run each prompt through a mock or real model adapter, and record the result.

Initial evaluation will use a mock model so the framework can be tested without paid APIs or private keys. Later milestones can compare real model responses and analyse which attack categories are most effective.
