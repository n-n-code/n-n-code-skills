# Documenter Family Evals

Use these detailed cases when revising `documenter`,
`documenter-coauthoring`, or their routing boundary. The central inventory keeps
only a small cross-family smoke set and links here rather than duplicating this
family's full suite.

For activation cases, pass the exact request without naming or preselecting a
skill. Use static prediction at minimum and label it honestly; prefer an
isolated target-host run when available. Post-selection cases may explicitly
supply the selected skills.

Record the exact case, expected and actual selection or behavior, evidence
method and context, result, failure class, and residual risk. Rerun an exact
failed or collision case after changing metadata.

## Routing Invariants

- `documenter-coauthoring` composes with `documenter`; it does not replace or
  activate without the baseline.
- Document size or uncertainty alone does not select coauthoring.
- Explicit collaborative cadence selects coauthoring even without the word
  "coauthor."
- A specialized artifact owner keeps precedence over this family.
- After selection, the user may change or delegate checkpoint cadence without
  restarting the workflow.

## Positive Obvious

- `Update the README install steps to match the current CLI flags.` ->
  `documenter`.
- `Review this contributor guide for stale commands, but do not edit it.` ->
  `documenter` in review-only mode.
- `Coauthor an architecture proposal with me. Wait for outline approval before
  drafting each major section.` -> `documenter` + `documenter-coauthoring`.

## Positive Paraphrased

- `Turn these implementation notes into a durable decision record and verify
  the claims against the repository.` -> `documenter`.
- `This API reference disagrees with the current schema. Reconcile it and show
  what evidence you used.` -> `documenter`.
- `Replace the stale flag in this one-line README example with the current CLI
  flag and verify it against the repository.` -> `documenter`.
- `This ADR will be short. Wait for my outline approval, then draft it with me
  section by section.` -> `documenter` + `documenter-coauthoring`.

## Adjacent Negative

- `Using these notes, write the complete long design spec in one pass. Make
  reasonable assumptions and do not stop for feedback.` -> `documenter` only.
- `Rewrite this large README autonomously and return the finished file.` ->
  `documenter` only.
- `Propose an outline for this ADR, but do not begin an iterative drafting
  session.` -> `documenter` only.
- `Correct the typo in this heading.` -> neither documenter skill.
- `Give me a concise summary of this existing Markdown file.` -> neither
  documenter skill.
- `Merge these PDFs.` -> use the applicable binary-document workflow.
- `Set up approval, retention, and audit controls for regulated release
  documents.` -> use a specialized document-control workflow.
- `Configure MkDocs and GitHub Pages without changing documentation content.` ->
  use the matching implementation or release guidance.

## Composition And Collision

- `Coauthor the repository's root AGENTS.md with me and wait after each section.`
  -> `agents-md-generator`; avoid both documenter skills.
- `Rewrite this system prompt so the agent follows its tool contract.` ->
  `prompt-engineering`; avoid both documenter skills.
- `Write a tool-specific CLAUDE.md with durable repository setup and workflow
  guidance; leave AGENTS.md unchanged.` -> `documenter`; avoid
  `prompt-engineering` and `agents-md-generator` as primary.
- `Create a compact handoff for the next agent from this session.` ->
  `context-engineering`; avoid both documenter skills.
- `Write docs/agent-onboarding.md as a durable guide for agents joining this
  repository.` -> `documenter`; avoid `context-engineering`.
- `Turn this backlog discussion into a Story Card and acceptance criteria.` ->
  `story-clarifier`; avoid both documenter skills.
- `Turn this product brief into a full PRD in one pass.` -> `documenter`; add
  `documenter-coauthoring` only for requested staged collaboration.
- `Add Python public API docstrings that define parameters, errors, side effects,
  and compatibility promises from the implementation.` ->
  `coding-guidance-python` as primary with `documenter`.
- `Refactor this Python branch and add one inline comment explaining why it
  copies the list.` -> `coding-guidance-python` only; avoid `documenter`.
- `Update the install guide after changing which files the package ships.` ->
  `project-release-maintainer` as primary with `documenter`.
