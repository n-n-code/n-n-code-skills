# Prompt Engineering Trigger Evals

Use these lightweight prompt-routing checks when revising the
`prompt-engineering` skill trigger or scope.

## Positive Prompts

These should trigger `prompt-engineering`.

- "Improve this system prompt and add eval cases."
  *Why:* prompt artifact + evals are the deliverable.
- "Our Claude prompt is inconsistent on edge cases; help rewrite and test it."
  *Why:* reliability of an existing prompt is the main concern.
- "Design a prompt for an agent that extracts invoice fields as JSON."
  *Why:* structured-output prompt design is the artifact.
- "Debug why this tool-use prompt keeps calling the search tool too early."
  *Why:* tool-boundary behavior in a prompt is the failure to diagnose.
- "Make this prompt cheaper and more cache-friendly without changing behavior."
  *Why:* cost/cache optimization with prompt-shape changes.
- "Create few-shot examples for this classifier prompt."
  *Why:* example *wording* is owned here (selection is `context-engineering`).
- "Review this prompt for injection risks and unclear output requirements."
  *Why:* prompt-level safety and output-contract review.

## Negative Adjacent Prompts

These should not trigger `prompt-engineering` by themselves.

- "Which OpenAI model should I use for this app?"
- "Rewrite this README section to sound clearer."
- "Write a polished LinkedIn post from these notes."
- "Add a Python API endpoint that calls an LLM."
- "Review this authentication flow for security issues."
- "Create an AGENTS.md for this repository."

## Routing Notes

- Model selection alone belongs to current official provider docs; for
  OpenAI-specific model guidance, use an OpenAI docs skill or official-doc tool
  when the session provides one, otherwise verify official OpenAI docs directly.
- Generic prose editing belongs to documentation, writing, or voice skills.
- LLM integration code should load the relevant implementation skill first;
  add `prompt-engineering` only when prompt behavior is the main problem.
- Prompt injection or tool-abuse reviews can use `prompt-engineering`, but load
  a security skill when data exposure, authorization, or trust boundaries are
  the central risk.
