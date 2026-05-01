---
name: story-implementation-planner
description: Model-aware implementation planning workflow for turning a clarified story card plus repo context into an actionable plan for a human or coding agent. Use after user-story-clarifier and story-repo-scout when a story needs ordered implementation steps; avoid for story drafting, repo scouting alone, or direct code implementation.
---

# Story Implementation Planner

Turn a clear story and repo context into an implementation plan sized for the
model, agent, or human who will execute it.

## When To Use

- create an actionable implementation plan from a story card and repo context
- optimize a plan for a named model, local model, coding agent, or human
- prepare a handoff before implementation starts
- break a story into ordered steps, risks, and validation targets

## Not For

- clarifying vague product behavior; use `user-story-clarifier`
- finding relevant repo files; use `story-repo-scout`
- direct code edits after a plan already exists
- broad architecture strategy or open-ended technical design

## Core Workflow

1. Read the `Story Card`, `Repo Context`, acceptance criteria, open questions,
   and relevant file list before planning.
2. Select a model profile:
   - `standard-agent` by default when the user is unsure
   - `frontier-gpt` for strong GPT/Codex-style agents with broad context and
     reliable multi-file reasoning
   - `local-small` for smaller local models such as Qwen-class 20B-30B models
   - `human` when the plan is primarily for a developer to execute manually
3. Check readiness. If behavior, repo context, or blockers are too unclear to
   plan honestly, list the missing inputs instead of inventing work.
4. Define the implementation boundary:
   - files likely to change
   - files likely to read only
   - files likely unrelated or explicitly not to touch
   - tests or validation targets
   - explicit non-goals and assumptions
5. Decide task shape before writing steps:
   - prefer vertical slices that produce working behavior
   - keep shared design decisions above the tasks that depend on them
   - mark dependencies and parallelizable work explicitly
6. Produce ordered steps that preserve behavior and reduce context load.
7. Attach the smallest validation path that proves the story.
8. Run a self-review before finishing: check acceptance-criteria coverage,
   placeholders, dependency order, risky assumptions, and rollback needs.
9. Tighten the plan for the selected model profile before finishing.

## Model Profiles

### `standard-agent`

- Use 4-8 ordered steps.
- Treat 9-12 steps as a warning range that may need re-splitting.
- Keep each step tied to known files or behavior.
- Include assumptions, blockers, and validation commands when known.
- Avoid broad refactors unless the story requires them.

### `frontier-gpt`

- Allow parallelizable tracks when file ownership is clear. Express as named
  tracks (e.g., `Track A: API`, `Track B: UI`) with explicit join points.
- Permit reading >5 files in parallel before the first edit when multi-file
  reasoning is required.
- Allow refactors when the story warrants and the repo's existing patterns
  support it; flag the refactor scope explicitly so it can be approved or cut.
- Require an invariant matrix when changes touch shared state across files
  (rows: invariants; columns: files affected).
- Include cross-file invariants, sequencing risks, and integration checks.
- Call out where deeper repo reading should happen before editing.
- Treat 9-12 top-level steps or tracks as a warning range that may need
  re-splitting.
- Keep the plan concise; do not use model strength as a reason to overplan.

### `local-small`

- Use simple linear steps with one main goal per step.
- Limit the first edit pass to 1-3 files when possible.
- Treat more than 8 steps as too large for this profile unless the user
  explicitly accepts the risk.
- Prefer explicit file paths, exact search terms, and concrete checkpoints.
- Avoid implicit architecture leaps, broad renames, and speculative abstractions.
- Include a `First Action` block with exact files to open, first change or
  decision, first validation checkpoint, and stop condition.
- Add a stop-and-report checkpoint before any risky or unclear change.
- **Output budget.** Plan ≤200 lines. Each step ≤5 lines. No inline code blocks
  longer than 10 lines unless naming an exact existing function signature.

### `human`

- Use a concise task list with rationale and validation notes.
- Surface decisions-needed-from-human as explicit checkpoints (`Decide:` lines).
- Name the runnable git/build/test commands the human will use, not pseudo-
  commands. Example: `pnpm test packages/auth -- --run`, not `run the tests`.
- Omit agent-only constructs (`First Action`, `Stop if`, model token budgets);
  the human reads the whole plan.
- Annotate steps with rough complexity (`~5 min`, `~30 min`, `half-day`) so the
  human can sequence around their own time.
- Name decisions the human should confirm before coding starts.
- Keep implementation details practical, not agent-instructional.
- Human plans may be longer than agent plans, but large plans should still name
  decision checkpoints and validation milestones.

## Implementation Plan Output

Use this structure by default:

```markdown
## Implementation Plan

Plan Status: Ready | Needs Inputs | Blocked

### Target Executor
Model/profile and why it was chosen.

### Size
Small | Medium | Large - relative to the executor profile. For agent profiles,
9-12 top-level steps/tracks is a warning range and more than 12 should be
re-split. For `local-small`, more than 8 steps should be re-split or accepted
explicitly by the user.

### Goal
The behavior to implement, in one or two sentences.

### Inputs
- Story card, repo context, assumptions, and blockers used for planning.

### First Action
Required for `local-small`, optional for agent profiles when it reduces
handoff ambiguity, and omitted for `human`.

- Open:
- Do:
- Check:
- Stop if:

### Files
- Change: path/to/file.ext - expected reason.
- Read: path/to/file.ext - context needed.
- Test: path/to/test.ext - validation target.
- Do Not Touch: path/to/file.ext - boundary reason.

### Steps
1. Ordered, concrete implementation step.

### Dependencies
- Step ordering, blockers, and safe parallel work.

### Risks and Blockers
- Anything that could change the plan or needs confirmation.

### Validation
- Smallest checks, tests, or manual probes that prove the acceptance criteria.

### Rollback
- How to back out or pause safely if the plan is risky.

### Handoff Notes
- What the implementing agent or human should do first.
```

