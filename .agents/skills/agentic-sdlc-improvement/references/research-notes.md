# Research transfer notes

These independently written notes connect research mechanisms to this workflow.
They are maintenance references, not evidence that this skill improves a user's
development outcomes. No external implementation, benchmark, or paper text is
bundled. The source versions below were reviewed on 2026-11-01; later versions
may change claims. Implementation choices remain hypotheses until evaluated.

## Dream-RSI

[Dream-RSI: Recursive Self-Improvement through Evolving Worlds, v1](https://arxiv.org/html/2609.14858v1)
uses recorded discovery trees as replay environments for selecting exploration
policies. Replay exposes only already revealed history, not outcomes of unexplored
branches. Its evidence supports selective historical screening followed by fresh
evaluation. It does not justify loading every past trace into ordinary tasks.
Reported efficiency depends on the comparison: the largest headline comparison
changes models, and directional advice hurt one evaluated setting. Replaying
recorded evidence cannot establish performance on an unseen branch or live task.

Workflow transfer: preserve useful ancestry, artifacts, outcomes, and costs;
retrieve relevant failed and successful attempts before repeating an intervention.
Use replay to screen a hypothesis, then verify it on fresh analogous cases.

## Survey of recursive self-improvement

[Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops, v2](https://arxiv.org/html/2607.07663v2)
distinguishes output, model, evaluator, and research-process improvement. The
original unversioned abstract link resolved to v2. The survey ranks formal
verification, execution feedback, learned judges, and intrinsic signals as
increasingly weak grounding; the claimed association with improvement is a
qualitative synthesis, not a measured law. Its sampled, recent arXiv corpus and
single-annotator classification limit general conclusions. Passing tests still
underdetermines correctness, and an honest loop can optimize the wrong objective.

Workflow transfer: prefer external observable checks, calibrate judges, retain
counterexamples, and keep objective selection and authority outside the candidate.
Do not equate repeated reflection or more iterations with learning.

## Regularized harness evolution

[RRSI: Regularized Recursive Self-Improvement of Agent Harnesses, v3](https://arxiv.org/html/2609.24972v3)
combines constrained edits, accepted/rejected history, exploration at plateaus,
screening for benchmark-specific changes, noise-aware selection, and pruning.
Its results motivate controlling complexity and measuring transfer beyond the
optimization cases. They do not establish a universal edit count or stopping
schedule. Reported token savings compare against unregularized evolution;
the improved harness can still cost more than the original baseline. Architecture
and search settings bound the evidence.

Workflow transfer: change a small meaningful unit, inspect suspicious rubric
leakage, preserve a validated incumbent, and evaluate the quality/cost tradeoff.
Prune obsolete instructions only when comparison supports the removal.

## Awesome RSI

[Awesome RSI](https://github.com/theseus-labs-rsi/awesome-rsi)
is a maintained discovery map, reviewed on 2026-11-01, rather than an experimental
validation source. Its organization helps identify mechanisms that turn experience
into modifications, verification, retention, and reuse. Autonomy or recursion
labels do not establish reliability, applicability, or comparative quality.

Workflow transfer: follow promising entries to primary evidence and inspect
version, evaluator, editable surface, cost, and failure modes. Do not install an
entire framework or copy its claimed improvement into a skill's acceptance record.

## Modular harness evolution

[ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement, v2](https://arxiv.org/html/2609.14857v2)
separates loop, tools, observation, context, and completion modules. It compares
successful and failed trajectories on the same tasks, develops modules with
separate lineage, and checks their integration. Its reported comparisons favor
modular evolution over joint/unrestricted editing in the tested setting. Repeated
evaluations and task-bootstrap intervals strengthen that setting's evidence;
cross-model transfer remains limited. A small sampled runtime gate is a smoke
check, not sufficient evidence of generalization or safe promotion.

Workflow transfer: use contrastive traces to locate the owning decision, distinguish
infrastructure from behavior, edit the responsible module, then verify affected
interactions and protected behavior. Do not impose the paper's five-module
architecture on an unrelated skill collection.

## Model and harness co-evolution

[When Harnesses Evolve, Which Models Should Follow?, v1](https://arxiv.org/html/2610.25078v1)
archives harnesses and model checkpoints, reuses historical pairings, and promotes
validated outcomes. Interface-mismatch diagnostics track malformed outputs,
unsupported calls, and contract violations. These diagnostics neither measure
all capability mismatch nor establish its causal contribution to success. Results
span specialized domains and combine harness evolution with full-parameter model
training; they cannot establish equivalent gains from changing Markdown skills.
Small quoted API expenditure is not total training cost.

Workflow transfer: record the skill/model/tool pairing, preserve working prior
versions, and retest relevant cases after drift. Treat valid tool calls as one
diagnostic alongside actual task success. Model training or checkpoint merging
is outside this skill's ordinary workflow.

## Improving the harness improver

[RSI-Harness: Optimizing the Harness Optimizer via Recursive Self-Improvement](https://openreview.net/pdf?id=EOrtreQLbv)
was reviewed as a 29-page anonymous ICLR 2027 submission under review. It separates
task-harness edits from edits to the improver, using successful and failed search
history. Its key comparison starts alternative improvers from matched harnesses,
history, tasks, and resources, then measures the resulting task performance.
The evaluator and acceptance machinery remain fixed outside the mutable state.
Some strongest-baseline average confidence intervals cross zero; the validation
audit reports false acceptance. Source code was promised rather than available
with the inspected submission. These limits preclude unconditional promotion.

Workflow transfer: investigate the improver only when its own failures justify
it, use matched frozen starts, and evaluate downstream changes. Do not copy the
paper's fixed outer-loop cadence or a positive-score gate as a universal rule.

## Additional skill-specific source

[Meta Context Engineering via Agentic Skill Evolution, ICML 2026 / PMLR 306](https://proceedings.mlr.press/v306/ye26g.html)
is an additional source, not the OpenReview submission above. It separates the
procedure for constructing context from the context artifacts it produces,
aggregates evidence across batches, and restructures context rather than only
appending rules. Its online setting uses fixed skills or no skill; it does not
demonstrate online skill evolution. The paper limits applicability for
reasoning-intensive work and long complex trajectories, and uses small benchmark
subsets. Its results do not establish a universal preference for short context.

Workflow transfer: permit consolidation, selective retrieval, and unchanged
guidance as outcomes. Judge revised skills through the behavior of agents using
them; a more elaborate procedure or larger library is not itself an improvement.
