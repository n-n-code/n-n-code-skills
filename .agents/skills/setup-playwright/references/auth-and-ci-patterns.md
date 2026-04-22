# Playwright Auth And CI Patterns

Load this file when the main setup skill needs a concrete auth or CI shape.
These concrete snippets are for Node Playwright Test. For Python, .NET, or
Java harness choices, first preserve the repo's runner using
[ecosystem-patterns.md](ecosystem-patterns.md).

## Setup Project And `storageState`

Use this when many tests need the same signed-in user.

```ts
// auth.setup.ts
import { test as setup } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD!);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.waitForURL(/dashboard/);
  await page.context().storageState({ path: 'playwright/.auth/user.json' });
});
```

```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  workers: process.env.CI ? 1 : undefined,
  projects: [
    { name: 'setup', testMatch: /.*\\.setup\\.ts/ },
    {
      name: 'chromium',
      dependencies: ['setup'],
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/user.json',
      },
    },
  ],
});
```

`storageState` captures cookies, local storage, and IndexedDB, but not
`sessionStorage`. If the app depends on `sessionStorage`, inject that state with
`addInitScript` or through a fixture.

UI Mode does not run the setup project by default. If state expires, re-run the
auth setup file manually from UI Mode or the CLI and then continue debugging.

## API Login Variant

Use API login when browser login is slow, brittle, or outside the claim.

```ts
import { request, test as setup } from '@playwright/test';

setup('authenticate', async () => {
  const api = await request.newContext({ baseURL: process.env.BASE_URL });
  await api.post('/api/test/login', {
    data: { email: process.env.TEST_USER_EMAIL, password: process.env.TEST_USER_PASSWORD },
  });

  await api.storageState({ path: 'playwright/.auth/user.json' });
  await api.dispose();
});
```

## One Account Per Parallel Worker

Use this when tests mutate shared server-side state and a shared account would
cause cross-worker interference.

```ts
import fs from 'node:fs';
import path from 'node:path';
import { test as base, request } from '@playwright/test';

export * from '@playwright/test';

export const test = base.extend<{}, { workerStorageState: string }>({
  storageState: ({ workerStorageState }, use) => use(workerStorageState),

  workerStorageState: [async ({}, use) => {
    const id = test.info().parallelIndex;
    const authFile = path.resolve(test.info().project.outputDir, `.auth/${id}.json`);
    if (fs.existsSync(authFile)) {
      await use(authFile);
      return;
    }

    const api = await request.newContext({
      baseURL: process.env.BASE_URL,
      storageState: undefined,
    });

    await api.post('/api/test/login', {
      data: {
        email: process.env[`TEST_USER_${id}_EMAIL`],
        password: process.env.TEST_USER_PASSWORD,
      },
    });

    await api.storageState({ path: authFile });
    await api.dispose();
    await use(authFile);
  }, { scope: 'worker' }],
});
```

Tests must import `test` from this fixture module rather than directly from
`@playwright/test`, otherwise the saved worker auth state will never be used.

## CI Posture

Recommended defaults:

- pull requests: smoke suite on Chromium, trace on first retry, upload artifacts
- scheduled or pre-release runs: broader browser matrix or shard when the repo
  actually needs that evidence
- for CI stability, prefer `workers: process.env.CI ? 1 : undefined`

### GitHub Actions Smoke Job

```yaml
name: Playwright Smoke

on:
  pull_request:

jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v6
        with:
          node-version: lts/*
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test --project=chromium --grep @smoke
      - uses: actions/upload-artifact@v5
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

### Broader Scheduled Matrix

Use a scheduled or manually triggered workflow for Firefox, WebKit, mobile, or
sharded regression when those costs are too high for every pull request.

For very large suites, `npx playwright test --only-changed=origin/$GITHUB_BASE_REF`
is a useful pull-request warmup, but it is a heuristic. Follow it with the full
configured suite rather than treating it as complete coverage.

## Sharded CI Reporting

When the suite is sharded across multiple CI jobs, emit blob reports from each
shard and merge them later.

```bash
npx playwright test --shard=1/4 --reporter=blob
```

```bash
npx playwright merge-reports --reporter=html,github ./blob-reports
```
