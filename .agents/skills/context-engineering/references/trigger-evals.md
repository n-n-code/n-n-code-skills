# Context Engineering Trigger Evals

Use these lightweight prompt simulations when changing this skill's trigger
description, boundaries, or README routing text.

## Expected `context-engineering`

- `Create a context packet before another agent starts this long repo migration.`
- `This session is drifting; audit what context is stale, missing, or noisy.`
- `Compact this conversation into a handoff so a new agent can continue safely.`
- `The agent keeps hallucinating APIs and ignoring repo conventions; fix the context setup.`
- `Decide what files, docs, logs, and tool output should be loaded for this task.`
- `We are switching from billing to auth work; refresh the working context.`
- `The context window is full of old tool results; decide what to trim, summarize, or keep verbatim.`
- `Design a session-memory handoff strategy for a long-running support agent without writing SDK code.`
- `The user's latest request conflicts with repo safety rules; decide what context and authority should govern.`
- `A handoff summary disagrees with current source files; audit which context should be trusted.`

## Expected `prompt-engineering`

- `Rewrite this system prompt so the agent calls tools more reliably.`
- `Design few-shot examples and a structured output schema for this classifier.`

## Expected `story-repo-scout`

- `Use this story card to find relevant implementation and test files.`
- `Append repo context with paths and evidence for this acceptance criteria card.`

## Expected `agents-md-generator`

- `Create an AGENTS.md for this repo from README and CI config.`
- `Convert these Claude instructions into generic repo agent instructions.`

## Expected `thinking`

- `Compare approaches and converge on a practical plan.`
- `Explore this vague product idea and decide the next experiment.`

## Expected domain or implementation skills first

- `Implement this Go worker cancellation fix.`
- `Security-review this tenant boundary for bypasses.`
- `Design a test strategy for this checkout flow.`
- `Add OpenAI Agents SDK session memory to this Python service.`

## Trigger Risks

- If the request says "context" but asks for repo file discovery from a story,
  route to `story-repo-scout`.
- If the request says "instructions", "prompt", or "few-shot", route to
  `prompt-engineering` unless the task is about selecting supporting material.
- If the request asks for durable repo-wide instructions, route to
  `agents-md-generator`.
- If the request asks for a persistent project artifact system, use this skill
  only if the user explicitly wants context management as the main workflow.
- If the request asks to implement a concrete SDK memory feature, route to the
  relevant implementation skill first and use this skill only for retention or
  compaction policy.
- If current source or repo instructions conflict with a summary, prefer the
  stronger authority or fresher evidence and record the conflict.
