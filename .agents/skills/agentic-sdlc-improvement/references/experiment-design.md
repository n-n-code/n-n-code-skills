# Experiment design

Read this when turning a diagnosis into a comparison. This reference owns the
workflow-level experiment. Use `prompt-engineering` for prompt-specific evals
and `tester-mindset` when the oracle or test strategy needs deeper investigation.

## Specify the decision before changing the candidate

State a hypothesis connecting the observed problem to one intervention. Name
the owning artifact and an observation that would reject the hypothesis. A
proposal such as "add more context" needs the missing fact, the affected
decision, and evidence that the agent lacked or failed to retrieve that fact.

Keep this compact experiment record in the conversation or an existing
authorized record; it is not a mandatory project schema:

```markdown
Question and failure evidence:
Hypothesis and contrary evidence:
Baseline and candidate versions:
Intervention and owning artifact:
Target behavior and unacceptable regressions:
Cases, protected regressions, and holdouts:
Oracle and grader calibration:
Execution conditions, limit sources/scopes, usage, and remaining allowance:
Observed results and excluded/inconclusive attempts:
Decision, limitations, recovery, and next action:
```

## Choose cases and observations

Preserve realistic inputs, relevant raw artifacts, and expected behavior before
editing the candidate. Include legitimate behavior that must continue, the
observed failure, and nearby cases that could expose an overcorrection. An agent
that avoids all external actions by refusing the whole task has not improved
if the task included authorized actions.

Reserve holdouts from examples used to author the change. Once a holdout informs
the design, treat it as a regression case and replace it before making further
generalization claims. Do not repeatedly tune against the same hidden set and
continue calling it independent evidence.

Choose observations that reveal the claimed improvement:

| Claim | Useful evidence |
|---|---|
| Better scope control | Accepted behavior delivered and unrelated work avoided |
| Better orchestration | Correct prerequisites, handoffs, action order, and endpoint |
| Better verification | Real defects detected, required checks exercised, no weakened oracles |
| Better recovery | Resumption preserves intent and existing work without duplicate side effects |
| Less friction | Unnecessary questions or repeated work decrease while necessary decisions remain |
| Better efficiency | Comparable completion quality with measured time, calls, or cost reduced |

Pick only material measures. Lines changed, number of agents, token volume, or
self-reported confidence are not substitutes for task success. Prefer behavioral
criteria over a brittle exact phrasing match.

## Keep comparisons interpretable

Record the code and task revision, model/provider and available settings,
skill/prompt/tool versions, retrieval inputs, host, environment, relevant resource
allocation, time limits, and retry policy. Use comparable starting artifacts;
candidate runs must not inherit the baseline's completed work or prior answers.

Distinguish available observations, eligible cases, completed executions, and
graded results. State denominators for rates. Report infrastructure failures and
inconclusive attempts alongside results rather than silently excluding them.
Avoid declaring a new winner from one small difference in noisy runs; repeat or
match conditions when that uncertainty would change the decision.

Change one meaningful variable at a time where practical. If several changes
must be bundled, describe the bundle as the intervention and limit attribution
accordingly. A better overall score does not identify which component helped.

## Grade independently of the proposed explanation

Prefer deterministic checks for properties they can actually verify. Give a
model or human grader authentic artifacts and explicit criteria; avoid supplying
the candidate's preferred diagnosis or authoring rationale as evidence of merit.
Calibrate model judges against reviewed pass/fail examples, inspect disagreement,
and check false positives as well as missed failures.

Same-agent review, a separate agent, a separate model, and a human review provide
different evidence. Record which occurred; none guarantees correctness. If the
host exposes no routing trace, reported skill selection is weaker evidence than
observed discovery or file access. Explicitly injecting a skill measures its
post-selection behavior, not automatic activation.

## Decide and recover

Retain a candidate only when the target behavior improves and protected behavior
remains acceptable under the declared criteria. Preserve mixed results and their
consequences. Without a usable comparison, return a hypothesis or an inconclusive
decision, not a measured improvement claim.

Correct a defective oracle only with independent justification; document the
correction and grade baseline and candidate on that same corrected basis.
Permission to improve the workflow does not permit silently changing success.

Carry user/host hard limits and consumption across experiment stages, sessions,
and delegated runs; record unknown accounting instead of resetting it. Reassess
an agent-chosen checkpoint against progress and remaining authorized work. Revise
that checkpoint only with a reason; it does not extend a hard allowance. Stop at
a hard limit, decisive evidence, stagnation, or unavailable authority.
Keep a previous usable version and a concrete recovery action for
adopted changes. Revert only the experiment's own changes; never overwrite
unrelated work. Where a required protective control is involved, a comparison
can support a proposal to simplify it but cannot authorize its removal.
