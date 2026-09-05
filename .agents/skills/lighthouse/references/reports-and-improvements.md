# Reports and improvements

Read this to interpret a report, compare builds, prioritize fixes, or verify
improvement. Keep the original report as evidence; a summary is not a replacement.

## Validate identity and completeness

Identify the input shape before selecting fields: CLI JSON is a Lighthouse
result (LHR); a Node runner result contains `lhr`; PageSpeed Insights JSON
contains `lighthouseResult`; a user-flow result has step-specific LHRs. An LHCI
manifest points to report files and is not itself a full audit result.

Check `lighthouseVersion`, `fetchTime`, `gatherMode`, requested and actual URLs,
`configSettings`, environment, `runtimeError`, and `runWarnings`. Current LHRs
distinguish `mainDocumentUrl` from `finalDisplayedUrl`; older reports may use
`finalUrl`. A redirect to a login/error page is not an audit of the intended
authenticated screen. Explain any warning that affects comparability or validity.

For standard category gauges, JSON scores are 0..1 and displayed scores are
0..100. Preserve null and absent categories. Inspect any other category's
display mode instead of assuming every category is a percentage.

| Result state | Interpretation |
|---|---|
| Category/audit missing | Not collected, unsupported, filtered, renamed, or incomplete; investigate |
| Null score | No numeric score; use display mode and explanation to determine why |
| `binary` | Evaluate the reported pass/fail result and affected instances |
| `numeric` | A scored measurement; preserve the raw value, units, and scoring context |
| `manual` | Requires human/targeted checking; absence of a failure is not a pass |
| `informative` or `notApplicable` | Context or non-applicability; not a failed audit |
| `error` | The audit could not complete; do not treat it as a measured zero or a pass |

Unknown display modes need inspection. Do not classify every `score < 0.9` as a
violation, or let a top-level runtime error disappear behind plausible scores.

## Small report-summary example

The following optional example uses only Node built-ins. Save it as
`summarize-lighthouse.mjs` in the task's artifact area and invoke it with a report
path. It accepts a single LHR or its Node/PSI envelope. For a flow, select each
step's LHR separately; for an LHCI manifest, read the referenced JSON files.
This example reports raw scores and measurement states, not severity or gates.
It retains selected comparison settings and browser information, flags missing
context, and excludes arbitrary configuration fields such as `extraHeaders`.
It is not a general redactor: URLs, warnings, and error messages still require
inspection before sharing.

