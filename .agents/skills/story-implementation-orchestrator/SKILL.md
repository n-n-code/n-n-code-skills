---
name: story-implementation-orchestrator
description: Coordinate the full story-to-plan preparation workflow across user-story-clarifier, story-repo-scout, and story-implementation-planner. Use when a rough ticket needs clarification, repo scouting, implementation planning, packet validation, partial-packet resumption, or downstream skill routing before coding; avoid direct implementation.
---

# Story Implementation Orchestrator

Coordinate the story-to-plan workflow without duplicating the detailed
instructions from the component skills.

This is a companion process overlay. Pair it with the component story skills
when the user wants end-to-end preparation before implementation.

## When To Use

- run the full pipeline from rough idea to actionable implementation plan
- prepare a story for a coding agent or human before code changes start
- choose which story-prep stages can be skipped because their outputs already exist
- produce a single handoff containing story, repo context, and implementation plan

## Not For

- direct implementation after a plan already exists
- story clarification only; use `user-story-clarifier`
- repo scouting only; use `story-repo-scout`
- model-aware planning only; use `story-implementation-planner`
- security review, broad architecture review, or whole-repo analysis

## Pipeline

0. **Inspect input.** Classify which stages already exist in the input
   (single story card? split story set? Repo Context? Implementation Plan?).
   Run the matching readiness check on each. Run only the missing or failing
   stages. This is the orchestrator's main reason to exist: do not re-run a
   stage whose output already passes its readiness check.
1. **Clarify.** Use `user-story-clarifier` unless the single-story or split-set
   readiness check passes.
2. **Select slice.** If clarification returns a split story set, plan only the
   first shippable slice by default unless the user asks for all slices.
   Materialize the selected slice as the active story card before scouting:
   copy relevant shared context, dependencies, assumptions, open questions, and
   deferred-work boundaries into the slice so downstream stages do not need to
   infer them from the full split set.
3. **Scout.** Use `story-repo-scout` unless the repo context readiness check
   passes.
4. **Plan.** Use `story-implementation-planner` with the story card, repo
   context, and target executor, unless the plan readiness check passes.
5. **Review.** Apply the Final Quality Gate (see below).
6. **Handoff.** Return the final preparation packet. Do not implement code.

## Resumption Examples

- **Story-only input.** Run scout + plan; skip clarify if the story passes
  its readiness check.
- **Story + Repo Context, no plan.** Run plan only.
- **Old plan + new story.** Re-scout if the named files no longer exist or
  the story's behavior changed; otherwise re-plan against existing context.
- **Full packet, user wants tweak.** Skip all stages; surface targeted edit.
- **Story marked `Blocked`.** Stop. Do not scout or plan against a blocked
  story; surface the blocker first.

## Readiness Checks

