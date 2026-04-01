---
name: recursive-thinking
description: Recursive self-questioning heuristic for stress-testing a plan, diagnosis, design, review, or recommendation before acting. Use when the user asks to use recursive thinking, go deeper, interrogate assumptions, pressure-test an approach, ask why/how questions, or find what would change the conclusion. Avoid for simple factual lookups or low-ambiguity tasks.
---

# Recursive Thinking

Use this skill when the task benefits from deliberate self-questioning before execution or conclusion.

The point is not to expand every branch mechanically. The point is to use recursive questioning to produce a better recommendation, plan, diagnosis, or critique.

## Use when

- the task has real ambiguity, trade-offs, or failure modes
- the user wants hidden assumptions, risks, or alternatives surfaced
- the answer should be stress-tested before committing to it
- the work would benefit from explicit why/how/evidence probes

## Avoid when

- the task is a simple factual lookup or direct transformation
- the user needs immediate execution rather than exploratory analysis
- recursion would add length without changing the work

## Success criteria

A good recursive-thinking pass should do at least one of these:

- sharpen the problem framing
- expose a hidden assumption
- identify a material risk or failure mode
- improve the implementation or decision path
- change the recommendation, confidence, or next action

If the recursion is not changing the work, compress or stop.

## Core heuristic

- treat `n` as the maximum number of first-order branches
- generate up to `n` strong first-order questions about the task
- answer each question directly and ground the answer in observed facts where possible
- expand only the highest-yield branches, usually `1-3` unless the user asks for more
- let depth be governed by marginal insight, not by `n`
- prefer depth that changes the work over coverage that pads the output
- synthesize what changed and what should happen next

## Grounding rules

- mark each important claim as `observed`, `inferred`, or `unknown`
- prefer task-specific evidence over generic reasoning
- if a branch depends on an unstated assumption, name it explicitly
- if evidence is missing, say what would verify or falsify the branch

## Workflow

1. Identify the object of analysis:
   the decision, implementation, request, plan, bug, design, or claim being worked on.
2. Determine `n`:
   if the user already gave `n`, use it unless it would make the output unusable. If the user did not give `n`, ask for it or choose a small default only when asking would add no value.
3. Define the success target:
   decide whether this pass is mainly for diagnosis, design, review, strategy, writing, or another concrete outcome.
4. Generate up to `n` first-order questions.
   Make them sibling questions covering meaningfully different angles such as objective, constraints, evidence, alternatives, failure modes, incentives, interfaces, reversibility, or verification.
5. Score branch quality before recursing.
   Prefer branches that expose a hidden assumption, reduce uncertainty, change the plan, improve verification, or eliminate a bad option.
6. Answer the first-order questions.
   Keep answers concrete and grounded in the current task.
7. Recurse selectively with `but why` questions.
   Use these for purpose, causality, necessity, priority, or assumption testing. Do not force `n` follow-ups if the branch is already exhausted.
8. Recurse selectively with `but how` questions.
   Use these for mechanism, implementation, validation, execution, rollback, recovery, or measurement.
9. Allow better probe types when they fit.
   If `but why` or `but how` is too narrow, substitute a sharper probe such as `but what evidence`, `but what fails`, `but what trade-off`, or `but what would change my mind`.
10. Stop when marginal insight drops.
    Stop or compress a branch when it becomes repetitive, stops changing the recommendation, adds no new constraint, or no longer sharpens verification.
11. Write branch syntheses.
   For each expanded first-order question, capture what changed in understanding and whether the branch affected the work.
12. Write the final synthesis.
   Summarize the strongest insights, the key unknowns, the confidence level, and the recommended next action.

## Branch selection rubric

Score a branch higher when it is likely to:

- change the recommendation or next action
- reveal a hidden assumption or dependency
- identify a meaningful failure mode or regression risk
- sharpen validation, rollback, or decision thresholds

Score a branch lower when it mostly:

- repeats known points
- chases trivia or edge cases that do not affect the decision
- adds abstraction without improving the work

## Question design rules

- First-order questions should be materially different, not rephrasings.
- Prefer question sets that cover fixed dimensions rather than free-form brainstorming alone.
- Good branches change framing, confidence, risk, implementation, or validation.
- Weak branches repeat known points, chase trivia, or do not affect the work.
- Replace weak questions instead of preserving the count mechanically.

## Task-mode presets

Use the preset that best matches the task:

- `diagnosis`: behavior, symptoms, reproduction, causal chain, observability, rollback, edge cases
- `design`: objective, constraints, interfaces, alternatives, failure modes, reversibility, verification
- `review`: correctness, regression risk, hidden assumptions, missing tests, maintainability, safety
- `strategy`: incentives, trade-offs, evidence, alternatives, downstream effects, decision thresholds
- `writing`: audience, claim strength, structure, evidence, ambiguity, consequences, tone

## Output shape

Use a compact structure unless the user asked for a different format:

1. `n`, object of analysis, and success target
2. Top-level questions with short answers
3. Expanded branches only for the highest-yield questions
4. For each expanded branch: the top-level question, one deeper probe, the answer, and what changed
5. Final synthesis:
   what changed, what is still unknown, and what should happen next

### Minimal branch template

Use this shape for each expanded branch unless the user asked for a different format:

- top-level question
- short first answer
- deeper probe:
  `but why`, `but how`, `but what evidence`, `but what fails`, `but what trade-off`, or `but what would change my mind`
- short deeper answer
- branch synthesis:
  what changed and whether it affects the recommendation

## Control rules

- If `n` would make the output unmanageably large, say so briefly and suggest selective expansion or a smaller `n`.
- If the user explicitly wants the full tree anyway, comply, but warn that it may become low-signal.
- Do not skip a branch silently if you claimed you would expand it.
- Do not invent certainty.
- Prefer concise branch summaries over exhaustive repetition.
- If the task is trivial, use the heuristic lightly or say it is overkill.

## Anti-patterns

- treating `n` as a requirement to generate all `n x n x n` nodes
- asking abstract philosophy questions disconnected from the task
- repeating the same concern with slightly different wording
- using recursion to sound deep instead of changing the work

## Example trigger phrases

- `use recursive thinking on this`
- `ask yourself n questions and go deeper`
- `do recursive why/how thinking`
- `interrogate your own reasoning before answering`
- `use a self-questioning heuristic for deeper understanding`
- `pressure-test this plan before we proceed`
- `what assumptions are we missing here`
- `what would change your recommendation`

## Example applications

- Good fit:
  `Use recursive thinking with n=5 on whether this refactor should happen before or after the API change.`
- Good fit:
  `Do recursive why/how thinking on this bug report and focus on diagnosis.`
- Poor fit:
  `Use recursive thinking with n=10 to answer a simple factual question with no real ambiguity.`
