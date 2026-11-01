# Sources and maintenance

Use when checking a technical claim or maintaining this skill. Prefer the project's
versioned documentation, class reference, and pinned binding/build source. The
`stable` links here are discovery entrypoints; follow the version selector for
older projects and do not replace missing versioned evidence with `latest` silently.

## Primary authorities

| Contract | Authority |
|---|---|
| Engine documentation and compatibility policy | [Godot docs](https://docs.godotengine.org/en/stable/index.html), [release policy](https://docs.godotengine.org/en/stable/about/release_policy.html) |
| Native binding version versus target API | [godot-cpp versioning](https://github.com/godotengine/godot-cpp#versioning), the project's pinned README and build definitions |
| Native compatibility and module boundary | [About godot-cpp](https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/about_godot_cpp.html) |
| Build and registration | [C++ guide](https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/gdextension_cpp_example.html), [SCons](https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/build_system/scons.html), [CMake](https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/build_system/cmake.html) |
| CMake API selection options | [Binding CMake source](https://github.com/godotengine/godot-cpp/blob/master/cmake/godotcpp.cmake); inspect the pinned revision rather than assuming master matches it |
| Native loading and export selectors | [GDExtension file](https://docs.godotengine.org/en/stable/engine_details/engine_api/gdextension/gdextension_file.html) |
| Ownership and threading | [Object ownership](https://docs.godotengine.org/en/stable/engine_details/architecture/object_class.html#object-ownership-and-casting), [Node](https://docs.godotengine.org/en/stable/classes/class_node.html), [thread-safe APIs](https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html) |
| Resource identity and import boundary | [Resources](https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html), [imports](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html), [4.4 UID changes](https://godotengine.org/article/uid-changes-coming-to-godot-4-4/), [VCS](https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html) |
| Execution semantics and export | [CLI](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html), [editor scripting](https://docs.godotengine.org/en/stable/tutorials/plugins/running_code_in_the_editor.html), [exporting](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html) |

The native version distinction is material: godot-cpp v10 introduced independent
versioning with target-API selection, while some Godot tutorials retain the older
matching-branch instructions. Neither a moving branch nor a tutorial example is a
project pin. Check the actual dependency's supported options and required APIs.

## Comparative skill collections

These informed capability selection and evaluation cases, not copied instructions,
code, or bundled assets. They are secondary references, not API authorities:

- [gamedev-skills Godot collection](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/tree/main/skills/godot):
  focused capability routing and the distinction between static resource checks
  and engine validation.
- [Game-Dev-Agentic-Skills](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/tree/main/skills):
  broad coverage and candidate testing/visual workflows; verify that proposed
  runners execute assertions and propagate failures before using them.
- [cc-godot](https://github.com/Zate/cc-godot/tree/main/plugins/gd/skills):
  separate debugging, UI, and profiling concerns; discover actual tools rather
  than assuming a collection's MCP names exist.
- [jwynia Godot skills](https://github.com/jwynia/agent-skills/tree/main/skills/tech/game-development/godot):
  selective references and scene/script patterns; verify linked resources,
  coroutine APIs, and import metadata against the engine.

Author future additions independently. Do not transplant snippets, templates, or
scripts without checking their licensing and the repository's incorporation rules.
Avoid generalizing a secondary source's version, performance target, or architecture
preference into a universal Godot rule.

## Refresh triggers

Recheck the affected primary sources when an engine/binding version changes, a
command or linked page disappears, a project contradicts a claimed API, or a
behavioral case fails. Follow moved official pages from the current index rather
than guessing new URLs. Add guidance only for a demonstrated decision gap.

Keep reusable cases and expectations in [the evaluation reference](trigger-evals.md).
Do not put per-run logs, hashes, transcripts, pass tables, or broad documentation
mirrors in this package. A verified link is not verification of every claim on its
page or of the engine workflow itself.
