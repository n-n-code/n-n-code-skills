# Debugging, testing, and export

Read when choosing evidence, diagnosing failures, or preparing an export.

## Keep inspection and execution distinct

For source-only review, inspect files, supplied diagnostics, and configuration;
do not launch/import the project, compile its build scripts, or load native
libraries. Editor tooling can run project code and modify scenes. Reuse existing
authorization when execution is part of the task, rather than asking again for
each ordinary check. See [running code in the editor](https://docs.godotengine.org/en/stable/tutorials/plugins/running_code_in_the_editor.html).

Discover the selected executable and project test/build commands. Check its
version and help when permitted; report missing tools instead of substituting
an arbitrary engine or installing a harness merely to claim validation.

## Choose the evidence layer

These are parameterized command patterns, not a sequence to run on every task:

| Purpose | Pattern | Limit |
|---|---|---|
| Executable identity/options | `godot --version`, `godot --help` | Use the actual binary; flags vary by build. |
| Import readiness | `godot --headless --path <project> --import` | Starts the editor, imports, then quits; writes artifacts. |
| One GDScript parse | `godot --headless --path <project> --check-only --script res://path/script.gd` | Checks the selected script, not the whole project. |
| Bounded launch | `godot --headless --path <project> --quit-after <iterations>` | Iterations are not seconds or assertions. |
| Existing export preset | `godot --headless --path <project> --export-release "<preset>" <output>` | Requires an editor, templates, preset, and existing output directory. |

Unknown flags can be silently ignored. Standalone runnable scripts need a
`SceneTree` or `MainLoop` entrypoint. `--test` concerns engine unit tests in a
`tests=yes` engine build, not a project's test suite. See the [CLI reference](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html).

Supply a host-process wall-time limit for execution that could hang. Capture
stdout, stderr, and exit status; check relevant diagnostics even after a zero
exit. An import pass or short launch is not an assertion that gameplay works.

Use the repository's real test runner and verify that tests were discovered and
executed. Distinguish a deliberately empty selection from a successful suite.
Preserve failures, explicit failure counts, and timeout results; do not add a
runner that returns success without running tests. If no harness exists, select
the smallest meaningful scene/manual check, or scope harness work explicitly.

## Diagnose the failing boundary

Start with the first relevant failure and a reproducible trigger. Separate:

- compiler/linker failures from library loading and registered-class discovery;
- parser failures from missing assets, broken scene references, or runtime logic;
- editor-only behavior from game behavior, and headless behavior from rendering;
- platform/toolchain differences from application defects.

For native failures, follow [GDExtension and C++](gdextension-cpp.md). A produced
library is not evidence that Godot loaded it or that its methods are bound.
Use symbols and the available native debugger for native crashes; preserve the
engine, binding, platform, and configuration associated with the failing binary.

For visible changes, inspect the affected scene interactively with its real
renderer, input, viewport sizes, and pause/focus states. Exercise relevant audio
and controller behavior separately. For optimization, compare the same workload
before/after and identify CPU, GPU, allocation, or loading evidence before
changing architecture. Headless results cannot establish these properties.

## Validate the deliverable, not just the editor

Inspect export templates, target SDKs, preset resource filters, and native-library
dependencies for the requested platform. Preserve secret credentials outside
committed configuration. Package debug/release variants as required and run the
resulting artifact on each claimed target; an editor launch proves neither
native dependency packaging nor target compatibility. A PCK/ZIP alone is data,
not a playable executable. See [exporting projects](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html).

Finish with the behavior checked, commands actually run, engine/configuration,
observed results, and remaining gaps. Keep source review, compile success,
engine execution, visual inspection, and export execution as separate claims.
