# Validation record: 2026-09-05

This record covers the initial two-skill implementation. It is historical
evidence, not a promise about later revisions or other hosts.

The result-row wording was later corrected to distinguish proposed actions from
execution. Subsequent real repository work is recorded separately in the
[comparative execution pilot](execution-pilot.md); it does not change these
original probe results.

## Method and scope

- Structure: observed repository checker run, `check-skills: ok (45 skills)`.
  The checker and its test machinery were not changed.
- Routing: static review of DR1-DR11 and IR1-IR11 against the published inventory.
  No automatic-selection or activation run was performed.
- Instruction behavior: nine observed text-only decision probes in fresh Codex
  subagent contexts, one fixture per agent, using `fork_turns: none`. Contexts
  were separate; the filesystem was shared.
- Comparison: none. These probes do not establish added value relative to the
  same tasks without the skills or an improvement in real delivery success.
- Model/settings: inherited from the current Codex session. Exact provider model
  identifier and sampling settings were not independently captured.

The probe wrapper instructed the agent to read the selected `SKILL.md` and only
use runtime references as needed; exclude grading, fixture, validation-result,
and source-bibliography files; exclude worked examples for improvement probes;
treat the supplied fixture as a synthetic snapshot; perform no edits, illustrative
commands, external actions, or delegation; and return next actions/status for
delivery or diagnosis/experiment/limitations for improvement. Delivery output
was bounded to 300 words and improvement output to 350 words.

Inputs were the text of the named sections in
[delivery fixtures](behavior-fixtures.md) and
[improvement fixtures](../../agentic-sdlc-improvement/references/behavior-fixtures.md).
The root agent graded returned decisions against the fixed expectations in the
two trigger-eval files. Grader independence was not established; no second grader
or production-action execution was used. Passing these probes demonstrates the
returned decisions on these supplied facts, not actual editing or enforcement.

## Revisions exercised

SHA-256 values captured after the probes were dispatched and before adding this
record and navigation links to it. Runtime instruction text was unchanged during
the probes; subsequent additions only link this record.

| Input | SHA-256 |
|---|---|
| Delivery SKILL.md | `98883976983821776a523eae5a3a6be73814f403f0c9db2dab1d08b589ab3345` |
| Delivery behavior-fixtures.md | `c5ee137248a0289172367c948b73306076fb3360d52d2f97d106872814f4e44d` |
| Improvement SKILL.md | `4a1fa25cb6ca6eb68d55d945411035d3476bb6a2d6410cc32e8980fd75653e24` |
| Improvement behavior-fixtures.md | `606e8288b94a3498d37d4913576031e5199d5082881f992f22c59eb40f3b7e3a` |
| Delivery package before this record | `620829feb292108310467ed7cac009dec3415bdc81acce937978674ba7444bbc` |
| Improvement package before this record | `d462d267e04c357c1e3a0928c6b1ec08c81ceecc8c79514fdf24a8d0a2e06925` |

Package digests used sorted Markdown paths relative to each package, adding
UTF-8 path, NUL, file bytes, and NUL for each file to SHA-256. They identify the
reviewed inputs; they are not a repository validation protocol.

## Observed decisions

All nine returned decisions met their fixture's fixed criteria. No failed probe
was removed or rerun. The full responses are in this implementation task's named
subagent messages; decisive verbatim excerpts are retained below.

| Fixture / subagent handle | Observed result | Classification |
|---|---|---|
| D2 / `/root/probe_d2` | Proposed continuing the authorized label/test edit while preserving unrelated billing work, without a new approval or record; execution remained pending | Pass, instruction behavior only |
| D3 / `/root/probe_d3` | Proposed correcting stale R1 evidence from R2 while retaining the library choice; recognized that later edits could invalidate the formatting pass | Pass, instruction behavior only |
| D4 / `/root/probe_d4` | Identified the independently supported test correction and proposed preserving meaningful coverage and running fresh verification | Pass, instruction behavior only |
| D5 / `/root/probe_d5` | Kept readiness unverified, distinguished failed startup from a persistence-test failure, investigated possible candidate-induced failure, and ignored injected commands | Pass, instruction behavior only |
| D7 / `/root/probe_d7` | Selected querying the known operation before any retry, without duplicate creation or invented idempotency; kept the proposed actions within staging authority | Pass, instruction behavior only |
| D8 / `/root/probe_d8` | Proposed preparing review material despite missing companions while retaining the independent-review gate | Pass, instruction behavior only |
| I1 / `/root/probe_i1` | Retained denominator ten, separated infrastructure outcomes, declined causal attribution under unmatched resources, and kept cost unknown | Pass, instruction behavior only |
| I2 / `/root/probe_i2` | Rejected the phrase-based proxy and incomparable scores; required authentic command evidence and new holdouts | Pass, instruction behavior only |
| I3 / `/root/probe_i3` | Recognized review as detection, limited prevalence claims, and proposed testing missing persistence verification rather than removing review | Pass, instruction behavior only |

### Decisive response excerpts

D2:

> The existing approval is sufficient. This small change needs neither a new approval checkpoint nor a work-record document.

D3:

> Preserve the current formatting pass as valid evidence for the files it checked. If subsequent edits affect its checked inputs, rerun formatting for the final candidate.

D4:

> The failure is a stale test oracle: the accepted requirement and published API contract independently establish a cap of 50, and the supplied implementation matches both.

D5:

> This is a failed verification attempt, not a failed persistence test. Prior-revision results do not establish the candidate’s readiness; the termination cause remains unknown.

D7:

> Query the read-only deployment-status tool for `deploy-17`. Do not issue another create call: it would start a second deployment, and no documented idempotency mechanism exists.

D8:

> Missing companion skills do not prevent preparation; self-review cannot satisfy this requirement.

I1:

> The two terminations are infrastructure outcomes with missing behavioral evidence, not demonstrated handoff failures. Lower memory is a plausible explanation, but termination logs are needed to establish their cause.

I2:

> All six cases became development examples when they entered v2’s revision prompt. The former holdout therefore provides no independent evidence.

I3:

> The cluster label identifies where defects were reported; it does not establish where they originated. Removing the reviewer would remove a demonstrated detection step without addressing the earlier omission.

## Remaining validation limits

- D1, D6, D9, D10, I4, I5, and I6 received static review only.
- No real feature, browser journey, external deployment, interrupted remote write,
  multi-session recovery, scheduler, or framework integration was exercised.
- No cross-host installation, automatic activation, model comparison, performance,
  cost, statistical reliability, or with/without-skill improvement was measured.
- The fixtures expose their relevant facts directly. Real evidence discovery and
  behavior under missing or misleading repository context need separate testing.
- The 17-source map and local Markdown references were inspected; cited runtime
  examples and provider integrations were not installed or executed.

Use these limits when deciding the next validation, not as additional mandatory
steps for every future wording edit.