```js
import {readFileSync} from 'node:fs';

const input = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const lhr = input?.lhr ?? input?.lighthouseResult ?? input;
if (!lhr || typeof lhr.lighthouseVersion !== 'string' ||
    !lhr.audits || typeof lhr.audits !== 'object' || Array.isArray(lhr.audits)) {
  throw new Error('Expected one Lighthouse result; inspect the input shape.');
}
const finiteOrNull = value =>
  typeof value === 'number' && Number.isFinite(value) ? value : null;
const scalarOrNull = value =>
  typeof value === 'string' || typeof value === 'boolean' ? value : finiteOrNull(value);
const pickScalars = (source, keys) => Object.fromEntries(
  keys.map(key => [key, scalarOrNull(source?.[key])]),
);
const stringListOrNull = value =>
  Array.isArray(value) && value.every(item => typeof item === 'string') ? value : null;
const settings = lhr.configSettings ?? {};
const conditions = {
  ...pickScalars(settings, ['formFactor', 'throttlingMethod', 'disableStorageReset', 'emulatedUserAgent']),
  throttling: pickScalars(settings.throttling, [
    'rttMs', 'throughputKbps', 'requestLatencyMs', 'downloadThroughputKbps',
    'uploadThroughputKbps', 'cpuSlowdownMultiplier',
  ]),
  screenEmulation: pickScalars(settings.screenEmulation, [
    'mobile', 'width', 'height', 'deviceScaleFactor', 'disabled',
  ]),
  ...Object.fromEntries(['onlyCategories', 'onlyAudits', 'skipAudits', 'blockedUrlPatterns']
    .map(key => [key, stringListOrNull(settings[key])])),
};
const environment = {
  ...pickScalars(lhr.environment, ['networkUserAgent', 'benchmarkIndex']),
  hostUserAgent: scalarOrNull(lhr.environment?.hostUserAgent ?? lhr.userAgent),
};
const missingComparisonFields = [];
for (const key of ['formFactor', 'throttlingMethod', 'disableStorageReset']) {
  if (conditions[key] === null) missingComparisonFields.push('configSettings.' + key);
}
for (const key of ['throttling', 'screenEmulation']) {
  if (!settings[key] || typeof settings[key] !== 'object' || Array.isArray(settings[key])) {
    missingComparisonFields.push('configSettings.' + key);
  }
}
for (const key of ['onlyCategories', 'onlyAudits', 'skipAudits', 'blockedUrlPatterns']) {
  if (!Object.hasOwn(settings, key)) missingComparisonFields.push('configSettings.' + key);
}
if (!environment.hostUserAgent) missingComparisonFields.push('environment.hostUserAgent');
const metricIds = [
  'first-contentful-paint', 'largest-contentful-paint', 'speed-index',
  'total-blocking-time', 'cumulative-layout-shift',
];
const scores = Object.fromEntries(Object.entries(lhr.categories ?? {}).map(
  ([id, category]) => [id, {
    score: finiteOrNull(category?.score),
    displayMode: category?.categoryScoreDisplayMode ?? 'gauge',
  }],
));
const metrics = Object.fromEntries(metricIds.map(id => {
  const audit = lhr.audits[id];
  return [id, {
    value: finiteOrNull(audit?.numericValue),
    unit: audit?.numericUnit ?? null,
    state: audit?.scoreDisplayMode ?? (audit ? 'unreported' : 'missing'),
  }];
}));
console.log(JSON.stringify({
  lighthouseVersion: lhr.lighthouseVersion,
  fetchTime: lhr.fetchTime,
  gatherMode: lhr.gatherMode,
  requestedUrl: lhr.requestedUrl,
  mainDocumentUrl: lhr.mainDocumentUrl ?? lhr.finalUrl,
  finalDisplayedUrl: lhr.finalDisplayedUrl ?? lhr.finalUrl,
  runtimeError: lhr.runtimeError ?? null,
  runWarnings: lhr.runWarnings ?? [],
  conditions,
  environment,
  missingComparisonFields,
  scores,
  metrics,
}, null, 2));
if (lhr.runtimeError) process.exitCode = 1;
```

```console
node summarize-lighthouse.mjs reports/mobile-01.report.json
```

Missing comparison fields mean unknown conditions, not default settings or a
failed audit. Inspect available nested values and the original reports; this
summary does not certify that two runs are comparable. Null filters can mean
no filter in a valid LHR; an absent filter key is also listed as missing context.

## Protect authenticated artifacts

A protected `--extra-headers` input file does not sanitize outputs. Lighthouse
includes resolved settings, including configured `extraHeaders`, in its LHR;
HTML reports embed report data. Treat raw JSON, HTML, flow status/error files,
traces, screenshots, and manifests from authenticated runs as sensitive.

1. Keep raw evidence in the task's restricted local artifact area, excluded
   from commits and publication. Retain originals only as required for the task.
2. Before presenting or sharing artifacts, inspect headers, URLs/query values,
   errors, captured page content, and screenshots for credentials and private
   data. Prefer a minimal sanitized summary when a full report is unnecessary.
3. Sanitize a separate copy and record the removed fields. Redact configured
   headers and any occurrences in audit details or other captured data; deleting
   just the header input file or hiding visible HTML fields is insufficient.
4. If sharing HTML, generate it from the sanitized report using a supported
   renderer for that version, then inspect the resulting file's embedded data.
   Otherwise share the inspected sanitized JSON/summary. Do not pair sanitized
   JSON with HTML generated from the original raw result.
5. Check the copies for known credential/private-data markers and inspect the
   visible output before sharing. A marker search alone does not establish that
   every kind of sensitive data was removed. Leave raw artifacts private.

Copy only explicitly selected comparison fields into summaries. Copying all of
`configSettings` or `environment` to recover context can expose unrelated data.

## Compare the same claim

Use matching page states, builds/configuration, device and throttling settings,
cache/auth state, runner versions, and materially similar hardware. Explain
environment differences between production and preview instead of attributing
all differences to a code change. Rebaseline both variants under the same
toolchain if a version change prevents meaningful comparison.

