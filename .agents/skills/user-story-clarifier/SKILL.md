---
name: user-story-clarifier
description: Workflow for drafting, rewriting, splitting, and auditing story-level requirements, user stories, feature definitions, definitions of done, and acceptance criteria into unambiguous story cards for humans and coding agents. Use for rough tickets, broad epics, or unclear product behavior; avoid for full PRDs, glossary definitions, and code implementation.
---

# User Story Clarifier

Turn rough product intent into a story card that a human or coding agent can
implement without guessing.

## When To Use

- draft a user story from a rough product idea, ticket, or feature note
- rewrite a vague story, definition of done, or acceptance criteria
- split a broad story, epic, or feature into smaller story-level slices
- audit story-level requirements for ambiguity, missing behavior, or weak testability
- tighten a ticket so an implementation agent can plan and execute safely

## Not For

- full PRDs, large product specs, ADRs, or long-form design proposals
- glossary definitions, terminology cleanup, or generic copy editing
- implementation after the story is already clear
- broad test strategy where the main question is what evidence is enough

## Core Workflow

1. Classify the mode: draft, rewrite, split, audit, or tighten.
2. Extract the story facts:
   - actor or user segment
   - user goal and value
   - trigger or entry point
   - expected behavior and visible outcome
   - data, state, permissions, and constraints
   - dependencies, assumptions, and non-goals
3. Ask at most 3 focused clarifying questions when the answers would materially
   change behavior, acceptance criteria, or implementation boundaries.
   Prioritize actor/outcome, behavior boundary, then acceptance oracle.
4. If clarity is good enough, draft with labeled assumptions instead of asking
   low-value questions.
5. If the input is too broad for one story, propose the smallest coherent story
   boundary before drafting. Prefer vertical slices that preserve user value.
6. Convert vague terms into observable behavior. Prefer concrete examples,
   states, limits, permissions, errors, and success signals.
7. Separate user-visible requirements from implementation suggestions. Include
   implementation notes only when they constrain the story.
8. Tighten before finishing: remove duplicate criteria, merge overlapping
   bullets, and keep the story card compact.
9. Run the ready check: the story is independent, valuable, small, testable, and
   an implementer can identify actor, trigger, behavior, pass/fail criteria,
   non-goals, dependencies, and blockers without hidden context.

**Definition of Ready checklist:**
- [ ] Actor and trigger are explicit.
- [ ] Expected behavior and visible outcome are described.
- [ ] Acceptance criteria are observable pass/fail.
- [ ] Out of scope is stated (even if empty).
- [ ] Dependencies and assumptions are listed or explicitly marked as none.
- [ ] No hidden context is required to understand the story.

## Story Card Output

Use this structure by default:

```markdown
Status: Ready | Needs Clarification | Split Candidate | Blocked
Confidence: High | Medium | Low - what would raise it.

## Title
Short action-oriented name.

## User Story
As a <user>, I want <capability>, so that <outcome>.

## Feature Definition
What behavior this story adds or changes, in concrete terms.

## Acceptance Criteria
- Observable pass/fail behavior.

## Edge and Failure Cases
- Boundary, invalid, empty, permission, unavailable, or retry cases that matter.

## Out of Scope
- Related behavior this story does not include.

## Dependencies and Assumptions
- External systems, data, policy, design, or implementation constraints.

## Open Questions
- Only questions that block or materially change implementation.

## Validation Notes
- Checks, manual probes, or test ideas tied to the acceptance criteria. Each
  note should reference the specific acceptance criterion it validates.
```

Status legend: `Ready` = clear enough for scouting/planning; `Needs Clarification`
= 1-3 answers would materially change the story; `Split Candidate` = too broad
for one story (use split output); `Blocked` = cannot produce a truthful story
without missing external input.

`Confidence` shares the High/Medium/Low scale with `story-repo-scout` file
evidence. The "what would raise it" note names the specific input (answer, repo
evidence, decision) that would lift the score.

Omit empty sections only when they add no signal. Keep unresolved assumptions
visible instead of hiding them in polished prose.

## Wording Variants

