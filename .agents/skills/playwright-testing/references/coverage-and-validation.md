# Playwright Testing Coverage And Validation

Maintainer-only audit reference for future doc refreshes and trigger checks.

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
  task boundary, apparatus inspection, CLI-first exploration order, locator
  priority, deterministic test rules, and escalation from exploration to reruns
- `testing-patterns.md`:
  page objects, fixtures, auth reuse, parameterization, tagging, mocking, HAR,
  multiple roles, and `test.step()`
- `browser-boundaries.md`:
  iframes, popups, downloads, dialogs, request fixture usage, evaluation,
  clock control, accessibility checks
- `playwright-cli-investigation.md`:
  snapshot discipline, sessions, tabs, saved state, CLI tracing, `--debug=cli`
  attachment
- `debugging-and-visual-qa.md`:
  runner-side debug commands, reports, traces, codegen/UI mode, screenshots

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

- `Explore this running app with Playwright CLI and write a login regression test.`
- `Debug this flaky Playwright spec and tell me why it only passes on retry.`
- `Use UI Mode/codegen to fix these brittle locators.`
- `Add responsive and visual coverage for this settings page.`
- `Review these Playwright tests for weak assertions and hidden waits.`

Expected to trigger `playwright-testing` plus another skill:

- `Security-review these Playwright auth tests.` -> add `security`
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

- If the harness exists and the user is asking about test behavior, flakiness,
  locators, or browser investigation, prefer `playwright-testing`.
- If the harness is missing, broken, or the main work is config/install/auth
  plumbing, prefer `setup-playwright`.
