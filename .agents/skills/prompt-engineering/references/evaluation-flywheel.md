# Prompt Evaluation Flywheel

Use this reference when a prompt needs evidence, not just better wording.

## Choose The Eval Set

Choose cases for the behavior at risk. A wording-only edit with unchanged
meaning can use a static comparison. Behavior changes need representative and
known-failure cases; add format, boundary, adversarial, and multi-step cases
when those contracts matter. No fixed count proves adequacy. Broaden until the
material decisions and failure modes have evidence, not until a quota is met.

Capture baseline cases before rewriting. Keep the same input and grading
criteria for comparisons unless an expectation was itself wrong; explain that
correction. Distinguish static predictions from executed cases and do not
report a run, pass rate, or generalization result without its actual evidence.

Categories the cases should cover:

- **happy path:** common representative request
- **format path:** request that stresses output structure
- **edge path:** sparse, ambiguous, large, malformed, or unusual input
- **negative path:** request the prompt should refuse, defer, or handle safely
- **regression path:** known prior failure or bug report

For high-risk prompts, expand cases before expanding prompt complexity.

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

When exact expected output is brittle, grade behavior against a rubric:

| Criterion                              | Pass example                          | Fail example                              | Grader hint                          |
|----------------------------------------|---------------------------------------|-------------------------------------------|--------------------------------------|
| Follows output schema                  | Valid JSON, all required keys present | Missing key, prose around JSON            | Run schema validator                 |
| Includes required fields or decisions  | Names every required field by name    | Omits or merges fields                    | Check key list against spec          |
| Uses source material correctly         | Cites provided IDs verbatim           | Invents IDs or rephrases away from source | String-match cited IDs to inputs     |
| Asks for clarification only when needed| Asks once when input is ambiguous     | Asks on clear inputs or never asks        | Inspect input clarity vs. behavior   |
| Preserves action boundaries | Completes allowed work and declines an unauthorized action | Performs the unauthorized action or blocks legitimate work | Inspect actions and side effects; a refusal phrase alone is insufficient |
| Preserves trust and confidentiality | Uses or quotes authorized source data without obeying embedded commands | Follows an injected command or exposes protected data | Check authority and protected outputs; copying task data is not inherently leakage |

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

## Illustrative Worked Example

A small invoice extractor that returns JSON. All inputs, outputs, and results
below are invented to demonstrate the method; no model execution is claimed.

**Before prompt (v1):**

```text
Extract the invoice fields from the text below and return them.
{{invoice_text}}
```

**Failing eval row:**

```text
case: missing_total
input: invoice text with no total line
observed: "Total: 0.00" (invented)
expected: total field omitted or null, with reason
failure category: weak output contract + missing context for unknowns
```

**Diagnosis:** prompt has no schema and no rule for missing fields, so the
model hallucinates plausible defaults.

**Revised prompt (v2):**

```text
Extract invoice fields from <<invoice>>{{invoice_text}}<</invoice>>.
Return JSON with exactly these fields; set any field you cannot find to null and
add a "missing": [field, ...] list. Do not infer values.
Output shape (type notation): { "vendor": string|null, "total": number|null, "currency": string|null,
"missing": [str] }
```

This is prompt-level type notation, not an executable JSON Schema. When the
caller uses schema-constrained output, supply the equivalent supported schema
through that runtime and validate its response; prompt wording alone is not
format enforcement.

**Passing eval row:**

```text
case: missing_total
observed: {"vendor":"Acme","total":null,"currency":"USD","missing":["total"]}
expected: total=null, "total" in missing
result: pass
```

An actual evaluation would rerun the missing-total case and the existing
"happy_path_full_invoice" regression against the revised prompt.

**Run metadata to record after execution:**

```text
prompt version: v2
model/provider: <actual resolved target>
settings: <actual supported settings>
cases run: <exact case IDs>
pass/fail: <observed outcomes; not run in this illustration>
material change since v1: added schema + missing[] rule
```

**Holdout discipline:** keep a case such as "ambiguous_handwritten_amount"
outside the examples used to revise the prompt. Evaluate it separately;
passing one holdout provides limited evidence, not proof of generalization.
