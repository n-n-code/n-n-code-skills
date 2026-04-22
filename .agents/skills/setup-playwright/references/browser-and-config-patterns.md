# Playwright Browser And Config Patterns

Load this file when setup decisions hinge on browser choice, project shape, or
configuration scope.
This file is intentionally Node Playwright Test-heavy. For Python, .NET, or
Java harness choices, preserve the repo's runner using
[ecosystem-patterns.md](ecosystem-patterns.md) before copying any `playwright.config.*`
pattern from here.

## Scaffold Defaults

Official Playwright initialization can bootstrap a new or existing repo:

```bash
npm init playwright@latest
```

Defaults worth remembering:

- default test folder is `tests/`
- if `tests/` already exists, the initializer suggests `e2e/`
- it can add a GitHub Actions workflow
- it can install Playwright browsers
- re-running it does not overwrite existing tests

## Choose The Right Config Scope

Use the narrowest scope that matches the behavior you need:

- global `use` for defaults shared by the whole suite
- project `use` for browser, device, environment, or setup-dependent variants
- `test.use()` for file- or `describe`-scoped overrides such as locale,
  timezone, permissions, color scheme, or viewport

```ts
import { test } from '@playwright/test';

test.describe('french locale flows', () => {
  test.use({ locale: 'fr-FR' });

  test('checkout renders french copy', async ({ page }) => {
    // ...
  });
});
```

Prefer this over creating a new top-level project for every minor scenario.

## Projects, Dependencies, And Teardown

Use projects when the suite genuinely splits by browser, environment, or setup
sequence.

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  projects: [
    { name: 'setup', testMatch: '**/*.setup.ts' },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
      dependencies: ['setup'],
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
      dependencies: ['setup'],
    },
  ],
});
```

Notes:

- dependent projects wait until setup passes
- setup traces and fixtures show up in reporters and trace viewer
- use `testProject.teardown` when setup must be cleaned after dependents finish
- `--no-deps` skips dependency projects and teardowns during targeted runs

## Project Dependencies Versus `globalSetup`

Project dependencies are the recommended default for setup work because setup
shows up in the HTML report, traces are available, and regular fixtures still
work. Use `globalSetup` / `globalTeardown` only when you need runner-external
bootstrap or environment-variable handoff that does not fit the project model.

## Browser Selection

Default Playwright coverage is usually enough:

- bundled Chromium is the default choice most of the time
- Firefox and WebKit belong in the matrix when you need browser diversity
- mobile device projects are useful for responsive or touch-sensitive flows

Use branded Chrome or Edge channels only when the requirement is specifically
about stable-channel parity, media codecs, or browser-policy behavior.

```ts
{
  name: 'Google Chrome',
  use: { ...devices['Desktop Chrome'], channel: 'chrome' },
}
```

If you only run headless bundled Chromium on CI, install cost can be reduced:

```bash
npx playwright install --with-deps --only-shell
```

If you opt into the newer Chromium headless mode with `channel: 'chromium'`,
you can instead skip the separate shell download:

```bash
npx playwright install --with-deps --no-shell
```

## Emulation And Override Order

Use devices for meaningful browser or mobile variants, then override only the
properties you actually need.

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  projects: [
    {
      name: 'mobile-safari-dark',
      use: {
        ...devices['iPhone 13'],
        viewport: { width: 430, height: 932 },
        colorScheme: 'dark',
      },
    },
  ],
});
```

Notes:

- put `viewport`, `isMobile`, or similar overrides after spreading the device
- use `test.use()` for file- or block-scoped locale, timezone, permissions,
  geolocation, or color-scheme overrides
- browser timezone and locale emulation do not change the Node test runner
  timezone; use `TZ` when the runner itself must match
- preconfigured desktop devices may set a platform-specific user agent; unset
  `userAgent` if you need the host platform value instead

## Timeout Strategy

Use the narrowest timeout scope that matches the risk.

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  timeout: 30_000,
  expect: { timeout: 5_000 },
  use: {
    actionTimeout: 10_000,
    navigationTimeout: 30_000,
  },
});
```

Notes:

- keep test timeout for the total scenario budget
- raise `expect` timeout for genuinely slow UI convergence, not as a blanket fix
- prefer fixture-specific timeout overrides for slow worker or setup fixtures
- raise `webServer.timeout` for slow app boot rather than inflating test timeouts

## Parallelism, Sharding, And Reporters

Default Playwright behavior runs files in parallel and keeps tests in one file
ordered unless you opt in further.

- use `fullyParallel: true` only when tests are truly isolated
- sharding is useful once one machine is no longer enough
- balanced shards work better with `fullyParallel: true`; otherwise keep files
  small and evenly sized
- use `blob` reporter on shards and merge reports afterward

```ts
export default defineConfig({
  fullyParallel: true,
  reporter: process.env.CI ? 'dot' : 'line',
});
```

```bash
npx playwright test --shard=2/4 --reporter=blob
npx playwright merge-reports --reporter=html ./blob-reports
```

## Reporter Strategy

Pick reporter combinations for the consumer of the run, not out of habit.

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  reporter: process.env.CI
    ? [['dot'], ['html', { open: 'never' }]]
    : [['list', { printSteps: true }], ['html', { open: 'on-failure' }]],
});
```

Notes:

- local iteration benefits from `list` or `line` output with visible step detail
- CI terminal output is usually cleaner with `dot`
- keep HTML for post-run triage rather than always auto-opening it
- use `blob` on shards, then merge into HTML, GitHub, or other final reporters
- add `json` or `junit` only when another system actually consumes them

## WebServer Details

`webServer` can manage one local app or several cooperating services.

```ts
export default defineConfig({
  webServer: [
    {
      command: 'npm run frontend',
      url: 'http://127.0.0.1:3000',
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
    },
    {
      command: 'npm run backend',
      url: 'http://127.0.0.1:3333',
      reuseExistingServer: !process.env.CI,
      gracefulShutdown: { signal: 'SIGTERM', timeout: 500 },
    },
  ],
});
```

Notes:

- a ready `url` may return 2xx, 3xx, or 400-403 and still count as ready
- use `reuseExistingServer` for local iteration, not CI
- raise server timeout for slow boots instead of raising the entire suite
- use graceful shutdown when background services do not exit cleanly on their own

## TypeScript Behavior

Playwright runs TypeScript out of the box, but it does not type-check tests as
part of execution.

- keep or add a separate compiler or `tsc --noEmit` step when the repo expects
  type safety
- path mappings from `tsconfig.json` are supported
- only precompile tests when Playwright's built-in transform is insufficient,
  such as very new or experimental TypeScript features

## Specialized Modes Outside Default E2E Setup

Some Playwright modes are real, but they are not the default web-app E2E
harness these skills optimize for.

- Component Testing uses `@playwright/experimental-ct-*` packages, `mount`, and
  a separate component-test scaffold.
- Chrome extensions require bundled Chromium plus a persistent context and
  extension launch args.
- WebView2 automation is Windows-specific host-app automation over CDP, not a
  normal browser project matrix.
- Raw `playwright` library scripts are valid automation, but unlike
  `@playwright/test` they require explicit browser/context lifecycle,
  assertions, reporting, and retries management.

## Browser Install And Update Hygiene

Keep the package version and browser binaries aligned.

```bash
npm install -D @playwright/test@latest
npx playwright install
npx playwright --version
```

Install only the browsers you actually need when the suite scope is narrower:

```bash
npx playwright install webkit
npx playwright install --with-deps chromium
```
