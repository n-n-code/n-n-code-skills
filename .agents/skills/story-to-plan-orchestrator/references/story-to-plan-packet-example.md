# Compact Story-To-Plan Packet Example

Use this only as a shape reference. A real packet must reflect the current
request, repository evidence, and component contracts.

```markdown
Artifact Type: Preparation Packet
Status: Ready
Reason: None

## Story Card

Artifact Type: Story Card
Status: Ready
Reason: None
Source: conversation

### Title
Separate artifact shape from readiness

### Intent
Format: Task Brief

For maintainers revising story-family skills, when an artifact moves between
clarification, repository scouting, and implementation planning, make its shape
explicit independently from whether the next stage can consume it.

### Feature Definition
Story Cards, Split Story Sets, Repo Context, Implementation Plans, and their
Preparation Packet use the same readiness statuses while retaining distinct
artifact types. This lets maintainers and downstream executors distinguish an
artifact's schema from its ability to advance.

### Acceptance Criteria
- AC-1: Every stage artifact and the Preparation Packet declare `Artifact Type`,
  `Status`, and `Reason` separately.
- AC-2: A coherent Split Story Set can be `Ready` before one slice is selected.
- AC-3: The orchestrator invalidates only outputs affected by a material change.

### Out of Scope
- Compatibility alias skills for retired package names.

### Constraints
- Skill folder names and frontmatter names must match.

### Dependencies and Assumptions
- Dependencies: the repository validator and published skill inventory.
- Assumptions: component skills remain independently usable; the orchestrator
  composes them when they are available together.

### Open Questions
- None

### Validation Notes
- AC-1 and AC-2: inspect the four story-family artifact contracts.
- AC-3: inspect the orchestrator invalidation table.

## Repo Context

Artifact Type: Repo Context
Status: Ready
Reason: None

### Scope and Instructions
- Input source and revision: the ready Story Card above; source `conversation`;
  no stable revision exposed.
- Repository scope: the four story-family skill packages, `README.md`, the
  story-family trigger evaluations, and validator implementation and tests.
- Applicable instructions: `AGENTS.md` requires skill inventory alignment and
  `python scripts/check_skills.py` for skill changes.
- Domain language and decisions: `README.md` owns published family routing;
  `AGENTS.md` requires folder/frontmatter alignment and targeted validation.

### Search Record
- Anchors: `Artifact Type`, `Status`, `Split Story Set`, and `invalidation`.
- Evidence trail: inspected all four story-family skills, README routing, and
  story-family validator invariants.
- Gaps: no observed activation runs; an isolated-host activation run is the
  next lead if host-specific confidence is required, but is not required for
  this static preparation packet.

### Existing Evidence
| Role | Priority | Path | Observed Evidence | Why It Matters | Evidence Strength |
|---|---|---|---|---|---|
| story owner | Primary | .agents/skills/story-clarifier/SKILL.md | Defines Story Card and Split Story Set contracts. | Owns story artifact shape and readiness. | Direct |
| repo-context owner | Primary | .agents/skills/story-repo-scout/SKILL.md | Defines Repo Context evidence and status. | Owns planning evidence. | Direct |
| plan owner | Primary | .agents/skills/story-implementation-planner/SKILL.md | Defines Implementation Plan status and inputs. | Owns plan readiness. | Direct |
| transition owner | Primary | .agents/skills/story-to-plan-orchestrator/SKILL.md | Defines ownership and invalidation tables. | Owns cross-stage state changes. | Direct |
| packet example | Supporting | .agents/skills/story-to-plan-orchestrator/references/story-to-plan-packet-example.md | Demonstrates the current packet schema and file traceability. | Must stay aligned with the contracts it illustrates. | Direct |
| published routing | Supporting | README.md | Publishes story-family ownership, defaults, and composition guidance. | Renames and boundaries must remain discoverable. | Direct |
| trigger evaluations | Supporting | .agents/skills/agent-skill-generator/references/inventory-trigger-evals.md | Contains story-family positive, negative, collision, and state-routing cases. | Provides static routing evidence. | Direct |
| validator | Supporting | scripts/check_skills.py | Checks published packages and stable story-family tokens. | Provides structural proof. | Direct |
| validator tests | Supporting | scripts/test_check_skills.py | Exercises repository-specific validator invariants. | Detects weakening or drift in those checks. | Direct |

### Documented Validation
| Evidence Type | Source | Observable Seam or Behavior | Prior-Art Basis and Limits |
|---|---|---|---|
| repository validator | scripts/check_skills.py | skill package structure, references, and stable story-family contracts | Required by `AGENTS.md`; structural proof, not observed activation |
| validator regression suite | scripts/test_check_skills.py | invariant failures after controlled fixture mutations | Required because the validator changes; does not exercise host routing |
| static routing fixtures | .agents/skills/agent-skill-generator/references/inventory-trigger-evals.md | positive, adjacent-negative, collision, and post-selection story-family cases | Supports routing review only; does not prove host activation |

### Authoritative Constraints / Do Not Edit
- None identified.

## Implementation Plan

Artifact Type: Implementation Plan
Status: Ready
Reason: None

### Target Executor and Constraints
- Executor: standard coding agent.
- Autonomy: edit only the paths listed under Files.
- Context capacity: sufficient for the four contracts, root routing, trigger
  fixtures, packet example, validator, and validator tests.
- Tool access: repository reads, `apply_patch`, and bundled Python.
- Parallelism: component files may be revised independently before integration.
- Checkpoint needs: run structural validation after all names and references align.

### Goal
Make story-family shape, readiness, and ownership unambiguous without creating
duplicate trigger aliases.

### Inputs
- Story Card: the ready artifact above.
- Repo Context: the evidence-backed artifact above.
- External primary evidence: None required.
- Accepted assumptions or decisions: component skills remain independently
  usable, and the rename migration is atomic.
- Non-blocking open questions: None.

### Scope and Risk Drivers
- Scope drivers: four published skills, README routing, trigger cases, example,
  and validator invariants.
- Risk drivers: broken skill references, frontmatter/folder mismatch, and
  component-orchestrator contract drift.

### Files
- Existing Change: .agents/skills/story-clarifier/SKILL.md - story contracts.
- Existing Change: .agents/skills/story-repo-scout/SKILL.md - repo-context contract.
- Existing Change: .agents/skills/story-implementation-planner/SKILL.md - plan contract.
- Existing Change: .agents/skills/story-to-plan-orchestrator/SKILL.md - transitions.
- Existing Change: .agents/skills/story-to-plan-orchestrator/references/story-to-plan-packet-example.md - packet-shape example.
- Existing Change: README.md - inventory and routing.
- Existing Change: .agents/skills/agent-skill-generator/references/inventory-trigger-evals.md - routing cases.
- Existing Change: scripts/check_skills.py - stable structural invariants.
- Existing Change: scripts/test_check_skills.py - validator regression suite and validation evidence.

### Steps
1. `P1 - Align component-owned contracts` - define one minimal artifact/status
   protocol in each component-owned contract.
   - Blocked by: None.
   - Preserve artifact-specific fields in the owning component.
   - Check that shape never substitutes for readiness.
2. `P2 - Align orchestration transitions` - reduce the orchestrator to stage
   routing, invalidation, resumption, and assembly.
   - Blocked by: P1.
   - Reference component contracts instead of copying their volatile schemas.
   - Verify behavior-only changes invalidate dependent evidence and planning.
3. `P3 - Align published routing and invariants` - align names, README routing,
   trigger cases, examples, and validator paths.
   - Blocked by: P2.
   - Remove old identifiers without adding alias packages.
   - Check that single-artifact requests still route to component owners.
4. `P4 - Validate the integrated migration` - run the repository validator and
   its focused regression tests.
   - Blocked by: P3.
   - Inspect any failure as structural, routing, workflow, resource, or evidence.
   - Stop if a failure requires inventing a repository workflow.

### Dependencies and Parallel Work
- Starting frontier: P1.
- External prerequisites: the repository validator and published skill
  inventory; satisfied by the inspected `scripts/check_skills.py` and
  `README.md` Existing Evidence rows.
- Component rewrites can proceed independently after the common protocol settles.
- Routing docs, examples, and validator checks join after component contracts stabilize.

### Risks
- Static trigger predictions may not match every target host - retain exact
  prompt cases and record the absence of observed activation evidence.

### Acceptance Criteria and Validation
| Acceptance Criterion | Planned Outcome | Validation Seam | Validation Evidence |
|---|---|---|---|
| AC-1 | Shared protocol aligned across all components. | repository structural validator plus semantic contract review | `python scripts/check_skills.py` plus contract inspection |
| AC-2 | Split-set shape is independent from readiness. | static artifact-schema and routing fixtures | Clarifier contract inspection and trigger fixture review |
| AC-3 | Invalidation follows material dependencies. | static transition-contract review | Orchestrator table inspection and packet example review |

### Delivery and Recovery
- Deliver as one atomic name/reference migration.
- If validation fails, correct the named contract or reference; do not restore
  deprecated alias skills that would duplicate activation.

### Handoff
- Return the changed-file summary, structural test results, static trigger
  evidence, and any residual host-specific activation risk.
```