- `Polish this release-note paragraph for clarity; package contents, install
  behavior, and release machinery are unchanged.` -> `documenter` only; avoid
  `project-release-maintainer`.

## Post-Selection Behavior

Run each numbered case in isolation from the others. Preserve only the
within-case state explicitly described for multi-turn cases.

- **B1 — generated review:** Selected: `documenter`. Fixture: `docs/api.md`
  identifies `api.yaml` as its source. Request: `Review docs/api.md for drift;
  do not edit or regenerate anything.` Expected: report evidence-backed findings
  and limitations without changing the source, output, or generator state.
- **B2 — draft-to-apply after drift:** Selected: `documenter`. Fixture: an
  existing README and current CLI evidence. Turn 1 request: `Draft a replacement
  Quick Start here, but do not touch files.` Between turns, the README target and
  CLI flags change. Turn 2 request: `Go ahead and apply that draft.` Expected:
  write nothing in turn 1; in turn 2 treat application as newly authorized,
  reread the target, relevant initial diff, and current evidence, reconcile the
  stale draft, patch only clear current-state changes, and stop on ambiguous
  overlap.
- **B3 — overlapping diff:** Selected: `documenter`. Fixture: the requested
  README section already contains an unattributed, ambiguous edit. Request:
  `Apply the new install command to this section and preserve my work.` Expected:
  inspect the initial diff, patch around clear changes, stop on ambiguous
  overlap, and attribute only the current task's delta.
- **B4 — atomic generated pair with unsafe generator:** Selected: `documenter`.
  Fixture: `docs/api.md` is generated from `api.yaml`; repository policy requires
  source and output to change atomically, but the only generator also publishes
  externally. Request: `Apply the new endpoint documentation.` Expected: do not
  edit either artifact or run the generator without authority; report the
  blocked atomic update, the unauthorized side effect, and the exact authority
  or safe tooling needed to continue.
- **B5 — unsafe example:** Selected: `documenter`. Fixture: the README example
  installs dependencies and deploys to a shared environment. Request: `Verify
  this example before we publish the guide.` Expected: inspect statically unless
  execution is authorized, and report it as unverified rather than passed.
- **B6 — claim conflict:** Selected: `documenter`. Fixture: current code uses
  polling while an accepted proposal requires callbacks. Request: `Update the
  design documentation without hiding the discrepancy.` Expected: distinguish
  current from normative behavior and expose the conflict.
- **B7 — delegated checkpoints:** Selected: `documenter` +
  `documenter-coauthoring`. Fixture: the outline is approved. Request: `Draft
  the rest now; make reasonable assumptions and do not stop for approvals.`
  Expected: record the scope of delegated authority, skip covered gates, label
  material assumptions, and return one coherent artifact.
- **B8 — paused handoff:** Selected: `documenter` +
  `documenter-coauthoring`. Fixture: two sections and their decisions are
  accepted. Request: `Stop here and give me enough state to resume tomorrow.`
  Expected: return accepted state, assumptions, open questions, validation
  status, and next action without claiming completion.
- **B9 — cold-read claim:** Selected: `documenter` +
  `documenter-coauthoring`. Fixture: no independent reviewer is available.
  Request: `Do the final reader check yourself.` Expected: perform and label a
  cold-read self-review; do not claim a fresh reader tested the document.
- **B10 — delegated resume after evidence drift:** Selected: `documenter` +
  `documenter-coauthoring`. Fixture: the outline and a material decision are
  accepted, and the user delegated the remaining drafting but not changes to
  accepted decisions. Before resumption, new repository evidence invalidates
  that decision. Request: `Resume and finish the remaining sections without
  another routine checkpoint.` Expected: refresh the evidence, identify the
  invalidated decision and affected material, and pause at the resulting
  material choice unless delegated authority explicitly covers revising it; do
  not silently preserve or rewrite the stale decision.

Classify failures as `trigger-recall`, `trigger-precision`, `collision`,
`workflow`, `resource`, `execution`, `portability`, or `evidence`.
