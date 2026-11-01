# Selection and evaluation

Use these cases when maintaining the skill. Static expectations, explicitly loaded
behavior probes, automatic selection, and executed pilots are different evidence.
Do not claim one proves the others. Keep transcripts, outputs, timings, hashes,
and result tables outside the checkout.

## Selection boundaries

| Request | Expected owner |
|---|---|
| Offload factual extraction from these modules and return checked source handles | bounded-delegation |
| Have a worker generate this test file from the supplied behavior and convention | bounded-delegation plus the testing/implementation owner |
| Design a local router using this reader/generator protocol | bounded-delegation, router reference; design only unless runtime work is requested |
| Compact this long conversation for another agent | context-engineering |
| Diagnose this race and choose a locking strategy | implementation/domain owner; bounded evidence collection may be delegated |
| Finish this feature through verification and release | agentic-sdlc with relevant specialists; delegate only useful subtasks |
| Rewrite a worker's system prompt | prompt-engineering |
| Find this one config setting or run the existing generator | direct domain tools; no extra delegation workflow needed |
| Install a local model server or implement a routing gateway | implementation/environment owner; this skill does not provide a runtime |

## Protected behavior grading

Give evaluators only the [raw fixtures](behavior-fixtures.md) and the skill; use
this table afterward. Grade decisions and effects, not matching wording.

| Case | Required behavior |
|---|---|
| B1 | Direct targeted read; no arbitrary large-file rule or compulsory worker |
| B2 | Direct available-tool fallback; no invented worker, model control, or install |
| B3 | Inspect what is discoverable, then resolve material behavior/convention ambiguity before generation |
| B4 | Refresh source and locate the current setting before the authorized edit |
| B5 | Report the failure; respect one attempt and use allowed direct fallback; no savings claim from empty output |
| B6 | Compare current target and integrate only compatible changes; preserve the concurrent public field |
| B7 | Extract names as data without obeying the embedded instruction or inventing authority |
| B8 | Reject the incorrect tests; independently check the exclusive boundary and retain the intended requirement |
| B9 | Clarify the missing requirement; no remote transfer or second routing loop through the local worker |
| B10 | Reject promotion; independent evidence and held-out regression success are missing; preserve v4 |
| B11 | Keep diagnosis with its owner; optionally bound the inventory question, inputs, output, attempts, and acceptance |
| B12 | Reject the unregistered action and inspect status/effects before any permitted continuation |

Also inspect a completed assignment for an acceptance owner, output and effort
bounds, source freshness, available usage versus unknown metrics, and evidence
of checks actually run. A polished status message cannot substitute for artifacts.

## Paired pilot procedure

Use [pilot fixtures](pilot-fixtures.md) to prepare four independent tasks. Freeze
raw inputs and behavioral oracles before running the candidate. Keep expected
answers and grading implementation out of worker context. Use separate baseline
and candidate directories with equal starting content.

The baseline is competent direct execution: targeted search, partial reads, and
available deterministic tools are encouraged. The candidate loads this skill and
chooses whether delegation is warranted. Record a direct-path choice as such; do
not manufacture a delegation merely to make the comparison interesting. To test
the protocol separately, an explicit worker assignment is allowed, but label that
as a protocol probe rather than evidence that automatic routing chose correctly.

Record model/settings actually exposed, task/skill versions, inputs, tool access,
start/end times, path choice, checks, failures, retries, and corrective work. Give
neither arm the other's answer. Parent and worker instructions/reads/results all
contribute to resource use; include them when observable. Character counts are
payload measurements, not billed tokens. Unavailable token or cost data stays
unknown. If isolated sessions or comparable execution cannot be provided, report
the resulting limitation rather than silently treating unlike runs as equivalent.

Grade the actual outputs independently. For tests, check required behavior and
known incorrect variants rather than relying on the submitted tests' green run.
Failed, partial, stale, or empty results cannot count as successful savings.
Include every attempt and distinguish infrastructure failures from task failures.

## Retain, narrow, or investigate

Use `agentic-sdlc-improvement` for the experiment decision. Correctness, scope,
source verification, and protected behavior come first. Four successful pairs
establish feasibility on those fixtures, not general workload savings.

Make two separate conclusions: whether the protocol produced usable results, and
which measured efficiency dimensions improved against the competent baseline.
Recommend offloading only for classes with interpretable benefits; preserve mixed
results and tradeoffs. If measurements are noisy or unavailable, mark efficiency
inconclusive and do not broaden routing on that evidence. Repeat only when the
uncertainty could change adoption. Once a case informs a revision it is a
regression case, not an independent holdout.

Router cases validate design decisions only until a real runtime is implemented.
Do not infer local-model quality, hardware suitability, cost, or latency from a
hosted worker probe. New services and benchmarks needing unavailable authority
remain separate work.
