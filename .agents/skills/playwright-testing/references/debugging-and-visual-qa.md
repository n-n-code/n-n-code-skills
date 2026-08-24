# Playwright Debugging And Visual QA

Load this file when the main skill needs concrete debugging commands, trace
inspection patterns, or screenshot guidance after the investigation has moved
from CLI exploration into runner-side debugging.

Commands and snippets below target Node Playwright Test. Use the active
runner's equivalents from [ecosystem-testing.md](ecosystem-testing.md) in
Python, .NET, or Java harnesses.

For CLI-first exploration and paused-test attachment, load
[playwright-cli-investigation.md](playwright-cli-investigation.md).

## Debugging Commands

Prefer narrow reruns over broad suites while debugging.

```bash
npx playwright test tests/e2e/login.spec.ts --project=chromium --reporter=line
npx playwright test tests/e2e/login.spec.ts:42 --debug
npx playwright test -g "user can reset password" --project=chromium
npx playwright test --max-failures=1
npx playwright test tests/e2e/login.spec.ts --project=chromium --workers=1 --headed
npx playwright test --last-failed
npx playwright test tests/e2e/login.spec.ts --project=chromium --ui
npx playwright show-report
npx playwright show-trace test-results/<trace>.zip
```

Open the trace before guessing. Look for selector ambiguity, missing waits,
state leakage, stale auth, or route mocks intercepted by service workers.

Prefer traces over raw video when diagnosing CI failures. Keep `trace:
'on-first-retry'` in normal config, and use `--trace on` locally only when you
need an every-run trace while debugging.

On Playwright 1.59 or newer, the agent-readable trace CLI can inspect a trace
without opening the GUI. Confirm the installed command surface first:

```console
npx playwright trace --help
npx playwright trace open test-results/<result>/trace.zip
npx playwright trace actions --grep="expect"
npx playwright trace action <action-number>
npx playwright trace snapshot <action-number> --name after
npx playwright trace close
```

Use action numbers and paths returned by the opened trace; do not assume an
artifact layout from another project or Playwright version.

## Codegen And Locator Picking

Use official Playwright tooling when a locator is hard to derive confidently.

```bash
npx playwright codegen http://127.0.0.1:3000
```

Workflow:

- stop recording before picking locators you plan to hand-author
- use the Inspector or UI Mode locator picker to see the generated locator
- refine to role, text, or explicit test id if the first suggestion is too broad
- copy the locator into the real test instead of shipping recorded code blindly
- use UI Mode filters by project, tag, or status when triaging a broad suite

## Visual Assertions

Use screenshot assertions only when rendering is the contract and the
environment can keep baselines stable.

```ts
import { expect, test } from '@playwright/test';

test('toolbar layout is stable', async ({ page }) => {
  await page.goto('/settings');
  const toolbar = page.getByRole('toolbar');
  await expect(toolbar).toHaveScreenshot('settings-toolbar.png', {
    animations: 'disabled',
  });
});
```

Guidelines:

- Prefer element or viewport screenshots over full-page captures.
- Disable animations for baseline comparisons.
- Mask or avoid dynamic content instead of accepting noisy diffs.
- Expand to Firefox or WebKit only when the claim needs browser-specific
  evidence.
