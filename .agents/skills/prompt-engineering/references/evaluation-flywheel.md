# Prompt Evaluation Flywheel

Use this reference when a prompt needs evidence, not just better wording.

## Minimum Eval Set

Start with 5-10 cases when practical:

- **happy path:** common representative request
- **format path:** request that stresses output structure
- **edge path:** sparse, ambiguous, large, malformed, or unusual input
- **negative path:** request the prompt should refuse, defer, or handle safely
- **regression path:** known prior failure or bug report

For small prompt edits, 3 cases can be enough: representative, edge, and known
failure. For high-risk prompts, expand cases before expanding prompt complexity.

Keep training examples and eval cases separate. Few-shot examples teach the
model; holdout and regression cases test whether the prompt generalizes. Do not
copy every failing eval into the prompt unless the goal is a narrow rule patch
and the regression risk is understood.

## Case Format

```markdown
## Case: <name>
Input:
Expected behavior:
Must include:
Must not include:
Grading notes:
```

When exact expected output is brittle, grade behavior instead:

- follows the requested output schema
- includes required fields or decisions
- cites or uses the provided source material correctly
- asks for clarification only when needed
- refuses or redirects unsafe requests
- avoids leaking hidden instructions or untrusted context

## Eval Run Metadata

Record enough context to reproduce or compare a run later:

```text
prompt version:
model/provider:
API or runtime surface:
temperature/reasoning/settings:
tools or retrieval sources:
eval date:
cases run:
pass/fail summary:
```

Also record material changes between runs, such as model upgrades, tool schema
changes, retrieval corpus changes, system/developer prompt changes, or grader
prompt changes. Without run metadata, prompt eval results are anecdotes.

## Iteration Loop

1. Run the current prompt against the eval cases.
2. Classify each failure as instruction, context, example, schema, tool, model,
   or eval problem.
3. Pick the smallest prompt change that should fix the highest-value failure.
4. Re-run the affected cases plus at least one regression case.
5. Keep the change only if it improves the target criteria without degrading
   important existing behavior.
6. Preserve at least one holdout case that was not turned into an example or
   rule during the iteration.

## Grading Options

- **Human review:** best when quality, tone, judgment, or safety is nuanced.
- **Exact or schema check:** best when output structure is machine-readable.
- **Rubric grading:** best when outputs vary but requirements are stable.
- **Model-as-judge:** useful for scale, but calibrate with human-reviewed
  examples and watch for grader bias.
- **Production telemetry:** useful after shipping, but do not use live anecdotes
  as the only pre-release evidence for risky prompts.

## Failure Analysis

Record failures in this shape:

```text
case:
observed output:
expected behavior:
failure category:
likely cause:
candidate prompt change:
regression risk:
```

Common causes:

- the instruction is absent, vague, or lower-priority than conflicting context
- the prompt asks for a format but gives examples in a different format
- the model lacks required facts or tool access
- the eval case encodes a hidden assumption not present in the prompt
- the prompt is too broad and optimizes for style instead of behavior
- provider settings or model choice changed between runs

## Stop Conditions

Stop iterating when:

- the prompt passes representative and known-failure cases at risk-appropriate
  quality
- remaining failures are named and accepted, or assigned to a later change
- further edits mostly trade one failure for another
- the next improvement requires product, data, tool, model, or policy changes
  rather than prompt wording

Ship with the eval cases and assumptions so future prompt changes can be
compared instead of rediscovered.
