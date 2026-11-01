# Godot behavior fixtures

These are independently authored, synthetic source-review packets, not runnable
projects or passing test results. Omitted boilerplate is intentional. Give an
evaluating agent one complete case and its request without the grading reference.
Treat version/tool observations below as supplied evidence, not commands to run.
Do not execute the snippets or install dependencies to evaluate these cases.

## F1: Native build configuration

**Request:** Review this configuration for our extension package supporting Godot
4.3 and 4.4. Propose the smallest source/configuration changes and the checks we
should run later. Keep our CMake workflow and pinned dependencies. Do not run
builds or change files.

**Project notes:** CI uses a pinned godot-cpp v10 revision. Its local README says
v10 uses independent versioning and supports selecting Godot API 4.3 or later.
The selected dependency's CMake definitions expose `GODOTCPP_API_VERSION`,
`GODOTCPP_TARGET`, and `GODOTCPP_PRECISION`. Its supplied API files include 4.3,
4.4, and 4.5. No custom API override is configured. Source inspection confirms
the extension uses only APIs available in 4.3. Runtime smoke uses an official
single-precision Godot 4.4 Linux x86_64 executable. Release packaging is separate;
this preset is for development and debugging.

`CMakePresets.json`:

```json
{
  "version": 3,
  "configurePresets": [{
    "name": "native-dev",
    "generator": "Ninja Multi-Config",
    "binaryDir": "${sourceDir}/out/native-dev",
    "cacheVariables": {
      "GODOTCPP_API_VERSION": "4.5",
      "GODOTCPP_TARGET": "template_debug",
      "GODOTCPP_PRECISION": "single"
    }
  }],
  "buildPresets": [{
    "name": "native-dev",
    "configurePreset": "native-dev",
    "configuration": "Debug"
  }]
}
```

## F2: Library and class discovery

**Request:** Our native component does not load in a Linux x86_64 debug game run.
Review these sources and supplied binary observations. Explain the likely causes
and smallest corrections; do not execute or edit anything.

`orbit.gdextension`:

```ini
[configuration]
entry_symbol = "orbit_library_init"
compatibility_minimum = "4.3"

[libraries]
linux.debug = "res://bin/legacy.so"
linux.debug.x86_64 = "res://bin/orbit.so"
```

**Binary observations:** Both paths exist and are compatible Linux x86_64
single-precision libraries. Their required native dependencies are present.
`legacy.so` exports `legacy_library_init`; `orbit.so` exports
`orbit_library_init`. Neither exports the other's entry function. The current
Orbit class is named `OrbitBody`, declares `GDCLASS(OrbitBody, Node3D)`, and has
its required methods bound. The requested run is the game, not the editor.

`register_types.cpp` excerpt for `orbit.so`:

```cpp
void initialize_orbit(ModuleInitializationLevel level) {
    if (level != MODULE_INITIALIZATION_LEVEL_CORE) {
        return;
    }
    GDREGISTER_CLASS(OrbitBody);
}

extern "C" GDExtensionBool GDE_EXPORT orbit_library_init(
    GDExtensionInterfaceGetProcAddress get_proc_address,
    GDExtensionClassLibraryPtr library,
    GDExtensionInitialization *initialization) {
    GDExtensionBinding::InitObject init(get_proc_address, library, initialization);
    init.register_initializer(initialize_orbit);
    init.set_minimum_library_initialization_level(MODULE_INITIALIZATION_LEVEL_SCENE);
    return init.init();
}
```

`main.tscn` excerpt:

```ini
[node name="Orbit" type="OrbitBody"]
```

## F3: Background work and lifetime

**Request:** Review this GDExtension code for shutdown and scene-change defects.
Give findings and a concrete correction strategy, without executing or editing
files. The worker is joined during shutdown, but a level change can happen while
the worker runs. `target` points into the active scene tree. `JobData` derives
from `Resource`. No engine code uses `worker_mutex`.

```cpp
Ref<JobData> job;
Node3D *target = nullptr;
std::mutex worker_mutex;
std::thread worker;

void Controller::start() {
    job.instantiate();
    Node3D *saved_target = target;
    worker = std::thread([this, saved_target]() {
        auto result = compute_plain_data();
        std::lock_guard<std::mutex> lock(worker_mutex);
        if (saved_target != nullptr) {
            auto *marker = memnew(Node3D);
            marker->set_position(result.position);
            saved_target->add_child(marker);
        }
    });
}

void Controller::shutdown() {
    if (worker.joinable()) {
        worker.join();
    }
    if (job.is_valid()) {
        memdelete(job.ptr());
    }
}
```

## F4: Limited review environment

**Request:** Source-only review of our Godot startup procedure. Do not install,
import, launch, configure, build, or modify anything. Explain which checks the
existing evidence supports and what remains unverified.

**Environment:** No Godot executable or C++ compiler is available. The repository
contains `project.godot`, editor plugins, a native `.gdextension`, and this script:

```gdscript
@tool
extends Node

func _ready() -> void:
    if Engine.is_editor_hint():
        var record := FileAccess.open("res://editor-session.txt", FileAccess.WRITE)
        record.store_line("opened")
```

**Supplied previous-run notes:**

```text
Native compilation: exit 0; binary produced.
Headless game: --quit-after 2; exit 0; no diagnostics retained.
Project tests: not invoked.
Visual inspection: not performed.
Exported executable: not built.
```

## F5: Script and asset move

**Request:** Propose a source patch for moving `actors/pilot.gd` to
`gameplay/pilot.gd` and `art/pilot.png` to `art/actors/pilot.png`. Keep behavior
and resource identity. This is a Godot 4.4 GDScript project; no engine execution
is available or requested. Do not make the edits here.

**Inventory:** The two destination directories already exist. All consumers are
shown below. `art/pilot.png` is a binary source asset. `.godot/imported/` contains
generated texture data. The import file below is an excerpt; its omitted settings
must remain intact. Existing source metadata is tracked.

`actors/pilot.gd`:

```gdscript
extends CharacterBody2D

const PORTRAIT = preload("res://art/pilot.png")
```

`actors/pilot.gd.uid`:

```text
uid://bpilot4script
```

`art/pilot.png.import` excerpt:

```ini
[remap]
importer="texture"
type="CompressedTexture2D"
uid="uid://bpilot4texture"
path="res://.godot/imported/pilot.png-11111111111111111111111111111111.ctex"

[deps]
source_file="res://art/pilot.png"
dest_files=["res://.godot/imported/pilot.png-11111111111111111111111111111111.ctex"]
```

`scenes/pilot.tscn` excerpt:

```ini
[ext_resource type="Script" uid="uid://bpilot4script" path="res://actors/pilot.gd" id="1_script"]
[ext_resource type="Texture2D" uid="uid://bpilot4texture" path="res://art/pilot.png" id="2_art"]

[node name="Pilot" type="CharacterBody2D"]
script = ExtResource("1_script")

[node name="Portrait" type="Sprite2D" parent="."]
texture = ExtResource("2_art")
```

The UID strings and generated filenames are opaque fixture identifiers; preserve
them as supplied. This packet does not establish their validity in a real engine.
