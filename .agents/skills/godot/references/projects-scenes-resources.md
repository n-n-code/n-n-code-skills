# Projects, scenes, and resources

Read for project discovery, scene changes, resource identity, or asset moves.
Use the project's Godot documentation version for API details; `stable` links
below are lookup entrypoints, not instructions to upgrade.

## Establish the project boundary

Find `project.godot`, the requested scene or resource, relevant scripts,
autoloads, addons, export presets, and existing tests. Read the working-tree
changes before editing. Reconcile repository/CI engine declarations with the
selected executable when execution is in scope. Project format and feature
markers are evidence of compatibility, not an exact patch-version lock.

Record the language, renderer, target platform, and build setup only where they
affect the request. A C++ extension can coexist with GDScript or C#; its presence
does not authorize rewriting those scripts. Keep missing dependencies separate
from missing source files. For a new project, resolve decisions that affect the
requested result without imposing a folder architecture or an autoload framework.

## Trace scene behavior before changing structure

- Treat a node hierarchy as composition. Trace instantiated and inherited
  scenes, attached scripts, exported references, and signal connections before
  replacing a subtree. Check native class registration/loading before diagnosing
  a scene's unknown native node type as corrupt serialization.
- Distinguish parentage from scene ownership. Parentage controls the hierarchy
  and child lifetime; `owner` determines inclusion when packing a scene. Tools
  that create persistent scene children may need to set their owner after
  adding them. Do not impose this on ordinary runtime-only children.
- Respect lifecycle order: parents enter the tree before children, while
  children become ready before their parent. Choose initialization according to
  when its dependencies exist, rather than moving everything to constructors.
- On renames or moves, inspect `NodePath` values, unique-name ownership,
  animation tracks, serialized connections, and code references. A valid new
  path does not prove every consumer was updated.

See the [Node lifecycle and ownership reference](https://docs.godotengine.org/en/stable/classes/class_node.html).

## Preserve resource semantics

For text scenes/resources, retain unrelated external-resource and subresource
IDs, UIDs, paths, inheritance, and connection records. Change the smallest
relevant records; do not renumber or regenerate a whole file as cleanup. Follow
binary or imported-scene dependencies through their source/import workflow
rather than pretending they can be repaired with text substitution.

Loaded Resources may be shared across nodes and scene instances. Before mutating
a material, shape, or custom Resource, establish whether the change should affect
all consumers. Use a supported duplication or local-to-scene strategy when
independence is required, checking nested resource behavior for the selected
version. Instantiating a `PackedScene` creates nodes; it does not inherently make
all referenced Resources independent. See [Resources](https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html).

## Move assets without discarding identity

Keep source assets and their adjacent `.import` configuration. Preserve existing
script/shader `.uid` companions on versions that use them, including moving the
companion with its source. Godot 4.4 introduced these companions; do not invent
random replacement UIDs or retrofit that convention blindly to older projects.
See the [version-specific UID introduction](https://godotengine.org/article/uid-changes-coming-to-godot-4-4/).

Let an authorized import refresh engine-owned generated paths. `.godot/` is
cache/output, distinct from adjacent source metadata. Do not delete caches as a
first diagnosis or commit them as a repair. Use `ResourceLoader`/language load
APIs for imported resources; use `FileAccess` for raw data with deliberate
export inclusion. Native Godot scene/resource formats do not use the non-native
asset import options. See [the import process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html)
and [version-specific VCS exclusions](https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html).

After an authorized edit, inspect the diff and resolve affected references;
validate with the selected engine only within the request's execution scope.
Report source inspection separately when import or runtime checks were unavailable.
