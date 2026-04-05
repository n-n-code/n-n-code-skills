---
name: thinking
description: Structured thinking skill. Merges ideation, systems analysis, critical reasoning, and convergent planning. Use when a user needs to explore and narrow a vague idea, challenge assumptions, compare approaches, or converge on a practical next move in the same pass. Do not use when sustained divergence alone is the goal or when a candidate plan already exists and needs adversarial stress-testing.
---

# Thinking

Adjacent skills: **thinking** (explore, analyse, converge) -> **recursive-thinking** (adversarial stress-test) -> **dream-thinking** (retrospective learning).

Use **thinking** when the job is to move from ambiguity to a clear recommendation, experiment, or implementation-ready plan.
Use it when exploration and convergence both matter in the same session.
Do not escalate to **recursive-thinking** unless the decision is high-risk, contentious, or likely to hide important assumptions after a solid first pass here.

## Core Cadence

Run the skill through one simple loop:

- understand what is stuck
- explore only enough to improve the decision
- name what matters
- choose what changes next

Everything else in this skill supports that loop.

## Switch Skills When

- switch to **recursive-thinking** when a candidate recommendation, design, or plan already exists and the main job is to pressure-test it
- switch to a dedicated brainstorming skill when the user wants sustained divergence, creative volume, or facilitated ideation without convergence pressure
- switch to implementation or plan-writing once the main trade-off is settled and the remaining work is execution detail

## Default Stance

- inspect the current repo, docs, and constraints before proposing changes
- treat exploration and planning as one continuum: diverge only enough to improve the decision, then converge
- prefer one focused question at a time when clarification materially changes the outcome
- make assumptions explicit instead of silently filling gaps
- prefer incremental, testable moves over rewrites unless the complexity is structural
- optimise for learning value, carrying cost, and reversibility, not novelty
- remove unnecessary complexity ruthlessly

## Modes

Pick the lightest mode that fits. Switch modes as new information arrives.

- **Problem framing**: clarify the real problem, user, constraint, and success signal before discussing solutions
- **Ideation**: generate multiple plausible directions when the path is unclear or the first idea is too narrow
- **Assumption testing**: surface what must be true, what evidence exists, and what would disprove the current idea
- **Systems analysis**: map players, incentives, feedback loops, stocks/flows, and second-order effects when multiple actors interact, local optimisation can damage the whole, or effects compound over time
- **Plan convergence**: compare approaches, choose the narrowest viable move, and define validation

## Mode Selection

Before doing substantive work, choose the current mode from the user's actual bottleneck:

- unclear problem or weak framing -> **Problem framing**
- clear problem, unclear options -> **Ideation**
- promising option, unclear evidence or risks -> **Assumption testing**
- multi-actor, ecosystem, or incentive-heavy problem; at least two actors with misaligned incentives; or clear risk of second-order effects -> **Systems analysis**
- enough context gathered, main question is "what should we do?" -> **Plan convergence**

If the bottleneck changes, say so briefly and switch modes. Do not stay in ideation once one option is clearly ahead and the remaining work is evaluation or planning.

## Workflow

1. **Inspect** the current code, docs, arguments, and constraints.
2. **Understand what is stuck.**
   - State the goal, success criteria, and out-of-scope items.
   - If the user starts with a solution, check whether the underlying problem is actually settled.
   - If ambiguity is low and one viable path exists, skip heavy ideation.
3. **Explore only enough to improve the decision.**
   - Ask one focused question at a time.
   - Prefer multiple choice when choosing one direction.
   - If the answer will not change the design, make a labeled assumption and continue.
4. **Diverge** when the solution space is still underexplored.
   - Generate 3-7 distinct directions depending on task size.
   - Vary along meaningful dimensions: scope, user segment, timing, process vs product, add vs remove, quick win vs durable investment.
   - Include at least one subtraction or inversion option when useful.
   - Do not evaluate too early; weak divergence produces fake convergence.
   - Stop diverging once the option set is meaningfully different and further ideas would mostly repeat earlier patterns.
