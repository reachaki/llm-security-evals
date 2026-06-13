# Research Question

How do language models respond to adversarial prompts such as prompt injection, jailbreak attempts, secret extraction, policy override, tool misuse, and data leakage attempts?

This project is motivated by a real academic problem: hidden prompt injection text can be placed inside project briefs or documents. If a student pastes that brief into an AI assistant, the model may follow the hidden instruction instead of helping with the actual task.

The first research aim is to build a structured local evaluation framework that can load adversarial prompts, run them through a model or mock model, and record whether the response follows safe behaviour.
