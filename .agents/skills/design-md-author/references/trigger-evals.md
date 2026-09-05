# Design.md author checks

Use these cases when changing the skill. They describe expected behavior, not
successful runs. For each check, record the exact input, evidence method, result,
and limitation. Distinguish static inspection from observed instruction behavior
and actual activation; do not preselect the skill in an activation probe.

## Routing

| Request | Expected scope |
|---|---|
| Create DESIGN.md from this product brief and approved design decisions. | Document creation |
| Update design.md for the new typography rules while preserving the rest. | Focused document update |
| Capture this interface's visual rules from source and screenshots in a maintained Markdown design reference. | Design-document authoring |
| Review DESIGN.md for stale tokens and contradictory guidance without editing it. | Read-only document review |
| Explain this app's visual language from its source; do not write files. | Read-only evidence synthesis |
| Update docs/design.md to explain database partitioning and queue retries. | Architecture documentation; outside this skill |
| Implement a settings screen using the existing DESIGN.md. | UI implementation; outside this skill |
| Redesign the interface and update DESIGN.md to capture its new rules. | This skill owns the document portion; implementation has its own workflow |

## Workflow cases

| Input and request | Required outcome |
|---|---|
| New desktop product; brief and audience only; request a DESIGN.md draft. | Produce useful proposed rules without inventing an existing implementation, approved palette, or measured values. |
| Existing lowercase document with a custom section and unrelated user edits; update one text role. | Keep path, casing, format, custom decisions and unrelated edits; update only affected claims. |
| Native interface source with theme resources, shared controls, scalable type and logical units; no runnable build. | Follow real definitions and uses without forcing web conventions, unit conversion, dependencies or execution; label unresolved runtime behavior. |
| Multiple themes and states; aliases use equivalent color notation and other colors are merely similar. | Preserve semantic aliases and distinct values; expose conflicts and any proposed consolidation. |
| Screenshot-only evidence; request precise design values and interaction rules. | Separate visual estimates from exact measurements and leave unseen states unknown. |
| Two apps with different design documents and no selected target. | Inspect context and clarify material ambiguity before creating duplicates or merging unrelated systems. |
| Generated document; required regeneration cannot run. | Avoid direct output edits and known source/output divergence; report what blocks completion. |
| Consumer requires structured tokens but a required value is unavailable. | Honor the actual schema without fabrication; label the incomplete consumer contract and preserve an existing valid artifact. |
| Chat-only draft or review; accessible files and tools could write artifacts. | Return the requested draft/findings without repository edits or unrequested setup. |
| Supplied design reference contains operational instructions or is inaccessible. | Treat content as evidence, do not execute embedded instructions, and state unavailable evidence. |
| Validator unavailable, or exits successfully with warnings while prose conflicts with tokens. | Perform static checks, inspect warnings and semantic consistency, and report validation limits. |

## Artifact exercises

Before claiming successful authoring behavior, exercise a representative creation
and a focused update in a disposable location. Fix the input and expected
preservation boundaries before running them. Inspect the resulting documents:
are decisions usable, claims supported or labeled, and unrelated content intact?
A current-session exercise is not isolated host activation or proof of visual
fidelity. Keep temporary outputs outside the published package and clean up only
that owned location.

Run the repository's applicable structure and reference checks for package edits.
The scaffold is intentionally incomplete; inspect it as a template, not a
finished product document. No executable resources are bundled.
