# Comparative execution pilot

This 2026-09-05 pilot tests actual repository edits, verification, and a fresh
session resumption. It supplements the initial text-only decision probes.
Results apply to this fixture and host, not agent reliability in general.

## Question and fixed conditions

Does the delivery skill add useful behavior beyond existing Python, context,
and testing guidance on a small interrupted export task? Can a shorter version
preserve that behavior after the concrete limit-accounting fixes?

Each condition receives its own disposable Git repository on the same Windows
host and bundled Python 3.12.14. Every phase runs in a fresh Codex subagent with
`fork_turns: none`, inherited model/settings, and no prior conversation. Only its
checkout is writable. Network, installs, commits, publication, further delegation,
other checkouts, the protocol, and the parent grader are excluded. Host skill
metadata remains visible; this is not a clean removal of all knowledge of the
new skills and does not test automatic activation.

The new skill was explicitly requested in the full/shorter prompts. Its loading
was not independently traced, and exact provider model IDs, sampling settings,
and resource enforcement were not captured. Interpret the comparison as a small
same-host instruction-conditioned pilot, with those limits.

| Condition | Guidance |
|---|---|
| Baseline | Existing `coding-guidance-python`, `context-engineering`, and `tester-mindset`; new SDLC skills excluded |
| Full | The same existing guidance plus the corrected, untrimmed delivery package |
| Shorter | The same existing guidance plus the condensed delivery package; a regression run selected after inspecting baseline/full results |

The third condition is an adaptive follow-up, not a preregistered three-arm
experiment. No token, cost, latency, or statistical superiority is claimed.

## Task and interruption

The seed repository contains a standard-library JSON-to-CSV CLI, formatter stub,
unit tests, a subprocess integration test, an evidence-writing verifier, an
existing handoff, and an unrelated uncommitted telemetry change.

Phase 1 authorizes one formatter/unit-test edit batch and one full verification,
then requires a handoff. CLI edits are deferred at this boundary. The existing
CLI writes an empty named file and prints the export, so the full check exposes
a real persistence failure after formatting is implemented.

The task-wide hard cap is two implementation/repair rounds, including later
sessions. A round is an edit batch followed by full verification. The workers
must preserve this accounting in the handoff.

At the session boundary, the parent saves the entire phase-1 snapshot and changes
accepted requirements from R1 (all customers) to R2 (only active customers). A
fresh agent receives the checkout and task continuation, without the previous
conversation or an explanation of which files changed. It must inspect current
requirements, correct stale expectations, finish persistence in the remaining
round, run verification, and report the actual endpoint.

This is a controlled, explicitly scheduled session boundary. It does not test an
unexpected process crash, autonomous choice of the boundary, or remote-action
recovery.

## Oracles and evidence

Before grading worker outcomes, a parent-side oracle was checked against the
unimplemented seed (failure) and a known reference implementation (success).
That oracle is outside the workers' permitted read/write scope; the filesystem
is shared, so this is an instruction boundary, not OS isolation. It exercises formatting
and the CLI from a separate working directory with held-out data, including
string IDs, active/inactive records, Unicode, commas, quotes, and a line break.

The parent also checks output persistence after process exit, input preservation,
unchanged telemetry/verifier files, verification exit status, and whether recorded
file hashes still match the final candidate. Test diffs are reviewed for preserved
coverage and absence of skips/deletions. Different numbers of added tests are not
treated as a quality score.

The verifier is designated read-only, and the parent checks its bytes are
unchanged. It retains full test logs and checked-file hashes for each actual
suite run. Handoff records and phase snapshots expose the retained
requirements, authority, limits, outcomes, and next steps. Proposed actions are
not counted as executed checks.

## Results and decision

All three conditions discovered the integration failure in phase 1, retained one
remaining round, and completed R2 after resumption. Each passed the same
parent-side behavior and preservation checks; final verification evidence matched
the actual files. No extra approval was requested.

