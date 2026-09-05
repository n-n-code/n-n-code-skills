# n-n-code-skills

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Storage for reusable agent skills.

This repository keeps reusable agent skills in a simple folder-based layout under `.agents/skills/`. Use one principle skill when the work is language- or discipline-specific, add the overlays that match the domain, and add a workflow skill only when the task clearly needs that mode.

The published repository is intentionally small at the root:

- `README.md` and `AGENTS.md` document the repo and its working rules
- `.gitattributes` keeps shell scripts and examples on LF line endings
- `.agents/skills/` contains the published skills
- `scripts/check_skills.py` runs cross-platform validation for skill structure,
  inventory, links, and stable routing contracts
- `scripts/check-skills.sh` is the Bash wrapper for the same validator
- `scripts/test_check_skills.py` contains focused standard-library regression tests for the validator
- `scripts/test_skill_resources.py` tests the release scaffold and optionally
  checks real CTest behavior and metadata against PyYAML
- `LICENSE` contains the repository's MIT license

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
  check_skills.py       # cross-platform skill and repository-contract validator
  check-skills.sh       # Bash wrapper
  test_check_skills.py  # validator regression tests
  test_skill_resources.py # resource checks and optional independent runtimes
```

`SKILL.md` is the required file for each skill. A skill folder may also include supporting files such as `references/`, `scripts/`, or `assets/` when the skill needs them.

The portable core uses `name` followed by `description` in frontmatter and a
non-empty instruction body. Names are 1–64 lowercase ASCII letters/digits with
single interior hyphens and must match their folders. Descriptions are 1–1024
characters. This repo deliberately supports single-line strings: plain text,
YAML single quotes, or JSON-style double quotes. Quote scalar-like text or
literal `: ` and ` #` sequences; collections, tags, anchors, inline comments,
and multiline YAML are outside this local authoring contract. Host-specific
metadata remains separate and is added only for a demonstrated target need.