Omit empty sections when they add no signal. Never invent paths, commands, or
repo structure not supported by the story or repo context.

`Plan Status` legend: `Ready` = plan is executable as written;
`Needs Inputs` = listed blockers must be resolved first; `Blocked` = cannot
plan honestly without missing repo or story input. See
`story-implementation-orchestrator` for the canonical vocabulary block when run
end-to-end.

## Planning Rules

- Preserve the story boundary; split the plan if the work spans unrelated goals.
- Prefer existing repo patterns over new abstractions.
- Keep steps observable: each step should produce code, tests, or a decision.
- Put validation close to the behavior it proves.
- Preserve `Do Not Touch` boundaries from repo scouting unless the story or user
  explicitly changes scope.
- For `local-small`, the `First Action` block must be executable without reading
  the whole plan again.
- Every verification step must name a runnable command, manual probe, or a clear
  reason validation is not yet available.
- If repo context is weak, include a scouting follow-up instead of guessing.
- If acceptance criteria and repo context disagree, flag the contradiction before
  planning implementation.
- **Migration / flag / rollout.** If the change alters persisted data, schema,
  wire format, public API, or shared file format: include a forward migration
  step, a backward-compatibility or rollback step, a backfill plan when data
  is rewritten, and a feature-flag or staged-rollout step. Risky or
  irreversible changes default to flag-gated. Note when the rollout requires
  coordinated deploys (e.g., consumer first, producer second).
- **Re-splitting.** If the plan exceeds 12 top-level steps or tracks for
  `standard-agent` or `frontier-gpt`, or 8 steps for `local-small`, recommend
  re-splitting the story instead of compressing steps. Return `Plan Status:
  Needs Inputs` with a split rationale unless the user explicitly accepts the
  larger plan.
- **Incremental delivery.** When possible, order steps so a working, verifiable
  checkpoint exists every 2-3 steps. Do not front-load all refactors before any
  behavior is visible.
- **Spike steps.** When a critical unknown (API contract, data shape, performance
  budget) blocks honest planning, include a `Spike:` step with a time-box, a
  concrete question to answer, and a stop-and-report checkpoint. Do not guess
  past a spike.

## Anti-Patterns

Reject and rewrite when these appear in a draft plan:

- **Vague refactor step.** `Refactor X for clarity` without a named target,
  observable change, or test that proves equivalence.
- **Vague test step.** `Add tests` without naming the assertion, fixture, or
  command that runs them.
- **Mixed-layer step.** A single step that touches DB schema and API surface
  and UI all at once. Split by layer with explicit ordering.
- **Missing rollback.** Plan changes production data, schema, or external
  contracts but has no rollback or backout entry.
- **Invented path.** Step references a file or symbol not present in repo
  context. Re-scout instead of guessing.
- **Placeholder padding.** Steps such as `Handle edge cases`, `Polish`, or
  `Finalize` without concrete behavior or verification.
- **Oversized plan.** A plan that exceeds the warning or split budget for its
  executor profile without flagging re-splitting or explicit acceptance.

## Composition Boundaries

- **Pipeline position.** Input comes from `user-story-clarifier` (story card)
  and `story-repo-scout` (Repo Context). Output is consumed by the executor
  named in `Target Executor`.
- **Shared vocabulary.** `Plan Status` (Ready / Needs Inputs / Blocked) joins
  story `Status` and `Confidence` from the upstream skills. See
  `story-implementation-orchestrator` for the canonical vocabulary block.
- **Downstream skills.** When the executor is an agent and the story implies
  repo-owned code changes, the plan should hand off to `project-core-dev`, plus
  the matching `coding-guidance-<lang>` overlay (e.g., `coding-guidance-go`,
  `coding-guidance-python`) and any relevant systems overlay
  (`backend-systems-guidance`, `ui-guidance`, `ui-design-guidance`). Use
  `documenter` for docs-only implementation plans and `project-config-and-tests`
  when config behavior or deterministic test coverage is the primary concern.
  Add `tester-mindset` when validation design, risk coverage, or
  acceptance-oracle quality is central to the story.
- **Re-scout, do not guess.** If repo context is weak or stale, return a
  `Needs Inputs` plan that asks for a re-scout instead of inventing paths.
- Use `user-story-clarifier` first when the story is unclear.
- Use `story-repo-scout` first when relevant files are missing.
- Use `tester-mindset` when the main question is what risk to cover.
- Use `security` for exploit-focused review.

## Examples

- `Create an actionable implementation plan from this story card and repo context.` ->
  choose a model profile and output `Implementation Plan`.
- `Plan this ticket for a local qwen coding agent using the relevant files found.` ->
  use the local-small profile and simple checkpoints.
- `Make a GPT-optimized plan from this story and repo scout output.` -> use
  `frontier-gpt` unless the user names a weaker executor.
- `Scour the repo and append relevant file paths.` -> use `story-repo-scout`.
