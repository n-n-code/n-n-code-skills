# n-n-code-skills

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Storage for reusable agent skills.

This repository keeps reusable agent skills in a simple folder-based layout under `.agents/skills/`. Use one principle skill when the work is language- or discipline-specific, add the overlays that match the domain, and add a workflow skill only when the task clearly needs that mode.

The published repository is intentionally small at the root:

- `README.md` and `AGENTS.md` document the repo and its working rules
- `.agents/skills/` contains the published skills
- `scripts/check_skills.py` runs cross-platform validation for skill structure,
  inventory, links, and stable routing contracts
- `scripts/check-skills.sh` is the Bash wrapper for the same validator
- `scripts/test_check_skills.py` contains focused standard-library regression tests for the validator
- `LICENSE` covers the repository contents

## Repository Layout

```text
.agents/
  skills/
    <skill-name>/
      SKILL.md
      references/   # optional
      scripts/      # optional
      assets/       # optional
scripts/
  check_skills.py       # cross-platform skill and routing-contract validator
  check-skills.sh       # Bash wrapper
  test_check_skills.py  # validator regression tests
```

`SKILL.md` is the required file for each skill. A skill folder may also include supporting files such as `references/`, `scripts/`, or `assets/` when the skill needs them.

## Skill Roles

This repo uses a small role vocabulary to keep overlapping skills understandable:

- **Principle skill** — portable, unconditional engineering guidance for a language or discipline.
- **Baseline overlay** — the thin default overlay for routine work in a domain.
- **Canonical overlay** — the stronger overlay for the same domain when the task is more demanding; it should subsume the baseline's core expectations rather than drift into a separate job.
- **Companion overlay** — a narrowly scoped overlay that adds an optional workflow on top of a baseline overlay without replacing it.
- **Project overlay** — cross-language guidance for a repository concern such as completion evidence, configuration, platform diagnosis, release maintenance, or vendored source boundaries.
- **Template overlay** — a pattern for repo-local adaptation rather than the default skill to load directly in this repo.
- **Process overlay** — workflow or enforcement guidance that composes with implementation skills.
- **System skill** — a build/create/install skill that leaves behind a repo-owned system rather than only guiding day-to-day execution.

When several skills touch the same job, the docs should name the baseline default and the canonical stronger option explicitly.

## Choosing A Skill Set

Most tasks should compose skills in this order:

1. Start with one principle skill when the work is language- or discipline-specific.
2. Add the overlays that match the domain or repo concern.
3. Add an orthogonal workflow skill only when the user explicitly wants that mode or the task clearly needs it.

For review-only work, guidance skills report prioritized evidence-backed
findings without editing files or requiring findings to be fixed. Add
remediation only when the user asks for it.

Examples:

- routine Python feature work: `coding-guidance-python`; add
  `project-core-dev` when repo-specific completion checks need discovery or
  reporting
- routine Go feature work: `coding-guidance-go`; add `project-core-dev` on the
  same condition
- Charmbracelet Go TUI work: `coding-guidance-go-tui`; add
  `project-platform-diagnose` for terminal, shell, or runtime smoke issues
- routine backend feature: principle skill + `backend-guidance`; add
  `project-core-dev` when the repo-specific completion path is not concrete
- backend config change: principle skill + `backend-guidance` + `project-config-and-tests`
- frontend redesign or polish work: principle skill + `ui-design-guidance`
- Go tests with stretchr/testify: `go-testing-with-testify`; add
  `tester-mindset` for claim or edge-case framing, plus `backend-guidance` or
  `backend-systems-guidance` when the seam is a service boundary
- Playwright setup and browser tests: `setup-playwright`, then
  `playwright-testing` + `tester-mindset` when generating or reviewing cases
  in an existing harness
- security review of auth flows: `security` + `security-identity-access`
- large doc rewrite with collaboration: `documenter` + `documenter-coauthoring`
- prompt design, rewrite, debugging, or prompt eval planning: `prompt-engineering`;
  add `tester-mindset` when the validation strategy is the main concern
- agent context setup, long task handoff, compaction, or context-quality
  debugging: `context-engineering`
- user story, acceptance criteria, discussion synthesis, or story splitting:
  `story-clarifier`
- one story-preparation artifact: use its owner — `story-clarifier`,
  `story-repo-scout`, or `story-implementation-planner`
- complete story-to-plan handoff, multi-stage preparation, or partial-packet
  resumption: `story-to-plan-orchestrator`
- test strategy or validation design: relevant skill set + `tester-mindset`

## Skill Families

The repository's published skills are grouped into these families.

### Skill Authoring And Documentation