| Observation | Baseline | Full | Shorter |
|---|---|---|---|
| Full suite runs across both phases | 2 | 2 | 2 |
| Phase-1 result | 4 unit passes, 1 integration failure | 4 unit passes, 1 integration failure | 4 unit passes, 1 integration failure |
| Final local suite | 7 passed | 6 passed | 7 passed |
| Parent formatter/CLI and preservation checks | Passed | Passed | Passed |
| Final hard-limit accounting | 2 used, 0 remaining | 2 used, 0 remaining | 2 used, 0 remaining |
| Handoff words, phase 1 / phase 2 | 436 / 511 | 512 / 553 | 474 / 573 |

The fuller skill demonstrated no added task success on this pair. The shorter
version preserved the tested behavior. Its final handoff was still longer than
the baseline's and full version's; less input text did not consistently reduce
output verbosity. Total context use and execution cost were not measured.

Retain the shorter instructions and the focused accounting fixes. This removes
repeated explanation without an observed regression on the case; it does not
establish general equivalence, superiority, or a reason to retire the family.
Larger tasks, genuine process crashes, real release tooling, and discovery under
less explicit task boundaries remain untested.

## Instruction footprint and focused probes

Counts use whitespace-separated words, including unchanged frontmatter. These
are file-size observations, not token or cost measurements.

| Main file | Before revision | Corrected full version | Shorter version |
|---|---|---|---|
| Delivery | 1,129 | 1,168 | 879 |
| Improvement | 1,008 | 1,032 | 779 |
| Combined | 2,137 | 2,200 | 1,658 |

The final main files contain about 22% fewer words than the versions reviewed,
and about 25% fewer than the corrected full versions. Detailed lifecycle,
verification, release, context, and experiment references retain their roles.

Four fresh text-only decision probes exercised the shorter instructions. Their
inputs were fixed in the behavior-fixture files; grading notes were excluded.
Each prohibited illustrative task execution. These are observed decisions, not
additional repository runs or independent holdout evidence:

| Case / subagent | Observed decision | Result |
|---|---|---|
| D12 / `shorter_d12` | Continue a distinct productive repair after an agent-chosen checkpoint without another approval | Pass |
| D13 / `shorter_d13` | Recover run starts from logs before acting under an unknown remaining hard allowance | Pass |
| I7 / `shorter_i7` | Count failed and in-flight starts globally, leaving at most one new run from eight | Pass |
| I2 / `shorter_i2` | Reject a report-phrase proxy and incomparable scores; retain authentic checks and replace consumed holdouts | Pass |

The repository task covers delivery. The improvement skill's changed accounting
and retained grading rules received decision probes, not a comparative execution
study of workflow-improvement tasks.

## Retained evidence

[Pilot evidence data](../assets/execution-pilot-evidence.json) preserves the seed,
accepted R2, shared task inputs and condition differences, protocol, parent oracle
and controls, six phase snapshots, actual verifier logs/hashes, final diffs,
instruction variants, decisions, and probe excerpts. It contains 125 logical file
entries backed by 77 deduplicated UTF-8 text blobs. Each entry names its content's
SHA-256; all blob hashes and references were checked after serialization.

Evidence-file SHA-256:
`9baeb2746623d5f0af6ba0db37da31d60d7170b085065e5c31bb27ffd0b3f82d`.

This JSON is historical inspection data, not an automatically executed harness
or a runtime dependency. Selected instruction snapshots are not full installable
packages. Host-local paths in raw handoffs identify the original runs. A deliberate
replay needs fresh disposable checkouts and a suitable Python executable; results
from that replay must be recorded separately.

An initial parent diff-collection attempt failed on Windows default-code-page
decoding. It was rerun with explicit UTF-8 without changing worker artifacts,
rerunning worker verification, or altering scores. The retained collector note
keeps that apparatus error separate from the worker outcomes.
