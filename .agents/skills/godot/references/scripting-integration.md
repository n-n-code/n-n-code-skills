# Scripting integration

Read for GDScript/C# changes or a script/native boundary. Keep existing language
choices. Do not turn a small script fix into a port or rewrite native code merely
to use this skill's more detailed C++ guidance.

## GDScript

- Follow the project's typing conventions. Add useful types at public boundaries
  and places where inference would conceal a `Variant` or nullable value; check
  syntax against the project's minor version. Typed collections and newer syntax
  are not uniformly available across Godot 4.
- Trace when node references become valid. `@onready` evaluation and `_ready()`
  differ from construction; a reference can still become invalid after a node is
  freed or a scene changes. Validate externally supplied or deferred targets where
  their lifetime is not guaranteed.
- Choose signals for notifications and direct calls for known dependencies;
  inspect existing connections before adding another. Do not prescribe one global
  event bus or ban ordinary node lookups.
- `await` suspends until the awaited signal/coroutine completes. Check whether the
  receiver and scene can disappear, whether a signal can be missed, and how the
  operation terminates. Do not import JavaScript `Promise` or Godot 3 coroutine
  state APIs into Godot 4 examples.
- Resolve resource paths and registered types before diagnosing script syntax.
  A missing imported asset or native class can cause secondary script failures.

Use the official [typing guide](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html),
[GDScript reference](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html),
and [Node lifecycle](https://docs.godotengine.org/en/stable/classes/class_node.html)
for the relevant version. A parser check alone does not exercise signal timing or
scene lifecycle.

## C#

Inspect the `.csproj`, solution/build entrypoint, `global.json` when present, and
Godot .NET version. Compilation needs the compatible .NET SDK as well as the
.NET-enabled Godot editor. Preserve SDK/framework/package pins; a missing SDK is
not a reason to rewrite in GDScript or install the newest SDK automatically.

Use the repository's build/test commands; `dotnet build` is a common build entry,
not proof that Godot can instantiate the resulting classes. Respect the C# API's
naming, generated/partial class requirements, signal conventions, and exported
property restrictions. Check the version-specific C# and export documentation
before promising web/mobile support; do not hardcode one SDK requirement for all
Godot 4 releases.

Sources: [C# basics](https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_basics.html),
[C# API differences](https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_differences.html).

## Script/native boundary

Verify the native class is registered and its library loads before investigating
script-side lookup. Methods, properties, and signals exposed through Godot must
use the applicable binding/registration mechanism; ordinary public C++ members
are not automatically script API. Follow the [C++ reference](gdextension-cpp.md)
for that contract.

Inspect the actual language bridge before choosing calls, casts, or generated
types; C# access to extension types must not be assumed identical to GDScript.
Keep boundary values compatible with Godot's exposed types and avoid leaking
native pointer ownership through a script API. Test the script call and signal or
property round trip in the engine when execution is authorized.

Keep substantial native computation separable from scene interaction where useful,
then hand results back through the engine's permitted thread/lifetime boundaries.
Measure expensive crossings before redesigning them. Pure C++ unit tests can
cover computation, while binding and scene behavior still need engine integration
checks.
