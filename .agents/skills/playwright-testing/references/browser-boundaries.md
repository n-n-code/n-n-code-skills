# Playwright Browser Boundaries

Load this file when tests cross iframe, popup, download, dialog, browser-API,
or time-control boundaries.

## Iframes

Use `frameLocator()` for iframe interactions.

```ts
const username = page.frameLocator('.auth-frame').getByLabel('User Name');
await username.fill('alice@example.com');
```

## Popups And New Tabs

Start waiting before the click that opens the new page.

```ts
const popupPromise = page.waitForEvent('popup');
await page.getByRole('link', { name: 'Open receipt' }).click();
const popup = await popupPromise;
await popup.waitForLoadState();
await expect(popup).toHaveURL(/receipt/);
```

For `target="_blank"` flows at the context level:

```ts
const pagePromise = context.waitForEvent('page');
await page.getByText('open new tab').click();
const newPage = await pagePromise;
```

## Dialogs

Handle dialogs before the action that triggers them or the action will stall.

```ts
page.once('dialog', async dialog => {
  expect(dialog.message()).toMatch(/delete/i);
  await dialog.accept();
});
await page.getByRole('button', { name: 'Delete' }).click();
```

## Downloads

Start waiting for the download before clicking.

```ts
const downloadPromise = page.waitForEvent('download');
await page.getByText('Download CSV').click();
const download = await downloadPromise;
await download.saveAs(`tmp/${download.suggestedFilename()}`);
```

## Request Fixture And Eventual Consistency

Use the built-in `request` fixture for backend setup or verification that
should respect config such as `baseURL`, headers, or auth defaults. Use
`playwright.request.newContext()` only when you need isolated cookies instead
of the browser-context-linked request client.

```ts
test('job eventually completes', async ({ page, request }) => {
  await page.getByRole('button', { name: 'Run job' }).click();

  await expect.poll(async () => {
    const response = await request.get('/api/job-status');
    return (await response.json()).state;
  }, {
    message: 'job should reach the done state',
    timeout: 30_000,
  }).toBe('done');
});
```

## Browser-Side Evaluation

Pass values into `page.evaluate()` explicitly.

```ts
const value = 'hello';
await page.evaluate(value => {
  window.localStorage.setItem('greeting', value);
}, value);
```

Use evaluation sparingly; prefer locators and assertions first.

## Time Control

Use `page.clock` for time-dependent UI.

```ts
await page.clock.install();
await page.goto('/session');
await page.getByRole('button', { name: 'Start session' }).click();
await page.clock.fastForward('05:00');
await expect(
  page.getByText(/logged out due to inactivity/i)
).toBeVisible();
```

## Accessibility Checks

Accessibility automation is useful but not full signoff; combine it with manual
assessment.

Use ARIA snapshots when the accessible tree itself is the contract:

```ts
await expect(page.getByRole('navigation')).toMatchAriaSnapshot(`
  - navigation:
    - link "Home"
    - link "Settings"
`);
```

Use `@axe-core/playwright` only when the repo already has it or the task
explicitly asks for it.
