# Godot skill evaluation

Read only when maintaining the skill. These are reusable procedures and expected
outcomes, not recorded passing results. Keep individual results outside the repo.

## Structure and activation

Run the repository's `python scripts/check_skills.py` after package/inventory
changes and the available host skill validator. Review link targets, the exact
two-field frontmatter, source-backed claims, and selective reference loading.
Structure checks do not prove routing or useful behavior.

Review the following activation boundaries separately. For observed activation,
expose the actual catalog and request without naming or preselecting this skill.
If only description inspection or a simulated catalog is available, record static
prediction or generic-harness evidence rather than native host activation.

| Request | Expected routing/behavior |
|---|---|
| Explain how Godot scenes differ from nodes; I have no project yet. | Godot; direct explanation, no environment prerequisite. |
| Start a Godot 4 3D prototype; the language is undecided. | Godot; clarify a consequential language choice, no automatic C++ mandate. |
| Our Godot C# signal handler never runs. Help diagnose it. | Godot; retain C# and inspect that language's binding/lifecycle. |
| This Godot 3 GDNative addon stopped loading. | Recognize the legacy boundary; use version-specific evidence, no silent Godot 4 port. |
| Fix an Unreal Actor lifetime bug. | Other engine guidance, not Godot. |
| Build a Unity menu with keyboard navigation. | Other engine guidance, not Godot. |
| Review a plain C++ library's unique_ptr ownership. | C++ principle guidance, not Godot. |
| Repair QObject thread affinity in this Qt widget. | Qt principle guidance, not Godot. |
| Implement a custom Godot renderer in our engine fork. | Engine-source/C++ workflow; Godot can explain the boundary but does not claim full coverage. |
| Our GDExtension library builds but its class is absent. | Godot plus C++ guidance where available; inspect registration/loading. |

## Cold-agent behavior

Use all five [raw fixtures](behavior-fixtures.md). Give each fresh agent the exact
request and its raw packet, the skill entrypoint and relevant runtime references,
and C++ principle guidance for F1-F3 when available. Do not give it this file,
previous outputs, suspected causes, or expected fixes. Confirm the decision-bearing
inputs were actually read. Use an external isolated packet/output directory and
limit the worker to that material; isolation is a task constraint unless the host
provides an enforced sandbox.

Grade decisions and concrete proposed changes, not preferred wording. A missing
fixture is inconclusive, not a skill failure or a pass. These cases request source
analysis/proposed patches; do not execute their intentionally incomplete snippets.

| Case | Required outcomes | Material failures |
|---|---|---|
| F1 | Identify API 4.5 as inconsistent with 4.3/4.4 support; select API 4.3 using the supplied CMake option. Preserve pinned v10, CMake, multi-config Debug, template_debug, and single precision. Propose compile, load, and engine checks for claimed versions without claiming they ran. | Match binding version numerically to engine; upgrade dependencies; migrate to SCons; confuse Debug with Godot target; assert compilation proves compatibility. |
| F2 | Identify broad-first selector choosing legacy.so and missing requested entry; prioritize the intended x86_64 mapping or remove obsolete fallback deliberately. Fix class-registration guard to SCENE consistently with the initialization minimum. Separate subsequent registration from first loader failure. | Blame missing files/dependencies contrary to evidence; change the correct intended entry symbol merely to load legacy code; assume GDCLASS registers the class; fix only one demonstrated defect. |
| F3 | Identify manual destruction through a live Ref, stale non-null pointer risk, and active scene-tree mutation from worker despite a private mutex. Retain Ref ownership, compute plain data off-thread, hand off safely and resolve/check the target on its owning context; manage cancellation/shutdown. | Replace engine ownership with default-deleting unique_ptr; treat a mutex or ObjectID as a lifetime guarantee; defer a call through a pointer that may already dangle. |
| F4 | Perform no project execution/install/edit. Recognize editor tool-script writes and native loading. Compilation notes support only reported build output; two iterations/exit 0 without diagnostics prove neither tests nor visual/export correctness. Name unavailable checks. | Launch/import/build to review; treat headless mode as a sandbox; claim tests or UI/export success; hide missing runtime. |
| F5 | Propose moving script with unchanged .uid and texture with preserved .import settings/UID; update script preload, scene paths, and import source_file. Preserve resource IDs and opaque metadata. Leave cache paths for authorized engine regeneration and report that pending check. Retain GDScript. | Fabricate UIDs/cache hashes; drop .import/.uid; rewrite unrelated scene records; commit generated cache; claim import validity without running Godot. |

Other correct implementations are acceptable when they preserve the same contracts.
Do not demand source edits from a review-only request or invent runtime failure
symptoms beyond the supplied evidence.

## Small paired comparison

Run F2 in two fresh agents with identical raw input, tool limits, and output
request. Both receive the same C++ principle guidance; only one receives Godot's
entrypoint/runtime references. Do not show the baseline agent Godot instructions
or these expectations. Compare defect coverage, proposed corrections, preservation
of user constraints, unnecessary actions, and evidence claims.

Treat this as one qualitative comparison, not a performance score or proof of
general superiority. If both solve it, report parity. Strengthen a demonstrated
Godot-specific gap or remove redundant generic instructions; do not manufacture a
benefit or add rules merely because two valid answers differ.

## Acceptance and evidence limits

Before delivery, all structure checks and the five observed behavioral cases must
be accounted for. Correct demonstrated material instruction failures and rerun
affected cases in fresh contexts. Keep unrelated legitimate behavior intact.

Record case ID/input, method, context, comparison, observed decisions, result, and
remaining uncertainty outside the checkout. Distinguish structure, activation,
instruction behavior, and resource execution. Record static activation review as
static; explicit skill invocation cannot prove automatic discovery.

No engine/compiler installation is required solely to evaluate this prose package.
Without engine execution, claim package/instruction validation only. Do not report
native loading, ABI compatibility, visuals, exports, or host installation as tested.
Reconsider splitting the skill only if observed use shows that selective reference
loading cannot keep general and native tasks appropriately focused.
