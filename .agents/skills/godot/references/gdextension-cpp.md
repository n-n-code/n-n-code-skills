# GDExtension and C++

Use for native Godot components, integration failures, or C++ review. Preserve
the project's language split; native integration does not require rewriting its
GDScript or C# orchestration. Treat configuration, generation, compilation,
editor loading, and execution as operations with side effects, not source
inspection. Keep them within the task's existing authorization.

## Establish the compatibility tuple

Inspect the engine version/build, pinned godot-cpp revision, target Godot API,
compiler/toolchain, platform, architecture, precision, and Godot build target.
Read submodule/dependency pins, presets, build files, and `.gdextension` together.
Do not infer compatibility from a filename or `compatibility_minimum` alone.

Distinguish two binding layouts. Legacy godot-cpp releases used Godot-aligned
`4.x` branches. Starting with v10, the bindings are independently versioned and
can target Godot 4.3+ through API selection. A mismatched version number is not
itself a defect. Inspect the pinned revision's README and supported options;
do not blindly apply the stable tutorial's older matching-branch prescription.
Do not update a pin merely to match today's documentation.
[Official binding versioning](https://github.com/godotengine/godot-cpp#versioning)

Target the oldest supported engine that supplies the required API. Earlier
target APIs are intended to work on later minor engines, not the reverse;
Godot 4.0 to 4.1 is a known exception. Custom engines may require their own
`extension_api.json`; floating-point precision must match. Test the oldest
claimed engine and actual deployment engine before claiming compatibility.
[Compatibility](https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/about_godot_cpp.html#version-compatibility)

## Preserve the build contract

Keep existing CMake presets, SCons options, toolchains, dependency pins, and
output conventions. Prefer SCons only for a new project without a build-system
choice; CMake is supported and does not need migration just because it is
secondary. Inspect the pinned binding's option definitions before translating
settings between build systems.

Distinguish compiler `Debug`/`Release` configuration from the Godot target
`editor`/`template_debug`/`template_release`. Symbols and optimization do not
select the extension's Godot feature contract. Preserve the project's
single- versus multi-config CMake usage, architecture, precision, exception
policy, and compatible native dependencies.
[CMake build distinctions](https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/build_system/cmake.html)

For SCons, consult the project's supported options rather than assuming every
revision accepts the same flags. Modern bindings expose `api_version`; custom
API builds use `custom_api_file`. Generating compilation metadata can help the
IDE, but it neither compiles nor validates the extension. API generation and
build help may execute project tooling; inspect source first in source-only
work. [SCons guidance](https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/build_system/scons.html)

## Trace registration and loading

Follow the chain from the selected library to the exported entry function,
initializer, class registration, bindings, and scene instantiation. Check:

- The exported C entry function matches `.gdextension`'s `entry_symbol` and
  initializes godot-cpp with the expected callbacks and minimum level.
- The initializer registers the intended class at its appropriate level.
  `GDCLASS` supplies class machinery; it does not replace registration.
- `_bind_methods` exposes callable methods, property accessors, and signals
  with compatible names and types; a public C++ method alone is not a script API.
- Registered class names agree with scene/resource types and script calls.

Check generated headers and pinned binding examples before borrowing engine
internal APIs. [Registration and binding workflow](https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/gdextension_cpp_example.html)

For a load failure, preserve the exact diagnostic. Inspect the first matching
library selector: every feature tag must match, and more specific selectors
belong before broad ones. Confirm the chosen binary exists and matches platform,
architecture, target, and precision. If it does, inspect its exported symbol and
transitive native dependencies using available platform tools. A missing DLL
message can describe a dependency rather than the named extension. Rebuilding
or upgrading blindly does not isolate the failure.
[Library selection and dependencies](https://docs.godotengine.org/en/stable/engine_details/engine_api/gdextension/gdextension_file.html)

## Honor Godot lifetime and threading

Use `Ref<T>` for `RefCounted` resources. Do not manually destroy an object held
by a `Ref`, or adopt an engine-owned object into `std::unique_ptr` with a default
deleter. Keep ordinary C++ value/RAII ownership for non-Godot state. For manually
owned Godot objects, use the matching Godot allocation/destruction contract and
make any ownership transfer explicit.
[Object ownership](https://docs.godotengine.org/en/stable/engine_details/architecture/object_class.html#object-ownership-and-casting)

Parented nodes are freed with their parent; `remove_child` alone does not free
them. Use the appropriate node deletion lifecycle, often `queue_free`, and
account for queued deletion when accepting work. `Node.owner` concerns scene
serialization, not a replacement C++ memory owner.
[Node lifecycle](https://docs.godotengine.org/en/stable/classes/class_node.html)

A raw pointer's non-nullness does not establish liveness. For a non-owning object
that may disappear before deferred work, retain its instance identity and resolve
it through the pinned binding's `ObjectDB::get_instance` API at use time; check
type, validity, and relevant deletion state. Resolve/use on the owning execution
context: an `ObjectID` is not a lifetime lock or permission for concurrent access.
[Binding object API](https://github.com/godotengine/godot-cpp/blob/master/include/godot_cpp/core/object.hpp)

Keep active scene-tree mutation on its owning thread. Transfer worker results
through a safe handoff/deferred operation; a private mutex does not synchronize
the engine's scene access. Avoid concurrent mutation of shared resources. Check
the selected server's settings and thread contract before parallelizing it;
native code does not bypass those rules.
[Thread-safe APIs](https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html)

## Verify the native boundary

When execution is authorized, build the relevant configuration, confirm library
loading and class instantiation, and exercise exposed methods/signals plus
construction, scene removal, and shutdown. Use matching symbols and a native
debugger for native crashes. Test reload only when supported and intended.

Verify the requested debug/release export separately: include the extension and
its native dependencies, then run the artifact on the claimed platform and
architecture. Editor success does not establish exported loading or gameplay.
Report unavailable execution explicitly.

Consider an engine module only for a demonstrated API/integration gap. Modules
require engine and applicable export-template builds; introducing one is a
separate scope decision, not a fallback for an unexplained loader error.
[GDExtension versus modules](https://docs.godotengine.org/en/stable/tutorials/scripting/cpp/about_godot_cpp.html#differences-between-godot-cpp-and-c-modules)
