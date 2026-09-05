# Technical references

Consult these primary sources when investigating the associated workflow
decision. They are optional maintenance references; using either skill does
not require fetching them or installing the authors' tools. The family owns
its procedures and uses the host and repository's available execution surface.

## Delivery and continuity

- [AI-Native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook)
  supports checking lifecycle coverage, artifact ownership, verification, and
  operational feedback. Use those concerns to inspect missing handoffs; its
  document layout and approval schedule are not required project conventions.
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) explains
  explicit control flow, context ownership, compact failure feedback, and
  resumable execution. Consult it for continuity problems without assuming
  that a new runtime, storage system, or agent topology is needed.
- [Memory and compaction](https://developers.openai.com/cookbook/examples/agents_sdk/building_reliable_agents_memory_compaction)
  helps distinguish restoring a particular run from retaining reusable
  knowledge. Use it when diagnosing lost decisions or inappropriate memory;
  accepted task artifacts and persistence authority still govern the work.
- [Iterative repair loops](https://developers.openai.com/cookbook/examples/codex/build_iterative_repair_loops_with_codex)
  provides a concrete repair/evaluate cycle for investigating convergence and
  stopping behavior. Select the repository's checks and resource bound rather
  than assuming the example's iteration schedule establishes reliability.

## Evaluation and workflow improvement

- [Macro evals](https://developers.openai.com/cookbook/examples/partners/macro_evals_for_agentic_systems/macro_evals_for_agentic_systems)
  connects individual traces to patterns across runs. Consult it when deciding
  how to sample evidence or investigate a suspected recurring failure; an
  aggregated pattern still needs attributable supporting examples.
- [Agent improvement loop](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop)
  connects traces, feedback, evaluations, and a proposed workflow change.
  Use it when specifying that comparison; the illustrated SDK, integrations,
  and live execution are optional and require their own authorization.
- [Infrastructure noise in coding evals](https://www.anthropic.com/engineering/infrastructure-noise)
  supports checking resource allocation, timeouts, and environment confounders
  before attributing a result to agent behavior. Its benchmark-specific
  measurements are not universal effect sizes or thresholds.
- [Harness design for long-running applications](https://www.anthropic.com/engineering/harness-design-long-running-apps)
  motivates testable increments, calibrated assessment, and interaction that
  exposes unfinished behavior. Consult it when a polished artifact passes
  inspection but fails in use. A separate evaluator is an option to assess,
  not a mandatory topology or proof of independence.

## Applicability

This selection was reviewed on 2026-09-05. Refresh a provider-specific command,
API, setting, or model claim against current official documentation before
using it. Keep examples and reported research results distinct from this
family's own observed validation; neither a citation nor a described workflow
establishes measured improvement on the user's task.
