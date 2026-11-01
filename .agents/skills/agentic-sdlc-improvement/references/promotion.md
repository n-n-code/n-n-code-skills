# Local promotion and recovery

Use this when the host has authorized installation of an evaluated personal skill
and configured the bundled [promotion helper](../scripts/promotion.py). The helper
is a standard-library Python utility for local file state. It does not run agents,
grade evidence, grant authority, publish Git changes, or install a background service.

## Separate eligibility from installation

The responsible agent establishes eligibility using the experiment contract and
the host's policy before preparing a transaction. Keep that decision outside the
candidate, with the tested revision, actual observations, limitations, and recovery
scope. Choose its evidence class honestly:

- `bootstrap`: explicitly requested new capability; functional acceptance, benefit
  still unmeasured.
- `maintenance`: direct invariant restored, such as an invalid reference or stale
  generated installation; independently edited copies must be preserved.
- `behavior`: matched behavioral comparison and fresh analogous evaluation support
  the stated scoped improvement while protected behavior remains acceptable.
- `improver`: the procedure itself had a demonstrated weakness, and matched-start
  downstream evaluation supports the revised procedure.

These labels are not bypasses. The helper verifies a local evidence artifact's
identity and structure, not the truth of its conclusions. Do not relabel a failed
behavioral comparison as maintenance or bootstrap to install it.

## Configure the host once

Keep the machine policy outside the candidate's writable targets. Its JSON fields
are `version` (currently `1`), `state_root`, `allowed_target_roots`,
`allowed_target_files`, `protected_paths`, and `helper_sha256`. Use absolute paths. Directory roots permit descendant targets;
exact file entries permit shared metadata without authorizing an entire repository.
Protect the trusted helper, personal authorization policy, and frozen grading
controls. The machine policy is itself protected. Preserve the target roots and
existing local changes; a portable skill cannot authorize expansion of this list.

Use a private state root outside checkouts for transactions, snapshots, staged
packages, and evidence. Keep candidate packages outside discoverable skill folders
until they are accepted. The target's parent directory must already exist; an
individual package or file target may initially be absent. Symlink/junction targets,
path escapes, overlapping targets, and state inside managed targets are unsupported.
On Windows, changing or deleting a read-only file, or creating a read-only candidate file, is unsupported; unchanged read-only package members are preserved.

Pin the reviewed helper's SHA-256 in the policy. A helper or policy change is a
separate authorized maintenance operation; the candidate being promoted cannot
replace, delete, or silently update these controls.

Keep policy versions at immutable paths while their transactions may need
recovery. Transactions pin the policy's path and contents and the executing
helper's identity. Bootstrap installation may use a separate explicit policy
and state directory; keep that policy and trusted helper for its recovery.

## CLI and request

Invoke the configured trusted helper with these operations:

```console
python promotion.py prepare --policy /absolute/policy.json --request /absolute/request.json
python promotion.py apply --policy /absolute/policy.json --transaction TRANSACTION_ID
python promotion.py status --policy /absolute/policy.json
python promotion.py recover --policy /absolute/policy.json --transaction TRANSACTION_ID
```

`prepare` returns the transaction ID and record location as JSON. `status` may also
take `--transaction` to inspect one record. Check the command's exit status and
returned status rather than treating an attempted operation as completion.
Statuses distinguish `prepared`, `applying`, `applied`, `interrupted`,
`recovering`, `recovered`, `cancelled`, and `conflicted`. Recovering an unapplied
prepared transaction cancels it without restoring older target contents.
Repeated recovery reports current target matches without rewriting subsequent
edits; a historical `recovered` status is not a claim that those files never drifted.
For another recorded policy path or hash, `status` returns metadata only and
flags that full inspection requires the recorded policy. It does not interpret
those targets under the current allowlist. Unresolved transactions still block
publication across policies sharing the state directory and lock.

The request contains:

```json
{
  "version": 1,
  "eligibility": {
    "class": "behavior",
    "evidence": "/absolute/accepted-evidence.md"
  },
  "targets": [
    {
      "path": "/absolute/maintained-source/skill-name",
      "candidate": "/absolute/staging/skill-name",
      "kind": "directory"
    },
    {
      "path": "/absolute/installed-skills/skill-name",
      "candidate": "/absolute/staging/skill-name",
      "kind": "directory"
    }
  ]
}
```

`kind` defaults to `directory`. A `file` target uses an absolute candidate file;
`candidate: null` explicitly removes that file. Declare every intended target,
including relevant source documentation. Do not replace a whole repository to
update one shared file. Unknown fields are errors, not extra authority.

## Publication and recovery contract

1. **Prepare:** freeze complete baseline and candidate manifests, including file
   membership, additions, deletions, and absence. Snapshot baseline bytes and the
   evidence decision outside the checkout. Preparation does not edit target files.
2. **Apply:** acquire the host's nonblocking operating-system lock and hold it for
   the operation. Another writer or unresolved transaction leaves the new candidate
   pending. Recheck policy, helper, protected controls, and every target against the
   prepared state before writes.
3. **Write:** keep full candidate stages and snapshots outside the checkout.
   Persist the intended transaction before mutation. A journaled final publication
   temporary is created briefly in the actual destination parent before replacement.
   On Windows this gives new files their intended inherited access rules; existing
   DACLs are applied before any private bytes are copied. Replace files individually
   and record progress. Verify complete membership, bytes, modes, and recorded
   Windows access rules before declaring success.
4. **Inspect after interruption:** use `status`, then `recover` when appropriate.
   Recovery reacquires the same lock and examines real files, including a replacement
   completed before its progress record was updated. Restore only unchanged writes
   attributable to this transaction. Preserve content or access rules that match
   neither recorded state and report the unresolved conflict. Clean only the
   transaction's journaled publication temporaries.

Do not remove or replace the lock file, steal a lock based on elapsed time, or
claim that a partial rollback restored the package. An unresolved transaction
blocks further managed publication until its state is reconciled. A process exit
does not by itself prove that its writes completed or were rolled back.

File replacements are individually atomic where the filesystem supports them;
publication of multiple files or drives is not one atomic operation. The lock
coordinates participating writers, not arbitrary editors. Evaluation uses frozen
complete package snapshots, and a new installed revision needs fresh-context
verification. An already-running chat may still use older instructions.
Check that the intended host can actually read the installed files; matching
content hashes alone cannot establish usable permissions or successful loading.

Internal journal version 2 records Windows DACLs and publication temporaries.
Retain the original trusted helper and policy for a version 1 journal. Those older
journals did not capture original Windows DACLs, so their snapshots cannot prove
exact permission restoration. Do not infer an original ACL from a copied snapshot
or reset existing custom permissions to guessed defaults.

## Validation and limits

The source repository's `scripts/test_skill_promotion.py` exercises real temporary
files, writer contention, interrupted operations, and conflict preservation. It is
also included in `scripts/test_skill_resources.py`. Test source/install targets on
the actual host; do not infer Windows or cross-volume behavior from a different
platform. This is recovery for process interruption and known file states, not a
claim of power-loss durability or a security boundary against a malicious process
with the user's filesystem access.
