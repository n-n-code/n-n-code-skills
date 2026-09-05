# Verification and recovery

Read this when selecting proof, interpreting a failure, or deciding whether
another repair attempt is useful. Use `tester-mindset` for deeper oracle and
test-strategy work; this reference owns the delivery decision from that evidence.

## Define what would count as evidence

Map the increment's acceptance to the narrowest credible observations. Record
the actual command or interaction, target revision, material environment, result,
and remaining gap. Repository-mandated checks still apply. Separate a required
check that did not run from a check that ran and failed.

For a bug, establish a reproduction or failing check that fails for the intended
reason when practical. For a feature, derive checks from accepted behavior rather
than merely asserting the implementation's current output. Do not add low-value
tests for mechanical edits just to satisfy a universal ritual.

For interactive software, exercise the critical journey through real controls
and inspect meaningful state or persistence. A prepared test scene, screenshot,
mocked response, or successful HTTP status may establish only part of the claim.
Use screenshots for visual properties and suitable runtime evidence for behavior.
Declare device, browser, rendering, or production conditions not exercised.

Use judgment for requirements that cannot be reduced to deterministic checks.
Give reviewers explicit criteria and authentic artifacts. If separate review is
available and useful, keep it distinct from generation. Same-agent self-review
can be useful but must not be represented as independent assurance.

## Diagnose the failed observation

| Failure class | Next useful action | Do not infer |
|---|---|---|
| Implementation defect | Reproduce, localize the cause, repair within scope, rerun affected checks and required regressions | A cosmetic diff or confident explanation fixed the behavior |
| Defective oracle or fixture | Check accepted intent and independent evidence; explain and correct the check when authorized | Any inconvenient failure permits changing the expectation |
| Missing or stale context | Retrieve the missing contract, source, or exact error and reassess | More generic instructions will supply missing facts |
| Infrastructure or tool failure | Inspect startup, versions, resource limits, connectivity, and exit results; use `project-platform-diagnose` when available | A failure before the test reached the behavior proves a product defect |
| Authority or access gap | Prepare the concrete proposal and identify the unavailable grant or capability | Permission can be widened by retrying elsewhere |
| Conflicting or insufficient evidence | Choose the smallest observation that distinguishes the explanations | A partial green result overrides contradictory behavior |

An infrastructure failure can itself be caused by the change. Investigate that
possibility before assigning it to an external environment. Report both the
failed attempt and any successful rerun; do not erase the history of a flaky run.

## Protect the oracle

Keep accepted behavior stable across a repair. Test changes are legitimate when
requirements changed, the fixture was defective, or assertions did not represent
the established contract. State the independent basis, preserve meaningful
coverage, and review the changed expectation separately from making code pass.

Do not delete, skip, weaken, or mock away a failure solely to claim success. A
required waiver or quarantine follows the repository's actual policy and remains
visible in the delivery report. Agent-generated review comments need validation
against the same authoritative behavior before they become repair instructions.

## Bound repair

Before a repeated loop, identify user/host hard limits, their scope, consumption,
and remaining allowance. Carry that accounting through handoffs; unknown usage
does not reset the limit. If no hard limit applies, state a finite reassessment
checkpoint. Each pass retains the finding, diagnostic action or change, observed
validation, remaining delta, and material usage.

Continue when the next action is authorized, affordable within any hard limit, and
has a reason to teach or improve something. For a transient failure, establish
that retry is safe and record why it may succeed. For an uncertain external
write, inspect its outcome before retrying; use the release reference.

Stop dependent actions when a hard limit is exhausted or required authority is
missing. At an agent-chosen checkpoint, assess whether the remaining failure is
shrinking and the next action can teach or improve something; continue or revise
the checkpoint with a reason when that work remains authorized. Stop or change
approach when the same hypothesis and failure recur without new evidence. A new
error message alone is not progress, and moving a checkpoint does not resolve
stagnation. Preserve the latest useful state and next action when stopping.

Once adequate evidence and required checks pass, proceed to the requested next
stage. Broaden verification only for a new change, failure, or material concern.
Do not spend the remaining budget rerunning passing checks without a reason.