Use three sequential runs per variant for performance comparisons, with the
same intended conditions reset each time. Report valid/attempted counts and
failed attempts. Summarize each metric using its median and range; do not pick
the best run. LHCI's representative `median-run` is one chosen complete run
and can differ from the independently calculated median of each metric.

Use signed absolute deltas in the original unit and category changes in score
points. Relative change is `(current - baseline) / baseline * 100` only for
comparable finite values with a nonzero baseline. A zero baseline means the
percentage change is unavailable, not zero or infinity. Do not aggregate the
four category scores into a synthetic overall total.

## Interpret metrics and version changes

The navigation Performance score is driven by scored metrics, not a sum of
estimated savings from insights. Improvements to an insight can affect metrics
indirectly; estimates are not guaranteed or additive score gains.

- Use LCP to investigate loading, CLS for observed layout shifts, and TBT for
  blocking during the measured load. FCP and Speed Index provide additional
  loading context. Read raw units instead of parsing localized display text.
- Field Core Web Vitals are LCP, INP, and CLS. Google's good thresholds are
  LCP <=2.5 seconds, INP <=200 milliseconds, and CLS <=0.1 at the 75th percentile,
  segmented by mobile/desktop. These are field targets, not automatic CI policy.
- A navigation audit has no user interaction from which to measure INP. TBT is
  a useful lab proxy, but meeting a TBT target does not establish good INP.
  Scripted interaction measurements can diagnose responsiveness; they are not
  a substitute for field population measurements. Report CrUX/RUM evidence,
  time window, URL/origin scope, and gaps separately when it is available.
- Lighthouse 13 removed older performance audits from JSON in favor of insights.
  Examples include `render-blocking-resources` becoming `render-blocking-insight`
  and several image audits being consolidated into `image-delivery-insight`.
  Inspect the report and official migration before changing parsers or gates;
  a consolidated insight is not necessarily a drop-in equivalent assertion.

## Turn findings into verified improvements

For each priority finding, capture the audit/insight ID, affected URL/resource
or element, observed condition, suspected cause, proposed change, and the check
that would support the cause. Inspect relevant `details`, explanations, and
linked official guidance; do not assume every audit uses `details.items`.

| Evidence | Useful next investigation |
|---|---|
| Slow LCP | Identify the actual LCP element and phases; distinguish server delay, resource discovery/download, and render delay before changing preloads or images |
| Layout shifts | Inspect the affected elements and timing; find unreserved media/embeds, fonts, or dynamic insertion before prescribing a layout change |
| Blocking/unused JavaScript | Inspect responsible tasks and bundles; verify delivery and execution costs before choosing deferral, splitting, or an interaction-specific fix |
| Accessibility failure | Inspect affected instances and user impact; verify semantics, keyboard/focus behavior, and relevant states alongside automated reruns |
| SEO finding | Inspect rendered metadata/links/indexing intent; preserve intentional staging or private-page restrictions |
| Best-practices finding | Trace the concrete error or resource; assess consequences before exposing source maps or changing third-party behavior |

Implement only the requested improvements and preserve the product's behavior.
Do not remove content, disable audits, hide errors, or omit real third parties
merely to raise scores. If an isolation experiment removes a resource, label
that changed condition and recheck the real configuration after the fix.

Rebuild and remeasure after a source change, and run relevant functional/UI
checks. Report remaining issues and uncertainty when noise or a limited mode
prevents a conclusion. Automated accessibility checks need manual follow-up;
score weights and score deltas are not universal severity assignments.

Sources: [LHR types](https://github.com/GoogleChrome/lighthouse/blob/main/types/lhr/lhr.d.ts),
[report construction](https://github.com/GoogleChrome/lighthouse/blob/main/core/runner.js),
[HTML report serialization](https://github.com/GoogleChrome/lighthouse/blob/main/report/generator/report-generator.js),
[performance scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring),
[Lighthouse 13](https://developer.chrome.com/blog/lighthouse-13-0),
[Web Vitals](https://web.dev/articles/vitals), and
[accessibility scoring](https://developer.chrome.com/docs/lighthouse/accessibility/scoring).
