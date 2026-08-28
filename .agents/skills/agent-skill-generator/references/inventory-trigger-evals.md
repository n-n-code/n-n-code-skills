# Inventory Trigger Evals

Use this reference when revising trigger descriptions, README composition
guidance, or baseline/canonical/companion boundaries across this skill
inventory. These are lightweight prompt simulations, not a benchmark suite.

## How to use this catalog

Use only the sections affected by the change. For each selected case, use the
same evidence schema as the main validation reference:

| Case (exact request or fixture) | Expected primary | Expected companions | Selection to avoid | Surface | Method | Context | Comparison | Result | Failure class | Residual risk |
|---|---|---|---|---|---|---|---|---|---|---|

For activation cases, use a realistic request without naming, injecting, or
otherwise preselecting the expected skill. Instruction behavior cases may
invoke the skill explicitly. Record method and context independently from the
surface and any comparison. Add a collision case when another available skill
can plausibly match the same request. Treat host-native skills as conditional
competitors only when they are exposed to or invoked in the current run.

## Sections

- [Backend](#backend)
- [UI](#ui)
- [Playwright](#playwright)
- [Go](#go)
- [Bash](#bash)
- [Python](#python)
- [C++ and Qt](#cpp-and-qt)
- [Documentation](#documentation)
- [Story clarification](#story-clarification)
- [Story repo scouting](#story-repo-scouting)
- [Story implementation planning](#story-implementation-planning)
- [Story-to-plan orchestration](#story-to-plan-orchestration)
- [Project overlays](#project-overlays)
- [Skill authoring and fusion](#skill-authoring-and-fusion)
- [Context engineering](#context-engineering)
- [Development contract](#development-contract)
- [Security and identity](#security-and-identity)
- [Thinking workflows](#thinking-workflows)

## Backend

Expected `backend-guidance`:

- `Add a thin HTTP route that validates input and calls an existing service.`
- `Fix this simple message consumer bug without changing retries or storage.`

Expected `backend-systems-guidance`:

- `Review this webhook consumer for idempotency, retry, and observability gaps.`
- `Add a new protected endpoint with repository, transaction, and permission logic.`
- `Apply one authorization policy to an HTTP endpoint and queue consumer that invoke the same business action.`

Expected neither as primary:

- `Refactor this HTTP client helper used by a CLI.`
- `Run a security audit of this tenant membership and authorization boundary.`
  -> use `security` first and add `security-identity-access` for the
  tenant-authorization model.

Instruction behavior after explicit selection:

- `Use backend-systems-guidance to review this endpoint, but do not edit files.`
  -> map the path and report prioritized evidence-backed findings; do not
  remediate or require findings to be fixed.
- `Use backend-guidance for an action reachable from HTTP and a queue.` ->
  decode and authenticate at each ingress, enforce shared authorization before
  the action, and keep domain and persistence invariants in their owning layers.

## UI

Expected `ui-guidance`:

- `Fix spacing and labels in this settings panel while matching nearby components.`
- `Add a small button to this existing desktop dialog.`

Expected `ui-design-guidance`:

- `Redesign this landing page so the visual direction feels intentional.`
- `Review this dashboard release for accessibility, interaction, and responsive UX issues.`

Expected neither as primary:

- `Change a backend API response with no UI surface.`
- `Fix a terminal ncurses screen unless the repo treats it as product UI.`

Instruction behavior after explicit selection:

- `Use ui-design-guidance to review this dashboard before release, but do not edit files.`
  -> choose review activity independently from preserve or redesign direction,
  then report prioritized findings and evidence without implementation.
- `Use ui-design-guidance to redesign this landing page.` -> choose
  implementation activity plus redesign direction, then build and validate the
  requested UI.

## Playwright

Expected `setup-playwright`:

- `Set up Playwright in this Python repo.`
- `Set up async pytest-playwright fixtures in this Python repo without adding Node tooling.`
- `Add a Chromium Playwright harness to this existing .NET NUnit project.`
- `Add Playwright to this Java JUnit Maven module without creating package.json.`
- `Repair browser install, webServer, and CI reporting after a monorepo package move.`
- `Add reusable auth setup so tests stop logging in through the UI every time.`
- `Configure Playwright's stories/gallery component testing model in this React app.`
- `Add Playwright Test Agents to this existing Node Playwright Test harness and review the generated files.`

Expected `playwright-testing`:

- `Debug this flaky Playwright spec and explain why it passes only on retry.`
- `Use Playwright CLI to explore checkout and add a regression test to the existing harness.`
- `Review these existing specs for brittle locators and weak assertions.`
- `Use Playwright CLI to inspect this running page; there is no harness and do not modify the repo.`
- `Fix this flaky pytest-playwright test without creating Node config.`
- `Fix this unawaited expect call in an existing async pytest-playwright test.`
- `Fix this flaky popup test in the existing .NET NUnit Playwright harness without changing config.`
- `Review BrowserContext isolation in these Playwright Java JUnit tests.`

Expected `tester-mindset` first:

- `Figure out what checkout edge cases we should test before writing browser specs.`

Collision and composition checks:

- `Install browser binaries and repair the Playwright webServer startup in CI.`
  -> `setup-playwright`; the requested artifact and repair are already known.
- `Diagnose why Playwright browser startup fails only in this container; do not
  change config until the cause is established.` ->
  `project-platform-diagnose` while the environment cause is uncertain, then
  `setup-playwright` only if the evidence calls for a repo-owned harness repair.
- `Explore login with Playwright CLI, then add a first regression test to this
  repo that has no harness.` -> `playwright-testing` owns exploration;
  `setup-playwright` owns the new harness; return to `playwright-testing` for
  the authored spec.
- `Security-review these existing Playwright tenant-authorization tests.` ->
  `security` leads the security work; `security-identity-access` adds the
  tenant-authorization model; `playwright-testing` supplies browser-test
  mechanics.
- `Add @playwright/cli as a reproducible developer tool, without adding tests.`
  -> `setup-playwright`; preserve the explicit repo-owned tool decision, but do
  not confuse it with the test runner or a production dependency; verify
  before/after dependency coexistence without aligning a stable runner to an
  alpha CLI dependency.
- `Generate Playwright Test Agent definitions in this Python repo, which has no
  Node Playwright Test harness or seed test.` -> `setup-playwright` owns the
  prerequisite decision. The missing compatible harness blocks generation; the
  missing seed alone would not. Do not introduce a Node sidecar without
  authority.
- `Generate Playwright Test Agents for this working Node Playwright Test harness;
  it has no seed test yet.` -> `setup-playwright`; verify current default-seed
  behavior and validate the generated default, or use an explicit seed when
  repo-specific bootstrap behavior requires one.
- `Generate Playwright Test Agents, then improve their instructions and MCP tool
  boundaries.` -> `setup-playwright` owns generation and placement;
  `prompt-engineering` owns the requested behavioral prompt review. Do not add
  `agent-skill-generator` because these are not reusable `SKILL.md` packages.
- `Both the local Playwright skills and Playwright's installed playwright-cli
  skill are available; inspect checkout and harden its existing regression
  test.` -> `playwright-testing` owns the claim, safety, repo decisions, and
  test artifact; the upstream skill may supply current command mechanics, with
  runtime help authoritative.

## Go

Expected `coding-guidance-go`, not `coding-guidance-go-tui`:

- `Review this Go worker for context cancellation and goroutine leaks.`
- `Refactor this Go service package without changing exported error contracts.`
- `Add a Go HTTP handler while keeping business logic testable.`
- `Add a gRPC method and preserve context deadlines plus domain error mapping.`
- `Optimize this Go hot path using pprof evidence and benchmarks.`
- `Implement a bounded Go worker pool with backpressure and clean shutdown.`

Expected `coding-guidance-go-tui`:

- `Build a Bubble Tea TUI with a list, details pane, and help bar.`
- `Review this Bubble Tea model for command ordering and focus bugs.`
- `Fix this Lip Gloss layout so it survives narrow terminals and Unicode text.`
- `Embed a Huh form into this Bubble Tea flow without blocking Update.`

Expected `coding-guidance-go`, not `coding-guidance-go-tui`:

- `Make this Go CLI print JSON when running in CI.`
- `Add a Cobra subcommand that parses flags and writes plain text output.`
- `Build a one-shot Huh questionnaire that exits after collecting answers.`

Collision cases:

- `Review the package boundaries around a Bubble Tea app; the screen behavior is unchanged.`
  -> `coding-guidance-go` when non-TUI package design is the main risk; add
  `coding-guidance-go-tui` only if the state machine or component integration
  also needs judgment.
- `Review this Bubble Tea model for focus and command-ordering bugs.` ->
  `coding-guidance-go-tui`, not generic Go guidance as primary.

Instruction behavior after explicit selection:

- `Use coding-guidance-go to review this worker, but do not edit files.` ->
  report findings without remediation and do not require findings to be fixed.
- `Use coding-guidance-go to add a benchmark in a module targeting Go 1.23.` ->
  preserve compatible `b.N` style rather than introducing `b.Loop`.

Expected `go-testing-with-testify`:

- `Write testify table-driven tests for this Go parser.`
- `Review this testify mock setup and fix weak assertions.`
- `Debug this flaky Go test that fails with -race.`

Expected `tester-mindset` first:

- `Decide what edge cases matter for this Go billing flow before writing tests.`
- `Design a test strategy for this Go payment subsystem before touching test code.`

Expected `backend-systems-guidance` + `coding-guidance-go`:

- `Design a Go service change that adds repository transactions, queue retries, and a new gRPC endpoint.`

## Bash

Expected `coding-guidance-bash`:

- `Harden this Bash deploy script for quoting, traps, and cleanup.`
- `Review this repo automation script for unsafe globbing and missing error handling.`
- `Refactor this shell helper without changing its CLI flags or exit codes.`

Expected not `coding-guidance-bash` as primary:

- `Run this one shell command and show me the output.`
- `Design a broader release workflow that only happens to call Bash scripts.` -> use `project-release-maintainer` first.

Instruction behavior after explicit selection:

- `Use coding-guidance-bash to review this script, but do not edit it.` ->
  report prioritized findings without remediation.
- `Use coding-guidance-bash; the script intentionally recovers from several non-zero commands.`
  -> inspect control flow before enabling `errexit`, and use explicit checks
  where recovery is part of the contract.

## Python

Expected `coding-guidance-python`:

- `Refactor this Python package boundary while preserving import compatibility.`
- `Review this Python service module for typing, errors, and testability.`
- `Fix this Python packaging/layout issue without inventing a second project structure.`

Expected `coding-guidance-python` + `project-config-and-tests`:

- `Change Python config defaults and add deterministic tests for path resolution.`

Expected `tester-mindset` first:

- `Decide what Python edge cases matter before writing tests for this parser.`

Instruction behavior after explicit selection:

- `Use coding-guidance-python in a Python 3.9 package that uses unittest.` ->
  preserve version-compatible typing syntax and the existing test framework.
- `Use coding-guidance-python to review this module, but do not edit files.` ->
  report findings without remediation and do not require findings to be fixed.

## Cpp And Qt

Expected `coding-guidance-cpp`:

- `Review this C++ ownership refactor for lifetime and exception-safety bugs.`
- `Modernize this C++ API without changing ABI-visible behavior.`
- `Fix this CMake-backed C++ test failure with the smallest safe patch.`

Expected `coding-guidance-qt`:

- `Fix this Qt QWidget layout and signal/slot behavior.`
- `Review this QAbstractItemModel implementation for invalid indexes and notifications.`
- `Move this Qt worker off the GUI thread without breaking QObject affinity.`

Collision cases:

- `Review this QWidget controller for QObject lifetime and queued-signal bugs.`
  -> `coding-guidance-qt`, not generic C++ guidance as primary.
- `Optimize the non-Qt parsing library used by this Qt application.` ->
  `coding-guidance-cpp` when no QObject, event-loop, widget, or Qt build
  behavior changes.

Instruction behavior after explicit selection:

- `Use coding-guidance-qt to review this dialog, but do not edit files.` ->
  report Qt-specific evidence without remediation.
- `Use coding-guidance-cpp to review this ownership refactor, but do not edit files.`
  -> report findings without requiring them to be fixed.

Expected `coding-guidance-cpp` + `project-vendor-boundary`:

- `Patch the app-owned wrapper around vendored C++ code without editing the vendor subtree.`

## Documentation

Use [the local documentation-family evals](../../documenter/references/trigger-evals.md)
for positive, paraphrased, within-family adjacent-negative, and post-selection
instruction-behavior cases. This central catalog keeps cross-family cases:

- `Turn this product brief into a full PRD in one pass.` -> use `documenter`,
  not `story-clarifier`; add `documenter-coauthoring` only when the user asks
  for staged collaboration.
- `Rewrite this system prompt so the agent follows its tool contract.` -> use
  `prompt-engineering`, not the documentation skills.
- `Create a compact handoff for the next agent from this session.` -> use
  `context-engineering`, not the documentation skills.
- `Write docs/agent-onboarding.md as a durable guide for agents joining this
  repository.` -> use `documenter`, not `context-engineering`.
- `Add Python public API docstrings that define parameters, errors, side effects,
  and compatibility promises from the implementation.` -> use
  `coding-guidance-python` as primary with `documenter`.
- `Refactor this Python branch and add one inline comment explaining why it
  copies the list.` -> use `coding-guidance-python` only, not `documenter`.
- `Polish this release-note paragraph for clarity; package contents, install
  behavior, and release machinery are unchanged.` -> use `documenter` only,
  not `project-release-maintainer`.
- `Configure MkDocs and GitHub Pages without changing documentation content.` ->
  use the matching implementation or release guidance; add `documenter` only
  when content structure or prose also changes.

Expected `agents-md-generator`:

- `Create an AGENTS.md for this repo from the README and existing scripts.`
- `Convert this CLAUDE.md guidance into repo-accurate AGENTS.md instructions.`
- `Review our repository coding-agent instructions for stale commands, but do not edit files.`
- `Draft repo-wide coding-agent guidance for this monorepo and recommend where local overrides are justified.`
- `Improve the existing AGENTS.md without overwriting unrelated edits.`

Expected not `agents-md-generator` as primary:

- `Rewrite this contributor guide for developers using coding agents.` -> use `documenter`.
- `Write a tool-specific CLAUDE.md with durable repository setup and workflow
  guidance; leave AGENTS.md unchanged.` -> use `documenter`, not
  `prompt-engineering` or `agents-md-generator` as primary.
- `Create a reusable skill for generating repository instructions.` -> use `agent-skill-generator`.

Instruction-behavior pressure cases for `agents-md-generator`:

- `Audit the current AGENTS.md and show a complete replacement, but do not edit files.` -> task `audit`, output `findings + draft`, root target, no writes.
- `Create services/api/AGENTS.md for its different test workflow; keep the existing root file unchanged.` -> task `create`, output `apply`, named nested target, root unchanged.
- A validation command is declared in the repository but its runtime is missing locally. -> retain the sourced command, record execution as environment-blocked, and do not present it as passed.
- `Draft a migration from CLAUDE.md to AGENTS.md, but preserve the tool-specific entry point and do not edit files.` -> task `migrate`, output `draft`, preserve the adapter, no writes.
- `Create an AGENTS.md for this small single-tool repo.` -> task `create`, output `apply`, root target, and a concise handoff limited to applicable evidence.

## Story Clarification

Expected `story-clarifier`:

- `Turn this rough feature idea into a user story with acceptance criteria.`
- `Rewrite this ticket so a coding agent can implement it without guessing.`
- `Turn this implementation task brief into an unambiguous story-level requirement.`
- `Split this oversized checkout epic into implementation-ready stories.`
- `Turn this broad feature into small vertical user-value slices.`
- `Add a readiness status to this story so the next agent knows whether to scout or ask questions.`
- `Make this definition of done less ambiguous.`
- `Audit these acceptance criteria for ambiguity.`
- `Tighten this task brief without changing its behavior.`
- `Synthesize the settled decisions in this conversation into a Story Card;
  do not interview me.`
- `Split this epic into independently verifiable slices with explicit blocker
  edges.`

Expected not `story-clarifier` as primary:

- `Write a full PRD for this product in one pass.` -> use `documenter`; add
  `documenter-coauthoring` only when staged collaboration is requested.
- `Summarize this conversation for the next agent.` -> use
  `context-engineering`; no story artifact was requested.
- `Synthesize this discussion into an ADR or design proposal.` -> use
  `documenter`; the requested artifact is a decision document, not a story.
- `Implement this story in code.` -> use implementation skills.
- `Design a test strategy for this billing flow.` -> use `tester-mindset`.
- `Find the code and tests that implement this ready story.` -> use `story-repo-scout`.
- `Turn this rough ticket into a complete coding-agent handoff.` -> use `story-to-plan-orchestrator`.
- `Define these glossary terms.` -> use documentation or copy-editing judgment.

## Story Repo Scouting

Expected `story-repo-scout`:

- `Use this story card to scour the repo and append relevant file paths.`
- `Find likely implementation and test files for this ticket before coding.`
- `Find relevant files and documented validation commands for this story card.`
- `Check repo docs for terminology conflicts before appending context.`
- `List relevant files with evidence, authoritative constraints, and nearby non-targets kept separate.`
- `Add repo context to this acceptance-criteria card.`
- `Given this story, scout the current repo for related features and files.`
- `This is a greenfield story; find existing conventions that justify proposed new paths.`
- `Record the scoped AGENTS.md rules and validation commands that apply to this ticket.`
- `Find the current glossary, applicable ADRs, analogous tests, and relevant
  existing validation seams for this story.`
- `Scout this vendor-integration story against the repo and the owning API
  documentation, including the applicable version.`

Expected not `story-repo-scout` as primary:

- `Turn this rough idea into a user story.` -> use `story-clarifier`.
- `Implement this story in code.` -> use implementation skills.
- `Review this module architecture broadly.` -> use `thinking` or relevant review skills.
- `Build a general context packet for a long agent session.` -> use `context-engineering`.
- `Security-review these files.` -> use `security`.
- `Research the latest vendor API and write a standalone findings note.` -> use
  a general research workflow, not the repo-focused story scout.

## Story Implementation Planning

Expected `story-implementation-planner`:

- `Create an actionable implementation plan from this story card and repo context.`
- `I have a story and file list; make the implementation plan.`
- `Make a human implementation plan from this completed story and repo context without inventing time estimates.`
- `Plan this ticket for an agent with a small context window and frequent checkpoints.`
- `Plan this story for an autonomous coding agent that can inspect several independent files in parallel.`
- `Create a plan with dependencies, rollback, and concrete validation from this story and repo context.`
- `Make a first-action handoff for a constrained agent from this story and repo context.`
- `Make a no-placeholder implementation plan for this story.`
- `Turn this Ready Story Card and sufficient Repo Context into an
  implementation-plan handoff for a coding agent.`
- `Plan the existing edits and convention-backed new files in this Repo Context.`
- `Turn this Story Card and Repo Context into vertical outcomes with direct
  blockers and an explicit starting frontier.`
- `From this Ready Story Card and Repo Context, plan the evidence-backed wide
  mechanical refactor with safe expansion, migration batches, and contraction.`

Expected not `story-implementation-planner` as primary:

- `Turn this rough idea into a user story.` -> use `story-clarifier`.
- `Scour the repo and append relevant file paths.` -> use `story-repo-scout`.
- `I have a rough ticket; clarify it, find files, and plan it.` -> use `story-to-plan-orchestrator`.
- `Run the full story-to-plan pipeline before implementation.` -> use `story-to-plan-orchestrator`.
- `Implement this plan in code.` -> use implementation skills.

## Story-To-Plan Orchestration

Expected `story-to-plan-orchestrator`:

- `Run the full story-to-plan pipeline on this rough feature idea.`
- `Use the story, repo scout, and planning workflow before implementation.`
- `I have a rough ticket; clarify it, find files, and plan it.`
- `Create a coding-agent-ready handoff from this ticket.`
- `Create a stable story-to-plan packet with required fields for a coding agent.`
- `I have a split story set; scout and plan the first shippable slice.`
- `This packet already has split stories; materialize the first slice, scout it, and make a handoff.`
- `Split this epic, then scout and plan only the first shippable slice.`
- `Clarify, scout, plan, and reject placeholders before implementation.`
- `Clarify this story, find relevant files, then make an implementation plan.`
- `Validate this partial packet, invalidate stale stages, and resume from the earliest owner.`
- `Resolve the current fact and decision frontier, then scout and plan without
  asking questions whose prerequisites are still open.`

Expected not `story-to-plan-orchestrator` as primary:

- `I have a story and file list; make the implementation plan.` -> use `story-implementation-planner`.
- `Create an implementation plan from this completed story card and repo context.` -> use `story-implementation-planner`.
- `Find likely implementation and test files for this ticket before coding.` -> use `story-repo-scout`.
- `Threat model this story before implementation.` -> use `security`.
- `Implement this plan in code.` -> use implementation skills.

### Story-Family Routing Matrix

- Rough idea, story artifact requested -> `story-clarifier`.
- Rough idea, complete implementation-ready handoff requested ->
  `story-to-plan-orchestrator`.
- Ready active Story Card, repository evidence requested -> `story-repo-scout`.
- Ready active Story Card, complete handoff requested with no Repo Context ->
  `story-to-plan-orchestrator`.
- Ready active Story Card plus sufficient Repo Context, plan requested ->
  `story-implementation-planner`.
- Ready Split Story Set requiring active-slice selection ->
  `story-to-plan-orchestrator`.
- Story-specific repo scouting that depends on a bounded external API or
  specification claim -> `story-repo-scout`; standalone external research is
  not this family.
- Partial packet with exactly one named artifact to repair -> that artifact's
  component owner.
- Partial packet needing stage selection, consistency validation, or two or
  more stages -> `story-to-plan-orchestrator`.
- Implementation requested from a ready plan -> implementation skills, not
  this family.

Collision cases:

- `Audit whether these acceptance criteria are clear and internally consistent.`
  -> `story-clarifier`; use `tester-mindset` instead when the main question is
  risk coverage, oracles, or what evidence is enough.
- `Find the files and repository instructions relevant to this story.` ->
  `story-repo-scout`; use `context-engineering` for a general session or
  handoff context packet.
- `Prepare this ticket for implementation.` -> ambiguous until the requested
  artifact is known; a complete handoff selects `story-to-plan-orchestrator`,
  while one named artifact selects its component owner.
- `Should we build this feature? Compare the product options before writing a
  story.` -> `thinking`, not the story family.
- `Premortem this existing Implementation Plan without rewriting it.` ->
  `recursive-thinking` for the pressure-test workflow; the planner contract
  remains the artifact authority.
- `Find existing validation seams and prior art for this story.` ->
  `story-repo-scout` when the request is to inspect repository evidence;
  `tester-mindset` when the request is to design test strategy or judge coverage.

Instruction behavior after explicit selection:

- `Use story-clarifier to audit this story, but do not rewrite it.` -> report
  findings and readiness without silently emitting a replacement story.
- `Use story-clarifier to synthesize this discussion without an interview; one
  material decision is unresolved.` -> emit the sourced artifact as
  `Needs Input` with the current decision frontier rather than inventing an
  answer or asking despite the no-interview constraint.
- `Use story-clarifier; decision B depends on decision A.` -> ask only A in the
  current frontier, give a non-binding recommendation when supported, and
  recompute after the answer instead of asking A and B together.
- `Use story-clarifier; a linked source can answer this Fact and exposes a
  revision.` -> inspect it and preserve its identifier and revision; ask the
  user only when they own the fact or required access.
- `Use story-clarifier; an in-scope area cannot yet be phrased as a sharp
  question.` -> keep it `[Not yet specifiable]` and non-ready until its
  prerequisite resolves; do not pre-slice it or move it Out of Scope.
- `Use story-clarifier; the split graph contains an unknown slice ID or a
  cycle.` -> keep the Split Story Set non-ready and name the invalid edge.
- `Use story-repo-scout; no implementation files exist yet.` -> report the
  search honestly and include convention-backed proposed paths when available,
  rather than inventing existing evidence or looping the same search.
- `Use story-repo-scout for an API-dependent story, but network access is
  unavailable and no applicable primary source is in the repo.` -> return a
  non-ready Repo Context with the missing claim, source, and smallest evidence
  action; do not rely on a secondary summary.
- `Use story-repo-scout; two official sources describe different API
  versions.` -> preserve both sources and the version conflict, and keep the
  artifact non-ready when the plan depends on choosing between them.
- `Use story-implementation-planner, but the Repo Context is insufficient.` ->
  return `Needs Input` with the missing evidence and upstream owner; do not
  silently run the complete pipeline.
- `Use story-implementation-planner; a planned external API decision has no
  matching External Evidence row.` -> return `Needs Input` and route the claim
  back to `story-repo-scout` instead of planning from memory.
- `Use story-implementation-planner; the proposed blocker graph contains a
  cycle.` -> keep the plan non-ready and name the cycle rather than inventing a
  starting frontier.
- `Use story-implementation-planner; one stable observable seam proves the
  criterion.` -> select that smallest sufficient seam rather than requiring
  redundant checks at every layer.
- `Use story-implementation-planner for a wide change that can still land as a
  green vertical outcome.` -> do not add automatic expand-migrate-contract
  scaffolding; use it only when the evidence shows vertical delivery cannot
  remain green.
- `Use story-to-plan-orchestrator; S1 is blocked but S2 is currently unblocked.`
  -> derive the current frontier and select S2 by default; if the user names S1,
  preserve its blockers and do not return a Ready plan or packet.
- `Use story-to-plan-orchestrator after only the target executor changed.` ->
  invalidate and rebuild the plan without rerunning clarification or scouting.
- `Use story-to-plan-orchestrator after the applicable vendor API version
  changed.` -> revalidate Repo Context and the plan, and return to clarification
  only when intended behavior or acceptance changed.

## Project Overlays

Expected `project-core-dev`:

- `Implement this routine repo-owned bug fix and run the smallest proof.`
- `Add this small feature and report build/test/format validation.`

Expected not `project-core-dev` as primary:

- `Change config precedence and test missing, empty, and invalid values.` -> use
  `project-config-and-tests` with the matching principle skill.
- `Debug why the packaged binary starts locally but fails in a headless
  container.` -> use `project-platform-diagnose` first.

Static with/without added-value fixtures for `project-core-dev`:

- `Fix this Python bug; AGENTS.md already names the exact focused test, format
  check, and required final report.` -> `coding-guidance-python` is sufficient;
  adding `project-core-dev` should produce no distinct behavior, so omit it.
- `Add this Go feature; validation commands are split across AGENTS.md, CI, and
  a Makefile, and it is unclear which gates apply to the touched package.` ->
  `coding-guidance-go` + `project-core-dev`; the project overlay resolves and
  reports the repository-specific completion path.
- `Refactor this C++ component; the repo has several build presets and only some
  are mandatory for this target.` -> `coding-guidance-cpp` +
  `project-core-dev` when the applicable preset and proof remain unclear.
- `Implement this routine change in a repo with no documented validation
  commands.` -> matching principle skill + `project-core-dev`; report the gap
  and use the narrowest honest proof without inventing a repo workflow.

Expected `project-config-and-tests`:

- `Change config precedence and add deterministic tests for defaults and env overrides.`
- `Review path-helper behavior for temp directories and repo-relative files.`

Expected not `project-config-and-tests` as primary:

- `Write table-driven tests for this Go parser.` -> use `coding-guidance-go` or
  `go-testing-with-testify` when testify is the main artifact.
- `Decide which failure cases and oracles matter for this billing flow.` -> use
  `tester-mindset`.

Expected `project-platform-diagnose`:

- `Debug why this service starts locally but fails in a headless container.`
- `Debug why this test suite passes locally but fails in CI.`
- `Diagnose install/runtime behavior that depends on the current platform.`

Expected not `project-platform-diagnose` as primary:

- `Repair Playwright browser installation and webServer configuration in this
  repo.` -> use `setup-playwright`.
- `Fix this reproducible null dereference in app-owned code.` -> use the matching
  principle skill; add `project-core-dev` only when repository-specific
  completion evidence remains unclear.

Expected `project-release-maintainer`:

- `Update release-facing install docs and packaging hygiene before publishing.`
- `Review license and notice alignment, release automation, and distribution
  docs for a release cut.`

Expected not `project-release-maintainer` as primary:

- `Rewrite this README paragraph for clarity without changing shipped
  behavior.` -> use `documenter`.
- `Refactor this internal helper; no package, install, or public documentation
  changes are involved.` -> use the matching principle skill; add
  `project-core-dev` only when repository-specific completion evidence remains
  unclear.

Expected `project-vendor-boundary`:

- `Change integration code around a vendored dependency without modifying vendor files.`
- `Review whether this third-party subtree patch belongs upstream or in app-owned glue.`

Expected not `project-vendor-boundary` as primary:

- `Upgrade this package-manager dependency and lockfile; no third-party source
  is checked into the repo.` -> use the matching language or packaging guidance.
- `Security-review this checked-in third-party parser for exploitable paths.` ->
  use `security` first and add `project-vendor-boundary` only for patch ownership
  and provenance.

Project-overlay collision and composition cases:

- `Add a small HTTP route and run the repo's focused checks.` -> matching
  principle skill + `backend-guidance`; add `project-core-dev` only when the
  repo-specific completion path is not concrete.
- `The env override works locally but CI falls back to the wrong default.` ->
  start with `project-platform-diagnose`; add `project-config-and-tests` when the
  failure is isolated to config precedence or normalization.
- `Update the install guide after changing which files the package ships.` ->
  `project-release-maintainer` + `documenter`.
- `Ship a patched vendored library and update its notice and package manifest.`
  -> `project-vendor-boundary` + `project-release-maintainer`.

Instruction behavior after explicit selection:

- `Use project-core-dev, but the documented validator is unavailable on this
  machine.` -> do not install tooling merely to close the checklist; report the
  exact gap and narrowest next command without implying it passed.
- `Use project-config-and-tests for this malformed security-sensitive config;
  help and version output must still work.` -> preserve safe recovery paths,
  fail closed for unsafe execution, and do not print secret values.
- `Use project-platform-diagnose to investigate this CI-only failure, but do not
  modify the machine or source code.` -> diagnose and report evidence only;
  permanent environment changes and code fixes remain out of scope.
- `Use project-release-maintainer to review release readiness, but do not tag,
  sign, upload, publish, or use credentials.` -> inspect local evidence and
  report unavailable checks without performing external release actions.
- `Use project-vendor-boundary for an app-owned adapter-only change around a
  vendored library.` -> validate the integration seam without editing vendor
  source, provenance, patch records, license files, or notices unnecessarily.

## Skill Authoring And Fusion

Expected `agent-skill-generator`:

- `Design a reusable skill for triaging flaky integration tests, but do not edit files.`
- `Create a portable reusable skill from this repeated debugging workflow.`
- `Review this reusable agent skill for portability and unclear triggers.`
- `Audit this skill for trigger precision and token bloat.`
- `Validate this skill against positive and negative prompts.`

Expected `agent-skill-generator`, with conditional host routing:

- `Update this skill package for portable use across several agent hosts.`
- `Review this SKILL.md and keep its core independent of platform metadata.`

If the current run exposes a host-native skill creator, treat generic
create/update requests as a host-specific collision case. Prefer the explicitly
named skill; otherwise use `agent-skill-generator` when portability, audit,
validation, or token optimization is material, and the host-native creator when
the user asks for that host's scaffolding or metadata. Ignore dormant
installations and creators listed only in another host's catalog.

Run `Create a reusable skill from this repeated debugging workflow.` in two
contexts: with no host-native creator exposed, where `agent-skill-generator` is
expected; and with one exposed, where a collision exists and the current host's
routing policy determines the generic winner. In the exposed context,
portability language should select `agent-skill-generator`, while a request for
host-specific scaffolding or metadata should select the host-native creator.

Expected `fuse-skills` (positive obvious and paraphrased):

- `Fuse these two local UI skills into one deduplicated skill.`
- `Fold these three inline skill drafts into the existing release-guidance skill.`
- `Merge the Go skills from this named remote package into our local Go guidance.`

Expected not `fuse-skills` (adjacent collisions; generic creation or one-package
updates still follow the host-native collision policy above):

- `Improve this existing skill by adding a new workflow; no other skill is being folded into it.`
  -> `agent-skill-generator` when portable authoring, validation, or optimization
  is material; otherwise apply the active host's creator policy.
- `Deduplicate repeated guidance across these four skills, but keep each as a separate package.`
  -> `agent-skill-generator`; optimize the packages without integrating their
  sources into one resulting skill.
- `Create an orchestrator skill that keeps delegating to these three existing skills.`
  -> generic one-package creation; apply the active host's creator policy.

Fusion collision and composition cases:

- `Fuse these two Codex skills into one package and preserve their supporting resources.`
  -> `fuse-skills` is primary even when a host-native skill creator is exposed;
  integrating multiple skill sources is the defining job.
- `Merge the guidance from these two skills for this task, but leave both packages unchanged.`
  -> ordinary runtime composition, not `fuse-skills`; no resulting package is
  requested.

Expected neither `agent-skill-generator` nor `fuse-skills` as primary (negative
and composition cases):

- `Which two existing skills should I load together for this task?` -> ordinary
  runtime composition.
- `Create an AGENTS.md for this repository.` -> use `agents-md-generator`.
- `Package this finished skill for a specific host marketplace.` -> use that
  host's active packaging or plugin workflow.

## Context Engineering

Expected `context-engineering`:

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

Expected not `context-engineering` as primary:

- `Rewrite this system prompt so the agent calls tools more reliably.` -> use `prompt-engineering`.
- `Use this story card to find relevant implementation and test files.` -> use `story-repo-scout`.
- `Create an AGENTS.md for this repo from README and CI config.` -> use `agents-md-generator`.
- `Compare approaches and converge on a practical plan.` -> use `thinking`.
- `Add OpenAI Agents SDK session memory to this Python service.` -> use implementation and OpenAI docs guidance first.

## Development Contract

Expected `development-contract-system`:

- `Port this tracked feature-record contract workflow into another repo.`
- `Create the policy, feature_records tree, checker, helper, tests, and docs.`

Expected `development-contract-process`:

- `Implement this feature in a repo that already requires feature records.`
- `Finish this substantive change and record verifier evidence under the existing policy.`

Expected `development-contract-repo-overlay-template`:

- `Generate the thin repo-local overlay after adopting the contract system.`
- `Update the local overlay because the policy path and checker command changed.`

## Security And Identity

Expected `security` (positive obvious and paraphrased):

- `Security-review this upload parser for exploit paths.`
- `Threat model this service boundary and rank concrete abuse paths.`
- `Could an untrusted archive escape its extraction directory? Trace the
  reachable path and state what would prove or disprove impact.`
- `Harden this archive-import boundary against traversal while preserving valid
  imports.` -> `security` leads the security judgment; matching implementation
  guidance supplies language and framework mechanics.

Expected `security` + `security-identity-access`:

- `Security-review this password reset and session revocation flow.`
- `Check this organization invitation flow for tenant-boundary bypasses.`
- `Could a member use an invitation for one organization to read another
  organization's data? Trace the server-side enforcement path.`
- `Audit OAuth account linking, callback trust, and session rotation for account
  takeover paths.`
- `Threat model WebAuthn recovery, trusted devices, and backup codes.`

Expected `security` without `security-identity-access`:

- `Audit this external image fetcher for SSRF and internal-network access.`
- `Security-review this payment-webhook callback signature and replay handling.`
- `Audit this shared cache for cross-tenant key collisions; no identity,
  membership, session, or authorization decision is involved.`

Expected neither security skill:

- `Add a routine login button style change.` -> use UI guidance.
- `Add a protected HTTP endpoint using the repo's existing authentication
  middleware and authorization policy; no security review is requested.` ->
  use matching implementation guidance plus `backend-systems-guidance`.
- `Write testify table tests for this already-defined permission matrix.` -> use
  `go-testing-with-testify`; do not add security merely because permissions are
  involved.
- `List password-reset test cases and oracles; do not assess exploitability.` ->
  use `tester-mindset`.
- `Discuss generic RBAC role names without tying them to a real identity,
  session, or tenant boundary.` -> use the relevant design workflow.
- `Add another OAuth provider using the repository's existing adapter and
  callback policy; no security review or hardening is requested.` -> use
  matching implementation guidance.

Security collision and composition cases:

- `Threat-model this protected endpoint, then implement the accepted fix.` ->
  `security` owns the threat model and security judgment; matching language and
  backend guidance own implementation structure.
- `Security-review this testify authorization suite for cross-tenant bypasses.`
  -> `security` leads; `security-identity-access` adds the tenant-authorization
  model; `go-testing-with-testify` supplies testify mechanics.
- `Review a tool-using agent prompt for indirect injection that bypasses
  tenant-scoped tool authorization and exfiltrates another tenant's data.` ->
  `security` leads the exploit and trust-boundary review; add
  `security-identity-access` for tenant authorization and `prompt-engineering`
  for prompt behavior.
- `Red-team this migration plan; there is no exploit, identity, secret, or trust
  boundary question.` -> use `recursive-thinking`, not either security skill.

Security instruction behavior after explicit selection:

- `Use security to review this parser, but do not edit files.` -> inspect the
  reachable data and control flow, report evidence-backed findings, and do not
  remediate or require findings to be fixed.
- `Use security to threat-model this path, but deployment details are missing.`
  -> bound the model, label assumptions and missing evidence, and do not turn
  scenarios into confirmed vulnerabilities.
- `Use security; no exploit path is confirmed.` -> distinguish needs-validation
  items and coverage gaps from confirmed findings; do not claim the system is
  secure.
- `Use security; the framework normally protects this API.` -> verify the
  resolved version, effective configuration, middleware order, and exact sink
  context when the conclusion depends on that protection.
- `Use security to fix the confirmed vulnerability.` -> enter secure
  implementation only for the authorized scope, compose matching implementation
  guidance, and validate both the closest abuse case and intended behavior.
- `Use security-identity-access to review this recovery flow.` -> retain
  `security` as primary, then apply the companion's identity state, transition,
  and invalidation model.
- `Use security-identity-access to review backup-code and TOTP storage.` ->
  retain `security` as primary and do not give one interchangeable
  hashing-or-encryption rule to materials with different verifier semantics.

These cases are static routing and instruction-behavior predictions. They are
not observed host-activation results.

## Thinking Workflows

Expected `thinking`:

- `Compare approaches and converge on a practical plan.`
- `Explore this vague idea and decide the next experiment.`
- `Help me decide whether we should build or buy; no option has won yet.`
- `Map the incentives in this partner ecosystem and recommend the next move.`
- `Compare the viable designs, choose one, and then implement the winner.`

Expected `recursive-thinking`:

- `Pressure-test this migration plan with n=5.`
- `Red-team this diagnosis and ask what would change the conclusion.`
- `Run a premortem on this rollout plan before we approve it.`
- `Play devil's advocate against this architecture recommendation.`
- `Find the strongest counterargument to this product proposal.`

Expected `dream-thinking`:

- `Sleep on what happened in this debugging session and extract lessons.`
- `Dream about yesterday's architecture disagreement and what it revealed.`
- `Give me a quick nightmare lens on this failed launch.`
- `Reflect on this project through one dream metaphor.`
- `Dream about why this successful refactor went smoothly.`

The boundary cases below are static-prediction fixtures; none have been exercised as observed activation runs yet.

Boundary cases for `thinking` versus `recursive-thinking`:

- `Challenge my assumptions about this migration plan.` -> expected
  `recursive-thinking`: a candidate plan exists, so stress-test it.
- `Help me think through whether we should build or buy.` -> expected
  `thinking`: no candidate yet, so explore and converge.
- `Find the strongest argument against this proposed queue design.` -> expected
  `recursive-thinking`: the candidate design already exists.
- `We need a queue but have not chosen an architecture; compare our options.` ->
  expected `thinking`: the task is candidate formation rather than adversarial review.
- `Implement this already-approved queue design.` -> expected implementation
  skills, not `thinking`: the decision is settled and the remaining work is execution.
- `Go deeper on how TLS certificate validation works.` -> expected explanation or
  relevant technical guidance, not `recursive-thinking`: there is no candidate
  conclusion to pressure-test.

Boundary cases for domain and workflow collisions:

- `Compact this long session into a handoff for the next agent.` -> expected
  `context-engineering`: the artifact is a handoff, not a reflection.
- `Write a factual incident retrospective with causes, impact, and follow-ups.` ->
  expected incident or documentation guidance, not `dream-thinking`: no dream
  or metaphorical framing was requested.
- `Security red-team this password reset flow for exploitable paths.` -> expected
  `security` plus `security-identity-access`, not `recursive-thinking` as primary.
- `Decide which checkout edge cases and oracles we need.` -> expected
  `tester-mindset`, not `thinking` or `recursive-thinking` as primary.
- `Turn this rough ticket into an implementation-ready story and plan.` ->
  expected story workflow skills, not `thinking` as primary.
- `Use a dream metaphor to generate hypotheses about this incident, but base the
  final conclusion on logs.` -> expected `dream-thinking` as an explicitly
  requested companion; imagery must not become the evidence basis.

Instruction-behavior fixtures after explicit selection:

- `Use thinking. There appears to be only one viable option; recommend the next move.` ->
  skip forced alternatives and make the decisive assumption visible.
- `Use thinking to decide whether to migrate now, defer, or keep the current
  system.` -> treat deferral and the status quo as serious options when credible,
  not as filler.
- `Use thinking; the trade-off is clear and no material uncertainty remains.` ->
  make the recommendation without inventing an assumption or unknown.
- `Use thinking to choose between two reversible internal naming conventions.` ->
  keep validation proportionate; do not manufacture an experiment or formal
  checkpoint for a low-cost choice.
- `Use recursive-thinking with n=10 on this short proposal.` -> treat `n` as
  maximum breadth, omit weak lenses, and lead with findings rather than a
  question tree.
- `Use recursive-thinking to review this diagnosis, but no logs or reproduction
  evidence are available.` -> label material uncertainty and state what evidence
  would resolve it; do not mark claims as observed.
- `Use dream-thinking on this routine session; there is no meaningful pattern,
  tension, or contrast.` -> use the brief reflection fallback instead of forcing
  imagery.
- `Use dream-thinking on this successful refactor; nothing went wrong.` -> use
  an alignment-focused scene when a meaningful success pattern exists rather
  than requiring conflict.
- `Use dream-thinking with an uneasy atmosphere, but do not infer how the team
  felt.` -> use symbolic mood without attributing unprovided emotions as facts.
- `Use dream-thinking for a playful, low-stakes reflection on this naming
  discussion.` -> keep the grounding note compact rather than forcing a full
  evidence, alternative, verification, and confidence report.
- `Use dream-thinking and compare recurring motifs, but I supplied no earlier
  logs.` -> do not invent prior motifs or imply memory access.
- `Use dream-thinking and save the log for later.` -> emit it in the conversation
  and request or use an explicitly authorized destination before persistence.
- `Use dream-thinking for one compact scene.` -> label the interpretation as a
  working hypothesis, not a morning revelation or factual finding.
