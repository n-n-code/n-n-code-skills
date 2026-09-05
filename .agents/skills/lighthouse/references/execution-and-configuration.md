# Execution and configuration

Read this before installing, running, configuring, or troubleshooting Lighthouse.
Runtime help and the selected version's package metadata own current syntax and
compatibility. Upstream examples are starting points, not evidence that the
same versions or startup commands exist in the target repository.

## Discover the apparatus

1. Reuse the available executable or repository-owned tool and inspect its
   version/help. Check Node's version against that Lighthouse package's `engines`
   and locate Chrome/Chromium. Inspect LHCI independently: its bundled Lighthouse
   can differ from the standalone CLI and Chrome DevTools.
2. Inspect package scripts, the active package manager/lockfile, build output,
   existing configuration, and server readiness. Use actual production build
   and serve commands, not a framework guess or an arbitrary port. Starting a
   new server is unnecessary for an already suitable URL.
3. If tooling is absent, identify a compatible version and permitted installation
   location. Prefer a disposable agent-side tool for one-off work; persist a
   project dependency only when repository setup is requested. Pin versions for
   reproducible CI. A global install or environment upgrade is not a prerequisite
   to interpreting an existing report.
4. Choose an unused local output directory/prefix and record the target, profile,
   configuration, and process ownership. Create the output directory if needed.

```console
node --version
lighthouse --version
lighthouse --help
lighthouse --list-all-audits
```

These are discovery commands, not a dependency installer. Resolve unfamiliar
flags through the executable's help before using them. The reviewed source
requires Node >=22.19; recheck the selected package rather than treating this
snapshot as a permanent minimum.

## Choose an execution surface

| Surface | Use when | Boundary |
|---|---|---|
| Lighthouse CLI | Repeatable navigation audits, local/remote URLs, saved reports | Own Chrome unless attaching to a deliberately prepared debugging session |
| Chrome DevTools Lighthouse panel | Inspect an existing logged-in state or run a selected interactive mode | Record the panel's version/settings and storage choice |
| Lighthouse Node API + Puppeteer | Programmatically control authentication, state, or a multi-step flow | Explicit lifecycle, readiness, output, and cleanup |
| Existing browser wrapper | The requested interface exposes the necessary audit | Discover modes/categories/output; do not assume full CLI parity |
| PageSpeed Insights | A public URL needs a hosted measurement, or supplied PSI data needs interpretation | Remote execution cannot reach localhost/private auth; separate lab data from field data |

Honor an explicit surface restriction. If it cannot answer the requested claim,
explain the gap; propose a supported alternative instead of silently switching.

## CLI recipes

These examples assume a verified server at `http://127.0.0.1:4173/`, an existing
`reports` directory, and unused prefixes. Substitute the actual target and
paths. The one-line commands work without shell-specific continuation syntax.

```console
lighthouse "http://127.0.0.1:4173/" --chrome-flags="--headless" --output=json --output=html --output-path="reports/mobile-01"
lighthouse "http://127.0.0.1:4173/" --preset=desktop --chrome-flags="--headless" --output=json --output=html --output-path="reports/desktop-01"
lighthouse "http://127.0.0.1:4173/" --only-categories=accessibility,seo --chrome-flags="--headless" --output=json --output=html --output-path="reports/a11y-seo-01"
```

For multiple output formats, Lighthouse appends `.report.json` and `.report.html`
to the prefix. Verify both files. Use a single `--output=json` with an explicit
JSON filename when only machine-readable output is needed; avoid mixing logs
with JSON by redirecting merged stdout/stderr.

Use `--preset=desktop` for coherent desktop defaults. Merely setting
`--form-factor=desktop` does not configure all desktop emulation/throttling.
For repeated measurements, invoke the command sequentially with `mobile-02`,
`mobile-03`, and so on. `--number-of-runs` is an LHCI collection option, not a
standalone Lighthouse repetition flag.

## Configuration and condition changes

A small JSON config avoids JavaScript module-format ambiguity:

```json
{
  "extends": "lighthouse:default",
  "settings": {
    "onlyCategories": ["performance", "accessibility"]
  }
}
```

Save it at the intended configuration path, then use, for example:

```console
lighthouse "http://127.0.0.1:4173/" --config-path="./lighthouse.config.json" --output=json --output=html --output-path="reports/configured-01"
```

Preserve an existing JS/ESM/CJS configuration's supported module contract rather
than renaming it reflexively. A CLI `--config-path` takes precedence over
`--preset`; do not combine them and assume the desktop preset still applies.
For desktop Node flows use the exported desktop config as described in the
[flow reference](auth-and-user-flows.md).

- Keep the selected throttling method and effective network/CPU settings
  consistent. `simulate`, `devtools`, and `provided` describe different
  apparatus; `provided` means Lighthouse relies on supplied conditions. Do not
  describe DevTools throttling as universally more accurate.
- Discover category/audit IDs for the installed version. Do not request the
  removed PWA category or copy old audit IDs into current configurations.
- Record filters, skipped audits, blocked resources, and storage-reset changes.
  A deliberately blocked third party can isolate its cost; that experiment is
  not the production baseline or proof of a shipped improvement.
- Use `--save-assets` only when traces/logs are needed. Gather/audit modes can
  reprocess compatible saved artifacts; re-auditing those artifacts does not
  measure a new build. Use the matching version and configuration.
- For a nondefault browser binary use `CHROME_PATH` according to the active
  shell, or the surface's supported executable-path option. Do not assume
  POSIX environment-assignment syntax on PowerShell.

## Recovery

Check dependencies and browser launch errors before changing launch flags.
Check the actual URL, redirects, content readiness, auth, HTTP failures, and
resource errors before increasing timeouts. A timeout increase needs a bounded
reason; fixed sleeps and huge traces are not readiness fixes.

Attach through `--port` only to an authorized prepared browser, preserve its
identity, and do not kill it afterward. Do not add `--no-sandbox` as a general
startup remedy. If an environment requires a documented exception, establish
that specific need and the applicable authorization first.

Keep failed-run logs and mark incomplete artifacts. Retry with a fresh output
prefix; never allow an old successful report to mask a failed invocation.
If a report was produced but the process fails during browser/profile cleanup,
record capture validity and cleanup failure separately. Check owned processes
and files before retrying. A demonstrated launcher cleanup problem can be
isolated by attaching through `--port` to a task-owned browser whose lifecycle
is managed explicitly; do not simply ignore the failing exit status.

Source: [CLI and Node documentation](https://github.com/GoogleChrome/lighthouse#using-the-node-cli),
[configuration](https://github.com/GoogleChrome/lighthouse/blob/main/docs/configuration.md),
and [variability](https://github.com/GoogleChrome/lighthouse/blob/main/docs/variability.md).