- `agent-skill-generator` — design, create, revise, audit, validate, or optimize reusable agent skills and portable `SKILL.md` packages across platforms
- `agents-md-generator` — create, draft, audit, revise, or migrate root and nested repository `AGENTS.md` files from repo evidence
- `documenter` — baseline documentation overlay for substantial documentation authoring or restructuring, including README files, specs, ADRs, tutorials, how-to guides, reference docs, API docs, code comments, changelogs, and agent-facing docs other than repository `AGENTS.md`
- `documenter-coauthoring` — companion overlay for multi-round collaborative drafting of large specs, proposals, decision docs, and similar documents

Defaults:

- Start with `documenter` for ordinary documentation work.
- Use `agents-md-generator` as primary for root or nested repository `AGENTS.md` work.
- Add `documenter-coauthoring` when the task needs explicit iteration, outline approval, or section-by-section collaboration.

### Principle Skills

- `coding-guidance-cpp` — portable C++ implementation and review guidance for feature work, bug fixes, refactors, and code review
- `coding-guidance-go` — portable Go implementation and review guidance for feature work, bug fixes, refactors, and code review
- `coding-guidance-go-tui` — portable Go terminal UI implementation and review guidance for interactive TUIs built with Charmbracelet Bubble Tea, Bubbles, Lip Gloss, embedded Huh forms, and related Charm stack patterns
- `coding-guidance-python` — portable Python implementation and review guidance for feature work, bug fixes, refactors, and code review
- `coding-guidance-bash` — portable Bash implementation and review guidance for automation scripts, repo tooling, refactors, and code review
- `coding-guidance-qt` — portable Qt C++ QWidget desktop implementation and review guidance for widgets, models, signals and slots, layout-heavy UI, Qt5/Qt6 CMake work, and code review

C++ and Qt routing note:

- Use `coding-guidance-qt` when QObject lifetime, signals and slots, QWidget or
  model/view behavior, thread affinity, or Qt-generated build steps are the main
  concern. Use `coding-guidance-cpp` for non-Qt C++ design even when that code
  happens to live in a Qt application repository.

Python skill note:

- `coding-guidance-python` includes bundled references under `.agents/skills/coding-guidance-python/references/` for packaging/layout and service-boundary concerns so the main skill stays focused on core Python engineering guidance.

Qt skill default:

- Use `coding-guidance-qt` as the default principle skill for Qt C++ QWidget desktop work, especially when QWidget architecture, QObject lifetime, signals and slots, layouts, or GUI-thread behavior are part of the job.

Go skill note:

- Use `coding-guidance-go` for Go implementation and review. Add `go-testing-with-testify` only when the main artifact is testify-based Go test code, test review, or Go test flake diagnosis.

Go TUI skill note:

- Use `coding-guidance-go-tui` as the default principle skill for Go terminal
  UI work built with Charmbracelet Bubble Tea, Bubbles, Lip Gloss, embedded Huh
  forms inside Bubble Tea flows, or related Charm stack patterns. Use
  `coding-guidance-go` instead when the task is a non-interactive Go CLI,
  library, worker, or service change with no TUI state machine.
- Treat a one-shot Huh questionnaire as ordinary Go CLI work unless it is
  embedded in a maintained Bubble Tea screen.

Bash routing note:

- Use `coding-guidance-bash` for Bash implementation and review. Use
  `project-release-maintainer` first when the main job is designing or
  maintaining a release or packaging workflow that only happens to call Bash.

### Implementation And Project Overlays

- `backend-guidance` — thin baseline overlay for backend and server-side networked code such as HTTP handlers, gRPC services, and message consumers
- `backend-systems-guidance` — canonical strong backend overlay for non-trivial service boundaries, repositories, queues, reliability, trust-boundary hardening, and backend review that needs stronger testing discipline
- `development-contract-process` — process overlay for repos that require tracked change contracts, verifier evidence, and smallest-proof validation
- `development-contract-repo-overlay-template` — template for the thin repo-local overlay a target repository should have after adopting the development-contract system
- `project-config-and-tests` — project overlay for config precedence, defaults, parsing, normalization, path helpers, and deterministic tests at those seams
- `project-core-dev` — thin project overlay for discovering, selecting, and reporting repository-specific completion checks when the validation path is not already concrete
- `project-platform-diagnose` — diagnostic project overlay for environment-dependent build, install, startup, CI, container, headless, terminal, and runtime failures
- `project-release-maintainer` — project overlay for release and packaging maintenance across install layout, shipped assets, release automation, license and notice alignment, and release-facing docs
- `project-vendor-boundary` — project overlay for checked-in or submodule-managed third-party source, provenance, local patches, and the app-owned integration seam
- `ui-guidance` — thin baseline overlay for ordinary graphical UI and frontend work
- `ui-design-guidance` — canonical strong UI overlay for redesigns, frontend polish, and UX-heavy UI work; extends the baseline with design-direction and UX-priority guidance