Each check has two tiers: **Presence** checks are mechanical (grep against the
upstream template's section names); **Quality** checks require semantic
judgment. Skip a stage only when both tiers pass.

**Single story ready** — `user-story-clarifier` template:

- *Presence:* `Status:`, `User Story` (or job-story / task-brief) block,
  `Acceptance Criteria`, `Out of Scope`, `Dependencies and Assumptions`,
  `Open Questions`, `Validation Notes` are all present.
- *Quality:* `Status: Ready`; acceptance criteria are observable pass/fail (no
  unfalsifiable adjectives); no Anti-Pattern phrasing per
  `user-story-clarifier`.

**Split story set ready** — `user-story-clarifier` split template:

- *Presence:* top-level `Status: Split Candidate`, `Split Story Set`, `Shared
  Context`, `Slice Order`, `Story Slices`, and `Deferred Work`; each slice has
  `Status`, `User Story`, `Acceptance Criteria`, `Out of Scope`,
  `Dependencies`, and `Validation Notes`.
- *Quality:* the first shippable slice is clearly marked and has
  `Status: Ready`; shared assumptions and deferred work are preserved; no slice
  silently merges unrelated personas, workflows, or dependency boundaries.

**Repo context ready** — `story-repo-scout` template:

- *Presence:* `Workspace` (when multi-workspace), `Search Handles`,
  `Relevant Files` table with >=1 row, `Tests and Validation Targets`,
  `Likely Unrelated / Do Not Touch`, `Open Repo Questions`.
- *Quality:* every `Relevant Files` row has Evidence and Confidence filled;
  no Anti-Pattern files (filename-only, generated, vendored); confidence
  values match the High/Medium/Low scale; terminology conflicts surfaced as
  open questions, not silently renamed; `Likely Unrelated / Do Not Touch` is
  populated when boundaries were found, or says `None identified` when no
  boundary was found.

**Plan ready** — `story-implementation-planner` template:

- *Presence:* `Plan Status:`, `Target Executor`, `Size`, `Goal`, `Files`,
  `Steps`, `Validation`, `Handoff Notes`. `First Action` block present when
  target executor is `local-small`, optional for agent profiles, and absent for
  `human`.
- *Quality:* `Plan Status: Ready` (not `Needs Inputs` or `Blocked`); every
  path in `Files` appears in upstream `Repo Context`; `Validation` names a
  runnable command, probe, or named acceptance check; no Anti-Pattern
  phrases (`TBD`, `handle edge cases`, `add tests`, `refactor X`, `polish`).

If any tier fails, run that stage instead of guessing.

## Preparation Packet Contract

The final packet must preserve these minimum fields when known:

- Story: status, title, actor or executor, goal, behavior, acceptance criteria,
  out of scope, dependencies or assumptions, and open blockers.
- Repo context: search handles, relevant files with evidence and confidence,
  likely entry points, tests or validation commands, do-not-touch boundaries or
  `None identified`, and open repo questions.
- Plan: target executor, first action when required or useful, ordered steps,
  dependencies, risks or blockers, validation, rollback, and handoff notes.

If a required field is unknown, mark it as blocked or unavailable instead of
silently omitting it.

## Shared Vocabulary

Single source of truth for all four pipeline skills:

- **Story Status** (`user-story-clarifier`): `Ready` | `Needs Clarification`
  | `Split Candidate` | `Blocked`.
- **Confidence** (story card + repo scout files): `High` | `Medium` | `Low`,
  with a one-line note naming what would raise it.
- **Plan Status** (`story-implementation-planner`): `Ready` | `Needs Inputs`
  | `Blocked`.

When a packet uses inconsistent labels, normalize to these names before
handoff.

## Orchestration Rules

- Keep stage outputs compact and appendable.
- Ask only questions that block the next stage or materially change the story.
- **Question cadence.** `user-story-clarifier` caps clarifying questions at
  ≤3. When orchestrated, surface them one at a time within that budget; stop
  asking once an answer removes the remaining questions. If code or docs can
  answer a question, inspect those first.
- For split story sets, preserve the remaining slices as deferred work instead
  of folding them into the first implementation plan.
- When selecting a split slice, do not pass the whole split set as the scouting
  input. Pass one materialized story card for the active slice and keep the
  other slices in deferred work or handoff notes.
- Preserve unresolved assumptions across stages instead of smoothing them out.
- Default the target executor to `standard-agent` when the user is unsure.
- Use local-small planning when the user names a smaller local model such as a
  Qwen-class 20B-30B model.
- Route to implementation skills only after the preparation packet exists.
- Stop before planning or implementation when a blocker would force guessing.

## Error Recovery & Loopback

The pipeline is not strictly one-way. When a downstream stage contradicts an
upstream assumption, loop back to the earliest affected stage and preserve the
already-validated sections.

**Contradiction triggers:**
- Repo scouting shows a term, API, or file the story assumes does not exist.
- Repo scouting reveals an existing behavior that conflicts with acceptance
criteria.
- Planning shows the story is too large for the chosen executor profile.
- Planning exposes an unresolved dependency that should have been a blocker.

**Loopback rules:**
1. Mark the affected upstream stage as failed in its readiness check.
2. Preserve the rest of the packet; do not discard scouting output just because
the story changed.
3. Re-run only the failed stage with the new context appended.
4. Cap total loopbacks at **2 per stage** before surfacing to the user with a
`Blocked On` summary instead of re-trying silently.

**Mid-pipeline interruption:**
If the user provides new requirements, constraints, or scope changes while a
stage is running, treat it as a fresh input. Re-run readiness checks from
stage 0 against the accumulated packet plus the new input. Do not append
unverified assumptions to an already-passed stage.

## Final Output

Use this structure by default:

```markdown
## Story Card
Clarified story or reference to existing story.

## Repo Context
Relevant files, tests, confidence, and open repo questions.

## Implementation Plan
Model-aware ordered plan, risks, validation, and handoff notes.
```

If a blocker prevents a complete packet, output the completed sections plus a
short `Blocked On` section.

## Final Quality Gate

Reject the packet at handoff if any of the following holds:

- `TBD`, `???`, or unresolved placeholder steps in the plan.
- Plan steps without verb-first phrasing (e.g., `Authentication module` is not
  a step; `Add token expiry check to auth middleware` is).
- Plan references a file path not present in `Repo Context`.
- `Validation` section missing or non-runnable (no command, probe, or named
  acceptance check).
- `Story Status` is `Blocked` but the packet still contains a non-empty plan.
- `Plan Status` is `Ready` but `Risks and Blockers` lists unresolved blockers.
- Agent plan exceeds 12 top-level steps or tracks, or `local-small` exceeds 8
  steps, without explicit user acceptance and a split rationale.
- Story-language and repo-language conflict was flagged during scouting and
  not resolved or reframed in the plan.
- Migration / flag / rollout coverage missing when the change touches
  persisted data, schema, wire format, or public API (per planner Planning
  Rules).

**Warn and acknowledge** (do not block handoff, but surface explicitly):

- Agent plan has 9-12 top-level steps or tracks, or `local-small` has 7-8
  steps.
- `Repo Context` lists more than 15 files.
- More than 2 open questions remain across story and repo context combined.
- No `Do Not Touch` boundaries were identified.
- A `Low` confidence file appears in the plan's critical path without a
  contingency step.

When warning, name the condition and state the risk. Confirm the user still
wants to proceed before downstream routing only when the warning materially
changes implementation risk or scope.

When rejecting, name the failing gate(s) and re-run the relevant stage.

## Downstream Handoff

After the packet passes the Final Quality Gate, route the executor to the
matching implementation skill set:

- Default for repo-owned code changes: `project-core-dev`.
- Language overlay: `coding-guidance-go`, `coding-guidance-python`,
  `coding-guidance-cpp`, `coding-guidance-bash`, `coding-guidance-qt`, or
  `coding-guidance-go-tui` based on the workspace named in `Repo Context`.
- Systems overlay: `backend-systems-guidance` (or `backend-guidance` for
  thin handler work), `ui-guidance` (or `ui-design-guidance` for redesign-
  heavy work) when the story implies UI changes.
- Documentation/config overlay: `documenter` for docs-only implementation
  plans, and `project-config-and-tests` when config behavior or deterministic
  test coverage is the primary concern.
- Workflow overlay: `tester-mindset` when validation design, risk coverage, or
  acceptance-oracle quality is central to the story.
- Process overlay: `security` only when security is the primary concern (do
  not auto-route on every backend or auth change).

## Resources

- [references/story-to-plan-packet-example.md](references/story-to-plan-packet-example.md)
  shows a compact complete packet shape.

## Examples

- `Run the full story-to-plan pipeline on this rough feature idea.` -> clarify,
  scout, then plan.
- `Use the story, repo scout, and planning workflow before implementation.` ->
  orchestrate all three stages and stop before coding.
- `Create a coding-agent-ready handoff from this ticket.` -> run missing stages
  and return the final packet.
- `Implement this plan in code.` -> use implementation skills instead.