5. **Name what matters.**
   - Steelman the core claim or proposal before critiquing it.
   - List key assumptions, missing evidence, and the riskiest unknown.
   - For complex systems, map players, incentives, feedback loops, stocks, and flows.
   - Activate systems analysis when at least two actors have meaningfully different incentives, when a local improvement could hurt the broader system, or when delayed effects are likely to matter.
   - Trace second-order effects before recommending changes that shift incentives or constraints.
   - If reasoning gets tangled, break it into sequential steps and revise earlier conclusions explicitly.
   - If the user mainly wants critique of an already-formed plan, spend most of the pass here instead of reopening wide ideation.
6. **Compare** 2-3 serious approaches when the choice materially affects the outcome.
   - Compare on: user value, complexity, risk, reversibility, time-to-validate, and carrying cost.
   - For each rejected approach, state why it lost in one line.
   - If only one viable approach exists, say so and skip the forced comparison.
7. **Choose what changes next.**
   - "Narrowest" means the smallest step that meaningfully improves the situation or tests the key assumption.
   - When narrowest conflicts with quality, prefer quality unless explicitly time-boxed.
   - For high-uncertainty ideas, prefer the cheapest credible experiment over a full build.
8. **Produce** a concrete output using the structure below.
   - If the best next move is learning rather than building, the output may be an experiment, decision memo, or research step instead of an implementation plan.

## Decision Rules

- Understand the argument in terms its owner would accept before critiquing it.
- Separate conclusions, supporting points, evidence, and assumptions.
- Distinguish symptoms from root causes; keep asking why until the frame stops moving.
- Keep the core cadence visible in the response: what is stuck, what matters, and what changes next.
- Keep divergence and convergence explicit; do not mix them so loosely that the user cannot tell whether you are still exploring or already recommending.
- Flag hidden incentives and local optimisations that could damage the larger system.
- Prefer options that create durable leverage, not just local relief.
- Use frameworks as tools, not templates. Pull in only the smallest one that improves the decision.
- If new constraints appear during implementation, update the plan before continuing.

## Planning Stop Test

Thinking is sufficient when all three are true:

- the next step is concrete
- the main trade-off has been decided or explicitly deferred
- validation is clear enough to detect failure

## Anti-patterns

- converging on the first plausible idea without exploring alternatives
- inventing weak alternatives just to satisfy the comparison step
- asking broad discovery questions that do not change the decision
- treating frameworks like checklists instead of thinking tools
- critiquing a claim before restating it fairly
- analysing only first-order effects in multi-stakeholder systems
- staying in ideation after the decision has effectively been made
- using "narrowest" to justify avoiding necessary quality improvements
- producing a plan that sounds organised but leaves the next action ambiguous

## Output Structure

Scale to task size.

**Small tasks** (clear issue, bounded change):

```markdown
## Goal
One sentence.

## Key Insight
What matters most about the problem or trade-off.

## Approach
What to change or test and why.

## Validation
How to verify it worked.
```

**Medium tasks** (multiple files, meaningful trade-offs, moderate ambiguity):

```markdown
## Goal
What we're trying to achieve and what success looks like.

## Constraints
What must not break, what is out of scope.

## Assumptions
What we're taking as given and what would invalidate the plan.

## Approach Comparison
| Approach | Pros | Cons | Risk |
|----------|------|------|------|
| A        | ...  | ...  | ...  |
| B        | ...  | ...  | ...  |

Chosen: A, because [reason]. Not B, because [reason].

## Key Changes
By subsystem, file group, or experiment.

## Validation
Tests, manual checks, or acceptance criteria.
```

**Large or ambiguous tasks** (cross-cutting, ecosystem, or strategic):

```markdown
## Goal
What we're trying to achieve and why it matters now.

## System View
Players, incentives, constraints, and important second-order effects.

## Assumptions and Risks
What must be true, what is most likely to fail, and what evidence is missing.

## Approach Comparison
| Approach | Upside | Cost | Risk | Reversibility |
|----------|--------|------|------|---------------|
| A        | ...    | ...  | ...  | ...           |
| B        | ...    | ...  | ...  | ...           |

Chosen: A, because [reason]. Not B, because [reason].

## Phases
Ordered steps with dependencies noted.

## Validation
What success and failure look like.

## Rollback
What to do if the chosen path fails.
```
