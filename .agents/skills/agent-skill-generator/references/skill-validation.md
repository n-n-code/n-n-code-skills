# Skill validation

Use this when a designed, generated, or revised skill needs trigger, workflow, resource, or execution evidence before shipping.

## Choose evidence on independent axes

Use the smallest combination that answers the risk. Do not collapse unlike evidence into a maturity ladder or report a prediction as an observed result.

Choose one or more test surfaces:

- `structure`: frontmatter, names, links, referenced files, package layout, and repository-specific checks;
- `activation`: whether a realistic request selects the intended skill without preselection;
- `instruction behavior`: whether an already selected or explicitly invoked skill follows its contract;
- `resource execution`: whether representative bundled scripts or tool workflows produce the expected outputs and side effects.

Record the evidence method separately:

- `static prediction`: inspect descriptions, instructions, and neighboring skills without running host routing or the workflow;
- `observed run`: exercise routing, instructions, scripts, or tools and inspect the result.

For an observed run, record its context:

- `generic harness`: an isolated runner that does not reproduce a named target host;
- `isolated target host`: a fresh session or agent in the actual target host;
- `current target host`: the current non-isolated session in the actual target host.

Use `N/A` for context when the method is static prediction.

Add a comparison only when it answers a distinct question:

- `none`: no comparison;
- `before/after`: regression check across a revision;
- `with/without`: measure the skill's added value;
- `A/B`: compare competing trigger or workflow variants.

A surface does not imply method or context: resource execution can occur in a generic harness, and a comparison can still be based only on static prediction. Prefer an isolated target-host activation run for high-risk reusable skills when the environment supports it. Do not build a heavy harness unless the user, repository, or risk justifies one.

## Build the prompt set

Before a substantive revision, preserve the relevant baseline requests, raw
artifacts, expected behavior, and material constraints. Reuse them afterward.
Correct a defective expectation explicitly; do not quietly redefine success to
match the new skill or a more permissive validator. Keep useful holdout cases
separate from examples used to design the change.

For activation, start with realistic requests that do not name, inject, or otherwise preselect the skill:

- `positive-obvious`: direct request using likely trigger language;
- `positive-paraphrased`: the same job expressed differently;
- `negative-adjacent`: nearby work that should select another skill or none;
- `collision`: a prompt likely to match a competing skill, when one exists.

For hosts that truncate or budget descriptions, repeat the static review against a realistic leading prefix. Treat the prefix length as a host-specific assumption unless the platform documents it.

For instruction behavior, the case may explicitly invoke or inject the skill. Add cases such as:

- missing or ambiguous inputs;
- read-only versus mutating intent;
- unavailable dependency or validator;
- partial failure, cleanup, or rollback;
- repo-bound behavior used outside the target repository.

## Protect evaluation integrity

For observed runs:

- for activation, pass a realistic request without the target skill name or selection instruction;
- for instruction behavior, pass the skill plus realistic inputs, not the intended answer or suspected defect;
- provide raw artifacts rather than prior conclusions;
- confirm that decision-bearing fixtures were actually exposed before grading
  the corresponding behavior; a missing-fixture case is inconclusive, not a
  pass or a reason to change the skill;
- isolate runs from previous outputs and temporary artifacts;
- compare observable decisions and outputs, not preferred wording; unchanged
  legitimate cases matter alongside the newly corrected failure;
- avoid hidden access to the proposed fix;
- ask before tests that could be slow, costly, destructive, or externally mutating.

If observation is unavailable, use static prediction and state that limitation.
When the host exposes no routing trace, distinguish an agent's reported skill
selection from independently observed discovery or file-reading events. Record
any corrected probe and rerun it in a fresh context without prior conclusions.

## Record results

Use a compact record:

| Case (exact request or fixture) | Expected primary | Expected companions | Selection to avoid | Surface | Method | Context | Comparison | Result | Failure class | Residual risk |
|---|---|---|---|---|---|---|---|---|---|---|

Use `N/A` where a routing field does not apply to a structure, instruction behavior, or resource execution case.

Classify failures as one or more of:

- `trigger-recall`: should activate but does not;
- `trigger-precision`: activates on adjacent work;
- `collision`: competing skills lack a clear boundary;
- `workflow`: instructions permit shortcuts or ambiguous order;
- `resource`: required file, script, or dependency is missing or stale;
- `execution`: a script or tool workflow fails or produces the wrong side effect;
- `portability`: behavior assumes an undeclared host or repository;
- `evidence`: the claimed result is stronger than the validation performed.

Summarize prompts, evidence, passes and failures, changes made because of validation, and residual risk.

## When to skip

Skip activation and instruction behavior cases only when the change leaves trigger surface, scope, workflow meaning, resources, dependencies, and runtime assumptions unchanged. Still run available structure checks for edited packages.
