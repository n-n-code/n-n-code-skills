# Local router integration

Use this reference when designing routing for coding-agent tasks or connecting an
existing router to bounded delegation. It specifies behavior, not an implemented
service, installed models, enforced hooks, or a promise of savings. Use the
[assignment and result contract](../SKILL.md) as the shared boundary; do not
maintain a second copy here.

## Routing and execution

Keep routing policy separate from workers. A local classifier selects an eligible
executor; a local thinking model performs an assigned task. Neither needs to run
on every request.

1. **Establish eligibility.** Carry forward the original requirements, relevant
   conversation context, permissions, data restrictions, resource limits, and
   acceptance owner. Check available executors and their actual capabilities.
   Missing requirements need clarification, not a cheaper model's guess.
2. **Try a deterministic match.** Prefer a registered operation when its purpose,
   validated arguments, and checks satisfy the task: targeted search, structured
   parsing, an existing generator, or a known validation command. This bypasses
   both models. The registry names available operations; it is not permission to
   execute them outside the task's authorized scope.
3. **Classify only unresolved eligible work.** Supply a compact task packet and
   eligible operation/capability descriptions. The classifier proposes a route
   and, for a deterministic operation, its registered identifier. It may abstain.
   The executor validates the route, identifier, arguments, and permissions;
   classifier output is not executable shell text or authority.
4. **Dispatch one bounded assignment.** Use the local thinking worker for task
   classes supported by evaluation, such as focused extraction or predictable
   generation with explicit behavior and references. Route complex diagnosis,
   architecture, or consequential judgment to the responsible reasoning agent
   directly. That may be a frontier executor when available and permitted.
5. **Verify and accept or escalate.** Apply the assignment's checks and acceptance
   ownership. Preserve the original requirements and source handles when handing
   off a failure; include what failed and the limits already consumed. Permit at
   most one escalation after failed local validation within the original budget.
   Escalation never grants remote-transfer permission or resets limits.

On classifier abstention, malformed output, or an unavailable executor, return
control to the responsible agent with the reason. Use an eligible fallback or
request missing information; do not call the local thinking model as a second
router. If no permitted route remains, report the limitation. Do not cycle
between executors or retry a failed classification indefinitely.

Before dispatch, the host must be able to identify the selected executor, provide
the required source access, and respect write ownership. Otherwise use the
skill's ordinary direct-work fallback. Advisory instructions cannot substitute
for runtime enforcement where enforcement is required.

## Acceptance without mandatory frontier calls

Declare the acceptance owner and checks before dispatch. A registered low-risk
operation may complete through deterministic checks when those checks establish
the requested behavior. Do not add a frontier review solely because a local
worker participated. Conversely, do not remove an applicable review because the
local worker reports confidence or its output parses successfully.

For summaries, verify the material source claims needed by dependent work; keep
omissions and uncertainty visible. For generated code, use the actual target
behavior and relevant source as well as a representative pattern. Passing tests
written by the same worker does not independently establish that behavior. Use
existing checks and declared behavioral expectations, and recheck source/target
state before integration.

Task-local output, attempt, and effort limits come from the shared contract.
Enforce supported limits in the executor, and identify advisory or unmeasurable
ones. A smaller parent context alone does not demonstrate lower total usage.

## Versioned improvement

Keep learning outside the request's routing path. The thinking model may propose
a rule or example change in a separate improvement task; it must not silently
rewrite live policy, expand its own permissions, or promote its answer into a
trusted example.

- Attribute each proposal to reviewed outcomes and the affected task class.
  Record only the evidence needed for evaluation; do not retain source corpora,
  secrets, or conversation history merely to accumulate examples.
- Version the rules and curated examples. Separate development examples from
  held-out cases, including failures, abstentions, and protected behavior.
- Compare the candidate with the current policy under comparable conditions.
  Require acceptable task outcomes and an interpretable benefit before claiming
  improvement. A favorable aggregate must not hide a protected-case regression.
- Promote explicitly through the policy owner's authorized workflow. Retain the
  prior version and a rollback path. New models, tools, or task distributions
  require renewed evidence for the affected routes.

This is improvement through rules and examples, not model-weight training.
Use the existing `agentic-sdlc-improvement` workflow when evaluating changes
across development runs.

## Evidence and runtime decisions

A design review can verify the decision paths and contracts. It cannot establish
local model quality, routing accuracy, latency, hardware suitability, or savings.
For a future runtime, resolve and test:

- executor adapters, model availability, source access, and how task context is
  supplied without losing constraints or copying unnecessary history;
- resource ceilings, timeouts, cancellation, concurrent writes, and which limits
  the host can actually enforce;
- representative task coverage, acceptance oracles, and abstention/escalation
  behavior, including restrictions on remote transfer;
- routing and validation overhead alongside all available worker/parent usage,
  retries, corrections, and latency; include model loading and contention when
  they affect the intended local workload.

Compare against competent direct execution using targeted reads and existing
tools. Report absent measurements as unknown. Derive eligibility and thresholds
from that workload; do not inherit a universal file-length cutoff, confidence
threshold, model name, or savings percentage.
