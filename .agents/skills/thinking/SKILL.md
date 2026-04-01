---
name: thinking
description: Planning and design skill. Merges convergent planning, focused inquiry, and kaizen-style incremental improvement. Use for quick-to-medium planning tasks where structured thinking improves the outcome. Lighter than a full plan document — heavier than just asking the LLM to think.
---

# Thinking

If the repo has an `AGENTS.md`, read it first for repo conventions.

Adjacent skills: **brainstorming** (divergent generation) → **thinking** (convergent planning) → **recursive-thinking** (adversarial stress-testing) → **dream-thinking** (retrospective learning).

Use **thinking** when the main need is to converge on a practical plan.
Do not escalate to **recursive-thinking** unless the decision is high-risk, ambiguous, contentious, or likely to hide important assumptions.

Typical chaining:
- use **thinking** to converge on a plan
- use **recursive-thinking** to challenge that plan when risk or ambiguity is high
- use **dream-thinking** after execution, conflict, or reflection-worthy experience

## Default Stance

- understand the current repo shape before proposing changes
- prefer incremental, testable improvements over rewrites — unless the complexity is structural (>3 files or ongoing maintenance burden), in which case compare rewrite cost against compounding workaround cost
- keep plans implementation-ready and decision-complete
- remove unnecessary complexity ruthlessly

## Workflow

1. **Inspect** the current code, docs, and constraints.
2. **Clarify** goal, success criteria, and out-of-scope items. If ambiguous, ask one focused question.
3. **Compare** 2-3 approaches when the choice materially affects the outcome.
   - Compare on: complexity, risk, reversibility, time-to-implement, dependency count.
   - For each rejected approach, state why it lost in one line.
   - If only one viable approach exists, say so and skip comparison.
4. **Choose** the approach with the least unnecessary complexity.
   - "Narrowest" = fewest behavioral changes, smallest API surface, least cross-cutting risk.
   - When narrowest conflicts with quality, prefer quality unless explicitly time-boxed.
5. **Produce** a concrete plan using the output structure below.

## Plan Revision

Watch for: blocked on something unanticipated, new constraint discovered during implementation, execution diverging from assumptions. When any fires: update the plan before continuing.

## Planning Stop Test

Planning is sufficient when all three are true:
- the next implementation step is concrete
- the main trade-off has been decided or explicitly deferred
- validation is clear enough to detect failure

## Focused Inquiry Rules

- ask only questions that materially change the design
- prefer one issue at a time over broad unfocused discovery
- validate assumptions early when they affect architecture or rollout

## Kaizen Rules

- make invalid states harder to express
- use the type system, validation, and clear contracts to prevent mistakes
- when modifying a file, fix at most one small adjacent issue — do not refactor unrelated code

## Anti-patterns

- inventing weak alternative approaches just to satisfy the comparison step
- asking broad discovery questions that do not change the plan
- producing a plan that sounds organized but leaves the next action ambiguous
- using "narrowest" to justify avoiding necessary quality improvements

## Output Structure

Scale to task size.

**Small tasks** (single file, clear approach):

```
## Goal
One sentence.

## Approach
What to change and why.

## Validation
How to verify it works.
```

**Medium tasks** (multiple files, trade-offs):

```
## Goal
What we're trying to achieve and what success looks like.

## Constraints
What's out of scope, what must not break.

## Approach Comparison
| Approach | Pros | Cons | Risk |
|----------|------|------|------|
| A        | ...  | ...  | ...  |
| B        | ...  | ...  | ...  |

Chosen: A, because [reason]. Not B, because [reason].

## Key Changes
By subsystem or file group.

## Validation
Tests, manual checks, or acceptance criteria.

## Assumptions
What we're taking as given. What would invalidate the plan.
```

**Large tasks** (cross-cutting, architectural): Medium template plus:

```
## Phases
Ordered steps with dependencies noted.

## Rollback
What to do if a phase fails.
```
