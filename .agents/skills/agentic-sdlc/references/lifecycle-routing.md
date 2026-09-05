# Lifecycle routing

Read this when selecting a stage, composing specialist skills, or recovering
stale delivery state. Stage names are navigation aids, not a mandatory sequence
of documents, agent roles, or approvals.

## Stage entry and exit

| Stage | Enter when | Obtain before dependent work advances |
|---|---|---|
| Intent | Desired behavior, scope, or acceptance is unclear | A sourced outcome, constraints, non-goals, and decisions sufficient for the next increment |
| Design | Architecture, UX, interfaces, or a material tradeoff is unresolved | A direction with relevant constraints and risks resolved by the authorized decision owner |
| Plan | Execution order, prerequisites, or proof is unclear | A feasible increment with dependency satisfaction, implementation boundaries, verification, and recovery needs |
| Implement | The next increment is sufficiently specified and authorized | Real changes consistent with intent; relevant tests and docs; an inspectable diff |
| Verify | Correctness or quality needs evidence | Observed, applicable checks and artifact inspection mapped to acceptance, with material gaps identified |
| Review | Judgment beyond mechanical checks is needed or repo policy requires review | Investigated findings, dispositions, and the required reviewer decision; self-review does not impersonate an independent reviewer |
| Release | The requested endpoint includes delivery to another environment | Required checks and authority for the actual candidate; release identity, observed outcome, and operational recovery route |
| Maintain | Requested follow-up or an authorized incident needs attention | Operational evidence, triaged consequences, and scoped remediation or follow-up ownership |

Inspect existing artifacts before producing new ones. For a bounded change, a
few clear decisions and the existing test suite may satisfy several stages.
For a multi-service migration, distinguish prerequisites, coordination, rollout,
and rollback explicitly. Choose the evidence depth from the consequences of
being wrong, not the apparent size of the diff.

Product intent comes from the user or accepted requirements. Code describes
current behavior and may reveal a defect. Neither a newer file nor an agent's
recommendation automatically supersedes accepted intent. Preserve material
conflicts until their owner resolves them.

## Specialist ownership

Load only specialists whose decisions are needed now. These are optional local
companions, not a requirement to install the whole repository.

| Needed output or concern | Existing owner when available | Fallback capability |
|---|---|---|
| Story, acceptance, or dependency-aware slices | `story-clarifier` | Clarify sourced behavior and prerequisites without inventing requirements |
| Story-specific repository evidence | `story-repo-scout` | Inspect code, contracts, tests, and applicable external docs |
| One implementation plan | `story-implementation-planner` | Plan the bounded increment from current requirements and repo evidence |
| Complete preparation packet or uncertain preparation resumption | `story-to-plan-orchestrator` | Prepare only missing upstream outputs in dependency order |
| Code, UI, backend, platform, or release engineering | Matching language, domain, and project guidance | Use the project's actual patterns, tools, and checks |
| Test strategy or weak evidence | `tester-mindset` | Identify a failure-revealing oracle and the smallest credible probe |
| Context selection, compaction, or handoff | `context-engineering` | Preserve current decisions and source handles; refresh material facts |
| Prompt wording or prompt evaluations | `prompt-engineering` | Define the prompt contract and compare representative behavior |
| Security as the primary risk | `security`, with `security-identity-access` for its identity scope | Obtain appropriate security evidence or name the unresolved specialist gap |
| Durable documentation or repo instructions | `documenter` or `agents-md-generator` | Maintain the existing authoritative artifact within scope |
| Tracked change-contract obligations | `development-contract-process` | Follow the actual repo policy, record schema, and checker |
| Improving repeated delivery behavior | `agentic-sdlc-improvement` | Form a bounded, evidence-backed improvement experiment |

When a story component is used, preserve its artifact fields, statuses, and
readiness criteria. The preparation orchestrator stops after its own output;
the delivery workflow decides whether separately authorized implementation can
begin. A `Ready` packet alone grants no implementation permission, and an
explicit plan-only request ends at preparation even if later stages are easy.

If a specialist is missing, use the fallback only to the extent supported by
actual tools and expertise. An absent skill package is not itself a blocker;
an unavailable required observation, tool, or authorized decision can be.

## Advance without losing control

Determine the next action from current evidence and remaining scope. Continue
within the accepted outcome even if an implementation detail changes. Reopen a
decision when it changes behavior, constraints, risk, dependencies, or the scope
of authorization; explain the concrete difference.

Respect mandatory repository checks even when a narrow local test passes.
Resolve flaky or disputed checks through the project's process; do not silently
reinterpret a required check as optional. A pause on one dependency does not
prevent independent authorized work.

## Invalidate only affected work

| New evidence | Revisit |
|---|---|
| Changed behavior, acceptance, or material product constraint | Owning requirement/design and dependent plans, code, tests, review, and release readiness |
| Changed code, interface, dependency, instructions, or environment | Affected implementation assumptions and the checks/reviews that relied on them |
| Corrected test oracle with unchanged intended behavior | Test and evidence; inspect whether the implementation and prior judgments still hold |
| Wording-only clarification | Its owning artifact and downstream coherence; no automatic rebuild |
| Interrupted or uncertain external action | Actual external state before deciding to retry, compensate, or continue |
| Changed executor or resource limit | Execution feasibility, tools, verification capacity, and handoff needs |

Preserve still-useful evidence with its original revision and limitations.
Never relabel old check results as observations of a new candidate. Reuse a
result only when the relevant artifact, inputs, and conditions remain applicable,
and explain that basis when it affects completion.
