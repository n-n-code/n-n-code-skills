# Worked examples

All inputs and numbers below are illustrative. These examples demonstrate
decision boundaries; they are not observed validation of this skill family.

## A handoff drops a required verification step

Evidence: three sampled delivery records ended with unit checks. Their accepted
plans also required a persistence journey. The final reports said delivery was
verified. A fourth record included the journey and found a reload defect.

Hypothesis: the handoff omitted the acceptance-to-evidence mapping, so execution
mistook the unit result for complete verification. Alternatives include a missing
browser environment or ambiguous acceptance; inspect the raw runs first.

Intervention: preserve the unresolved persistence check in the existing handoff
and name its owner. `context-engineering` owns context curation; the delivery
workflow owns whether the available evidence permits completion. A prompt edit
would belong to `prompt-engineering` if wording is the demonstrated cause.

Experiment: replay comparable unfinished tasks with the old and revised handoff.
Require actual journey evidence or an honest environment gap. Include a unit-only
task to detect needless browser work, and hold out a different persistence path.

Decision: retain only if the missing verification decreases without fabricated
execution or unnecessary gates. This sample does not establish the prevalence
of the problem across all development tasks.

## An apparent regression is confounded by resources

Evidence: baseline completed 9/10 cases; candidate completed 7/10. Two candidate
attempts were killed before tests started. Baseline had 8 GB memory; candidate
had 2 GB. One further candidate run produced an actual behavioral failure.

Interpretation: retain all ten attempts in the outcome report. The data contains
two infrastructure failures and one behavioral failure, but does not isolate the
effect of the workflow change. Do not call the candidate either better or worse
from the aggregate score alone.

Next action: reproduce the behavioral failure and rerun comparable cases under
matched resource conditions when authorized. If the resource restriction itself
is the intended deployment condition, evaluate adaptation to that condition as
the explicit experiment instead of normalizing it away.

## A model upgrade may make a reset step unnecessary

Evidence: a workflow resets context at each increment because an earlier model
ended tasks prematurely. The current model now completes the relevant tasks
without that symptom in initial observations.

Hypothesis: removing the reset preserves completion and reduces repeated
discovery. Compare the current model with and without the reset using identical
starting tasks, limits, and oracles. Preserve constraints, interrupted-task
recovery, and difficult long-task holdouts.

Decision: remove the reset only after evidence supports the behavior and the
change is authorized. A newer model name alone does not justify removal. If a
reset also enforces a required isolation boundary, treat that as a separate
protected requirement; performance gains do not waive it.
