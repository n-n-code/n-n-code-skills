# Exploration And Oracle Prompts

Load this reference only when a test strategy needs broader context, exploratory
ideas, or a perspective change. Select relevant lenses; these are prompts, not
mandatory output fields or a checklist to exhaust.

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

## Perspective Rotation

When the test strategy is contentious, high-risk, or stuck, rotate perspectives:

- **Facts:** What evidence, metrics, coverage, incidents, and constraints do we know?
- **Feelings:** What makes the team uneasy or confident, without forcing justification?
- **Risks:** What could go wrong, where are the gaps, and what assumptions could fail?
- **Strengths:** What is already working and can be leveraged?
- **Ideas:** What alternative probes, tools, charters, or checks could reveal more?
- **Process:** What action, owner, stop condition, and next review point follow?

## Useful Questions

- What consequence is this test actually inviting?
- Is the scale large enough to teach, but small enough to survive?
- What kind of reality is excluded from the room?
- Who or what is allowed to disagree?
- Which oracle says this is a problem, and how could that oracle mislead us?
- What would this passing result still not prove?
- Is this testing, checking, or proof theater?
- What should we automate, and what still needs human investigation?
