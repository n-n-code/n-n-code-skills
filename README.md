# n-n-code-skills

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Storage for reusable agent skills.

This repository keeps reusable agent skills in a simple folder-based layout under `.agents/skills/`. Use one principle skill when the work is language- or discipline-specific, add the overlays that match the domain, and add a workflow skill only when the task clearly needs that mode.

The published repository is intentionally small at the root:

- `README.md` and `AGENTS.md` document the repo and its working rules
- `.agents/skills/` contains the published skills
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
```

`SKILL.md` is the required file for each skill. A skill folder may also include supporting files such as `references/`, `scripts/`, or `assets/` when the skill needs them.

## Skill Roles

This repo uses a small role vocabulary to keep overlapping skills understandable:

- **Principle skill** — portable, unconditional engineering guidance for a language or discipline.
- **Baseline overlay** — the thin default overlay for routine work in a domain.
- **Canonical overlay** — the stronger overlay for the same domain when the task is more demanding; it should subsume the baseline's core expectations rather than drift into a separate job.
- **Companion overlay** — a narrowly scoped overlay that adds an optional workflow on top of a baseline overlay without replacing it.
- **Template overlay** — a pattern for repo-local adaptation rather than the default skill to load directly in this repo.
- **Process overlay** — workflow or enforcement guidance that composes with implementation skills.
- **System skill** — a build/create/install skill that leaves behind a repo-owned system rather than only guiding day-to-day execution.

When several skills touch the same job, the docs should name the baseline default and the canonical stronger option explicitly.

## Choosing A Skill Set

Most tasks should compose skills in this order:

1. Start with one principle skill when the work is language- or discipline-specific.
2. Add the overlays that match the domain or repo concern.
3. Add an orthogonal workflow skill only when the user explicitly wants that mode or the task clearly needs it.

Examples:

- routine Python feature work: `coding-guidance-python` + `project-core-dev`
- backend feature or config change: principle skill + `backend-guidance` + `project-config-and-tests`
- frontend redesign or polish work: principle skill + `ui-design-guidance`
- Go tests with stretchr/testify: `go-testing-with-testify`; add
  `tester-mindset` for claim or edge-case framing, plus `backend-guidance` or
  `backend-systems-guidance` when the seam is a service boundary
- Playwright setup and browser tests: `setup-playwright`, then
  `playwright-testing` + `tester-mindset` when generating or reviewing cases
  in an existing harness
- security review of auth flows: `security` + `security-identity-access`
- large doc rewrite with collaboration: `documenter` + `documenter-coauthoring`
- test strategy or validation design: relevant skill set + `tester-mindset`

## Skill Families

The repository's published skills are grouped into these families.

### Skill Authoring And Documentation

- `agent-skill-generator` — create or revise reusable agent skills from a problem statement, workflow, or existing skill folder
- `agents-md-generator` — create or revise repository `AGENTS.md` files from repo inspection and existing docs
- `documenter` — baseline documentation overlay for substantial documentation authoring or restructuring, including README files, specs, ADRs, tutorials, how-to guides, reference docs, API docs, code comments, changelogs, and agent-facing docs
- `documenter-coauthoring` — companion overlay for multi-round collaborative drafting of large specs, proposals, decision docs, and similar documents

Defaults:

- Start with `documenter` for ordinary documentation work.
- Add `documenter-coauthoring` when the task needs explicit iteration, outline approval, or section-by-section collaboration.

### Principle Skills

- `coding-guidance-cpp` — portable C++ implementation and review guidance for feature work, bug fixes, refactors, and code review
- `coding-guidance-python` — portable Python implementation and review guidance for feature work, bug fixes, refactors, and code review
- `coding-guidance-bash` — portable Bash implementation and review guidance for automation scripts, repo tooling, refactors, and code review
- `coding-guidance-qt` — portable Qt C++ QWidget desktop implementation and review guidance for widgets, models, signals and slots, layout-heavy UI, Qt5/Qt6 CMake work, and code review

Python skill note:

- `coding-guidance-python` includes bundled references under `.agents/skills/coding-guidance-python/references/` for packaging/layout and service-boundary concerns so the main skill stays focused on core Python engineering guidance.

Qt skill default:

- Use `coding-guidance-qt` as the default principle skill for Qt C++ QWidget desktop work, especially when QWidget architecture, QObject lifetime, signals and slots, layouts, or GUI-thread behavior are part of the job.

### Implementation And Project Overlays

- `backend-guidance` — thin baseline overlay for backend and server-side networked code such as HTTP handlers, gRPC services, and message consumers
- `backend-systems-guidance` — canonical strong backend overlay for non-trivial service boundaries, repositories, queues, reliability, trust-boundary hardening, and backend review that needs stronger testing discipline
- `development-contract-process` — process overlay for repos that require tracked change contracts, verifier evidence, and smallest-proof validation
- `development-contract-repo-overlay-template` — template for the thin repo-local overlay a target repository should have after adopting the development-contract system
- `project-config-and-tests` — overlay for config contracts, defaults, path helpers, and deterministic test coverage
- `project-core-dev` — overlay for day-to-day feature work and bug fixes in repo-owned code
- `project-platform-diagnose` — overlay for environment-sensitive diagnosis such as startup issues, install problems, and runtime smoke checks
- `project-release-maintainer` — overlay for release-facing docs, install layout, workflows, licenses, and hygiene scripts
- `project-vendor-boundary` — overlay for app-owned versus vendored dependency boundaries
- `ui-guidance` — thin baseline overlay for ordinary graphical UI and frontend work
- `ui-design-guidance` — canonical strong UI overlay for redesigns, frontend polish, and UX-heavy UI work; extends the baseline with design-direction and UX-priority guidance

Defaults:

- Start with `backend-guidance` for ordinary backend changes that mostly need boundary hygiene and thin handlers.
- Prefer `backend-systems-guidance` when the task includes multi-layer backend work, repositories or transactions, auth or trust-boundary logic, queue or webhook processing, or backend review that needs explicit testing and reliability checks.
- Start with `ui-guidance` for ordinary UI changes that mostly need repo-native consistency and basic UI hygiene.
- Prefer `ui-design-guidance` when the task needs stronger design direction, more frontend polish, or explicit UX review across accessibility, interaction, layout, forms, navigation, or data display.

### Workflow Skills

- `dream-thinking` — reflective sleep-and-dream heuristic for learning from recent work
- `go-testing-with-testify` — workflow for writing, reviewing, and hardening Go tests built on the standard `testing` package plus `stretchr/testify`, including `assert`, `require`, `mock`, and `suite`
- `playwright-testing` — workflow for generating, debugging, reviewing, and hardening Playwright E2E specs in an existing harness, including `playwright-cli` exploration and flake triage
- `recursive-thinking` — recursive self-questioning to stress-test plans, diagnoses, designs, and recommendations
- `security` — security guidance for threat modeling, secure defaults, and security-focused code review
- `security-identity-access` — companion overlay for auth, session, identity recovery, and tenant-boundary work when paired with `security`
- `tester-mindset` — testing mindset workflow for designing meaningful tests, validation strategy, acceptance criteria, edge cases, experiments, and probes
- `thinking` — planning and design guidance for quick-to-medium structured problem solving

Defaults:

- Use `go-testing-with-testify` when the main artifact is testify-based Go test code, test review, or Go test flake diagnosis; add backend overlays only when the seam is actually a service boundary.
- Start with `security` when the task is explicitly security-focused or the change is high-risk.
- Add `security-identity-access` for auth, session, recovery, invitation, callback-origin, or tenant-boundary work.
- Use `playwright-testing` when a Playwright setup exists and the job is to design, generate, harden, or review Playwright browser tests.

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

This repository does not currently have a build, test, or lint pipeline. Validation is structural:

- every skill lives under `.agents/skills/`
- every skill has a `SKILL.md`
- examples and references point to files that exist
- documentation claims match the repository contents

## License

This repository is licensed under the MIT License. See [LICENSE](LICENSE).
