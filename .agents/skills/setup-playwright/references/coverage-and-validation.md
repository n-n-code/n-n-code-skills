# Setup Playwright Coverage And Validation

Maintainer-only audit reference for future doc refreshes and trigger checks.

## Review Snapshot

Last evidence refresh: 2026-08-24.

- Stable [Playwright 1.62.1](https://github.com/microsoft/playwright/releases/tag/v1.62.1)
  reviewed.
- Standalone [`@playwright/cli` 0.1.18](https://github.com/microsoft/playwright-cli/releases/tag/v0.1.18)
  reviewed, including the output of `playwright-cli install --skills` and
  current runtime help.
- Its [package manifest](https://raw.githubusercontent.com/microsoft/playwright-cli/v0.1.18/package.json)
  depends on a Playwright 1.63 alpha while the stable runner is 1.62.1, so
  persisted CLI tooling requires a before/after coexistence proof rather than
  aligning the stable runner to the CLI dependency.
- Primary sources: [installation](https://playwright.dev/docs/intro),
  [configuration](https://playwright.dev/docs/test-configuration),
  [browsers](https://playwright.dev/docs/browsers),
  [authentication](https://playwright.dev/docs/auth),
  [CI](https://playwright.dev/docs/ci),
  [component testing](https://playwright.dev/docs/test-components),
  [Test Agents](https://playwright.dev/docs/test-agents), and
  [release notes](https://playwright.dev/docs/release-notes).
- Current Playwright source makes the planner seed optional and creates a
  default when omitted; see
  [`plannerTools.ts`](https://github.com/microsoft/playwright/blob/main/packages/playwright/src/mcp/test/plannerTools.ts).
- Cross-language sources: [Python introduction](https://playwright.dev/python/docs/intro),
  [.NET introduction](https://playwright.dev/dotnet/docs/intro), and
  [Java introduction](https://playwright.dev/java/docs/intro).

Current-version features stay version-gated in the skill. In particular,
Playwright 1.62 introduced the stories/gallery component model, isolated retry
strategy, and bundled `npx playwright cli`; older harnesses must not receive
those shapes by assumption.

## Official Doc Coverage Map

### Primary official pages shaping this skill

- Setup/bootstrap pages:
  `intro`, `running-tests`, `ci`, `browsers`, `languages`
- Node Playwright Test runner/config pages:
  `test-configuration`, `test-use-options`, `emulation`, `test-fixtures`,
  `test-global-setup-teardown`, `test-projects`, `test-webserver`,
  `test-parallel`, `test-sharding`, `test-reporters`, `test-timeouts`,
  `test-typescript`
- Cross-ecosystem pages:
  `python/docs/intro`, `python/docs/test-runners`,
  `python/docs/running-tests`, `python/docs/browsers`,
  `python/docs/auth`, `dotnet/docs/intro`, `dotnet/docs/browsers`,
  `dotnet/docs/auth`, `java/docs/intro`, `java/docs/browsers`,
  `java/docs/junit`, `java/docs/auth`
- Auth and execution boundaries:
  `auth`, `best-practices`, `library`
- Specialized-mode boundary pages:
  `test-components`, `chrome-extensions`, `webview2`, `test-agents`

### Where that guidance currently lands

- `SKILL.md`:
  harness, repo-owned CLI, and Test Agent extension lanes; repo inspection;
  boundary selection; minimal durable config; CI posture; package manager
  rules; and specialized-mode exclusions
- `ecosystem-patterns.md`:
  Node vs Python vs .NET vs Java runner selection, install commands,
  sync/async Python requirements, config shape, and auth-state placement rules
- `auth-and-ci-patterns.md`:
  Node setup project auth, API login, one-account-per-worker, CI posture,
  sharded report merge
- `browser-and-config-patterns.md`:
  Node scaffold defaults, config scope, projects/dependencies/teardown,
  browser and channel selection, emulation, timeouts, reporters, webServer
  details, specialized modes

### Pages intentionally routed elsewhere

- Using `agent-cli/*` for browser investigation belongs to
  `playwright-testing`; only an explicit request to persist the CLI as repo
  developer tooling belongs to this setup skill.
- Day-to-day spec authoring pages such as `locators`, `mock`, `trace-viewer`,
  `test-parameterize`, `test-annotations`, and most debugging flows belong
  primarily to `playwright-testing`.

### Intentionally excluded or kept implicit

- `test-agents` is limited to an explicitly requested extension of a compatible
  Node Playwright Test harness and target host. An existing seed is optional;
  validate either it or the planner's generated default. The skill does not add
  a Node sidecar to another ecosystem.
- Structural generation review stays in `setup-playwright`; behavioral review
  or customization of agent instructions and tool boundaries composes with
  `prompt-engineering`.
- `library` is covered only as a routing boundary between raw automation and
  Playwright Test harness setup; this skill does not try to teach the full
  library workflow.
- Deeper component-testing, Chrome-extension, and WebView2 mechanics were not
  expanded into full setup recipes here because the default job for this skill
  is ordinary web-app E2E harness setup unless the user explicitly asks for one
  of those specialized modes.
- Narrow browser-install subcases stay implicit unless they change the repo
  setup materially; the skill keeps only the install/channel guidance that
  affects harness shape or CI cost.

## Prompt-Routing Validation

Expected to trigger `setup-playwright`:

- `Set up Playwright in this fresh repo.`
- `Set up pytest-playwright in this Python package without adding Node tooling.`
- `Set up async pytest-playwright fixtures for these async_api tests.`
- `Add a Chromium Playwright harness to this existing .NET NUnit project.`
- `Add Playwright to this Java JUnit Maven module without adding Node tooling.`
- `Generate Playwright Test Agents for this Node harness, which has no seed yet.`
- `Repair this broken Playwright harness after moving packages in a monorepo.`
- `Add Playwright auth reuse with storageState and a setup project.`
- `Configure webServer, Chromium smoke runs, and CI reporting for this app.`
- `Add browser projects and sharding to the existing Playwright config.`

Expected to trigger `setup-playwright` plus another skill:

- `Set up Playwright in this Python repo.` -> add `coding-guidance-python`
- `Set up Playwright in this .NET test project.` -> add the relevant
  principle skill for surrounding code if non-trivial repo code changes are
  needed, but preserve the .NET test framework
- `Set up Playwright in this Java Maven repo.` -> preserve JUnit/TestNG and
  Maven/Gradle wiring instead of inventing Node package scripts
- `Add Playwright plus deterministic config tests for this config-heavy repo.` ->
  add `project-config-and-tests`
- `Scaffold Playwright in this Bash-heavy tooling repo.` -> add
  `coding-guidance-bash`
- `Generate Playwright Test Agents, then improve their instructions and MCP
  tool boundaries.` -> keep generation and placement in `setup-playwright` and
  add `prompt-engineering` for the requested behavioral prompt work

Expected not to trigger `setup-playwright` as the primary skill:

- `Debug this flaky Playwright test.` -> route to `playwright-testing`
- `Explore the product with Playwright CLI before writing tests.` -> route to
  `playwright-testing`
- `Inspect this live page with Playwright CLI; the repo has no test harness.` ->
  route to `playwright-testing`, not setup
- `Review these specs for brittle locators and missing assertions.` -> route to
  `playwright-testing`
- `Add responsive visual assertions to this existing Playwright suite.` ->
  route to `playwright-testing`

Boundary check:

- Prefer `setup-playwright` when the main artifact left behind is config,
  browser installation, auth plumbing, repo layout, or CI shape.
- Prefer `playwright-testing` when the main artifact is knowledge about live
  product behavior, test design, flake diagnosis, or spec hardening. Live CLI
  investigation does not require a harness.
- Treat persisted `@playwright/cli` tooling and Test Agents as separate setup
  lanes: the former requires dependency coexistence evidence, while the latter
  requires a compatible Node Playwright Test harness and target host plus
  validation of an existing or generated default seed.

## Validation Evidence — 2026-08-24

- **Structure:** the bundled workspace Python ran `scripts/check_skills.py`
  successfully against all 38 skills and local links. Plain `python` was not on
  this machine's `PATH`; that lookup failure is environment evidence, not a
  checker failure.

Focused post-selection evidence:

| Case | Expected primary | Expected companions | Selection to avoid | Surface | Method | Context | Comparison | Result | Failure class | Residual risk |
|---|---|---|---|---|---|---|---|---|---|---|
| `Use setup-playwright. Python 3.12, pytest 8, pytest-asyncio>=0.26, async_api, no package.json; plan a Chromium harness without edits.` | N/A | N/A | N/A | instruction behavior | observed run | isolated target host | before/after | Pass after revision: a fresh rerun used the documented `page` fixture, preserved deliberate auto mode, added session loop scope, awaited actions and assertions, and introduced no Node artifacts. The initial probe had invented `async_page`. | workflow (corrected) | No package, browser, collection, or smoke execution. |
| `Use setup-playwright. .NET 8 NUnit project, no Node tooling; plan a Linux Chromium harness without edits.` | N/A | N/A | N/A | instruction behavior | observed run | isolated target host | none | Pass: preserved NUnit and proposed the .NET package, build-before-`playwright.ps1` flow, and focused `dotnet test` validation. | N/A | No NuGet resolution, generated install script, browser, or CI execution. |
| `Use setup-playwright. Java 21 Maven/JUnit 5 module, no Node tooling; plan a Chromium harness without edits.` | N/A | N/A | N/A | instruction behavior | observed run | isolated target host | none | Pass: preserved Maven/JUnit, proposed Java CLI wiring and per-test contexts, and added no Node artifacts. | N/A | No Maven resolution, browser, smoke, or parallel execution. |
| `Use setup-playwright. Persist @playwright/cli 0.1.18 beside a working @playwright/test 1.62.1 pnpm harness without edits.` | N/A | N/A | N/A | instruction behavior | observed run | isolated target host | none | Pass: required before/after version and dependency-tree evidence, kept the stable runner separate, and rejected forced alpha alignment. | N/A | No real install, lockfile diff, command resolution, or runner smoke. |
| `Use setup-playwright. Generate Codex planner, generator, and healer definitions for a working Node harness with tests/seed.spec.ts, without edits.` | N/A | N/A | N/A | instruction behavior | observed run | isolated target host | none | Pass: required runtime help, seed execution, scoped generation, untracked-file review, host discovery, and no `agent-skill-generator`. | N/A | No generation, seed run, browser use, or fresh-host discovery. |
| `Use setup-playwright. Generate Codex Test Agent definitions for a working Node harness with no seed, without edits.` | N/A | N/A | N/A | instruction behavior | observed run | isolated target host | none | Pass: a fresh probe did not block generation on seed absence; it required installed-version verification, review of any default seed, and an explicit seed only when custom bootstrap behavior needs one. | N/A | No generation, default-seed inspection, host discovery, or seed execution. |

- **Static routing prediction:** fresh catalog-review probes selected
  `setup-playwright` for async Python, .NET, Java, persisted CLI, and Test Agent
  prerequisite cases; selected `setup-playwright` + `prompt-engineering` only
  for requested Test Agent instruction/tool-boundary changes; and rejected a
  Node sidecar for a Python repo without a compatible Node harness. Seed absence
  alone was removed as a blocker after current source verification.
- **Activation limitation:** the routing probes were explicitly asked to select
  from the catalog, so they remain static predictions rather than automatic
  host activation. The observed rows above test behavior after explicit skill
  selection, not metadata activation or resource execution.
