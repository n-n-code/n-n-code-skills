---
name: prompt-engineering
description: Prompt engineering workflow for designing, rewriting, debugging, evaluating, and optimizing LLM prompts, system prompts, developer prompts, few-shot examples, structured-output instructions, tool-use prompts, and prompt eval cases. Use when prompt behavior, reliability, safety, cost, latency, or model fit is the main task. Do not use for generic prose editing, model selection alone, or ordinary documentation work with no prompt artifact.
---

# Prompt Engineering

Treat prompts as small behavioral specs. Improve them by naming the job,
testing the behavior, changing one important thing at a time, and preserving
the prompt's operating context.

## Core Workflow

1. **Scope the prompt job.**
   Identify the target model or provider, audience, runtime surface, inputs,
   tools, output contract, constraints, and where the prompt will live. If the
   prompt belongs to a repo, inspect existing prompts, schemas, examples,
   tool definitions, evals, logs, and docs before asking avoidable questions.
2. **Define success before rewriting.**
   State the desired behavior, hard requirements, acceptable variation, known
   failure modes, and evidence that would prove the prompt improved. If success
   is vague, turn it into 3-7 concrete cases before editing.
3. **Choose the lightest pattern that fits.**
   Use direct instructions for simple tasks, structured sections for context
   control, few-shot examples for format or judgment calibration, schemas for
   machine-readable output, tool-use instructions for action boundaries, and
   repetition only when the model repeatedly drops critical constraints.
4. **Draft with clean boundaries.**
   Put task, context, constraints, examples, tools, and output format in
   separate labeled sections. Delimit user-controlled or retrieved content
   clearly. Keep stable instructions before variable content when prompt
   caching, reuse, or maintainability matters.
5. **Evaluate against reality.**
   Test representative, edge, adversarial, and regression cases. Compare outputs
   against explicit criteria instead of intuition. Record which failures changed
   and which remained.
6. **Iterate deliberately.**
   Change one major variable at a time: instruction wording, context ordering,
   examples, output schema, tool contract, reasoning guidance, or model
   settings. Preserve the previous prompt and test cases until the new version
   wins on the target criteria.
7. **Ship the prompt with evidence.**
   Return the final prompt, assumptions, changed behavior, eval cases, expected
   outputs or grading criteria, remaining risks, and any provider-specific
   settings the caller must preserve.

## When To Use

- design, rewrite, debug, or review an LLM prompt
- create or revise a system prompt, developer prompt, tool-use prompt, few-shot
  examples, structured-output instruction, grader prompt, or prompt eval set
- investigate why a prompt is unreliable, unsafe, too costly, too slow, or
  mismatched to a target model
- optimize an existing prompt while preserving behavior and evidence

## Not For

- model selection alone
- generic prose editing, README writing, marketing copy, or voice matching
- ordinary LLM integration code when the prompt behavior is not the main issue
- security review where data exposure, authorization, tenant isolation, or tool
  abuse is the central risk

## Compose With

- Use a provider documentation workflow when the prompt depends on current model,
  API, structured-output, tool-calling, reasoning, caching, or pricing behavior.
- Add a testing workflow when the main job is test strategy, evidence quality,
  grading design, or acceptance criteria rather than prompt wording.
- Add a security workflow when prompt injection, hidden instruction leakage,
  unsafe tool use, data exposure, or trust boundaries dominate the risk.

## Prompt Design Rules

- Put the user's real task first; do not optimize a prompt before the objective
  and failure mode are clear.
- Prefer explicit success criteria over broad "be better" instructions.
- Separate stable policy from per-request data and untrusted content.
- Specify output shape with examples or schemas when downstream code depends on
  structure.
- Use examples that demonstrate decisions, not examples that merely repeat the
  instruction.
- Include negative and boundary cases when failure would be costly, silent, or
  hard to notice.
- Keep prompts short enough to maintain; move large context to retrieval,
  tools, files, or references when possible.
- Verify current official provider guidance before making model- or API-specific
  claims. Do not rely on memory for rapidly changing model behavior.
- Treat provider guidance as conditional. Load provider notes only when the
  target model, API, or runtime surface makes them relevant.

## Failure Diagnosis

When a prompt fails, classify the failure before rewriting:

- **missing context:** the model did not receive facts it needed
- **ambiguous instruction:** multiple reasonable outputs satisfy the prompt
- **weak output contract:** format, fields, or refusal behavior are underspecified
- **bad examples:** examples teach the wrong pattern or conflict with rules
- **context collision:** retrieved, user, or tool content overrides intent
- **tool boundary drift:** the model calls tools too early, too late, or with bad arguments
- **model mismatch:** the prompt assumes capabilities, settings, or reasoning behavior the model does not provide
- **evaluation gap:** the prompt looks better on anecdotes but fails representative cases

## Output Shapes

For a prompt rewrite:

```markdown
## Final Prompt
...

## What Changed
...

## Eval Cases
...

## Assumptions And Risks
...
```

For prompt debugging:

```markdown
## Diagnosis
Failure category and evidence.

## Revision
Changed prompt section or full prompt.

## Validation
Cases that should pass, fail, or remain uncertain.
```

## Reference Map

- [patterns-and-provider-notes.md](references/patterns-and-provider-notes.md) -
  prompt patterns, source synthesis, and provider-specific notes.
- [evaluation-flywheel.md](references/evaluation-flywheel.md) - lightweight
  prompt eval design, iteration, and grading workflow.
- [trigger-evals.md](references/trigger-evals.md) - positive and negative
  trigger checks for this skill.