Use job-story (`When <situation>, I want <motivation>, so I can <outcome>`) or
task-brief wording when `As a <user>...` would create a fake user, hide the
real implementation boundary, or describe a system-to-system interaction. Never
write `As a system, I want...` — that is an anti-pattern (see below).

## Split Story Output

When splitting a broad input, output a compact story set instead of one giant
card:

```markdown
Status: Split Candidate
Confidence: High | Medium | Low - what would raise it.

## Split Story Set

### Shared Context
- Assumptions, non-goals, dependencies, and open questions shared by all slices.

### Slice Order
1. First shippable slice - why it comes first.

### Story Slices
#### <Slice Title>
- Status: Ready | Needs Clarification | Blocked
- Confidence: High | Medium | Low - what would raise it.
- User Story:
- Acceptance Criteria:
- Out of Scope:
- Dependencies:
- Validation Notes:

### Deferred Work
- Work intentionally left for later slices or another artifact.
```

The split set remains `Split Candidate` until a downstream orchestrator or
human chooses a slice. Each slice must still pass the ready check. Mark the
first useful slice clearly so an implementation planner can start without
re-splitting the epic.

## Ambiguity Rules

- Replace adjectives such as `fast`, `simple`, `secure`, `easy`, and `correct`
  with observable behavior or an explicit open question.
- Quantify non-functional requirements (performance, security, compliance). If
  a quantified target is not available, move the NFR to `Dependencies and
  Assumptions` with an open question rather than leaving an unfalsifiable
  adjective in the acceptance criteria.
- Define who can do the action, when it is available, what changes state, and
  what the user sees after success or failure.
- Turn conjunction-heavy criteria, multiple workflows, multiple personas,
  multiple `When` events, or multiple outcome branches into split candidates.
- Keep acceptance criteria independent of a specific UI, API, or architecture
  unless that surface is part of the requirement.
- Flag contradictions between the story, existing criteria, and stated non-goals.

## Anti-Patterns

Reject and rewrite when these appear:

- **Fake persona.** `As a system, I want...`, `As the database, I want...`, or
  `As a developer, I want...` when no developer-facing capability is being shipped.
- **Implementation in AC.** `Uses Redis`, `Stores in Postgres`, `Calls
  /api/v2/foo` — name behavior, not mechanism, unless the surface is the
  requirement.
- **Unfalsifiable AC.** `Works correctly`, `Is fast`, `Handles errors
  gracefully`, `Is user-friendly`. Rewrite as observable pass/fail.
- **Hidden conjunctions.** Single criterion that smuggles `AND`/`OR`/comma-
  separated outcomes; split into separate criteria or separate stories.

## Splitting Heuristics

Use the first pattern that preserves a useful outcome:

- workflow step: split sequential user actions
- business rule: split permissions, calculations, or policy variations
- data variation: split input types, object types, or states
- dependency boundary: split external systems or integrations
- discovery slice: when unknowns dominate, create a small research/prototype
  story before implementation

Do not split into frontend-only, backend-only, or setup-only stories unless that
technical slice is the smallest honest deliverable.

## Composition Boundaries

- **Pipeline position.** Output is consumed by `story-repo-scout`. Do not embed
  file paths, symbol names, or repo structure in the story card — that belongs
  in scout output.
- **Shared vocabulary.** Story Status and story Confidence are defined here.
  `story-repo-scout` reuses the Confidence scale for file evidence, and
  `story-implementation-planner` defines Plan Status. When orchestrated
  end-to-end, see `story-implementation-orchestrator`
  for the canonical vocabulary block.
- **Question cadence.** This skill caps clarifying questions at ≤3. When run
  under `story-implementation-orchestrator`, surface them one at a time within
  that budget.
- Use `documenter` or `documenter-coauthoring` for full PRDs, long specs, ADRs,
  or proposal writing.
- Use `tester-mindset` when the main task is test strategy, risk coverage, or
  deciding whether evidence is enough.
- Use implementation skills (`project-core-dev` plus the matching
  `coding-guidance-<lang>` overlay) when the story is already clear and the
  user wants code changes. Add `tester-mindset` when validation design or risk
  coverage is the main concern.
