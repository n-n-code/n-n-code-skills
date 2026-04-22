# Setup Playwright Coverage And Validation

Maintainer-only audit reference for future doc refreshes and trigger checks.

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
  repo inspection, boundary selection, minimal durable config, CI posture,
  package manager rules, specialized-mode exclusions
- `ecosystem-patterns.md`:
  Node vs Python vs .NET vs Java runner selection, install commands,
  config shape, and auth-state placement rules
- `auth-and-ci-patterns.md`:
  Node setup project auth, API login, one-account-per-worker, CI posture,
  sharded report merge
- `browser-and-config-patterns.md`:
  Node scaffold defaults, config scope, projects/dependencies/teardown,
  browser and channel selection, emulation, timeouts, reporters, webServer
  details, specialized modes

### Pages intentionally routed elsewhere

- `agent-cli/*` is agent-side browser investigation guidance and belongs to
  `playwright-testing`, not this setup skill.
- Day-to-day spec authoring pages such as `locators`, `mock`, `trace-viewer`,
  `test-parameterize`, `test-annotations`, and most debugging flows belong
  primarily to `playwright-testing`.

### Intentionally excluded or kept implicit

- `test-agents` is represented only as a boundary rule: do not scaffold
  repo-owned planner/generator/healer agents unless explicitly requested.
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

Expected not to trigger `setup-playwright` as the primary skill:

- `Debug this flaky Playwright test.` -> route to `playwright-testing`
- `Explore the product with Playwright CLI before writing tests.` -> route to
  `playwright-testing`
- `Review these specs for brittle locators and missing assertions.` -> route to
  `playwright-testing`
- `Add responsive visual assertions to this existing Playwright suite.` ->
  route to `playwright-testing`

Boundary check:

- Prefer `setup-playwright` when the main artifact left behind is config,
  browser installation, auth plumbing, repo layout, or CI shape.
- Prefer `playwright-testing` when the harness exists and the main artifact is
  knowledge about product behavior, test design, flake diagnosis, or spec
  hardening.
