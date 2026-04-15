---
name: tester-mindset
description: Testing mindset skill for context-driven test strategy, exploratory
  testing, validation design, acceptance criteria, oracles, weak-test detection,
  edge cases, heuristics, checklists, and evidence review for code, products,
  plans, or claims. Use when the user asks what to test, how to test, whether
  evidence is enough, or to bring a tester mindset. Do not use for merely running
  an existing test command.
---

# Tester Mindset

A test is a small, deliberate meeting with consequence, arranged so truth can
arrive before ruin does.

Use this as an orthogonal workflow skill. Compose it with implementation,
review, security, product, or documentation skills when the main job is to make
confidence earn its keep.

## When To Use

- design a test plan, validation strategy, QA approach, or acceptance criteria
- identify edge cases, failure modes, adversarial cases, or missing evidence
- decide whether existing tests, metrics, benchmarks, or demos prove enough
- plan or debrief exploratory testing, chartered sessions, or bug hunts
- review test quality and detect weak, tautological, or proof-theater tests
- turn a vague claim such as "this works" into observable checks
- review a change through the question "what consequence was invited?"

## Not For

- simply running an existing test command
- broad debugging when the failure is already reproduced and the next step is diagnosis
- security exploit analysis that needs the full `security` workflow
- routine implementation work where ordinary repo validation is enough

## Core Workflow

1. **Map the context.**
   Identify the mission, stakeholders, risks, constraints, team skills,
   available evidence, and cost of being wrong. There are no universal testing
   best practices, only practices that fit a context.
2. **Name the claim.**
   State the belief being tested in falsifiable language. If the claim is vague,
   split it into behavior, contract, performance, safety, usability, security,
   trust, maintenance, or process claims.
3. **Separate testing from checking.**
   Checking applies explicit pass/fail rules to known expectations. Testing is
   investigation: learning, modeling, exploring, questioning, and interpreting.
   Automate checks, but do not pretend automation replaces judgment.
4. **Invite consequence.**
   Ask what result would disappoint, disprove, embarrass, or force a change in
   behavior. If no outcome can change the conclusion, this is a ritual, not a
   test.
5. **Choose a survivable scale.**
   Make the test strong enough to teach and small enough to survive. Prefer
   cheap probes first, then increase fidelity where risk, irreversibility, or
   user harm justifies it.
6. **Choose oracles deliberately.**
   Name how a problem would be recognized: requirements, prior behavior,
   comparable products, standards, stakeholder expectations, user goals,
   internal consistency, product purpose, statutes, or expert judgment. Treat
   every oracle as fallible.
7. **Inspect the apparatus.**
   Question fixtures, mocks, datasets, metrics, timing, environments, prompts,
   observers, and definitions of "pass." A failing test may expose a broken
   question, not only a broken system. Ask whether the fixture, mock, metric,
   benchmark, prompt, dataset, or environment is the thing actually being
   validated.
8. **Let reality disagree.**
   Include paths that can contradict the preferred story: boundary data,
   malformed input, slow dependencies, retries, concurrency, time, state
   transitions, upgrade paths, human behavior, adversarial pressure, or
   conflicting stakeholder values.
9. **Interpret narrowly.**
   Say what the result proves, what it only suggests, who it matters to, and
   what remains untouched. Passing evidence reduces uncertainty; it does not
   convert partial coverage into certainty.
10. **Choose the next consequence.**
   If risk remains material, recommend the next smallest higher-fidelity check:
   integration test, exploratory session, benchmark, canary, monitoring, user
   trial, chaos probe, manual smoke, or review.

## Context Map

Use this quick scan before recommending tests:

- **Mission:** What are we trying to learn or protect?
- **Stakeholders:** Who matters, and what does quality mean to them?
- **Risk:** How likely is failure, how costly is it, and how visible is it?
- **Constraints:** Time, budget, access, tools, environments, compliance, and skills.
- **Product factors:** Structure, Function, Data, Interfaces, Platform, Operations, Time.
- **Evidence so far:** Existing checks, exploratory notes, production telemetry,
  bug history, user reports.
- **Unknowns:** What would still surprise us if this passed?

## Consequence Types

Use these categories to make vague confidence concrete:

- **correctness:** wrong output, broken contract, data loss, or invalid state
- **safety:** user harm, irreversible action, unsafe default, or bad recovery
- **performance:** latency, throughput, memory, battery, cost, or degradation
- **usability:** confusion, failed task, inaccessible path, or poor feedback
- **security:** unauthorized access, data exposure, tampering, or abuse path
- **trust:** misleading result, broken promise, weak audit trail, or bad handoff
- **maintenance:** brittle change, unclear ownership, migration pain, or drift

## Test Idea Heuristics

Use heuristics as fallible lenses, not scripts to exhaust:

- **Boundaries:** zero, one, many, min/max, just below/above, empty, null, huge, duplicate.
- **Data:** Unicode, RTL text, whitespace, special characters, malformed payloads, stale data.
- **State:** skipped steps, back button, retry, undo/redo, double submit, timeout, expired session.
- **Interfaces:** APIs, DBs, queues, auth providers, file systems, browsers, devices, humans.
- **Operations:** install, deploy, migrate, recover, observe, rollback, support, maintain.
- **Time:** concurrency, ordering, scheduling, DST, leap days, long-running
  sessions, race conditions.
- **Tours:** money path, bad-neighborhood, historical, landmark, data-flow,
  all-nighter, garbage tour.

## Exploratory Sessions

Use a charter when scripted checks are too narrow or unknowns matter.

Charter format:

```text
Explore <target>
with <resources, tools, data, or conditions>
to discover <information, risks, or surprises>
```

Session discipline:

