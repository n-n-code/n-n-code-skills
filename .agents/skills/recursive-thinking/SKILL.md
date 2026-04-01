---
name: recursive-thinking
description: Recursive self-questioning heuristic for stress-testing a plan, diagnosis, design, review, or recommendation before acting. Use when the user asks to use recursive thinking, go deeper, interrogate assumptions, pressure-test an approach, ask why/how questions, or find what would change the conclusion. Avoid for simple factual lookups or low-ambiguity tasks.
---

# Recursive Thinking

Deliberate self-questioning to stress-test a recommendation, plan, diagnosis, or critique before acting. Not for simple lookups or low-ambiguity tasks.

Adjacent skills: **brainstorming** (divergent generation) → **thinking** (convergent planning) → **recursive-thinking** (adversarial stress-testing) → **dream-thinking** (retrospective learning).

A good pass should: sharpen the problem framing, expose a hidden assumption, identify a material risk, improve the decision path, or change the recommendation. If the recursion is not changing the work, compress or stop.

Use this after **thinking** when a candidate plan, diagnosis, or recommendation exists and confidence needs to be challenged.
If there is no candidate object to stress-test yet, use **thinking** first.

Typical chaining:
- use **thinking** to converge on a plan
- use **recursive-thinking** to challenge that plan when risk or ambiguity is high
- use **dream-thinking** after execution, conflict, or reflection-worthy experience

## Understanding n

`n` controls **breadth** (number of top-level questions), not **depth** (levels of follow-up). Depth is governed by insight yield.

Do not treat `n` as recursion depth or expand every branch to `n` levels. This is selective iterative deepening: generate breadth, then deepen only the highest-yield branches.
Default to `n=4` or `n=5` unless the user asks otherwise. Higher `n` should widen coverage, not justify exhaustive expansion.

## Core heuristic

- generate up to `n` first-order questions covering meaningfully different angles
- answer each directly, grounded in observed facts where possible
- expand only the highest-yield branches (usually 1-3 unless asked for more)
- each expanded branch needs at least 2 levels of follow-up probes
- synthesize what changed and what should happen next

## Grounding rules

Mark each important claim as `observed`, `inferred`, or `unknown`.

**Light grounding** (default for design, strategy, writing):
- tag claims, name unstated assumptions, say what would verify or falsify

**Heavy grounding** (for diagnosis and review):
- `observed` must cite a source: `observed (file: path:line)`, `observed (git: hash)`, `observed (test output: result)`
- `inferred` must note derivation: `inferred (from: observed X + assumption Y)`
- `unknown` must note what would resolve it

## Workflow

1. **Identify** the object of analysis and define the success target (diagnosis, design, review, strategy, red-team, learning, decision, writing).
2. **Determine n.** Use the user's value, or ask, or pick a small default.
3. **Generate up to n first-order questions.** At least 2 must be adversarial — arguing against the obvious answer. Cover different angles: objective, constraints, evidence, alternatives, failure modes, incentives, interfaces, reversibility, verification.
4. **Honesty check.** Which question am I most uncomfortable answering? If it is not on the list, add it and drop the weakest.
5. **Score and answer.** Prefer branches that expose hidden assumptions, reduce uncertainty, change the plan, or eliminate bad options. Answer concretely.
6. **Recurse selectively.** Deepen with `but why`, `but how`, `but what evidence`, `but what fails`, `but what trade-off`, or `but what would change my mind` — whichever probe is sharpest. Do not force follow-ups on exhausted branches.
7. **Apply stopping tests.** Stop a branch when **all three** are true:
   - **Delta:** no longer changes the recommendation or next action
   - **Novelty:** introduces no new constraint, risk, or option
   - **Evidence:** does not move any claim between unknown → inferred → observed
8. **Synthesize.** For each expanded branch, state what changed. Then give a final synthesis: strongest insights, key unknowns, confidence level, contradictions (named, not smoothed over), recommended next action, and what not to do yet.

## Question design

- Questions must be materially different, not rephrasings
- Replace weak questions instead of preserving the count mechanically
- Good branches change framing, confidence, risk, or validation; weak branches repeat known points

## Task-mode presets

- `diagnosis`: behavior, symptoms, reproduction, causal chain, observability, rollback, edge cases. **Heavy grounding.**
- `design`: objective, constraints, interfaces, alternatives, failure modes, reversibility, verification
- `review`: correctness, regression risk, hidden assumptions, missing tests, maintainability, safety. **Heavy grounding.**
- `strategy`: incentives, trade-offs, evidence, alternatives, downstream effects, decision thresholds
- `writing`: audience, claim strength, structure, evidence, ambiguity, consequences, tone
- `red-team`: strongest counter-argument, adversarial exploitation, weakest link, worst case, what are we refusing to consider
- `learning`: what do I not understand, where does my mental model break, what would a worked example show
- `decision`: options with trade-offs, uncertainty, reversibility, regret minimization, decision thresholds

## Output shape

- **n ≤ 5:** Compact. Light grounding unless diagnosis/review.
- **n > 5:** Start with a **tl;dr** (3-5 lines). Expand only highest-yield branches; one-line answers for the rest.

Structure: tl;dr → n/object/target → questions with short answers → expanded branches → final synthesis.

Each expanded branch: question → short answer → deeper probe → deeper answer → (continue until stopping tests trigger) → branch synthesis.

## Anti-patterns

**Mechanical:** generating all n×n×n nodes; abstract philosophy disconnected from the task; repeating the same concern reworded; using recursion to sound deep instead of changing the work.

**Epistemic:** **confirmation deepening** (probing to reinforce rather than challenge — guard with adversarial questions); **authority laundering** (marking inferences as observed — guard with heavy grounding); **question gerrymandering** (avoiding questions that expose uncertainty — guard with honesty check); **synthesis whitewashing** (smoothing over contradictions — guard by naming them explicitly).

## Examples

- `Use recursive thinking with n=5 on whether this refactor should happen before or after the API change.`
- `Red-team this deployment plan with n=5 — what would go wrong?`
- `Do recursive why/how thinking on this bug report, focus on diagnosis.`
- Poor fit: `Use recursive thinking with n=10 to answer a simple factual question.`
