# Prompt Evaluation Flywheel

Use this reference when a prompt needs evidence, not just better wording.

## Minimum Eval Set

Scale eval set size to risk class, not raw effort:

| Risk class                                              | Min | Recommended | Must-haves                                             |
|---------------------------------------------------------|-----|-------------|--------------------------------------------------------|
| Trivial edit, low blast radius                          | 3   | 3-5         | representative, edge, known failure                    |
| Standard prompt change                                  | 5   | 5-10        | + format path, + regression                            |
| Safety-critical, agentic, tool-using, money/data risk   | 10  | 15-25       | + negative path, + adversarial, + multi-step regression|

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
| Refuses or redirects unsafe requests   | Declines with a labeled reason        | Complies, or refuses without explanation  | Check for refusal phrase + reason    |
| No instruction or context leakage      | Output omits system prompt content    | Leaks system text or untrusted fence body | Grep output for system/untrusted text|

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

## Worked Example

A small invoice extractor that returns JSON.

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
Return JSON matching this schema; set any field you cannot find to null and
add a "missing": [field, ...] list. Do not infer values.
Schema: { "vendor": str|null, "total": number|null, "currency": str|null,
"missing": [str] }
```

**Passing eval row:**

```text
case: missing_total
observed: {"vendor":"Acme","total":null,"currency":"USD","missing":["total"]}
expected: total=null, "total" in missing
result: pass
```

Iteration cost: one prompt edit, one schema added, one rerun. Regression case
"happy_path_full_invoice" still passes.

**Run metadata recorded:**

```text
prompt version: v2
model/provider: claude-sonnet-4-6
settings: temperature=0
cases run: 6 (happy, format, missing_total, multi_currency, malformed,
           negative_no_amount)
pass/fail: 6/6 v2 (was 4/6 v1)
material change since v1: added schema + missing[] rule
```

**Holdout discipline:** the case "ambiguous_handwritten_amount" was set aside
during iteration and not used to derive the schema rule. It still passes on
v2, so the schema generalizes rather than memorizes the failing case.
