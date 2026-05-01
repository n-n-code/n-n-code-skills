# Compact Story-To-Plan Packet Example

Use this only as a shape reference. Keep real packets grounded in the current
story and repository evidence.

```markdown
## Story Card
Status: Ready
Confidence: High - the change is limited to published story-skill docs.

### Title
Normalize split story readiness

### User Story
As a maintainer of the story-to-plan skill family, I want split story packets to
carry a distinct top-level status and ready slice status, so that orchestrated
resumption can choose a slice without treating the whole epic as one ready
story.

### Acceptance Criteria
- The split story template uses `Status: Split Candidate` at the packet level.
- Each slice has its own readiness status.
- The orchestrator readiness check accepts a split set only when the first
  shippable slice is marked `Ready`.

### Out of Scope
- Renaming published skill folders.

### Dependencies and Assumptions
- Existing vocabulary remains `Ready | Needs Clarification | Split Candidate |
  Blocked`.

### Open Questions
- None.

### Validation Notes
- AC1-AC3: run `bash scripts/check-skills.sh` and inspect the edited templates.

## Repo Context
### Search Handles
- Split Candidate
- Story ready
- Slice Order

### Relevant Files
| Path | Evidence | Why It Matters | Confidence |
|---|---|---|---|
| .agents/skills/user-story-clarifier/SKILL.md | Defines `Split Story Output`. | Owns the split packet template. | High |
| .agents/skills/story-implementation-orchestrator/SKILL.md | Defines readiness checks. | Owns resumption and slice selection. | High |
| scripts/check-skills.sh | Validates skill structure and skill references. | Repository structural validation command. | High |

### Likely Entry Points
- .agents/skills/user-story-clarifier/SKILL.md: update split output shape.
- .agents/skills/story-implementation-orchestrator/SKILL.md: update readiness
  checks.

### Tests and Validation Targets
- `bash scripts/check-skills.sh`

### Likely Unrelated / Do Not Touch
- LICENSE: unrelated repository metadata.

### Open Repo Questions
- None.

## Implementation Plan
Plan Status: Ready

### Target Executor
standard-agent - small documentation-only skill update.

### Size
Small.

### Goal
Make split-story readiness unambiguous across the clarifier and orchestrator.

### Files
- Change: .agents/skills/user-story-clarifier/SKILL.md - split output shape.
- Change: .agents/skills/story-implementation-orchestrator/SKILL.md - readiness
  and resumption checks.
- Test: scripts/check-skills.sh - validation command, not edited for this story.
- Do Not Touch: LICENSE - unrelated metadata.

### Steps
1. Update the split story template so the packet remains `Split Candidate`.
2. Add per-slice readiness fields and first-slice guidance.
3. Update orchestrator story readiness checks for single stories and split sets.
4. Run the repository skill checker.

### Validation
- `bash scripts/check-skills.sh`

### Rollback
- Revert the two skill-doc edits; no generated content or folder rename is
  involved.

### Handoff Notes
- Start by checking the split output block in
  .agents/skills/user-story-clarifier/SKILL.md.
```
