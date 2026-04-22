# Playwright Ecosystem Patterns

Load this file when the repo is not a standard Node Playwright Test setup or
when you need to decide which Playwright runner/config shape to preserve.

Use the repo's strongest local signal before reaching for scaffold defaults.

## Reference Naming

Two neighboring reference files keep generic historical names:

- `auth-and-ci-patterns.md`
- `browser-and-config-patterns.md`

Treat both as Node Playwright Test-only helpers. Keep cross-ecosystem routing,
runner choice, and non-Node guardrails here so future edits do not quietly
re-expand the Node files into ambiguous "general Playwright" docs.

## Choose By Repo Truth

- Node / TypeScript / JavaScript app with `package.json` and no stronger
  testing signal: default to `@playwright/test` and `playwright.config.*`.
- Python repo with `pyproject.toml`, `requirements*.txt`, or pytest usage:
  prefer the Playwright Pytest plugin over inventing a Node harness.
- .NET repo with `.csproj` and MSTest, NUnit, or xUnit tests: preserve the
  existing test framework and use Playwright's .NET packages and
  `playwright.ps1` install flow.
- Java repo with `pom.xml` or `build.gradle`: preserve JUnit/TestNG and the
  build tool's Playwright dependency and CLI wiring.

If two ecosystems are equally plausible and the target app package is unclear,
ask before installing dependencies.

## Node Playwright Test

Use when the repo is already Node-based or there is no stronger stack signal.

- Install or extend `@playwright/test`.
- Keep harness config in `playwright.config.*`.
- Use `webServer`, projects, reporters, setup-project auth, and `test.use()`
  patterns from the main Node references in this skill folder.
- Browser install commands use `npx playwright install ...`.

## Python

The recommended E2E runner is the official Playwright Pytest plugin.

- Install `pytest-playwright` and Playwright with the repo's Python package
  manager.
- Install browsers with `playwright install` or
  `playwright install --with-deps chromium` for narrower CI scope.
- Preserve pytest-native config in `pytest.ini`, `pyproject.toml`, or existing
  fixture files rather than creating `playwright.config.ts`.
- Run narrow validation with `pytest`, `pytest test_file.py`, or
  `pytest --browser chromium --headed` as appropriate.
- Reusable auth should stay in pytest fixtures or helper setup, using ignored
  storage-state files rather than Node `auth.setup.ts`.

## .NET

Use Playwright's provided MSTest, NUnit, xUnit, or xUnit v3 integrations
instead of inventing a Node runner beside the test project.

- Add the Playwright package that matches the repo's current test framework.
- Build first so `playwright.ps1` exists under `bin/...`, then install only the
  browsers the repo needs, for example
  `pwsh bin/Debug/netX/playwright.ps1 install --with-deps chromium`.
- Keep configuration in the test framework's existing conventions such as
  runsettings or launch options, not in `playwright.config.ts`.
- Run narrow validation with `dotnet test` against the target test project.
- Reusable auth can still use ignored `playwright/.auth` state files or API
  login helpers, but wire them through .NET fixtures/helpers and
  `StorageStateAsync`, not Node setup projects.

## Java

Playwright integrates with Java test frameworks through normal Maven or Gradle
project structure.

- Preserve JUnit or TestNG instead of adding Node package scripts unless the
  repo is already hybrid on purpose.
- Keep dependencies and browser-install commands in the Java build tool, for
  example
  `mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install --with-deps chromium"`.
- Keep runner behavior in the existing test framework and build-tool config,
  not in `playwright.config.ts`.
- Run narrow validation with the repo's existing test command such as `mvn test`
  or the targeted Gradle equivalent.
- Reusable auth still uses ignored storage-state files and
  `BrowserContext.storageState()`, but the setup belongs in Java helper code or
  fixtures, not Node `auth.setup.ts`.

## Cross-Ecosystem Rules

- Do not create a Node Playwright Test sidecar inside Python, .NET, or Java
  repos just because the Node docs are easier to remember.
- Do not claim `webServer`, setup projects, or `test.use()` exist outside the
  Node Playwright Test runner unless the repo is actually on that runner.
- Keep browser installation commands aligned with the active ecosystem's CLI.
- Keep auth state, traces, screenshots, and reports out of git unless the repo
  has an explicit artifact policy.
