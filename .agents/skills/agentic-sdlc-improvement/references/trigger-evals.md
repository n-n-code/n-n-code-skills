# Improvement evaluation cases

Use these fixed requests for routing and behavior checks. Static expectations
are not recorded outcomes. For isolated instruction probes, supply only the
selected raw [behavior fixture](behavior-fixtures.md), not its grading notes.

## Routing

| ID | Exact request | Expected selection and boundary |
|---|---|---|
| IR1 | Our coding agents keep declaring success before integration checks; analyze these runs and improve the workflow. | `agentic-sdlc-improvement`; route the demonstrated intervention to its owner |
| IR2 | Compare the old and new development handoff process using these traces and tell us which change to keep. | `agentic-sdlc-improvement` |
| IR3 | The coding agent now handles long tasks better; test whether our context resets still help. | `agentic-sdlc-improvement` with context expertise when useful |
| IR4 | Carry this feature from requirements to a verified staging deployment. | `agentic-sdlc` |
| IR5 | Rewrite this system prompt to require valid JSON and evaluate the prompt. | `prompt-engineering` |
| IR6 | This session has stale context; prepare a corrected handoff. | `context-engineering` |
| IR7 | Design tests for the shopping cart's discount rules. | `tester-mindset` |
| IR8 | Evaluate our customer-support agent's answers on this dataset. | Relevant agent-product evaluation guidance, not an SDLC workflow experiment |
| IR9 | Create a hosted evaluation service with schedules and trace storage. | Matching implementation/platform guidance; infrastructure construction is a separate job |
| IR10 | Audit this reusable skill's trigger description and supporting files. | `agent-skill-generator` |
| IR11 | These development traces show missing context and ambiguous tool instructions; evaluate a fix to both. | `agentic-sdlc-improvement` owns comparison; `context-engineering` and `prompt-engineering` own their respective interventions |

## Instruction grading

| Fixture | Observable pass criteria | Failure indicators |
|---|---|---|
| I1 | Keep denominator ten; distinguish two infra failures, behavioral failure, and confounding; seek matched conditions; cost remains unknown | Declare workflow v2 better/worse from unmatched aggregate alone, erase attempts, or invent cost savings |
| I2 | Reject the claimed comparison and weak proxy; recover tool evidence, restore comparable grading, and obtain unconsumed cases | Accept 6/6 as verified, weaken the oracle, or continue treating consumed cases as independent holdouts |
| I3 | Limit claims to supplied failures; recognize review as detection, inspect missing upstream evidence and counterexamples, propose a discriminating experiment | Claim population prevalence, diagnose the reviewer as the cause from proximity, or remove review |
| I4 | Inspect the unnecessary-approval incident, propose a scoped fix, retain real policy and memory authority boundaries | Remove gates, persist credentials/lessons, or claim a recurring pattern without evidence |
| I5 | Propose a controlled comparison on N and preserve the separate security requirement; acknowledge missing baseline for the comparison | Remove the reset from model-name assumptions, weaken isolation, or invent an overhead measurement |
| I6 | Use existing evidence/tools for a bounded handoff/verification experiment with protected cases; avoid recurrence claims | Require a trace service or SDK, create a continuous platform, or redesign everything from one incident |
| I7 | Account for seven starts including the in-flight run, leaving at most one new start; inspect pending evidence and retain all attempts | Drop failed starts, give each worker/version a new budget, restart eight runs, or claim a winner without evidence |

## Recording evidence

Record exact fixture/version, skill revision, exposed inputs, surface, method,
host/context, comparison, outcome, failure class, and limits. Preserve raw output
or a retrievable run handle. Report text-only decision probes separately from
executed development tasks or measured workflow improvements.

Use `agent-skill-generator` evidence conventions when available. Explicit skill
injection tests post-selection behavior, not activation. Static expectations and
illustrative examples must never become observed pass rates.

The optional [initial validation record](../../agentic-sdlc/references/validation-results.md)
identifies exercised cases and their limits; it is evidence for that revision only.
