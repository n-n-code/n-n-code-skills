# Skill quality checklist

Use this after the skill works. Preserve behavior while improving trigger quality, portability, execution reliability, and context cost.

## Problem and scope

- Is the target problem concrete, repeatable, and coherent?
- Are users, target platforms, inputs, outputs, and success criteria clear?
- Are non-goals and adjacent skills distinguishable before the body loads?
- Are temporary authoring decisions kept out of runtime instructions?

## Trigger quality

- Do the platform's active trigger fields front-load the job and likely user language?
- Do they cover obvious requests and paraphrases without summarizing the workflow?
- Do they name negative boundaries where confusion is likely?
- Are stable identifiers preserved unless an explicit migration is requested?
- Were competing skills checked only when they were exposed to or invoked in the current run?
- If a host may shorten descriptions, does the meaningful prefix still route well?

## Workflow quality

- Are steps ordered, imperative, and specific enough for the workflow's risk?
- Does the skill inspect local context before asking discoverable questions?
- Are defaults, decision points, side-effect boundaries, and completion criteria explicit?
- Does the skill avoid forcing read-only modes through mutating steps?

## Packaging and portability

- Is the portable core independent of one host's optional metadata or tools?
- Does `portable` mean host-neutral semantics rather than unsupported universal installability?
- Are named target hosts, minimum package contract, required adapters, and host-specific evidence explicit?
- Are repo-bound or host-enhanced assumptions named and isolated?
- Does each bundled file directly support runtime behavior?
- Are references linked from `SKILL.md` with clear read conditions?
- Are scripts reserved for deterministic, fragile, or repeated execution?
- Are assets output resources rather than documentation in disguise?

## Trust and execution

- Are tools, permissions, network access, authentication, and external writes declared?
- Are secrets excluded from the package?
- Are partial failure, cleanup, and rollback covered when relevant?
- Were representative scripts or tool workflows actually run?
- Are unavailable or unsafe validation steps reported honestly?

## Validation

- Were structure checks run?
- Were activation and post-selection instruction behavior tested separately where both matter?
- Do activation cases avoid naming, injecting, or otherwise preselecting the target skill?
- Were obvious, paraphrased, adjacent-negative, and collision requests considered as applicable?
- Are surface, method, context, and comparison recorded independently?
- Does each case preserve the exact request or fixture needed to reproduce it?
- Are failures classified and residual risk stated?

## Context cost

Optimize in this order:

1. Delete repeated or generic guidance.
2. Compress wording without weakening decisions.
3. Move selectively needed details into references.
4. Replace prose with a checklist when fidelity is unchanged.
5. Remove examples that merely restate rules.

Keep in `SKILL.md` only trigger-bearing metadata, core workflow, critical decisions, resource routing, and examples that resolve ambiguity. Move long primers, catalogs, schemas, variant details, large examples, and discoverable repository facts out of the main file.

Finish by asking what can be deleted with no loss of behavior and whether the active trigger fields still route correctly after trimming.
