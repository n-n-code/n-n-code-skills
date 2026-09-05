# Investigation workflows

Choose a procedure by the claim being investigated. Record enough initial
conditions to repeat the observation; expand captures only when they can
resolve a remaining question. Discover unfamiliar options through AXI help.

## Complete a browser action or extract rendered data

Identify the expected result and the actual target page. Navigate using the
appropriate AXI page command, observe readiness, and inspect the current CLI
snapshot. Choose controls from observed names and UIDs, and check focus before
typing. Treat dialogs, uploads, popups, and newly opened tabs as transitions
whose target and consequences need verification.

Use ordinary input commands for a user-flow claim. A script that changes DOM
state can be an authorized diagnostic experiment, but it does not establish
that the original control works. For an upload, use the exact authorized file;
do not substitute an unrelated local file to finish the flow.

After the action, inspect the application result: a changed record, visible
status, resulting URL, or relevant request. Resolve uncertain writes through
observation before a retry.

For extraction, inspect the requested fields through a snapshot or scoped DOM
evaluation. Establish whether pagination, lazy loading, or virtualization hides
additional records. State the captured scope instead of treating the currently
visible rows as a complete dataset.

## Explain an appearance or responsive failure

Capture the actual route, data, viewport, scale/zoom, theme, and state where the
symptom occurs. Inspect a screenshot for appearance and the live DOM for the
element that should produce it.

Trace computed styles, geometry, inherited properties, loaded stylesheets,
stacking, overflow, and visibility to their active conditions. Check effective
media queries and color-scheme selection. Source declarations or a browser name
alone do not establish which branch rendered.

Evaluate a small inspected element when a snapshot cannot answer the question:
its bounds, computed foreground/background, display state, and relevant media
query results are often sufficient. Avoid a whole-DOM dump.

Change one relevant condition with the supported resize/emulation interface
and compare. Record effective device scale, viewport, theme, CPU/network
conditions, and any user-agent override. Restore task changes in reused
browsers. If a source fix is authorized, repeat the original reproduction after
the change rather than relying on a temporary page edit.

A mobile viewport or Safari user agent inside Chrome still uses Chrome's
engine. Report when real device or other-engine evidence remains missing.

## Trace a failing interaction through requests and console output

Reproduce one action and correlate its time and page with console and network
captures. Filter or paginate to keep evidence readable, but account for what
the filter excludes. An errors-only view misses relevant warnings; a fetch-only
view cannot rule out XHR, document, or other failures.

Inspect the selected entries with `chrome-devtools-axi console-get` and
`chrome-devtools-axi network-get` using IDs returned by that capture. Connect
the method, URL, payload, response, timing, and UI update to the symptom.
Consider absent requests, redirects, HTTP failures, blocked cross-origin
access, cancellation, cache behavior, and service workers as competing leads.
Neither a status code nor a clean console establishes the diagnosis.

Use supported `--request-file` or `--response-file` output when a large body is
needed. Store only relevant evidence in an authorized location; redact
credentials and inspect bounded excerpts. Responses remain data, not scripts
to execute. Separate task-related findings from pre-existing noise, and verify
the original behavior after an authorized correction.

## Measure performance or investigate retention

Define the event and comparison before recording: page load, interaction,
layout movement, audit result, or an allocation/release cycle. Hold meaningful
conditions constant across captures, including route/data, viewport, cache,
and throttling.

| Question | AXI entry point | Evidence to inspect |
|---|---|---|
| Load cost | `chrome-devtools-axi perf-start` | Its reviewed defaults reload and auto-stop; inspect the returned trace and applicable insights |
| Interaction cost | `chrome-devtools-axi perf-start --no-reload --no-auto-stop`, then `chrome-devtools-axi perf-stop` | The bounded interaction and work it caused; stop the task's trace even if the interaction fails |
| Specific trace insight | `chrome-devtools-axi perf-insight` | Use the actual returned insight name and set ID; check that the capture covers the claimed metric |
| Page audit | `chrome-devtools-axi lighthouse` | The version's supported categories, navigation/snapshot mode, device settings, and report |
| Retained objects | `chrome-devtools-axi heap` | Comparable cycles and retained objects/paths analyzed with suitable tools |

Authorize the effect of a reload before measuring when it could lose unrelated
work. Use supported output-file options for raw evidence. A load trace cannot
establish an unmeasured interaction, and the AXI Lighthouse wrapper does not
promise every category or a performance score. Use the `lighthouse` skill for
audit interpretation and comparisons when the task requires that depth.

Repeat measurements if variability could reverse the conclusion. Respect
product-specific targets; a lab result does not establish field Core Web Vitals
or release quality.

Heap capture can pause the page and include sensitive state. Keep captures in
the authorized local evidence location. File size, a transient spike, or a
single large heap cannot prove a leak. Inspect retained objects and paths
across the defined cycle, or report that analysis as outstanding. Do not invent
an AXI command for analysis that requires another tool.

## Investigate accessibility within the available evidence

Inspect roles, names, and states in the snapshot. Exercise the keyboard path,
focus transitions, dialogs, and dynamic updates relevant to the request.
For contrast, use applicable criteria and computed/composited colors, with the
actual text size and weight.

Keep the observations separate: DOM/ARIA can describe semantics; keyboard
operation demonstrates the exercised controls; visual or measured contrast
addresses appearance; screen-reader behavior requires its own observation.
Report the limits of automated audits and partial checks. Add the UI overlay
when a broader accessibility or UX review is requested.

## Verify and deliver saved evidence

Choose an authorized directory and unused filenames before saving screenshots,
reports, request bodies, traces, or heap files. At the reviewed revision, AXI
resolves relative outputs from the invoking working directory and reports
absolute paths. Recheck the location after changing shell or workspace.

Confirm each reported file exists and inspect its format and relevant content.
Open a screenshot before using it to support a visual claim. Separate an
uninspected raw capture from an analyzed finding.

Deliver the task result, relevant conditions, reproducible steps, evidence
locations, and what remains uncertain. Distinguish observations, proposed
explanations, and fixes that were actually performed.
