# Sources and adaptations

Research basis reviewed on 2026-09-05. These sources informed an original
procedural synthesis; this package does not bundle their articles, code,
notebooks, or runtime integrations. Source examples are evidence for design
choices, not requirements imposed on every repository.

Read this file when maintaining the family. Routine delivery does not require
fetching the bibliography. Recheck current official documentation before using
provider-specific APIs, settings, models, or commands. Research/source inspection
does not establish executed SDK examples, agent reliability, or cross-host
installation compatibility.

## Baseline sources

1. [OpenAI: Building an AI-native engineering team](https://cdn.openai.com/business-guides-and-resources/building-an-ai-native-engineering-team.pdf)
   (20-page guide). **Adopt:** lifecycle coverage from planning and design through
   implementation, testing, review, documentation, and operations; explicit human
   ownership and tool-backed results. **Adapt:** stage-specific delegation to
   existing task authority. Capability horizons and customer anecdotes are not
   completion guarantees or universal productivity targets.

2. [HumanLayer: 12-Factor Agents](https://github.com/humanlayer/12-factor-agents).
   **Adopt:** explicit control flow, owned prompts/context, compact failure
   feedback, resumability, and focused work. **Adapt:** preserve enough recorded
   state to resume without requiring a particular storage architecture. The
   production-agent patterns inform coding workflow decisions; they do not
   require constructing a new agent runtime or using multiple agents.

3. [Anthropic: The AI-Native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook)
   (2026-08-21). **Adopt:** connected lifecycle stages, authoritative artifacts,
   verification, operational feedback, and explicit action boundaries. **Adapt:**
   reuse existing artifacts and risk-based authority. Do not impose its document
   tree, stage approvals, hook examples, blanket ban on test edits, or statistical
   monitoring bands as portable requirements.

## Evaluation and recovery

4. [OpenAI: Macro Evals for Agentic Systems](https://developers.openai.com/cookbook/examples/partners/macro_evals_for_agentic_systems/macro_evals_for_agentic_systems)
   (2026-05-19). **Adopt:** separate per-run findings from recurring patterns and
   inspect underlying traces before an intervention. **Adapt:** manual analysis
   for small samples. Its synthetic EV workflow, clustering stack, and upstream
   suspect rankings do not prove causes or require those tools.

5. [OpenAI: Build an Agent Improvement Loop with Traces, Evals, and Codex](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop)
   (2026-05-12). **Adopt:** connect traces, attributable feedback, repeatable evals,
   and a concrete improvement handoff. **Adapt:** proposals and authorized edits
   are separate activities. The financial example, Agents SDK, HALO, Promptfoo,
   live calls, and deeper automation remain optional implementation choices.

6. [OpenAI: Build iterative repair loops with Codex](https://developers.openai.com/cookbook/examples/codex/build_iterative_repair_loops_with_codex)
   (2026-05-11). **Adopt:** review, focused repair, observed validation, and the
   remaining delta; stop for success, bounds, stagnation, or required judgment.
   **Adapt:** discover project checks instead of copying notebook execution or a
   fixed three-pass schedule. The example's designed progression is not measured
   convergence of this skill.

7. [Anthropic: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
   (2026-03-24). **Adopt:** testable increments, calibrated assessment, and live
   interaction that exposes unfinished behavior. **Adapt:** separate evaluation
   when it adds evidence; record its cost and independence. Do not require its
   planner/generator/evaluator topology, expanded product scope, grading weights,
   or reset schedule. Its comparisons motivate experiments, not universal gains.

8. [Anthropic: Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise)
   (2026-02-05). **Adopt:** document resource allocation, limits, timeouts, and
   other confounders; distinguish infrastructure errors from behavior failures.
   **Adapt:** match conditions before attributing a small difference. Its
   benchmark-specific resource multipliers and score ranges are not general
   thresholds for this family.

## Context, continuity, and reusable procedures

9. [OpenAI: Iterating Development Workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex)
   (2026-08-03). **Adopt:** separate outcomes, execution guidance, phase context,
   and observed progress. **Adapt:** use existing repository conventions and
   compact records. Its optional `GOALS.md`, `PLANS.md`, `PROMPTS.md`, and harness
   directory are not host requirements or mandatory artifacts here.

10. [OpenAI: Building Reliable Agents with Memory and Compaction](https://developers.openai.com/cookbook/examples/agents_sdk/building_reliable_agents_memory_compaction)
    (2026-05-01). **Adopt:** distinguish continuity within a run from reusable
    lessons across runs; preserve provenance and uncertainty. **Adapt:** accepted
    task artifacts retain authority. Do not store case-specific conclusions as
    general memory or require the notebook's sandbox SDK and workspace layout.

11. [OpenAI: Automating repetitive work at OpenAI with Codex](https://developers.openai.com/blog/automating-repetitive-work-at-openai-with-codex)
    (2026-08-25). **Adopt:** retain commands, outcomes, dead ends, and reasons that
    make the next run easier. **Adapt:** use existing work records. Runme,
    WebMCP, Google Drive, and the author's approval cadence are examples rather
    than dependencies or automatic permission to persist information.

12. [OpenAI: Shell + Skills + Compaction](https://developers.openai.com/blog/skills-shell-tips)
    (2026-02-11). **Adopt:** precise routing, adjacent negatives, selective
    references, and continuity for long work. **Adapt:** discover the available
    host and artifact boundary. Explicit skill invocation reduces selection
    ambiguity but does not make execution deterministic. Hosted shell paths and
    networking configuration are outside the portable contract.

## Runtime interfaces and product feedback

13. [OpenAI: Codex as a platform](https://developers.openai.com/blog/codex-as-a-platform)
    (2026-08-19). **Adopt:** distinguish workflow policy and records from the
    execution harness and its tools. **Adapt:** use an existing runtime with
    available capabilities. Choosing SDK, CLI, or app-server integrations and
    building their infrastructure remain separate implementation tasks.

14. [OpenAI: From prompts to products: One year of Responses](https://developers.openai.com/blog/one-year-of-responses)
    (2026-03-11). **Context:** developer examples connect behavior monitoring,
    contextual investigation, and improvement. **Adapt:** keep context preparation
    and judgment separately owned when useful. The product stories do not
    establish universal architecture, model, or provider requirements.

15. [OpenAI: Building games with Astra](https://developers.openai.com/blog/how-to-build-games-with-astra)
    (2026-09-04). The supplied URL repeated itself; this is the corrected page.
    **Adopt:** start from the intended experience, inspect meaningful state, use
    repeatable scenes, and test real journeys separately from prepared scenes.
    **Adapt:** distinguish visual, simulation, and device evidence. Rendering
    measurements and game-specific tools do not generalize to production hardware.

16. [Anthropic: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)
    (2026-04-08). **Adopt:** separate durable session evidence, current context,
    control flow, and execution capability; re-examine assumptions after upgrades.
    **Adapt:** records support recovery without prescribing infrastructure. Its
    service architecture and credential isolation are not capabilities a skill
    file can itself enforce.

17. [Anthropic: Persona vectors](https://www.anthropic.com/research/persona-vectors)
    (2025-08-01). **Context only:** the research studies internal model activations
    and behavioral changes. Our evaluation cases inspect observable unsupported
    claims and unwarranted agreement. That is an engineering hypothesis to test,
    not implementation of persona-vector measurement or control. No internal
    model access, personality diagnosis, or steering capability is claimed.

## Deliberate synthesis choices

- Preserve one authoritative owner per artifact while making useful progress
  visible; neither a monolithic context window nor a new database is mandated.
- Keep human accountability with risk-based action authority; do not reproduce
  every approval step from a vendor's organizational example.
- Preserve oracle integrity while allowing evidence-backed test corrections.
- Use existing tools for trustworthy feedback. Extra agents, larger contexts,
  resets, and more iterations require demonstrated value and adequate bounds.
- Keep source-specific mechanisms outside the core. Evaluate behavior in the
  actual host and repository before making stronger portability or quality claims.
