# Sources and validation

Maintainer reference for tool contracts, refresh decisions, routing, and evidence.
Runtime agents should load the reference matching their task instead.

## Primary technical sources

Technical evidence reviewed 2026-09-05.

- [Lighthouse overview](https://developer.chrome.com/docs/lighthouse/overview)
  owns the supported usage surfaces and their general purpose.
- Lighthouse source snapshot:
  [`74d982bd211c5fb12c4b2c18c4a1fc8bc17f6b6c`](https://github.com/GoogleChrome/lighthouse/tree/74d982bd211c5fb12c4b2c18c4a1fc8bc17f6b6c).
  Reviewed package metadata identifies version 13.4.1 and Node >=22.19. This
  records the source reviewed, not an assertion about an installed or published
  package on a future host.
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

These are **static predictions**, context **N/A**, comparison **none**, unless
an observed execution record below explicitly says otherwise. Passing code
examples does not turn these into observed agent-behavior tests.

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

## Validation evidence

Reviewed and followed up 2026-09-05. Do not treat source review or candidate
cases as observed routing. The initial runtime skips were followed by the
temporary integration checks below. Comparison is **none** unless noted.

| Surface / method / context | Evidence | Result and limit |
|---|---|---|
| Structure / observed run / current target host | Repository `python scripts/check_skills.py`, using the bundled Python executable because Python is absent from PATH | Passed with 45 skills at follow-up; checks metadata, inventory, local references, and layout |
| Structure / observed run / current target host | `git diff --check` and trailing-whitespace inspection of the new untracked package | Passed; Git also emitted existing LF-to-CRLF conversion warnings |
| Activation / static prediction / N/A | Ten routing cases above, reviewed against the current neighboring descriptions and README ownership | Expected boundaries are consistent; actual host selection unobserved |
| Instruction behavior / static prediction / N/A | Fifteen requests/fixtures above reviewed against the workflow and references | Required responses are specified; no isolated agent-behavior run |
| Resource execution / observed run / generic Node harness on Windows | Extracted examples: original nine parser fixtures, four comparison/redaction fixtures, and eight flow-failure scenarios | All 21 passed; review counterexamples changed from lost comparison context/exports to preserved context/partial evidence (before/after) |
| Structure / observed run / generic Node harness on Windows | `node --check` on both extracted JS examples and `JSON.parse` on both JSON config examples | Syntax passed; does not establish Puppeteer or LHCI compatibility at runtime |
| Resource execution / observed run / current target host | Native Lighthouse navigation through an owned browser port, with a synthetic Authorization header on a loopback-only fixture | Valid LHR and HTML; four standard categories; CLI exit 0; actual report summarized with comparison metadata present |
| Resource execution / observed run / current target host | Synthetic secret-marker inspection in raw JSON/HTML, selected-field summary, sanitized JSON copy, and HTML regenerated from that copy | Raw reports retained the configured header; summary and sanitized copies excluded the marker. This is a targeted check, not a universal redaction guarantee |
| Resource execution / observed run / current target host | Unmodified flow example against complete, missing-control, and inert-control fixtures | Complete flow exported three steps with exit 0; readiness failure preserved one step; active-timespan failure preserved two. Both failures exported JSON/HTML, marked incomplete, exited 1, and preserved the original error |
| Resource execution / observed run / current target host | LHCI collection through an owned browser port, three runs, then error/pass/warn assertions and filesystem export | Three valid Lighthouse 12.6.1 reports; breached error exit 1, passing assertion exit 0, breached warning exit 0, filesystem export exit 0 |
| Resource execution / observed run / generic pipeline wrapper on Windows | Run a failing LHCI assertion, export locally afterward, and return the retained assertion status | Wrapper exited 1 while export exited 0; local manifest and report files existed. No named CI provider was exercised |
| Resource execution / observed run / current target host | Initial default Chrome-launcher lifecycle in standalone Lighthouse and LHCI | Failed during Windows temporary-profile cleanup with EPERM after capture. Owned-browser attachment passed; the underlying default-launch cleanup issue was not fixed or reclassified as success |

No isolated target-host activation or cross-host installation was exercised.
The evidence does not establish cross-host execution or discovery behavior.

The nine parser fixtures were: a single LHR, its Node `lhr` envelope, its PSI
`lighthouseResult` envelope, an LHR with a runtime error, unusual display/value
types, an LHCI-style manifest array, a flow-result envelope, malformed JSON,
and JSON null. The base synthetic LHR used performance score 0.91, null
accessibility score, no SEO category, TBT 0 milliseconds, no CLS audit, and an
explicit fixture warning. Checks preserved zero/null/missing distinctions and
warnings. The runtime-error fixture returned nonzero with its error visible;
unsupported envelopes and malformed inputs returned nonzero. A numeric string
was not converted to a measurement, and a custom fraction display mode survived.

The four additional summary fixtures checked complete comparison context with
zero/false values, differing devices/browsers/throttling, unexpected nested
objects and secret markers, and absent comparison context. Only selected fields
survived; missing conditions remained explicit rather than receiving defaults.

The eight flow adapter scenarios covered success, a failed click, a failed click
plus finalization/export/cleanup failures, browser-launch failure, navigation
failure, snapshot failure, a captured runtimeError, and status-write failure.
They checked first-error identity, secondary failures, partial exports, incomplete
status, and cleanup. These are code-behavior tests, not agent instruction tests.

The live environment used Windows, Node 24.19.0, Lighthouse 13.4.1, LHCI CLI
0.15.1 with Lighthouse 12.6.1, Puppeteer 25.10.0, and Chrome for Testing
152.0.7977.75. Packages and Chrome were provisioned only in an owned temporary
directory, with no repository dependency or global installation. Browser audits
ran sequentially against a disposable loopback HTTP server. The flow fixtures
either exposed the documented details control, omitted it, or prevented its
default opening action to provoke a timeout inside an active timespan.

Native execution used the documented CLI flags plus `--port` for an owned
Puppeteer browser. LHCI used the documented config with the local URL, filesystem
output directory, and `collect.settings.port` substituted. Scratch error
thresholds were set below all captured LCP values to fail, then above all values
to pass; existing repository budgets were not involved. Three JSON/HTML report
pairs and a local manifest were verified. No external report upload or status
publication was requested or configured.

The initial default-launch failure is an environment observation, not proof of
its root cause or a general Windows limitation. Direct-launch cleanup remains
unverified beyond that failure; the successful attachment path has separate
evidence. Keep that distinction when refreshing the skill or testing another host.
Synthetic markers and fixture measurements are validation data, not real-site
performance claims. Temporary dependencies and artifacts are not shipped with
this package. The integration directory, downloaded browser, packages, and
artifacts were removed after verification; no process using the task's browser
binary remained at cleanup.