Literal metadata source must use the
[YAML printable character range](https://yaml.org/spec/1.2.2/#51-character-set),
including inside quotes. Tabs are permitted within quoted scalar text, while a colon followed
by a space or tab requires quoting. Quoted escape sequences remain supported.

Portable means a host-neutral semantic core, not verified installation in every
agent. Preserve supported language and dependency versions; use current primary
documentation for material version-dependent behavior.

## Skill Roles

This repo uses a small role vocabulary to keep overlapping skills understandable:

- **Principle skill** — portable, unconditional engineering guidance for a language or discipline.
- **Baseline overlay** — the thin default overlay for routine work in a domain.
- **Canonical overlay** — the stronger overlay for the same domain when the task is more demanding; it should subsume the baseline's core expectations rather than drift into a separate job.
- **Companion overlay** — a narrowly scoped overlay that extends a named base
  skill without replacing its workflow or ownership.
- **Project overlay** — cross-language guidance for a repository concern such as completion evidence, configuration, platform diagnosis, release maintenance, or vendored source boundaries.
- **Template overlay** — a pattern for repo-local adaptation rather than the default skill to load directly in this repo.
- **Process overlay** — workflow or enforcement guidance that composes with implementation skills.
- **System skill** — a build/create/install skill that leaves behind a repo-owned system rather than only guiding day-to-day execution.

When several skills touch the same job, the docs should name the baseline
default and identify any canonical stronger option or companion workflow
explicitly.

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
- Jekyll concepts and page/site explanation, design, implementation, or
  troubleshooting: `jekyll`; optionally add `ui-guidance` for routine visual
  work or `ui-design-guidance` for deeper design and UX review
- Go tests with stretchr/testify: `go-testing-with-testify`; add
  `tester-mindset` for claim or edge-case framing, plus `backend-guidance` or
  `backend-systems-guidance` when the seam is a service boundary
- ad hoc Chrome investigation or browser use: `chrome-devtools-axi`; add the
  matching UI overlay for UI implementation or UX review, and use simpler
  fetching when live browser state is unnecessary
- Google Lighthouse audits, report comparisons, measured improvements, or LHCI
  gates: `lighthouse`; add `chrome-devtools-axi` when AXI is the chosen execution
  surface, or the matching UI/implementation guidance for fixes
- Playwright browser work: `playwright-testing` for explicitly requested
  Playwright CLI investigation or test work in an existing harness;
  `setup-playwright` for a new, extended, or broken repo-owned harness;
  add `tester-mindset` when claims, risks, or edge cases still need framing
- security review of auth flows: `security` + `security-identity-access`
- documentation audit or direct authoring/revision: `documenter`
- visual `DESIGN.md` creation, updates, or audit: `design-md-author`
- source, screenshot, or design-reference extraction into maintained visual
  context: `design-md-author`, across web, mobile, and desktop products
- explicit staged coauthoring with outline agreement: `documenter` +
  `documenter-coauthoring`
- prompt design, rewrite, debugging, or prompt eval planning: `prompt-engineering`;
  add `tester-mindset` when the validation strategy is the main concern
- agent context setup, long task handoff, compaction, or context-quality
  debugging: `context-engineering`
- DeepSeek Harness operation, configuration, SDK/ACP integration, plugin
  extension, or source-checkout maintenance: `deepseek-harness`; add
  `coding-guidance-python` when implementing a Python SDK caller
- user story, acceptance criteria, discussion synthesis, or story splitting:
  `story-clarifier`
- one story-preparation artifact: use its owner — `story-clarifier`,
  `story-repo-scout`, or `story-implementation-planner`
- complete story-to-plan handoff, multi-stage preparation, or partial-packet
  resumption: `story-to-plan-orchestrator`
- end-to-end delivery or resumed work spanning preparation, implementation,
  verification, and release: `agentic-sdlc` + the relevant implementation/domain
  skills; stop at the requested endpoint
- recurring coding-agent failures or evaluation of a development workflow
  change: `agentic-sdlc-improvement`; add `prompt-engineering` or
  `context-engineering` when their artifacts are the demonstrated intervention
- test strategy or validation design: relevant skill set + `tester-mindset`

## Skill Families

The repository's published skills are grouped into these families.

### Skill Authoring And Documentation

- `agent-skill-generator` — design, create, revise, audit, validate, or optimize reusable agent skills and portable `SKILL.md` packages across platforms
- `fuse-skills` — fuse two or more bounded local, remote, or inline skill sources into one new or explicitly named existing package, with capability, trigger, resource, and source-action accounting
- `agents-md-generator` — create, draft, audit, revise, or migrate root and nested repository `AGENTS.md` files from repo evidence
- `design-md-author` — standalone authoring workflow for creating, updating, or
  auditing visual `DESIGN.md`/`design.md` context from product evidence, including
  source extraction without a build and supplied visual references; includes an
  adaptable template, consumer-aware format guidance, and
  preservation of existing design decisions and component-library ownership
- `documenter` — baseline documentation overlay for evidence-backed review,
  authoring, restructuring, and repo-truth-sensitive correction of durable
  technical and agent-facing docs other than repository `AGENTS.md` and visual
  `DESIGN.md` files, which have specialized artifact owners
- `documenter-coauthoring` — companion to `documenter` for explicit outline
  agreement, staged drafting, and cold-read self-review before completion of
  specs, PRDs, proposals, ADRs, and decision docs

Defaults:

- Start with `documenter` when documentation needs document-type judgment,
  repository-truth checks, restructuring, or example validation. Review-only
  requests return findings without editing files.
- Use `fuse-skills` when two or more bounded sources must become one resulting
  skill package. Use `agent-skill-generator` to create a skill from one problem
  or workflow, or to revise, audit, validate, or optimize a package without
  integrating another skill source. Ordinary composition and cross-skill cleanup
  that retains separate packages are not fusion.
- Use `agents-md-generator` as primary for root or nested repository `AGENTS.md` work.
- Use `design-md-author` as primary when the artifact is visual design context
  in `DESIGN.md`, including existing lowercase filenames. Use `documenter` for
  software architecture documents even when named `design.md`. Implementing or
  reviewing UI against an existing design file belongs to the UI overlays; add
  `design-md-author` only when the file itself needs authoring or maintenance.
  Source-based visual-language explanations can use it read-only. Preserve
  existing formats and follow the intended consumer when structured tokens are
  needed. Creating or changing UI and configuring external design tools remain
  separate from document authoring.
- Add `documenter-coauthoring` only when the user wants staged collaboration,
  such as outline approval or section-by-section iteration. Document length
  neither selects nor excludes it.

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
- For visual `DESIGN.md` authoring alone, use `design-md-author`. Combine it with
  the UI overlay only when the request also includes UI work; existing tokens
  and shared components remain the implementation authority.
- Add `project-core-dev` when repository-specific completion checks or gap reporting still need to be discovered for routine repo-owned implementation. Omit it when the selected principle skill plus repository context already makes that evidence concrete.
- Prefer `project-config-and-tests`, `project-platform-diagnose`, `project-release-maintainer`, or `project-vendor-boundary` when that concern is primary. Add matching language or discipline guidance only when the task needs implementation judgment in that domain.
- Use `project-platform-diagnose` first while the environment remains a plausible cause; hand off to the matching implementation, config, setup, release, or vendor skill after the failure is isolated.
- Use `documenter` alone for content-only release or install documentation. Compose it with `project-release-maintainer` when documentation must be reconciled with shipped artifacts or release automation.
- Compose specialized project overlays only when each adds a distinct decision or evidence obligation, such as vendor plus release for a patched library that also changes package metadata.

### Workflow Skills

- `agentic-sdlc` — process overlay for end-to-end or resumed software delivery,
  lifecycle transitions, evidence-backed verification and recovery, adaptive work
  records, and release/maintenance within existing authority
- `agentic-sdlc-improvement` — independently usable workflow for turning
  development runs, failures, and feedback into bounded experiments and evaluated
  improvements to how coding agents work
- `chrome-devtools-axi` — default workflow for ad hoc Chrome investigation and
  browser operation through AXI, including interaction, extraction, DOM/CSS,
  console/network, responsive, performance, accessibility, and memory evidence
- `context-engineering` — workflow for curating, auditing, compacting, and refreshing AI-agent context before or during agent work
- `deepseek-harness` — workflow for installing, operating, configuring,
  automating, extending, troubleshooting, or maintaining DeepSeek Harness
  across Profiles, patches, plugins, Web/headless/SDK/ACP surfaces, Cordis
  extension points, and source checkouts
- `dream-thinking` — explicitly invoked creative retrospective that uses simulated dream imagery and metaphor to derive grounded hypotheses and next observations or actions without treating imagery as evidence
- `go-testing-with-testify` — workflow for writing, reviewing, and hardening Go tests built on the standard `testing` package plus `stretchr/testify`, including `assert`, `require`, `mock`, and `suite`
- `jekyll` — standalone workflow for explaining Jekyll concepts and reviewing,
  designing, implementing, and troubleshooting pages and sites with core Jekyll,
  including content, Liquid, layouts, theme overrides, assets, and static HTML
  conversion; external tools require a concrete capability gap
- `lighthouse` — workflow for Google Lighthouse audits, report interpretation
  and comparisons, verified improvements, authenticated user flows, and
  Lighthouse CI collection, budgets, regression gates, and local reports
- `playwright-testing` — workflow for explicitly requested `playwright-cli` investigation or for writing, debugging, reviewing, and hardening Playwright tests in an existing Node, Python, .NET, or Java harness
- `prompt-engineering` — workflow for designing, rewriting, debugging, evaluating, and optimizing LLM prompts, system prompts, developer prompts, few-shot examples, structured outputs, tool-use prompts, and prompt eval cases
- `recursive-thinking` — adversarial review workflow for pressure-testing an existing plan, diagnosis, design, argument, proposal, or recommendation without replacing domain-specific review
- `security` — primary workflow for repo-grounded threat modeling,
  exploit-focused review, and secure implementation when security properties
  are the primary objective
- `security-identity-access` — companion used with `security` when that
  security work centers on authentication, sessions, recovery, federation,
  invitations, identity-provider or recovery callback trust, or tenant
  authorization
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

Agentic SDLC family: `agentic-sdlc` owns coordination across delivery stages;
`agentic-sdlc-improvement` owns the experiment that improves repeated development
behavior. The story family retains preparation-artifact ownership,
`prompt-engineering` retains prompt wording and prompt evaluations, and
`context-engineering` retains context selection, compaction, and handoffs.
Readiness does not grant action authority. Existing repository contract policy
and specialist engineering guidance still apply.

Defaults:

- Use `agentic-sdlc` when the requested outcome spans delivery stages or requires
  recovery across them. An assessment remains read-only; a single planning,
  coding, test-strategy, or handoff artifact uses its existing owner. Use current
  evidence and prior authority to continue routine work without repeated gates.
- Use `agentic-sdlc-improvement` for development-workflow diagnosis and comparison
  across runs, including a bounded experiment from one known failure. A
  prompt-only rewrite, context-only repair, skill audit, or general agent-product
  evaluation retains its own primary workflow. Missing infrastructure does not
  mandate installing an evaluation platform.
- Both SDLC skills use optional specialists and available host capabilities,
  with explicit gaps when required evidence is unavailable. Prefer existing
  authoritative artifacts, compact authorized work records, and one agent unless
  useful delegation is available and authorized. The packages provide procedures,
  not a scheduler, runtime, or enforcement service. See their
  [technical references](.agents/skills/agentic-sdlc/references/sources.md) and
  [delivery](.agents/skills/agentic-sdlc/references/trigger-evals.md) /
  [improvement](.agents/skills/agentic-sdlc-improvement/references/trigger-evals.md)
  evaluation cases for the detailed boundaries.
- Use `go-testing-with-testify` when the main artifact is testify-based Go test code, test review, or Go test flake diagnosis; start with `coding-guidance-go` for non-test Go implementation and add backend overlays only when the seam is actually a service boundary.
- Use `jekyll` for Jekyll concepts or confirmed page/site work. Conceptual
  questions need no repository or runtime discovery. It is independently usable;
  add a UI overlay only when it contributes useful visual guidance. Prefer core
  Jekyll and relevant existing capabilities, adding an external dependency only
  for a requested capability they cannot reasonably provide. Inspect hosting
  only when it affects the task; Shopify Liquid, other generators, prose-only
  editing, and design-document authoring have different primary workflows.
- Start with `security` when the user explicitly requests security work, or
  when security properties are the primary concern in a high-risk change. Do
  not add it merely because code contains APIs, auth, or secrets.
- Add `security-identity-access` only alongside `security` when the security
  task centers on authentication, sessions, recovery, federation, invitations,
  identity-provider or recovery callback trust, or tenant authorization.
  Routine login, signup, endpoint, or generic RBAC work does not select it.
- Use `chrome-devtools-axi` by default for ad hoc Chrome investigation and
  browser use. Respect explicitly chosen browsers, tools, and host interfaces;
  direct-MCP-only requests do not select this AXI-only workflow. Static fetching
  does not require a browser. Let UI or security skills lead their domain work
  and add AXI when live browser evidence is needed.
- Use `lighthouse` for Lighthouse-specific measurement, interpretation, fixes,
  and LHCI integration. Honor the chosen execution surface and its capabilities;
  add AXI only for AXI execution. Keep general browser debugging, Playwright
  tests/harnesses, backend load testing, and broader UI/accessibility review
  with their existing owners. Report-only requests need no browser execution.
- Use `playwright-testing` for explicitly requested live `playwright-cli`
  investigation even when no repo harness exists, or when a working harness
  exists and the job is to design, generate, harden, debug, or review browser
  tests. AXI findings can feed a regression test owned by `playwright-testing`;
  investigation alone does not authorize a new harness.
- Use `prompt-engineering` when the main artifact is an LLM prompt, system or developer prompt, prompt eval set, structured-output instruction, or prompt-behavior diagnosis.
- Use `context-engineering` when the main artifact is a context packet, context audit, long-session compaction, or handoff summary for AI-agent work.
- Use `deepseek-harness` when the work centers on `dsh` Profiles, patches,
  plugins, sessions, SDK/ACP integration, Cordis extension points, runtime
  troubleshooting, or an explicit Harness source checkout. Let
  `prompt-engineering`, `security`, `project-platform-diagnose`, or
  `project-release-maintainer` lead when prompt behavior, a security review,
  unresolved platform variance, or publication machinery is the primary job.
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
- `setup-playwright` — set up or repair a repo-owned Playwright harness across Node, Python, .NET, or Java test stacks, explicitly persist repo-owned Playwright CLI tooling, or add Test Agent definitions to a compatible Node Playwright Test harness; covers dependencies, config, browsers, startup, auth, CI, and one harness smoke check

Defaults:

- Use `setup-playwright` when the requested artifact is dependency or browser installation, runner config, startup wiring, reusable auth, CI harness changes, an explicitly repo-owned Playwright CLI tool, or Test Agent definitions for a compatible Node Playwright Test harness; absence of a harness alone does not select it for a standalone CLI investigation.
- For Test Agents, keep generation, placement, versioning, and regeneration in `setup-playwright`; add `prompt-engineering` only when evaluating or changing their instructions, tool boundaries, or prompt behavior.

Published skills live under `.agents/skills/`, and every published skill folder has a `SKILL.md`. Some skills also include `references/` directories for bundled supporting material. Keep the family sections above aligned with that live inventory whenever a skill is added, removed, or retitled.

## Adding a Skill

1. Create a new folder under `.agents/skills/<skill-name>/`.
2. Add a `SKILL.md` file that states the skill name, when it should be used, and the workflow it expects.
3. Add only the supporting files the skill actually needs.
4. Keep examples and instructions aligned with the files that exist in the folder.

## Editing Guidelines

- Keep skill descriptions concise and operational, with the job and decisive
  trigger terms first.
- Prefer repository-grounded instructions over generic advice.
- Keep the skill taxonomy honest: thinking skills change reasoning mode, overlays add domain or process rules, and generator/system skills should say when they produce repo-local overlays.
- Use the role vocabulary consistently: baseline, canonical, template, process, and system should mean the same thing everywhere in the repo.
- Avoid near-duplicate skill families. If several skills cover the same job,
  document the baseline default and keep canonical, companion, or other
  specialized variants sharply scoped.
- Preserve stable folder names once a skill is published or referenced elsewhere.
- Avoid adding tooling, build, or install steps unless the repository actually needs them.
- Justify substantive revisions with a defect, ambiguous decision, unsupported
  claim, unnecessary obligation, or useful gap. Preserve intended outputs and
  safeguards; explain meaningful relocations and removals. Correct skills may
  remain unchanged after review.
- Keep essential rules available to independently usable skills. Remove redundant
  explanation without introducing undeclared cross-package dependencies.
- Preserve regression cases before changing behavior. Compare the same inputs
  afterward and explain any corrected expectation. Keep static predictions,
  observed host behavior, and executed resource checks distinct.

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

When the metadata parser, executable skill resources, or their tests change, run:

```console
python scripts/test_skill_resources.py
```

The resource tests use disposable fixtures and discover Bash from PATH or a
standard Git for Windows installation. Set `SKILL_TEST_BASH` for another Bash
executable; on Windows these tests use Git Bash/Cygwin path conversion, not WSL.
Real CMake/CTest 3.20+ and PyYAML comparisons run when available, with explicit
skips otherwise. `SKILL_TEST_CMAKE` and `SKILL_TEST_CTEST` can identify installed
executables outside PATH. The command does not install dependencies or run a
production build; stubbed process checks and real-tool evidence are reported
separately.

When `scripts/check-skills.sh` changes, run its wrapper on a Bash-capable
system:

```console
bash scripts/check-skills.sh
```

The validator checks structure, inventory, links, likely skill references, and
selected stable repository contracts:

- every directory under `.agents/skills/` contains a `SKILL.md` with valid
  string frontmatter, supported names and lengths, a matching declared name,
  and non-empty instructions
- relative Markdown links point to existing local targets
- likely skill-name references in Markdown point to published local skills

It cannot prove arbitrary documentation claims. Review those claims against the
repository evidence relevant to each change before finishing.

## License

Repository content is licensed under the [MIT License](LICENSE).
External tools and linked resources retain their own terms.
