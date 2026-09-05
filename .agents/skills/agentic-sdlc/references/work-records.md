# Work records and resumption

Read this when work crosses stages or sessions and the next executor would
otherwise have to reconstruct decisions. The record supports continuity;
accepted requirements, repository policy, and observed system state retain
their own authority.

## Choose the existing home first

Use a maintained issue, plan, change-contract record, task notebook, or equivalent
already associated with the work. Identify which artifact owns each fact and
link to it. Do not create another authoritative copy of requirements or approvals.

For an authorized durable handoff with no existing convention, use one Markdown
record in an agreed location. Its filename is not a runtime contract. If file
output is not authorized, provide the same essential information in conversation;
do not create a document tree just because the task is long.

Keep the existing schema and status vocabulary when one exists. Append only
missing continuity information where the schema allows it, or link a handoff
instead of silently changing the schema. For small work, a concise result and
next step can be the entire record.

## Minimum information

Use this shape only when there is no existing suitable record. Omit empty fields
and preserve exact wording where it governs acceptance or authority.

```markdown
Goal and source:
Requested endpoint:
Current increment and remaining scope:
Prerequisites and satisfaction evidence:
Decisions and action authority:
Limits (source, hard limit or checkpoint, scope), usage, and remaining allowance:
Current artifacts and revisions:
Verification evidence and limitations:
Failed attempts and do-not-repeat notes:
Unresolved issues and owners:
Next action and refresh needs:
```

Distinguish authorization to edit locally, open a PR, merge, deploy, roll back,
and schedule future work as applicable. Record existing grants with their source
and scope; do not create additional approvals merely to populate fields.

Preserve each applicable limit's source and scope: a task-wide limit does not
restart at a stage, session, tool retry, or delegation boundary. Record consumption
and remaining allowance with the evidence or estimate behind them; use `unknown`
when they cannot be established. Include in-flight delegated work when it shares
the allowance. Recover missing accounting before an action whose permission or
feasibility depends on it; never assume an unknown balance is a fresh allowance.

Distinguish user/host hard limits from an agent's reassessment checkpoint. A
checkpoint records when to review progress, remaining work, and resources. It can
be revised with a reason while useful work remains authorized; it cannot extend
a hard limit or justify repeating a stagnant approach.

For each consequential attempted action, retain its target, available operation
identifier, result evidence, and whether the outcome is known. Do not store
credentials, protected payloads, or unnecessary raw logs. Retain retrievable
handles where access policy permits.

## Update at useful boundaries

Update when a decision changes, an increment is verified, a blocker is found,
an external action changes state, or a handoff is imminent. Do not transcribe
every tool call. Keep failed attempts that would prevent repeated mistakes and
link to the detailed results when needed.

Delegate context curation and compression to `context-engineering` when present.
The delivery record points to the current work; the context handoff decides what
the next executor must load. Avoid two competing progress summaries.

## Resume from evidence

1. Read the latest user direction and governing instructions, then the record.
2. Inspect current relevant files, working-tree changes, and external operations
   that could affect the next action. Keep unrelated work intact.
3. Check dependencies against actual completion evidence. A plan to do upstream
   work does not satisfy the dependency.
4. Recover source evidence when a summary omits a material detail. A lost approval
   or an unknown action outcome cannot be reconstructed from confidence.
5. Preserve applicable prior authorization. If the candidate or target changed,
   check whether the grant still covers it; do not assume all grants expire on
   every edit or that all grants cover any future candidate.
6. Recover limit accounting and pending work before starting another bounded
   action. Honor remaining hard allowance across the whole declared scope;
   reassess an agent-chosen checkpoint against progress instead of restarting it.
7. Refresh affected evidence, invalidate only its dependents, and continue the
   next authorized action. If a required fact remains unavailable, state the
   exact gap and continue independent work where possible.

The host's session history and the model's current context may retain different
information. Do not claim full recovery when only a summary is available, or
guarantee that context compaction preserves every decision. Keep source handles
and uncertainty so important details can be checked again.
