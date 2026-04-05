# Skill validation

Use this when a generated or revised skill needs prompt-level validation before shipping.

## Goal

Prove that the skill:

- triggers for obvious requests
- triggers for paraphrased requests
- does not trigger for nearby but unrelated work
- gives another agent enough workflow detail to act without guessing

## Minimum prompt set

Write at least 3 prompts:

- `positive-obvious`: direct request using the most likely trigger words
- `positive-paraphrased`: same job, different wording
- `negative-adjacent`: close enough to confuse a weak description, but should not load the skill

Add more prompts only when the surface area is large or the user explicitly wants deeper validation.

## Comparison modes

Choose the lightest comparison that still answers the risk:

- `manual simulation`: read the prompt against the skill and judge whether the trigger and workflow would work
- `before vs after`: compare the current skill against the revised skill
- `with-skill vs without-skill`: use when the question is whether the skill adds real value
- `trigger wording A vs B`: use when the main risk is activation quality rather than body content

Do not build a heavy benchmark harness unless the repo or user wants it.

## When validation can be skipped

Skip validation only when all of these are true:

- the edit does not change the trigger surface
- the edit does not change the workflow meaning
- the edit does not add or remove important resources or assumptions

If any of those changed, run at least a lightweight prompt simulation.

## Review checklist

For each prompt, record:

- should the skill trigger
- which words or phrases should cause activation
- which part of the body should guide the next step
- where an agent could take a shortcut or misread the instructions

Common failures:

- description too vague to trigger
- description so broad that it over-triggers
- description summarizes workflow and tempts the agent to skip the body
- body assumes repo facts it never tells the reader to discover
- examples are longer than the rules they are supposed to clarify
- the agent over-validates a trivial copy edit because the skill never said when validation can be skipped

## Output

Summarize validation in 3 parts:

1. prompts used
2. what passed and failed
3. what changed because of the validation

If full validation was not practical, say so and state the residual risk plainly.
