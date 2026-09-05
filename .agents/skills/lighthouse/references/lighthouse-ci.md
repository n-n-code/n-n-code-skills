# Lighthouse CI

Read this for LHCI setup, config review, budgets, regression gates, and collection
failures. Use the repository's actual CI provider and scripts; do not introduce
a new provider or a separate Playwright harness just to run Lighthouse.

## Inspect before integrating

- Find existing `lighthouserc` / `.lighthouserc` JS, CJS, JSON, YAML/YML files,
  package scripts, lockfiles, pipeline references, assertion/budget files, and
  report retention. LHCI searches the current directory, not parent directories;
  pass `--config` explicitly when invoking from another directory.
- Check `lhci --version`, help, package metadata/lockfile, and the LHR's
  `lighthouseVersion`. LHCI bundles its own Lighthouse dependency; do not apply
  standalone Lighthouse 13 audit IDs to an LHCI Lighthouse 12 report blindly.
- Decide how the actual target becomes available. Use `collect.staticDistDir`
  for a built static site served by LHCI; `startServerCommand` for a real custom
  app server; or an already running URL. Do not combine the static server with
  an unrelated remote URL or a second server command.
- Define representative URL/state/device coverage and the source of budgets.
  Preserve existing thresholds. Without them, collect a baseline and calibrate
  targets before adding new hard gates; sample numbers are not product policy.

## Local-artifact starter

This JSON example assumes the production server is already ready at
`http://127.0.0.1:4173/`. Save it at the intended `lighthouserc.json` path and
choose an unused artifact directory for the run/build. The warning thresholds
illustrate syntax and units only; replace them with the actual agreed budget.

```json
{
  "ci": {
    "collect": {
      "url": ["http://127.0.0.1:4173/"],
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "categories:performance": ["warn", {"minScore": 0.9, "aggregationMethod": "median"}],
        "largest-contentful-paint": ["warn", {"maxNumericValue": 2500, "aggregationMethod": "median"}],
        "resource-summary:script:size": ["warn", {"maxNumericValue": 200000, "aggregationMethod": "median"}]
      }
    },
    "upload": {
      "target": "filesystem",
      "outputDir": "./artifacts/lighthouse-01"
    }
  }
}
```

```console
lhci autorun --config=./lighthouserc.json
```

Inspect the config before `autorun`: it can collect, assert, export/upload, and
start an app server, and inherited settings can change its effects. Explicit
CLI flags override configuration; `LHCI_` environment settings can also matter.
Check relevant overrides without dumping secret environment values.

The `filesystem` target exports reports and a manifest locally, without posting
GitHub status checks. Temporary public storage is accessible to anyone with
the URL; a secret gist is also shareable by URL. Neither is a private default.
Use external upload/status integrations only when included in the task's scope.
Protect screenshots, URLs, page content, and authentication artifacts.
Before sharing or publishing authenticated artifacts, follow
[artifact protection](reports-and-improvements.md#protect-authenticated-artifacts).
Local filesystem export does not remove credentials from raw report settings
or embedded HTML data.

For diagnosis, the phases can be run separately:

```console
lhci collect --config=./lighthouserc.json
lhci assert --config=./lighthouserc.json
lhci upload --config=./lighthouserc.json
```

In automation, preserve the assertion exit status while exporting useful
artifacts afterward; a successful final export must not mask an earlier gate
failure. Verify report contents and `manifest.json`, not just the command exit.
Collection normally clears earlier working collection data; export an intended
baseline first. Use unique export directories to avoid overwriting earlier runs.

## Assertions, aggregation, and budgets

- `off` disables a check; `warn` reports a breach without a failing exit status;
  `error` breaches must produce a nonzero exit. A warning-only run is not an
  enforcing regression gate. Keep the check level visible in the report.
- Use `categories:<id>` plus `minScore` for a standard category score, and
  audit IDs plus `maxNumericValue`, `minScore`, or `maxLength` according to the
  supported value being checked. Category assertions do not enable every
  individual audit assertion in that category.
- Choose and record aggregation. `median` uses each asserted value's median;
  `median-run` uses one representative report; `optimistic` selects the most
  passing value; `pessimistic` selects the least passing value. For new
  performance checks default to explicit `median` across three runs. Preserve
  an existing justified policy and avoid silent fallback to more lenient checks.
- Timing audit values such as LCP/TBT use milliseconds; CLS is unitless. Resource
  assertions such as `resource-summary:script:size` use bytes, while the
  Lighthouse budget JSON resource-size format uses kilobytes. Verify the value
  and unit before applying a threshold.
- `assert.budgetsFile` accepts a budget JSON file and cannot be combined with
  other assert options. When metrics and resources need one assertions map,
  use resource-summary size/count assertions there instead. Do not assume a
  legacy standalone `--budget-path` flag exists in the selected Lighthouse.
- Use `assertMatrix` only when route groups actually have different contracts;
  verify that the matching rules cover the intended URLs. Do not copy retired
  PWA/TTI audits or blanket perfect-score presets from older examples.
- Do not assert INP from ordinary navigation collection. Gate the actual
  supported lab metrics and track field responsiveness separately.

## Startup and authentication

Use the real production build command before collection. If LHCI owns startup,
configure `startServerCommand`, a specific `startServerReadyPattern`, and a
bounded timeout based on the app's output. The readiness timeout can elapse
before collection proceeds; also verify that the target serves the intended
page rather than assuming a timeout proves readiness.

`collect.puppeteerScript` runs browser preparation before auditing each URL's
group of runs; it is not necessarily called before every repetition. Keep it
idempotent and verify authenticated state for the intended role. Inspect the
installed LHCI callback contract before authoring the script. Puppeteer must be
available separately, and non-cookie state may require
`collect.settings.disableStorageReset`. Record the resulting cache conditions.
Do not mistake this setup hook for Lighthouse's multi-step flow API.

For a demonstrated launcher/profile-cleanup problem, collection can attach to
an explicitly owned browser using `collect.settings.port`. Keep that browser
alive for collection and close it afterward. Choose one lifecycle owner:
LHCI-managed `puppeteerScript` supplies its own port and should not be combined
with a competing manually managed browser-port setting.

Scope dependency/config/pipeline changes to the requested integration. Preserve
secret handling and artifact access/retention already used by the repository.
Record runtime incompatibility or a failing collection separately from a genuine
budget breach; do not solve either by weakening the thresholds.

## Verify a new or changed gate

1. Collect a valid local fixture with the configured URLs, versions, settings,
   and repetitions; inspect the produced LHRs and exported reports.
2. In a disposable copy of the assertion config, use a measured numeric audit
   with an `error` maximum below every captured valid value. Run `lhci assert`
   against that same collection; require a nonzero exit and the expected breach.
3. Change only that scratch threshold to a clearly passing value and require a
   passing assertion. Verify warning behavior separately when it is part of the
   changed contract. Do not alter the production budget to make this probe pass.
4. Verify that reports stayed at the configured filesystem destination and
   that CI propagates assertion failures even when artifacts are preserved.

If dependencies or a valid browser fixture are unavailable, classify live
collection and failure-propagation checks as skipped. Static config inspection
does not prove a gate ran or failed correctly.

Sources: [configuration and command contracts](https://googlechrome.github.io/lighthouse-ci/docs/configuration.html),
[getting started](https://googlechrome.github.io/lighthouse-ci/docs/getting-started.html),
and [LHCI's Lighthouse dependency](https://github.com/GoogleChrome/lighthouse-ci/blob/main/packages/cli/package.json).
