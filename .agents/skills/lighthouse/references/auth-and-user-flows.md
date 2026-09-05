# Authentication and user flows

Read this when the relevant page is behind login, depends on persisted state,
or only appears after an interaction. Ordinary navigation audits alone do not
cover an entire application lifecycle.

## Match the mode to the state

| Mode | What to measure | Important limits |
|---|---|---|
| Navigation | A document load, including a deliberately captured interaction-triggered navigation | Loading metrics and Performance score; not later SPA states |
| Timespan | A short interval containing a specific interaction or SPA transition | No overall Performance score or navigation LCP; no accessibility category |
| Snapshot | The current rendered state, such as an expanded menu or form errors | No overall Performance score or loading metrics; no trace/network history |

Check the chosen version/surface's actual supported audits. Combine steps when
both interaction performance and final-state accessibility matter: timespan
for the transition, then snapshot after meaningful readiness. Use navigation
for a hard document navigation. Keep step names and states explicit in reports.

## Prepare authenticated access

Prefer a task-owned test account and isolated browser when available. Identify
whether authentication lives in cookies, localStorage, IndexedDB, or headers;
preserving storage in an empty new browser does not create a logged-in session.

- **DevTools:** log in to the intended account and verify the actual page.
  The Lighthouse panel preserves cookies. If localStorage/IndexedDB is needed,
  review and disable its `Clear storage` setting for this measurement. Record
  the resulting warm-state conditions and restore settings changed in a reused
  browser afterward.
- **Node/Puppeteer:** use the repository's existing approved authentication
  procedure, prepare the page in the same browser that will be audited, and
  verify authenticated content before starting the relevant step. Keep credentials
  in approved secret inputs and out of source and command arguments. Treat raw
  reports as sensitive and sanitize copies before presenting or sharing them.
- **CLI attachment:** use a deliberately prepared debugging instance. Verify
  its port/profile identity and attach with `--port`; use
  `--disable-storage-reset` only when the required storage must survive. Do not
  attach to an unrelated browser or close a user-owned browser on completion.
- **Headers:** use only when header-based access matches the app. The CLI accepts
  `--extra-headers` from a JSON file as well as inline JSON. Prefer a protected
  temporary file over secrets in shell history, and verify where the runner
  sends those headers. A supplied Cookie header can overwrite other cookies;
  a browser login is more flexible for normal cookie authentication.
  Headers can also persist in report settings and embedded HTML data; follow
  [artifact protection](reports-and-improvements.md#protect-authenticated-artifacts).
- **LHCI:** prepare its browser using `collect.puppeteerScript`; pair with
  `collect.settings.disableStorageReset` when non-cookie auth requires it.
  This is pre-audit setup, not a multi-step user-flow measurement. Read
  [the CI reference](lighthouse-ci.md) before integrating it.

After collection, verify the destination URL and expected authenticated state.
A 200 response can still be a login page or an error screen. If preservation of
auth changes the cold-cache baseline, disclose that tradeoff instead of claiming
an equivalent cold load. Capture the login transition itself only when it is
the requested performance claim and its side effects are authorized.

## Minimal scripted flow

The example below expects one closed `<details id="audit-details">` element
containing `<summary>`. It measures initial navigation, opening the details,
and the expanded state. Adapt selectors and readiness to an inspected app;
do not run arbitrary interactions against production to satisfy an example.

Use compatible `lighthouse` and `puppeteer` packages in the chosen task/project
environment. Save as `audit-flow.mjs`; pass the verified URL and a new artifact
directory. No credentials are needed for this example.

```js
import {mkdir, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import puppeteer from 'puppeteer';
import {startFlow} from 'lighthouse';

const [url, outputDirectory] = process.argv.slice(2);
if (!url || !outputDirectory) {
  throw new Error('Usage: node audit-flow.mjs <url> <new-output-directory>');
}
await mkdir(outputDirectory);
let browser, flow;
let timespanOpen = false;
let stage = 'launch browser';
const failures = [];
const exported = [];
async function attempt(stage, action) {
  try { await action(); }
  catch (error) { failures.push({stage, error}); }
}
try {
  browser = await puppeteer.launch({headless: true});
  const page = await browser.newPage();
  flow = await startFlow(page, {name: 'Load and expand details'});
  stage = 'initial load';
  await flow.navigate(url, {name: 'Initial load'});
  stage = 'details readiness';
  await page.waitForSelector('#audit-details:not([open]) > summary');
  stage = 'expand details';
  await flow.startTimespan({name: 'Expand details'});
  timespanOpen = true;
  await page.click('#audit-details > summary');
  await page.waitForFunction(() => document.querySelector('#audit-details')?.open === true);
  stage = 'finish interaction';
  await flow.endTimespan();
  timespanOpen = false;
  stage = 'expanded-state snapshot';
  await flow.snapshot({name: 'Expanded state'});
} catch (error) {
  failures.push({stage, error});
} finally {
  if (timespanOpen) await attempt('finalize partial timespan', () => flow.endTimespan());
  if (flow) {
    await attempt('export JSON', async () => {
      const result = await flow.createFlowResult();
      await writeFile(resolve(outputDirectory, 'flow.json'), JSON.stringify(result, null, 2));
      exported.push('flow.json');
      if (result.steps.some(step => step.lhr.runtimeError)) {
        throw new Error('A captured step has a runtimeError; inspect flow.json.');
      }
    });
    await attempt('export HTML', async () => {
      await writeFile(resolve(outputDirectory, 'flow.html'), await flow.generateReport());
      exported.push('flow.html');
    });
  }
  if (browser) await attempt('close browser', () => browser.close());
  await attempt('write status', () => writeFile(
    resolve(outputDirectory, 'flow-status.json'),
    JSON.stringify({
      complete: failures.length === 0,
      exported,
      failures: failures.map(({stage, error}) => ({stage, message: String(error?.message ?? error)})),
    }, null, 2),
  ));
}
if (failures.length) throw failures[0].error;
```

```console
node audit-flow.mjs "http://127.0.0.1:4173/" "artifacts/details-flow-01"
```

Create the parent artifact directory first. The example refuses to reuse an
existing final directory. Check `flow-status.json`, the exported files, and
every captured step's identity, warnings, and runtime status. A later failure
still triggers best-effort export of completed steps and any finalized partial
timespan. `complete: false` distinguishes that capture from a successful flow.
Export and cleanup failures are recorded separately and cannot replace the
original thrown error. If capture/export is impossible, status and the nonzero
process result still expose the failure; partial report files are not success.
Status/error messages can themselves be sensitive in authenticated runs.
For a reused browser, end task-owned recordings and disconnect without closing
the user's browser or leaving a recording active.

For desktop flows, import `desktopConfig` from `lighthouse` and pass
`config: desktopConfig` in the `startFlow` options. To retain an explicitly
prepared Puppeteer viewport, use `flags: {screenEmulation: {disabled: true}}`
with the appropriate mobile/desktop scoring config. A viewport alone does not
define the scoring/throttling apparatus.

For a navigation initiated by an action, use `flow.navigate` with an async
callback that actually causes navigation, or bracket it with
`startNavigation` / `endNavigation`. Do not apply that contract to an SPA-only
transition. Interaction-triggered navigation may preserve service-worker/cache
state differently from a URL-triggered run; document that condition.

Sources: [user flows](https://github.com/GoogleChrome/lighthouse/blob/main/docs/user-flows.md),
[authenticated pages](https://github.com/GoogleChrome/lighthouse/blob/main/docs/authenticated-pages.md),
and [Puppeteer integration](https://github.com/GoogleChrome/lighthouse/blob/main/docs/puppeteer.md).
