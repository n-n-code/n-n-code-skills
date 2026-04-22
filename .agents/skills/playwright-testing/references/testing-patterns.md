# Playwright Testing Patterns

Load this file when the main skill needs concrete structure for reusable test
code.

## Page Objects

Use page objects only when flows or locator groups repeat across files.

```ts
import { expect, type Locator, type Page } from '@playwright/test';

export class LoginPage {
  readonly email: Locator;
  readonly password: Locator;
  readonly submit: Locator;

  constructor(private readonly page: Page) {
    this.email = page.getByLabel('Email');
    this.password = page.getByLabel('Password');
    this.submit = page.getByRole('button', { name: 'Sign in' });
  }

  async goto() {
    await this.page.goto('/login');
    await expect(this.email).toBeVisible();
  }

  async login(email: string, password: string) {
    await this.email.fill(email);
    await this.password.fill(password);
    await this.submit.click();
  }
}
```

## Fixtures Over Broad `beforeEach`

Prefer fixtures when setup should be explicit, composable, or worker-scoped.

```ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/login-page';

type Fixtures = {
  loginPage: LoginPage;
};

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await use(loginPage);
  },
});
```

Override built-in fixtures only for strong repo-wide defaults. Keep the side
effect obvious to readers.

```ts
import { test as base } from '@playwright/test';

export const test = base.extend({
  page: async ({ baseURL, page }, use) => {
    await page.goto(baseURL!);
    await use(page);
  },
});
```

## Reusable Auth State

The canonical `auth.setup.ts` + setup-project wiring is owned by
`setup-playwright`. See
[setup-playwright/references/auth-and-ci-patterns.md](../../setup-playwright/references/auth-and-ci-patterns.md)
for the full code (setup project, API-login variant, one-account-per-worker,
sharded CI reporting).

At the test author's side, assume the wiring exists and consume it:

```ts
// tests already inherit storageState from the configured project.
test('dashboard loads', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page.getByRole('heading', { name: 'Overview' })).toBeVisible();
});
```

If login UI is itself the claim under test, bypass `storageState` for that
spec (`test.use({ storageState: { cookies: [], origins: [] } })`) and drive
the UI explicitly rather than fighting the reused state.

`storageState` covers cookies, local storage, and IndexedDB, but not
`sessionStorage`. If the app depends on `sessionStorage`, inject it with
`addInitScript` or a fixture that seeds it per test.

## Locator Refinement

Refine ambiguous locators with chaining and filtering before reaching for
`first()` or `nth()`.

```ts
const product = page.getByRole('listitem').filter({ hasText: 'Product 2' });
await product.getByRole('button', { name: 'Add to cart' }).click();
```

```ts
await page
  .getByRole('listitem')
  .filter({ hasText: 'Mary' })
  .filter({ has: page.getByRole('button', { name: 'Say goodbye' }) })
  .screenshot({ path: 'mary-goodbye.png' });
```

`getByTestId()` is an explicit contract, not a fallback of shame. Use it when
role or text is not stable enough, and honor the repo's configured
`testIdAttribute`.

## Parameterized Cases

Parameterize repeated scenarios instead of copying the same spec body with tiny
input changes.

```ts
import { test, expect } from '@playwright/test';

const cases = [
  { name: 'admin', path: '/admin' },
  { name: 'settings', path: '/settings' },
];

test.beforeEach(async ({ page }) => {
  await page.goto('/');
});

for (const scenario of cases) {
  test(`navigation reaches ${scenario.name}`, async ({ page }) => {
    await page.goto(scenario.path);
    await expect(page).toHaveURL(new RegExp(`${scenario.path}$`));
  });
}
```

Keep `beforeEach` / `afterEach` outside the loop so hooks run once per test,
not once per generated case definition.

## Tags And Annotations

Use tags for filtering and built-in annotations for deliberate execution
semantics.

```ts
import { test } from '@playwright/test';

test.describe('billing', { tag: '@smoke' }, () => {
  test('loads invoices', async ({ page }) => {
    // ...
  });

  test('known upstream bug', { tag: '@vrt' }, async ({ page }) => {
    test.fail();
    // ...
  });
});
```

Use `test.fixme()` when running the test is currently wasteful or unstable, and
`test.slow()` when the behavior is valid but legitimately takes longer.

## Route Mocking

Mock external or intentionally injected boundaries only.

```ts
test.use({ serviceWorkers: 'block' });

test('shows upstream error state', async ({ page }) => {
  await page.route('**/billing-provider/**', route =>
    route.fulfill({ status: 503, json: { error: 'upstream unavailable' } })
  );

  await page.goto('/billing');
  await expect(page.getByRole('alert')).toHaveText(/try again/i);
});
```

## HAR Replay And Live Response Patching

Use HAR when the same external traffic needs to be replayed repeatedly.

```ts
test('replays catalog responses from HAR', async ({ page }) => {
  await page.routeFromHAR('playwright/catalog.har', {
    url: '**/api/catalog/**',
    update: false,
  });

  await page.goto('/catalog');
  await expect(page.getByText('Playwright')).toBeVisible();
});
```

Use `route.fetch()` when you want the real upstream response with a targeted
patch.

```ts
await page.route('**/api/products', async route => {
  const response = await route.fetch();
  const json = await response.json();
  json.products[0].name = 'Playwright';
  await route.fulfill({ response, json });
});
```

## Multiple Signed-In Roles

When one test must exercise two authenticated roles together, use separate
contexts with separate storage states.

```ts
test('admin approves a request visible to the user', async ({ browser }) => {
  const adminContext = await browser.newContext({ storageState: 'playwright/.auth/admin.json' });
  const userContext = await browser.newContext({ storageState: 'playwright/.auth/user.json' });
  const adminPage = await adminContext.newPage();
  const userPage = await userContext.newPage();

  await adminPage.goto('/admin/requests');
  await userPage.goto('/requests');

  await adminPage.getByRole('button', { name: 'Approve' }).click();
  await expect(userPage.getByText('Approved')).toBeVisible();

  await adminContext.close();
  await userContext.close();
});
```

## `test.step()` for Multi-Phase Flows

Wrap meaningful sub-flows so traces and reports show where failure occurred.

```ts
test('user upgrades a plan', async ({ page }) => {
  await test.step('open billing settings', async () => {
    await page.goto('/settings/billing');
    await expect(page.getByRole('heading', { name: 'Billing' })).toBeVisible();
  });

  await test.step('submit the upgrade', async () => {
    await page.getByRole('button', { name: 'Upgrade' }).click();
    await expect(page.getByText('Plan updated')).toBeVisible();
  });
});
```
