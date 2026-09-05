# Release and feedback

Read this before external delivery, operational follow-up, or recovery of an
interrupted side effect. A requested local patch or review ends at that endpoint;
release procedures apply when release is included in scope.

## Prepare the actual candidate

Discover the existing PR, merge, packaging, migration, deployment, and operational
procedures relevant to the change. Use `project-release-maintainer` for release
and packaging engineering when available. Record only applicable evidence:

- candidate revision and intended target/environment;
- required checks, reviews, and authority covering this action;
- migration or compatibility conditions;
- observable success/failure signals and access to inspect them;
- the existing rollback, compensation, or forward-repair path and its authority.

Do not invent commands, environments, approvals, or recoverability. An irreversible
migration may require an explicit risk decision even if ordinary deployment is
authorized. Prepare the candidate and its evidence before escalating that decision.

Respect already-granted release authority. Permission to prepare a patch does
not imply permission to publish, merge, or deploy. A deployment grant also does
not automatically authorize every possible recovery action.

## Execute and inspect

Use the existing delivery mechanism. Record its operation identifier or result
URL when provided. Check that the system acted on the intended candidate and
target, then inspect the required operational signals. A command being accepted
is not the same as a deployment becoming healthy.

For a failed release, follow the actual authorized runbook. Preserve results,
assess impact, and escalate missing authority or unavailable recovery capability.
Do not claim rollback success from a planned command or promise that a rollback
will undo data already changed.

## Recover uncertain actions

A timeout, disconnected session, or missing response can occur after a remote
write succeeded. Before reissuing a create, publish, merge, deploy, or rollback:

1. Query the authoritative system using the known operation ID, target, candidate,
   or other reliable correlation data.
2. If success is confirmed, continue from that outcome rather than repeating it.
3. If failure without the side effect is confirmed, choose a justified retry or
   repair under the existing authorization and retry bound.
4. If the outcome is unknown, use documented idempotent retry semantics only when
   they apply to this exact operation. Otherwise pause the dependent action and
   preserve the uncertainty for the operator.

Do not invent an idempotency key or assume that every command accepts one.

## Follow through without inventing a service

For requested observation, use existing metrics, logs, checks, and incident
procedures. Identify the observation period or terminal condition from the task
or runbook. Report what was actually observed and which production conditions
remain outside that evidence.

For recurring monitoring or future wakeups, use an available authorized scheduler
or monitoring service. Define the trigger, target, permitted response, meaningful
notification conditions, and termination criteria. Do not claim continuous
monitoring from a single tool call or schedule work merely because the skill
covers maintenance.

Triage findings against current state and existing work items before creating
duplicates. A relevant fix within the current scope can enter the delivery loop;
larger or unrelated work becomes a bounded proposal with evidence and an owner.
Do not treat an alert or an agent's diagnosis as authority to change production.

Turn confirmed incidents and review findings into regression coverage when an
appropriate stable oracle exists. Use `agentic-sdlc-improvement` when the finding
concerns how development agents plan, route, verify, recover, or learn across
runs. Feedback does not automatically authorize a policy or memory rewrite.