Defaults:

- Start with `backend-guidance` for ordinary backend changes that mostly need boundary hygiene and thin handlers.
- Prefer `backend-systems-guidance` when the task includes multi-layer backend work, repositories or transactions, auth or trust-boundary logic, queue or webhook processing, or backend review that needs explicit testing and reliability checks.
- Start with `ui-guidance` for ordinary UI changes that mostly need repo-native consistency and basic UI hygiene.
- Prefer `ui-design-guidance` when the task needs stronger design direction, more frontend polish, or explicit UX review across accessibility, interaction, layout, forms, navigation, or data display.
- Add `project-core-dev` when repository-specific completion checks or gap reporting still need to be discovered for routine repo-owned implementation. Omit it when the selected principle skill plus repository context already makes that evidence concrete.
- Prefer `project-config-and-tests`, `project-platform-diagnose`, `project-release-maintainer`, or `project-vendor-boundary` when that concern is primary. Add matching language or discipline guidance only when the task needs implementation judgment in that domain.
- Use `project-platform-diagnose` first while the environment remains a plausible cause; hand off to the matching implementation, config, setup, release, or vendor skill after the failure is isolated.
- Use `documenter` alone for content-only release or install documentation. Compose it with `project-release-maintainer` when documentation must be reconciled with shipped artifacts or release automation.
- Compose specialized project overlays only when each adds a distinct decision or evidence obligation, such as vendor plus release for a patched library that also changes package metadata.

### Workflow Skills

- `context-engineering` — workflow for curating, auditing, compacting, and refreshing AI-agent context before or during agent work
- `dream-thinking` — explicitly invoked creative retrospective that uses simulated dream imagery and metaphor to derive grounded hypotheses and next observations or actions without treating imagery as evidence
- `go-testing-with-testify` — workflow for writing, reviewing, and hardening Go tests built on the standard `testing` package plus `stretchr/testify`, including `assert`, `require`, `mock`, and `suite`
- `playwright-testing` — workflow for generating, debugging, reviewing, and hardening Playwright E2E specs in an existing harness, including `playwright-cli` exploration and flake triage
- `prompt-engineering` — workflow for designing, rewriting, debugging, evaluating, and optimizing LLM prompts, system prompts, developer prompts, few-shot examples, structured outputs, tool-use prompts, and prompt eval cases
- `recursive-thinking` — adversarial review workflow for pressure-testing an existing plan, diagnosis, design, argument, proposal, or recommendation without replacing domain-specific review
- `security` — security guidance for threat modeling, secure defaults, and security-focused code review
- `security-identity-access` — companion overlay for auth, session, identity recovery, and tenant-boundary work when paired with `security`
- `story-clarifier` — workflow for drafting, synthesizing, rewriting, or splitting story-level requirements into sourced Story Cards or dependency-aware Split Story Sets, or auditing existing story inputs with a separate readiness report, without forcing fake user personas
- `story-implementation-planner` — workflow for turning a ready active Story Card plus evidence-backed Repo Context into an executor-aware implementation plan with explicit blocker edges, validation seams, and risk-appropriate recovery
- `story-repo-scout` — workflow for turning a searchable story or ticket into evidence-backed Repo Context, including applicable instructions and decisions, existing files, convention-backed proposed paths, validation prior art, bounded external primary evidence, and authoritative boundaries
- `story-to-plan-orchestrator` — process overlay and multi-stage entry point for complete handoffs, dependency-frontier slice selection, fact and decision routing, packet validation, resumption, and stale-stage recovery before coding
- `tester-mindset` — testing mindset workflow for designing meaningful tests, validation strategy, acceptance criteria, edge cases, experiments, and probes
- `thinking` — decision-framing workflow for exploring an ambiguous problem, comparing serious approaches, and converging on a testable next move

Story-to-plan family: each component owns one artifact — `story-clarifier`
owns the story, `story-repo-scout` owns repository evidence, and
`story-implementation-planner` owns the plan. Use
`story-to-plan-orchestrator` as the entry point when the requested result spans
two or more stages, needs split-slice selection, or requires packet validation
or resumption. It is not a fourth sequential stage.

Defaults:

- Use `go-testing-with-testify` when the main artifact is testify-based Go test code, test review, or Go test flake diagnosis; start with `coding-guidance-go` for non-test Go implementation and add backend overlays only when the seam is actually a service boundary.
- Start with `security` when the task is explicitly security-focused or the change is high-risk.
- Add `security-identity-access` for auth, session, recovery, invitation, callback-origin, or tenant-boundary work.
- Use `playwright-testing` when a Playwright setup exists and the job is to design, generate, harden, or review Playwright browser tests.
- Use `prompt-engineering` when the main artifact is an LLM prompt, system or developer prompt, prompt eval set, structured-output instruction, or prompt-behavior diagnosis.
- Use `context-engineering` when the main artifact is a context packet, context audit, long-session compaction, or handoff summary for AI-agent work.
- Use `thinking` when no candidate has won yet and the job is to frame an ambiguous decision, compare plausible approaches, and converge. It may precede or accompany implementation while the decision remains open.
- Use `recursive-thinking` when a candidate already exists and the user wants a premortem, countercase, assumption challenge, or evidence-based stress test.
- Use `dream-thinking` only for an explicit dream, sleep, nightmare, or metaphorical-reflection request; use ordinary retrospective or postmortem guidance otherwise, and never treat dream imagery as an evidence basis.
- Use `story-clarifier` when rough tickets, broad epics, prior discussion, story-level requirements, definitions of done, or acceptance criteria need to become a sourced Story Card or dependency-aware Split Story Set; synthesis mode consolidates supplied context without interviewing.
- Route a ready Split Story Set to `story-to-plan-orchestrator` for active-slice selection before repository scouting or planning.
- Use `story-repo-scout` when a searchable story or ticket needs evidence-backed repository context, applicable language and decisions, validation prior art, proposed-path basis, authoritative boundaries, or a bounded planning-critical external claim checked against its owning primary source.
- Use `story-implementation-planner` when a ready active Story Card and sufficient Repo Context exist and the requested artifact is an implementation plan for a target executor, including explicit blockers and validation seams.
- Use `story-to-plan-orchestrator` when the desired output is the complete packet, two or more stages are needed, a split dependency frontier must be selected, or partial artifacts need validation, invalidation, or resumption.

### System Skills

- `development-contract-system` — build a portable change-contract workflow with tracked feature records and lifecycle helpers
- `fuse-skills` — combine multiple skills into one fused skill without duplicated guidance or lost capability
- `setup-playwright` — set up or repair a repo-owned Playwright harness across Node, Python, .NET, or Java test stacks, including config, browser installation, auth plumbing, and a first smoke test

Defaults:

- Use `setup-playwright` when Playwright is absent, broken, or needs repo-level harness changes before test generation begins.

Published skills live under `.agents/skills/`, and every published skill folder has a `SKILL.md`. Some skills also include `references/` directories for bundled supporting material. Keep the family sections above aligned with that live inventory whenever a skill is added, removed, or retitled.

## Adding a Skill

1. Create a new folder under `.agents/skills/<skill-name>/`.
2. Add a `SKILL.md` file that states the skill name, when it should be used, and the workflow it expects.
3. Add only the supporting files the skill actually needs.
4. Keep examples and instructions aligned with the files that exist in the folder.

## Editing Guidelines

- Keep skill descriptions concise and operational.
- Prefer repository-grounded instructions over generic advice.
- Keep the skill taxonomy honest: thinking skills change reasoning mode, overlays add domain or process rules, and generator/system skills should say when they produce repo-local overlays.
- Use the role vocabulary consistently: baseline, canonical, template, process, and system should mean the same thing everywhere in the repo.
- Avoid near-duplicate skill families. If several skills cover the same job, document the canonical default and keep specialized variants sharply scoped.
- Preserve stable folder names once a skill is published or referenced elsewhere.
- Avoid adding tooling, build, or install steps unless the repository actually needs them.

## Validation

This repository does not currently have an application build or lint pipeline.

For changes to skills, supporting files, root documentation, or validation
behavior, run the repository skill validator:

```console
python scripts/check_skills.py
```

When `scripts/check_skills.py` or `scripts/test_check_skills.py` changes, also
run the focused validator tests:

```console
python scripts/test_check_skills.py
```

When `scripts/check-skills.sh` changes, run its wrapper on a Bash-capable
system:

```console
bash scripts/check-skills.sh
```

Validation is structural:

- every skill lives under `.agents/skills/`
- every skill has a `SKILL.md`
- examples and references point to files that exist
- likely skill-name references in Markdown point to published local skills
- documentation claims match the repository contents

## License

This repository is licensed under the MIT License. See [LICENSE](LICENSE).
