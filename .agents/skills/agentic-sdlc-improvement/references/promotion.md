# Host promotion and recovery

Use this when a candidate is ready for installation through an existing
authorized host, project, or manual process. This guidance requires no particular
tool or runtime and does not provide installation authority.

## Establish readiness and scope

Use [active-session learning](active-session-learning.md) for eligibility and
evidence criteria. Accepted evidence supports retaining a candidate; authorization
determines whether and where it may be installed. Confirm the permitted changes
and destinations, preserving existing grants rather than asking again for covered
actions.

Identify the maintained source, tested candidate, and current installation before
replacement. Inspect local drift and unrelated edits. If the current installation
differs from the tested baseline, reconcile the difference and obtain the needed
comparison evidence before replacing it; preserve the current work.

Choose an existing authorized process and retain a recoverable predecessor with
the information needed to restore a usable installation. Keep the replacement and
recovery scope limited to the accepted changes. If no suitable authorized mechanism
is available, leave the prepared candidate and evidence intact and report the
missing capability. Do not install dependencies merely to complete this workflow.

## Apply and verify

Make the scoped changes through the chosen process. Verify the actual installed
version and that the intended host can read and load it. Use a reload or fresh
context when the host requires one; a source edit or successful copy does not prove
that an already-running agent is using the new instructions. Check affected
behavior with the available, appropriate verification.

## Inspect interruptions before retrying

Determine what completed, what is currently installed, and how that state relates
to the candidate and predecessor before retrying or restoring anything. Use the
chosen process's recovery route. Restore only changes attributable to this work;
preserve conflicting edits and report any unresolved state. If recovery would
overwrite unrelated work, stop those mutations until the conflict is resolved.

Verify the restored installation and its usability. Report partial recovery as
partial; do not assume that interruption left everything unchanged or that the
chosen process provides atomic replacement or complete rollback.

Report source, tested, installed, and confirmed-loaded states separately, with
their versions, evidence, verification limits, and recovery outcome when relevant.
