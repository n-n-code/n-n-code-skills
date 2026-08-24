# Playwright Testing Across Ecosystems

Load this reference when editing tests in an existing Python, .NET, or Java
harness, or when Node Playwright Test terminology might leak into another
runner.

Preserve the repository's runner, package manager, fixture model, and lifecycle.
Translate Playwright concepts across languages; do not transliterate Node
Playwright Test syntax.

## Identify The Active Contract

| Ecosystem | Runner and config | Test isolation | Retrying assertions |
|---|---|---|---|
| Node | `@playwright/test`, `playwright.config.*` | runner-created context and page fixtures | `await expect(locator).to...()` |
| Python sync | pytest plus `pytest-playwright`; pytest config and `conftest.py` | function-scoped `context` / `page` fixtures | `expect(locator).to_...()` |
| Python async | pytest plus `pytest-playwright-asyncio`; pytest config and `conftest.py` | async `context` / `page` fixtures under the repo's asyncio mode | `await expect(locator).to_...()` |
| .NET | MSTest, NUnit, xUnit, or xUnit v3 with matching Playwright integration | `PageTest` / `ContextTest`, or repo-owned fixtures | `await Expect(locator).To...Async()` |
| Java | usually JUnit or TestNG under Maven or Gradle | repo lifecycle hooks; one fresh `BrowserContext` per test | `assertThat(locator).is...()` / `has...()` |

Treat a custom library-mode harness as authoritative even if an official runner
integration also exists. Changing runners, adding packages, or repairing
configuration belongs to `setup-playwright`.

## Node Playwright Test

Only this lane owns Playwright Test concepts such as projects, project
dependencies, `test.use()`, `test.step()`, retries in
`playwright.config.*`, UI Mode, and Playwright Test fixtures.

Use the repository's package runner and scripts when present. Otherwise, narrow
with commands such as:

```console
npx playwright test tests/checkout.spec.ts --project=chromium
npx playwright test tests/checkout.spec.ts -g "declines an expired card" --workers=1
npx playwright test --ui
```

Validate flags against `npx playwright test --help` for the installed version.
Run setup projects explicitly when UI Mode or a targeted project selection does
not include them automatically.

## Python

Keep pytest-native structure. Use the official plugin's `page`, `context`,
`new_context`, and browser fixtures when the harness already relies on them.
Preserve synchronous versus asynchronous style and existing fixture scopes.
Await actions and `expect(...)` assertions in async tests; never copy the sync
assertion form into `playwright.async_api` code.

```console
pytest tests/test_checkout.py --browser chromium
pytest tests/test_checkout.py -k test_declines_expired_card --browser chromium
pytest tests/test_checkout.py -k test_declines_expired_card --headed
pytest tests/test_checkout.py -k test_declines_expired_card --tracing retain-on-failure --screenshot only-on-failure
```

Important differences from Node:

- configure pytest in `pyproject.toml`, `pytest.ini`, and `conftest.py`; do not
  create `playwright.config.ts`
- use pytest fixtures and markers, not `test.use()`, setup projects, or
  Playwright Test projects
- use Python's `expect` API; do not replace it with one-shot boolean assertions
- plugin CLI options apply to the plugin's default browser, context, and page
  fixtures; manually created objects need their options set in code
- parallel execution requires the harness's pytest parallelization plugin; do
  not assume Node worker flags exist

## .NET

Preserve the existing MSTest, NUnit, xUnit, or xUnit v3 framework and its
matching Playwright package. Official base classes reuse Playwright and Browser
while giving each test an isolated context:

- `PageTest` provides a page in a fresh context
- `ContextTest` supports multiple pages in one fresh context
- `BrowserTest` leaves creation and cleanup of contexts to the test
- `PlaywrightTest` leaves browser lifecycle to the test

Narrow with the test framework's filters:

```console
dotnet test --filter "ExampleTest"
dotnet test --filter "Name~declines_expired_card"
dotnet test --filter "Name~declines_expired_card" -- Playwright.BrowserName=chromium
```

Use `.runsettings`, base-class overrides, or established fixtures for context
and launch options. Parallelism controls differ among MSTest, NUnit, xUnit, and
xUnit v3; inspect the active framework before changing worker behavior. Use
Playwright's async `Expect` assertions rather than immediate property checks.

## Java

Playwright Java is a library integrated with the repository's JUnit, TestNG, or
other test runner. It does not provide the Node Playwright Test runner model.

Reuse Playwright and Browser only where the existing lifecycle permits it.
Create and close a fresh `BrowserContext` for each test. Keep Page and other
Playwright objects on the thread that created their Playwright instance;
Playwright Java objects are not thread-safe.

Run the smallest class or method through the repository's Maven or Gradle
wrapper. Filter syntax belongs to the configured test plugin, so inspect the
build before choosing it:

```console
./mvnw test
./gradlew test
```

Use Java's retrying `PlaywrightAssertions.assertThat` API. Do not import Node
projects, fixtures, hooks, `test.step()`, or config semantics. When the harness
records traces through `BrowserContext.tracing()`, remember that library-level
traces do not capture test-runner assertions.

## Shared Editing Rules

Across all four ecosystems:

- preserve local naming, fixtures, helpers, auth-state wiring, and package
  boundaries before introducing a new abstraction
- use semantic locators and the language binding's retrying Playwright
  assertions
- keep each test isolated; share a Browser only when the harness gives each
  test a fresh BrowserContext
- start event waits before the action that triggers the event
- diagnose one test and one browser first, then broaden only when the claim
  needs more coverage
- use the active runner's filter and artifact controls; never copy Node flags
  into pytest, `dotnet test`, Maven, or Gradle
- verify commands against installed versions and repository wrappers before
  reporting that they ran
- translate CLI- or codegen-discovered locators into the active language and
  runner; do not add a Node sidecar merely to preserve generated syntax

## Node-Only Leakage Check

Before finishing a non-Node edit, search the proposed change for:

- `playwright.config`
- `test.use`, `test.step`, or `test.describe`
- setup projects or project dependencies
- `--project`, `--repeat-each`, `--ui`, or Node worker flags
- `@playwright/test` imports

Keep an occurrence only when the repository deliberately combines ecosystems
and that line belongs to its Node harness.