- Take notes during the session, not after.
- Tag findings as `BUG`, `QUESTION`, `IDEA`, `RISK`, or `NOTE`.
- Pause on anomalies: reproduce, vary conditions, collect evidence, assess impact.
- Debrief with what was covered, what was not covered, what surprised you, and what follows.
- Convert reproducible exploratory findings into automated regression checks
  when the behavior is stable and the oracle is clear.

## Perspective Rotation

When the test strategy is contentious, high-risk, or stuck, rotate perspectives:

- **Facts:** What evidence, metrics, coverage, incidents, and constraints do we know?
- **Feelings:** What makes the team uneasy or confident, without forcing justification?
- **Risks:** What could go wrong, where are the gaps, and what assumptions could fail?
- **Strengths:** What is already working and can be leveraged?
- **Ideas:** What alternative probes, tools, charters, or checks could reveal more?
- **Process:** What action, owner, stop condition, and next review point follow?

## Weak Test Detector

Reject tests that cannot meaningfully fail for the right reason.

Before writing or approving test code:

- Read the requirement or acceptance criteria.
- Read the implementation or behavior under test.
- Select a technique: equivalence partitioning, boundary values, decision table,
  state transition, error category, or exploratory charter.
- Enumerate cases before writing code.
- Use Arrange, Act, Assert for executable tests.
- Self-verify: would this fail if the production behavior were genuinely broken?

Forbidden patterns:

- tautological assertions such as `expect(true).toBe(true)`
- self-referential assertions such as `expect(x).toBe(x)`
- truthiness-only assertions where specific values matter
- empty tests, commented-out assertions, or tests with no production call
- mocking the system under test instead of only external boundaries
- schema-success-only assertions that do not verify parsed or computed data
- literal roundtrips that only prove the test built its own fixture

## Heuristics And Checklists

- Use heuristics for decisions under uncertainty; validate them against outcomes.
- Use checklists for error-prone procedures with critical steps.
- Keep checklists short: critical skipped-often steps only.
- Use `READ-DO` for unfamiliar or irreversible procedures.
- Use `DO-CONFIRM` for expert routine procedures.
- Prefer forcing functions over reminders when a critical check can be automated.
- Revisit heuristics and checklists when the environment changes.

## Evidence Ladder

- Use unit checks for stable pure behavior and fast feedback.
- Use integration checks for collaboration contracts and real boundaries.
- Use end-to-end or smoke checks sparingly for critical user journeys.
- Use exploratory sessions when the unknowns matter more than repeatability.
- Use monitoring, canaries, synthetic checks, or staged rollout when time,
  scale, or production context is the real risk.

## Decision Rules

- Test claims and contracts before testing implementation details.
- Treat hard-to-test behavior as design feedback; refactor coupling before
  mocking everything.
- Name executable tests as behavior specifications, not implementation details.
- Prefer pressure with fidelity: too little pressure teaches nothing, the wrong
  pressure teaches the wrong lesson.
- Treat coverage, green checks, dashboards, and sign-off as evidence, not truth.
- Prefer real boundaries over mocks when the risk lives in integration,
  serialization, time, identity, permissions, or external behavior.
- Add adversarial and negative cases when failure would be costly, silent, or
  exploitable.
- Scale effort to blast radius, reversibility, novelty, and user harm.
- Name what is excluded from the room: time, data diversity, production traffic,
  user incentives, hardware, network behavior, organizational incentives, or
  maintenance burden.
- Avoid proof theater: tests designed to preserve confidence rather than risk it.
- Prefer clarity over coverage; coverage says what ran, not what was understood.
- Do not hide uncertainty behind procedure. The danger is a closed room calling
  itself evidence.

## Stopping Rule

Stop when the claim has risk-appropriate evidence, remaining uncertainty is
named, and the next check would cost more than the confidence it can reasonably
add. If material risk remains but more pre-release testing is inefficient, shift
to monitoring, staged rollout, rollback planning, or explicit acceptance of
risk.

## Useful Questions

- What consequence is this test actually inviting?
- Is the scale large enough to teach, but small enough to survive?
- What kind of reality is excluded from the room?
- Who or what is allowed to disagree?
- Which oracle says this is a problem, and how could that oracle mislead us?
- What would this passing result still not prove?
- Is this testing, checking, or proof theater?
- What should we automate, and what still needs human investigation?

## Output Shape

For a testing recommendation, keep the structure compact:

```markdown
## Context
Mission, stakeholders, risks, constraints, and evidence so far.

## Claim
What belief or contract is being tested.

## Consequence
What result would change our mind or behavior.

## Oracles
How problems will be recognized, and where those oracles are fallible.

## Tests Or Probes
Concrete checks, exploratory charters, or experiments ordered from cheapest
credible probe to higher-fidelity evidence.

## Apparatus Risks
Where mocks, data, metrics, environments, prompts, or definitions could mislead us.

## Remaining Uncertainty
What passing still would not prove, and the next consequence to invite if needed.
```

## Examples

- "Bring a tester mindset to this checkout refactor." -> identify stakeholders,
  contracts, risks, oracles, integration boundaries, weak tests, and a validation ladder.
- "Do these benchmarks prove the new parser is faster?" -> inspect workload,
  measurement setup, excluded cases, metric incentives, and remaining uncertainty.
- "Does this rollout plan have enough evidence?" -> identify trust, adoption,
  reversibility, monitoring, rollback, and excluded real-world conditions.
- "Plan exploratory testing for the billing flow." -> write charters, choose
  heuristics, time-box sessions, define notes, and decide what findings become checks.
- "Review these tests for slop." -> reject tautologies, no-production-call tests,
  truthiness-only assertions, mock-the-SUT patterns, and tests that cannot fail usefully.
- "What tests should cover this password reset flow?" -> compose with
  `security` when exploit paths and identity boundaries are the main risk.
