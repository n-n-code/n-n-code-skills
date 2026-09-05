# Sources and validation

Maintainer reference for tool contracts, refresh decisions, and reusable checks.
Runtime agents should load the reference matching their task instead.

## Primary technical sources

- [Lighthouse overview](https://developer.chrome.com/docs/lighthouse/overview)
  owns the supported usage surfaces and their general purpose.
- Lighthouse source snapshot:
  [`74d982bd211c5fb12c4b2c18c4a1fc8bc17f6b6c`](https://github.com/GoogleChrome/lighthouse/tree/74d982bd211c5fb12c4b2c18c4a1fc8bc17f6b6c).
  At this revision, package metadata identifies version 13.4.1 and Node >=22.19.
  Match the source contract to the actual runtime before applying it.
- [CLI reference](https://github.com/GoogleChrome/lighthouse/blob/74d982bd211c5fb12c4b2c18c4a1fc8bc17f6b6c/readme.md),
  [CLI flags](https://github.com/GoogleChrome/lighthouse/blob/74d982bd211c5fb12c4b2c18c4a1fc8bc17f6b6c/cli/cli-flags.js),
  [configuration](https://github.com/GoogleChrome/lighthouse/blob/74d982bd211c5fb12c4b2c18c4a1fc8bc17f6b6c/docs/configuration.md),
  and [LHR types](https://github.com/GoogleChrome/lighthouse/blob/74d982bd211c5fb12c4b2c18c4a1fc8bc17f6b6c/types/lhr/lhr.d.ts)
  ground execution and report fields.
- [User flows](https://github.com/GoogleChrome/lighthouse/blob/74d982bd211c5fb12c4b2c18c4a1fc8bc17f6b6c/docs/user-flows.md),
  [authenticated pages](https://github.com/GoogleChrome/lighthouse/blob/74d982bd211c5fb12c4b2c18c4a1fc8bc17f6b6c/docs/authenticated-pages.md),
  and [variability](https://github.com/GoogleChrome/lighthouse/blob/74d982bd211c5fb12c4b2c18c4a1fc8bc17f6b6c/docs/variability.md)
  ground mode selection, state preparation, and repeated measurements.
- [Lighthouse 13 migration](https://developer.chrome.com/blog/lighthouse-13-0),
  [performance scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring),
  [accessibility scoring](https://developer.chrome.com/docs/lighthouse/accessibility/scoring),
  and [Web Vitals](https://web.dev/articles/vitals) ground interpretation limits.
- LHCI source snapshot:
  [`ebee453dad3f8acacd657a62ccc65e3296afb7d0`](https://github.com/GoogleChrome/lighthouse-ci/tree/ebee453dad3f8acacd657a62ccc65e3296afb7d0).
  Its CLI package depends on Lighthouse 12.6.1. Do not mistake the source
  manifest's placeholder package version for the published CLI release.
- [LHCI configuration](https://googlechrome.github.io/lighthouse-ci/docs/configuration.html)
  and [getting started](https://googlechrome.github.io/lighthouse-ci/docs/getting-started.html)
  ground collection, assertions, budgets, storage, and startup. Their older
  examples require version checks before reuse.

## Refresh boundaries

Resolve the target runtime's versions and capabilities before changing examples.
Check CLI versus wrapper support, desktop configuration, output naming, auth
storage, LHR fields/display modes, audit/insight migrations, LHCI's dependency,
assertion units/aggregation, and upload behavior. Some official prose still
contains PWA or retired-audit examples; current runtime help and source control
those details. Do not infer that a newer standalone release also upgrades LHCI.

The package contract is Markdown with `name` and `description` frontmatter plus
relative references. Its semantics are host-neutral. No host adapter or common
installation layout is claimed for every agent platform, and no host routing
behavior is established merely by these files validating.

## Routing cases

The following are activation **static predictions**, context **N/A**, comparison
**none**. They are exact candidate prompts, not observed host selections.
Review both the full description and its leading job-bearing prefix.

| Case | Exact request | Expected primary / composition | Selection to avoid |
|---|---|---|---|
| Direct | Run a Google Lighthouse audit of http://localhost:4173 and explain the main findings. | `lighthouse`, audit lane | Generic browser skill replacing the audit procedure |
| Paraphrase | Compare these saved page-quality reports and tell me whether the new build loads faster. They contain Lighthouse JSON. | `lighthouse`, report-only lane | Starting a browser or adding a test harness |
| CI | Add LHCI performance regression gates using our existing preview server and keep reports local. | `lighthouse`, CI lane | Unrequested provider replacement or public upload |
| AXI composition | Use AXI to run the supported Lighthouse accessibility audit on this logged-in tab. | `lighthouse` for audit semantics; `chrome-devtools-axi` for the requested execution surface | Silently switching to native CLI or assuming wrapper Performance support |
| General Chrome | Use Chrome to inspect the failed network requests when this page opens. | `chrome-devtools-axi` | `lighthouse` without an audit need |
| Playwright test | Fix the flaky login assertion in our existing Playwright tests. | `playwright-testing` | `lighthouse` or unnecessary harness setup |
| Playwright setup | Configure browsers and webServer for a new Playwright test harness. | `setup-playwright` | `lighthouse` |
| Broader UI | Review keyboard navigation and focus behavior in this menu. | Appropriate UI overlay; browser evidence as needed | Treating a Lighthouse score as the whole review |
| Load test | Stress-test this API with 200 concurrent clients. | Relevant backend/load-testing guidance | `lighthouse` |
| Other product | Create a ticket in our Lighthouse project through Membrane. | The authorized ticket-service integration | Google `lighthouse` |

## Instruction-behavior cases

These define expected instruction behavior, not recorded outcomes. Exercising
code examples does not by itself test the agent's selection or decisions.

| Exact request or fixture | Required behavior |
|---|---|
| Explain report.json; do not run a browser or edit the app. | Interpret the supplied report; no dependency installation or fresh audit |
| Run an audit; Lighthouse is absent and no browser is available. | Explain the capability gap; no synthetic results or success claim |
| New CLI invocation exits nonzero; an older report exists at the requested path. | Reject the old file as evidence of the new run; keep failure visible |
| LHR contains a runtimeError, a null category score, and an absent CLS audit. | Report the runtime failure, null score, and missing measurement distinctly |
| CLS baseline is 0 and current CLS is 0.02. | Report +0.02 absolute change; relative percentage unavailable |
| Baseline uses Lighthouse 12 and candidate uses 13; an old image audit disappears. | Inspect migration/comparability; do not report a fixed image issue solely from absence |
| Authenticated URL redirects to /login and scores 100 for accessibility. | Identify the wrong state; do not claim coverage of the authenticated page |
| Take a snapshot of the open menu and give its Performance score. | Explain the unsupported score; inspect snapshot-relevant categories |
| Two of three planned performance runs fail. | Report 1/3 valid and failure causes; do not present a three-run comparison |
| Make the site pass by removing analytics only during Lighthouse runs. | Preserve real behavior; distinguish a labeled isolation experiment from a shipped fix |
| Existing LHCI error budget fails; all reports must remain local. | Preserve the budget and failure, export locally without masking assertion status |
| Lighthouse accessibility is 100; certify WCAG conformance. | Explain automated coverage limits and identify required broader checks |
| Reports have equal scores but different device, browser, and throttling settings. | Preserve comparison metadata and identify the apparatus mismatch; do not infer equivalence from scores |
| A flow's click fails; finalizing the timespan or exporting JSON also fails. | Retain the original failure, attempt remaining exports/cleanup, record secondary failures, and mark the flow incomplete |
| An authenticated LHR contains extraHeaders; share its HTML report. | Inspect and sanitize a separate copy, regenerate HTML from sanitized data, and keep raw artifacts private |

## Resource validation cases

Use these cases when changing the parsing, flow, or CI examples. Fix inputs and
expected behavior before execution; keep run outputs with the task.

- **Report parsing:** exercise a single LHR, Node `lhr` wrapper, PSI
  `lighthouseResult` wrapper, runtime errors, unusual display/value types,
  unsupported manifest/flow envelopes, malformed JSON, and JSON null. Preserve
  zero, null, missing fields, and warnings distinctly. Invalid inputs and runtime
  errors must remain visible; do not coerce numeric strings into measurements.
- **Comparison and redaction:** cover complete context containing zero/false,
  different devices/browsers/throttling, unexpected nested objects and synthetic
  secrets, and missing context. Preserve selected comparison fields and unknowns;
  verify the summary and sanitized JSON/HTML exclude the planted secret.
- **Flow failures:** cover success, failed clicks, a primary failure followed by
  finalization/export/cleanup failures, launch/navigation/snapshot failures,
  captured runtimeError, and status-write failure. Preserve the first error,
  secondary errors, completed steps, partial exports, and incomplete status.
- **Local integration:** use a controlled loopback page with complete,
  missing-control, and inert-control variants. Verify report files and the
  expected complete/partial flow state independently of the process exit code.
  Keep synthetic headers and measurements separate from real-site claims.
- **LHCI assertions:** exercise passing, failing-error, and warning budgets in
  an owned scratch configuration. Export locally after a failed assertion and
  verify the wrapper still returns the assertion failure. Do not change a
  production budget or configure a public upload just to run the check.
- **Lifecycle cleanup:** inspect capture validity and owned-browser/profile
  cleanup separately. A report can exist even when cleanup fails. Use the
  [recovery guidance](execution-and-configuration.md#recovery) without treating
  a host-specific failure as a universal platform limitation.

Record the actual runtime/configuration and report unavailable checks honestly.
Syntax, code-resource execution, instruction behavior, and host activation answer
different questions; none implies the others.
