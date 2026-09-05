# Setup Playwright Coverage And Validation

Maintainer-only audit reference for future doc refreshes and trigger checks.

## Versioned technical sources

These versions are reference points; match guidance to the actual installed
runner and CLI before relying on a version-dependent feature.

- Stable [Playwright 1.62.1](https://github.com/microsoft/playwright/releases/tag/v1.62.1)
  is the runner reference.
- Standalone [`@playwright/cli` 0.1.18](https://github.com/microsoft/playwright-cli/releases/tag/v0.1.18)
  is the standalone CLI reference; its executable help owns command syntax.
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

## Setup instruction cases

These are reusable planning fixtures, not recorded outcomes. Requests below are
read-only; expected setup and verification steps must not be reported as executed.

| Input | Expected behavior |
|---|---|
| Python 3.12, pytest 8, pytest-asyncio>=0.26, async API, no package.json; plan a Chromium harness. | Use the supported `page` fixture, deliberate async mode and compatible loop scopes; await actions/assertions and avoid a Node sidecar. Do not invent `async_page`. |
| .NET 8 NUnit project without Node tooling; plan a Linux Chromium harness. | Preserve NUnit, select the .NET package, build before using the generated `playwright.ps1`, and specify focused `dotnet test` verification. |
| Java 21 Maven/JUnit 5 module without Node tooling; plan a Chromium harness. | Preserve the module and Java runner, install browsers through the supported Java CLI, and avoid a Node test project. |
| Stable Playwright 1.62.1 harness; plan persisted `@playwright/cli` 0.1.18 tooling. | Inspect coexistence, manifests/lockfile and command resolution; distinguish the CLI's runtime from the stable runner and avoid forced alpha alignment. |
| Working Node harness with `tests/seed.spec.ts`; plan Codex planner/generator/healer definitions. | Verify installed help and host support, exercise the seed when authorized, scope generation, and inspect outputs including untracked files. This is harness work, not reusable skill authoring. |
| Working Node harness without a seed; plan Test Agent definitions. | Check installed-version default-seed behavior and review a generated default; require an explicit seed only when project bootstrap needs it. Seed absence alone does not establish a blocker. |

Keep package/browser resolution, collection, seed execution, generated-file
inspection, and host discovery as separate checks. A setup proposal or explicit
skill selection does not establish successful installation or activation.
