# Playwright Testing Coverage And Validation

Maintainer-only audit reference for future doc refreshes and trigger checks.

## Review Snapshot

Last evidence refresh: 2026-08-24.

- Stable [Playwright 1.62.1](https://github.com/microsoft/playwright/releases/tag/v1.62.1)
  reviewed.
- Standalone [`@playwright/cli` 0.1.18](https://github.com/microsoft/playwright-cli/releases/tag/v0.1.18)
  reviewed, including the files produced by `playwright-cli install --skills`
  and the executable's own `--help`.
- That CLI package depends on a Playwright 1.63 alpha while the stable runner is
  1.62.1. Review its runtime and skill as a separate moving surface; do not
  import alpha-only assumptions into stable test-runner guidance.
- Primary sources: [release notes](https://playwright.dev/docs/release-notes),
  [best practices](https://playwright.dev/docs/best-practices),
  [test CLI](https://playwright.dev/docs/test-cli),
  [UI Mode](https://playwright.dev/docs/test-ui-mode),
  [authentication](https://playwright.dev/docs/auth),
  [API testing](https://playwright.dev/docs/api-testing),
  [Trace Viewer](https://playwright.dev/docs/trace-viewer-intro), and
  [Playwright CLI skills](https://playwright.dev/agent-cli/skills).
- Cross-language sources: [Python test runners](https://playwright.dev/python/docs/test-runners),
  [.NET test runners](https://playwright.dev/dotnet/docs/test-runners), and
  [Java test runners](https://playwright.dev/java/docs/test-runners).

The installed upstream CLI skill is comparison evidence, not a specification.
Retained ideas: snapshot/ref discipline, scoped `find`, current request
inspection, named sessions, targeted cleanup, saved-state secrecy,
  `--debug=cli`, and runtime help discovery. Rejected ideas: incompatible
frontmatter, Node-only test assumptions, default scaffolding during
investigation, contradictory `networkidle` and parallelism rules, broad
  `close-all` / `kill-all`, and treating the live app as the intended spec.
  Although the 0.1.18 release notes advertise broader generated-code
  languages, the installed CLI skill, config schema, and `generate-locator`
  runtime surface still expose TypeScript-oriented action/locator output.
  Translate that evidence into the active binding instead of claiming a
  selectable non-Node target that the command does not expose.

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

- `Set up Playwright in this fresh repo.` -> route to `setup-playwright`
- `Repair playwright.config.ts and browser installation after a package move.` ->
  route to `setup-playwright`
- `Add a setup project and storageState so tests stop logging in every time.` ->
  route to `setup-playwright` (config-shape change, even if specs exist)
- `Install Playwright browsers in CI and configure sharding.` ->
  route to `setup-playwright`

Boundary check:

- Live `playwright-cli` investigation belongs to `playwright-testing` whether
  or not a repo harness exists.
- If a harness exists and the user is asking about test behavior, flakiness,
  locators, or assertions, prefer `playwright-testing`.
- If the harness is missing, broken, or the main work is runner config,
  browser install, CI shape, or reusable-auth plumbing, prefer
  `setup-playwright`.

Coexistence check:

- When both this skill and Playwright's upstream `playwright-cli` skill are
  exposed, the upstream skill supplies current command mechanics while
  `playwright-testing` owns the claim, safety boundary, repo decision, and test
  artifact. Runtime `--help` is authoritative over either document.

## Validation Evidence — 2026-08-24

- **Structure:** the bundled workspace Python ran `scripts/check_skills.py`
  successfully against all 38 skills, including the new cross-ecosystem
  reference and all local links.
- **Resource surface:** the actual `@playwright/cli` 0.1.18 installer output and
  runtime help were inspected. This verifies documented command availability,
  not successful browser execution in a target application.
- **Static routing prediction:** fresh, no-edit catalog-review probes selected
  `playwright-testing` rather than `setup-playwright` for a standalone staging
  investigation with no harness, and selected `playwright-testing` plus
  `coding-guidance-python` for a pytest-playwright flake. These were explicit
  selection requests, not automatic host activation.

Focused cross-ecosystem post-selection evidence:

| Case | Surface | Method | Context | Comparison | Result | Failure class | Residual risk |
|---|---|---|---|---|---|---|---|
| `Use playwright-testing. Working pytest-playwright-asyncio harness; fix an unawaited async expect without changing setup.` | instruction behavior | observed run | isolated target host | none | Pass: proposed `await expect(locator).to_be_visible()`, preserved auto mode and the Python harness, and selected a targeted pytest node without Node flags. | N/A | No source, collection, assertion warning, or test execution. |
| `Use playwright-testing. Working .NET NUnit harness; replace a flaky popup Task.Delay without changing setup.` | instruction behavior | observed run | isolated target host | none | Pass: pre-armed `WaitForPopupAsync`, preserved semantic locators and retrying assertions, and proposed focused repeated `dotnet test` commands without Node flags. | N/A | No source, trace, locator, or test execution; the lost-event diagnosis remains a hypothesis. |
| `Use playwright-testing. Working Java Maven/JUnit harness; harden a flaky multi-user test that shares one BrowserContext.` | instruction behavior | observed run | isolated target host | none | Pass: isolated roles in fresh per-test Java contexts, used `PlaywrightAssertions`, preserved Maven/JUnit, and proposed focused repeated Maven runs without setup changes. | N/A | No source, artifacts, or test execution; server-side data coupling remains possible. |

- **Activation limitation:** those probes explicitly asked for routing and
  immediate behavior, or explicitly selected the skill for post-selection
  behavior. They are not evidence that every host will activate the metadata
  automatically. The prompt fixtures above remain static routing predictions
  elsewhere.
