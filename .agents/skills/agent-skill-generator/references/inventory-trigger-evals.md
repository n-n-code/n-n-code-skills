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
- [User stories](#user-stories)
- [Story repo scouting](#story-repo-scouting)
- [Story implementation planning](#story-implementation-planning)
- [Story implementation orchestration](#story-implementation-orchestration)
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

Expected neither as primary:

- `Refactor this HTTP client helper used by a CLI.`
- `Run a security audit of this tenant boundary.` -> use `security` first.

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

## Playwright

Expected `setup-playwright`:

- `Set up Playwright in this Python repo.`
- `Repair browser install, webServer, and CI reporting after a monorepo package move.`
- `Add reusable auth setup so tests stop logging in through the UI every time.`

Expected `playwright-testing`:

- `Debug this flaky Playwright spec and explain why it passes only on retry.`
- `Use Playwright CLI to explore checkout and write a regression test.`
- `Review these existing specs for brittle locators and weak assertions.`

Expected `tester-mindset` first:

- `Figure out what checkout edge cases we should test before writing browser specs.`

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

## Python

Expected `coding-guidance-python`:

- `Refactor this Python package boundary while preserving import compatibility.`
- `Review this Python service module for typing, errors, and testability.`
- `Fix this Python packaging/layout issue without inventing a second project structure.`

Expected `coding-guidance-python` + `project-config-and-tests`:

- `Change Python config defaults and add deterministic tests for path resolution.`

Expected `tester-mindset` first:

- `Decide what Python edge cases matter before writing tests for this parser.`

## Cpp And Qt

Expected `coding-guidance-cpp`:

- `Review this C++ ownership refactor for lifetime and exception-safety bugs.`
- `Modernize this C++ API without changing ABI-visible behavior.`
- `Fix this CMake-backed C++ test failure with the smallest safe patch.`

Expected `coding-guidance-qt`:

- `Fix this Qt QWidget layout and signal/slot behavior.`
- `Review this QAbstractItemModel implementation for invalid indexes and notifications.`
- `Move this Qt worker off the GUI thread without breaking QObject affinity.`

Expected `coding-guidance-cpp` + `project-vendor-boundary`:

- `Patch the app-owned wrapper around vendored C++ code without editing the vendor subtree.`

## Documentation

Expected `documenter`:

- `Rewrite this README section so it matches the current repo behavior.`
- `Create an ADR for this implementation decision using evidence from the code.`

Expected `documenter` + `documenter-coauthoring`:

- `Coauthor this long design proposal with outline approval before drafting sections.`
- `Iterate section by section on this product spec with reader-testing.`

Expected `agents-md-generator`:

- `Create an AGENTS.md for this repo from the README and existing scripts.`
- `Convert this CLAUDE.md guidance into repo-accurate AGENTS.md instructions.`

## User Stories

Expected `user-story-clarifier`:

- `Turn this rough feature idea into a user story with acceptance criteria.`
- `Rewrite this ticket so a coding agent can implement it without guessing.`
- `Turn this implementation task brief into an unambiguous story-level requirement.`
- `Split this oversized checkout epic into implementation-ready stories.`
- `Turn this broad feature into small vertical user-value slices.`
- `Add a readiness status to this story so the next agent knows whether to scout or ask questions.`
- `Make this definition of done less ambiguous.`
- `Audit these acceptance criteria for ambiguity.`

Expected not `user-story-clarifier` as primary:

- `Write a full PRD for this product.` -> use `documenter` or `documenter-coauthoring`.
- `Implement this story in code.` -> use implementation skills.
- `Design a test strategy for this billing flow.` -> use `tester-mindset`.
- `Define these glossary terms.` -> use documentation or copy-editing judgment.

## Story Repo Scouting

Expected `story-repo-scout`:

- `Use this story card to scour the repo and append relevant file paths.`
- `Find likely implementation and test files for this ticket before coding.`
- `Find relevant files and documented validation commands for this story card.`
- `Check repo docs for terminology conflicts before appending context.`
- `List relevant files with evidence and do-not-touch boundaries for this story.`
- `Add repo context to this acceptance-criteria card.`
- `Given this story, scout the current repo for related features and files.`

Expected not `story-repo-scout` as primary:

- `Turn this rough idea into a user story.` -> use `user-story-clarifier`.
- `Implement this story in code.` -> use implementation skills.
- `Review this module architecture broadly.` -> use `thinking` or relevant review skills.
- `Security-review these files.` -> use `security`.

## Story Implementation Planning

Expected `story-implementation-planner`:

- `Create an actionable implementation plan from this story card and repo context.`
- `I have a story and file list; make the implementation plan.`
- `Make a human implementation plan from this completed story and repo context, no first-action block needed.`
- `Plan this ticket for a local qwen coding agent using the relevant files found.`
- `Make a GPT-optimized implementation plan from this story and repo scout output.`
- `Create a plan with dependencies, rollback, and concrete validation from this story and repo context.`
- `Make a first-action handoff for a local qwen model from this story and repo context.`
- `Make a no-placeholder implementation plan for this story.`
- `Turn this acceptance-criteria card plus relevant files into a coding-agent handoff.`

Expected not `story-implementation-planner` as primary:

- `Turn this rough idea into a user story.` -> use `user-story-clarifier`.
- `Scour the repo and append relevant file paths.` -> use `story-repo-scout`.
- `I have a rough ticket; clarify it, find files, and plan it.` -> use `story-implementation-orchestrator`.
- `Run the full story-to-plan pipeline before implementation.` -> use `story-implementation-orchestrator`.
- `Implement this plan in code.` -> use implementation skills.

## Story Implementation Orchestration

Expected `story-implementation-orchestrator`:

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

Expected not `story-implementation-orchestrator` as primary:

- `I have a story and file list; make the implementation plan.` -> use `story-implementation-planner`.
- `Create an implementation plan from this completed story card and repo context.` -> use `story-implementation-planner`.
- `Find likely implementation and test files for this ticket before coding.` -> use `story-repo-scout`.
- `Threat model this story before implementation.` -> use `security`.
- `Implement this plan in code.` -> use implementation skills.

## Project Overlays

Expected `project-core-dev`:

- `Implement this routine repo-owned bug fix and run the smallest proof.`
- `Add this small feature and report build/test/format validation.`

Expected `project-config-and-tests`:

- `Change config precedence and add deterministic tests for defaults and env overrides.`
- `Review path-helper behavior for temp directories and repo-relative files.`

Expected `project-platform-diagnose`:

- `Debug why this service starts locally but fails in a headless container.`
- `Diagnose install/runtime behavior that depends on the current platform.`

Expected `project-release-maintainer`:

- `Update release-facing install docs and packaging hygiene before publishing.`
- `Review license, workflow, and distribution docs for a release cut.`

Expected `project-vendor-boundary`:

- `Change integration code around a vendored dependency without modifying vendor files.`
- `Review whether this third-party subtree patch belongs upstream or in app-owned glue.`

## Skill Authoring And Fusion

Expected `agent-skill-generator`:

- `Design a reusable skill for triaging flaky integration tests, but do not edit files.`
- `Create a reusable skill from this repeated debugging workflow.`
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

Expected `fuse-skills`:

- `Fuse these two local UI skills into one deduplicated skill.`
- `Merge the Go skills from this named remote package into our local Go guidance.`

Expected neither `agent-skill-generator` nor `fuse-skills` as primary:

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

Expected `security`:

- `Security-review this upload parser for exploit paths.`
- `Threat model this service boundary and rank concrete abuse paths.`

Expected `security` + `security-identity-access`:

- `Security-review this password reset and session revocation flow.`
- `Check this organization invitation flow for tenant-boundary bypasses.`

Expected not `security` as primary:

- `Add a routine login button style change.`
- `Implement an ordinary endpoint in a repo that happens to contain auth code.`

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
