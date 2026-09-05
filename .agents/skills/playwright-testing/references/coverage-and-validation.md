# Playwright Testing Coverage And Validation

Maintainer-only audit reference for future doc refreshes and trigger checks.

## Versioned technical sources

These versions are reference points; match guidance to the actual installed
runner and CLI before relying on a version-dependent feature.

- Stable [Playwright 1.62.1](https://github.com/microsoft/playwright/releases/tag/v1.62.1)
  is the runner reference.
- Standalone [`@playwright/cli` 0.1.18](https://github.com/microsoft/playwright-cli/releases/tag/v0.1.18)
  is the standalone CLI reference; its executable help owns command syntax.
- That CLI package depends on a Playwright 1.63 alpha while the stable runner is
  1.62.1. Review its runtime as a separate moving surface; do not
  import alpha-only assumptions into stable test-runner guidance.
- Primary sources: [release notes](https://playwright.dev/docs/release-notes),
  [best practices](https://playwright.dev/docs/best-practices),
  [test CLI](https://playwright.dev/docs/test-cli),
  [UI Mode](https://playwright.dev/docs/test-ui-mode),
  [authentication](https://playwright.dev/docs/auth),
  [API testing](https://playwright.dev/docs/api-testing),
  [Trace Viewer](https://playwright.dev/docs/trace-viewer-intro), and
  [Playwright CLI command documentation](https://github.com/microsoft/playwright-cli/tree/v0.1.18#commands).
- Cross-language sources: [Python test runners](https://playwright.dev/python/docs/test-runners),
  [.NET test runners](https://playwright.dev/dotnet/docs/test-runners), and
  [Java test runners](https://playwright.dev/java/docs/test-runners).

Keep command guidance grounded in executable behavior: snapshot/ref lifetimes,
scoped queries, current requests, named sessions, targeted cleanup, saved-state
secrecy, and `--debug=cli`. Although the 0.1.18 release notes advertise broader
generated-code languages, the inspected config schema and `generate-locator`
runtime expose TypeScript-oriented action/locator output. Translate that
evidence into the active binding instead of promising an unsupported output
target.

## Official Doc Coverage Map

### Primary official pages shaping this skill

- Core test authoring and reliability:
  `writing-tests`, `best-practices`, `locators`, `mock`, `auth`,
  `test-annotations`, `test-parameterize`, `test-retries`, `test-ui-mode`,
  `trace-viewer-intro`
- Guides that changed authoring or debugging behavior:
  `actionability`, `test-assertions`, `api-testing`, `clock`,
  `accessibility-testing`, `events`, `dialogs`, `downloads`, `frames`,
  `navigations`, `network`, `test-snapshots`, `pages`, `pom`
- Agent-side browser investigation:
  `agent-cli/introduction`, `agent-cli/snapshots`,
  `agent-cli/commands/navigation`, `agent-cli/commands/interaction`,
  `agent-cli/commands/tabs`, `agent-cli/commands/dialogs`,
  `agent-cli/commands/storage`, `agent-cli/commands/console-eval`,
  `agent-cli/commands/tracing`, `agent-cli/commands/test-debugging`,
  `agent-cli/sessions`

### Where that guidance currently lands

- `SKILL.md`:
  live-investigation versus existing-harness lanes, artifact routing,
  apparatus inspection, proportional case design, durable authoring rules,
  and evidence-led debugging
- `testing-patterns.md`:
  page objects, fixtures, auth reuse, parameterization, tagging, mocking, HAR,
  multiple roles, and `test.step()`
- `browser-boundaries.md`:
  iframes, popups, downloads, dialogs, request fixture usage, evaluation,
  clock control, accessibility checks
- `playwright-cli-investigation.md`:
  runtime command discovery, snapshot discipline, sessions, saved-state
  safety, request inspection, CLI tracing, and `--debug=cli` attachment
- `debugging-and-visual-qa.md`:
  runner-side debug commands, reports, traces, codegen/UI mode, screenshots
- `ecosystem-testing.md`:
  existing-harness runner and lifecycle boundaries for Node, Python, .NET,
  and Java

### Pages intentionally routed elsewhere

- Harness/bootstrap pages like `intro`, `test-configuration`, `test-projects`,
  `test-webserver`, `test-fixtures`, `test-sharding`, `test-reporters`,
  `test-timeouts`, `test-typescript`, and `browsers` primarily belong to
  `setup-playwright`.
- `library` is only a boundary reminder here; repo-owned harness setup still
  belongs to `setup-playwright`.

### Intentionally excluded or kept implicit

- `handles` and `other-locators` were reviewed but not promoted to first-class
  guidance because this skill should keep agents on locator-first, higher-level
  APIs unless lower-level handles are truly required.
- `touch-events` is legacy and not worth dedicated skill surface unless the
  user explicitly asks for that compatibility layer.
- `extensibility` and deeper `run-code`-style CLI power are kept implicit; the
  skill points to them only when they change a real investigation, not as a
  default workflow.
- `service-workers`, `test-generator`, and related pages are reflected only in
  the narrower rules they changed, such as blocking service workers for mocks
  and using `codegen` as a locator-discovery aid rather than shipping recorded
  code blindly.

## Prompt-Routing Validation

Expected to trigger `playwright-testing`:

- `Use Playwright CLI to inspect this running checkout; there is no test harness and do not modify the repo.`
- `Explore this running app with Playwright CLI and add a login regression test to its existing harness.`
- `Debug this flaky Playwright spec and tell me why it only passes on retry.`
- `Fix this flaky pytest-playwright test without adding a Node sidecar.`
- `Fix this unawaited expect call in an existing async pytest-playwright test.`
- `Fix this flaky popup test in the existing .NET NUnit Playwright harness.`
- `Review the isolation in this Playwright Java JUnit test.`
- `Use UI Mode/codegen to fix these brittle locators.`
- `Add responsive and visual coverage for this settings page.`
- `Review these Playwright tests for weak assertions and hidden waits.`

Expected to trigger `playwright-testing` plus another skill:

- `Security-review these Playwright auth tests.` -> add `security` and
  `security-identity-access`; `security` leads, the identity companion adds its
  boundary model, and this skill owns browser-test mechanics
- `Figure out edge cases before writing Playwright coverage for checkout.` ->
  add `tester-mindset`
- `Validate the visible accessibility regressions on this page with Playwright.` ->
  add `ui-guidance` or `ui-design-guidance`

Expected not to trigger `playwright-testing` as the primary skill:

- `Open this site, search for the product, and verify the results.` ->
  `chrome-devtools-axi` for generic browser operation
- `The save button does nothing; inspect the browser console and requests
  without editing code.` -> `chrome-devtools-axi` for ad hoc investigation
- `Set up Playwright in this fresh repo.` -> route to `setup-playwright`
- `Repair playwright.config.ts and browser installation after a package move.` ->
  route to `setup-playwright`
- `Add a setup project and storageState so tests stop logging in every time.` ->
  route to `setup-playwright` (config-shape change, even if specs exist)
- `Install Playwright browsers in CI and configure sharding.` ->
  route to `setup-playwright`

Boundary check:

- Explicitly requested `playwright-cli` investigation and investigation that
  serves Playwright test work belong to `playwright-testing` whether or not a
  repo harness exists. Generic ad hoc Chrome work defaults to
  `chrome-devtools-axi`; an existing harness alone does not turn every browser
  question into test work.
- If a harness exists and the user is asking about test behavior, flakiness,
  locators, or assertions, prefer `playwright-testing`.
- When harness creation or repair is requested, or the main work is runner
  config, browser install, CI shape, or reusable-auth plumbing, prefer
  `setup-playwright`. Harness absence alone does not select setup for a live
  investigation.

Coexistence check:

- Generic Chrome operation selects `chrome-devtools-axi`; explicit Playwright
  CLI sessions retain this skill. For `Inspect the failing request in Chrome
  DevTools, then add a regression test to the existing Playwright harness`,
  AXI owns browser investigation and this skill owns the resulting test.
- CLI help and official tool documentation supply current command mechanics;
  `playwright-testing` owns the claim, safety boundary, repo decision, and test
  artifact without depending on another installed skill. Runtime `--help`
  takes precedence when a documented example disagrees.

## Cross-ecosystem instruction cases

These input/expectation pairs supplement the routing and pressure cases. They
may explicitly select the skill to test post-selection behavior; actual runs
and their results are recorded with the task.

| Input | Expected behavior |
|---|---|
| Working pytest-playwright-asyncio harness; fix an unawaited async expect without changing setup. | Await actions/assertions, preserve the Python runner and deliberate async mode, and choose a targeted pytest node without Node flags. |
| Working .NET NUnit harness; replace a flaky popup `Task.Delay` without changing setup. | Inspect event ordering and readiness; pre-arm the popup wait where appropriate, preserve semantic locators/retrying assertions, and propose focused `dotnet test` checks. Treat the diagnosis as a hypothesis until verified. |
| Java Maven/JUnit multi-user test shares one `BrowserContext`. | Isolate role contexts per test, use the Java binding's assertions, preserve Maven/JUnit, and check for remaining server-side data coupling. |

Report proposed fixes separately from source edits, test execution, and actual
browser observations. Explicit selection does not establish metadata activation.
