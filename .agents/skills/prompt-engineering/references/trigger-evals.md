# Prompt Engineering Trigger Evals

Use these lightweight prompt-routing checks when revising the
`prompt-engineering` skill trigger or scope.

## Positive Prompts

These should trigger `prompt-engineering`.

- "Improve this system prompt and add eval cases."
- "Our Claude prompt is inconsistent on edge cases; help rewrite and test it."
- "Design a prompt for an agent that extracts invoice fields as JSON."
- "Debug why this tool-use prompt keeps calling the search tool too early."
- "Make this prompt cheaper and more cache-friendly without changing behavior."
- "Create few-shot examples for this classifier prompt."
- "Review this prompt for injection risks and unclear output requirements."

## Negative Adjacent Prompts

These should not trigger `prompt-engineering` by themselves.

- "Which OpenAI model should I use for this app?"
- "Rewrite this README section to sound clearer."
- "Write a polished LinkedIn post from these notes."
- "Add a Python API endpoint that calls an LLM."
- "Review this authentication flow for security issues."
- "Create an AGENTS.md for this repository."

## Routing Notes

- Model selection alone belongs to provider docs or model-selection guidance.
- Generic prose editing belongs to documentation, writing, or voice skills.
- LLM integration code should load the relevant implementation skill first;
  add `prompt-engineering` only when prompt behavior is the main problem.
- Prompt injection or tool-abuse reviews can use `prompt-engineering`, but load
  a security skill when data exposure, authorization, or trust boundaries are
  the central risk.
