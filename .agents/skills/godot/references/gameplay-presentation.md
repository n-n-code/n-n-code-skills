# Gameplay and presentation

Use this as a decision map, not a requirement to inspect every subsystem. Start
with the requested behavior, existing scene, target device, renderer, and visible
acceptance condition. Follow version-matched class documentation for exact APIs.

| Concern | Decision and evidence |
|---|---|
| 2D/3D movement and physics | Identify the body type and who owns movement. Use physics callbacks for physics-driven updates; distinguish velocity, displacement, local/global transforms, and collision layers/masks. Do not multiply by delta twice or manually animate a simulated body's transform without understanding its contract. |
| Input | Reuse named Input Map actions and project bindings. Inspect UI consumption, gameplay input, and device support; test keyboard/controller focus and pause behavior where relevant. |
| Scene communication | Keep reusable scenes' external dependencies explicit. Prefer existing direct references/signals before adding autoloads or a global event system. Test scene replacement and repeated instantiation. |
| UI | Work with the Control/Container layout model, theme resources, minimum sizes, and focus neighbors. A Container manages its children's layout; changing child positions may be overwritten. Inspect multiple aspect ratios, text lengths, and input methods. |
| Animation | Identify the authority for the property: gameplay code, animation tracks, or an animation state machine. Avoid competing writers; verify transitions, interrupts, and reset/re-entry behavior. |
| Audio | Inspect bus routing, positional versus non-positional playback, pause behavior, and resource lifecycle. Audible validation requires an appropriate runtime/output environment. |
| Rendering/shaders | Confirm renderer and target-device capabilities before selecting features. Test material/resource sharing and actual output; headless success cannot establish shader appearance or lighting. |
| Performance | Reproduce on the relevant device/build, identify the limiting frame stage, change one demonstrated bottleneck, and remeasure. Pooling, threading, batching, and native rewrites have costs; none is a universal first step. |

For 2D, watch pixel scaling/filtering and camera transforms when they affect the
brief. For 3D, inspect coordinate spaces, lighting/material configuration, camera
placement, and collision representation. Do not turn these into mandatory style
choices or assume a 2D game needs no GPU investigation.

Use a small observable scenario: the player lands without jitter, a pause menu
captures input, controller focus survives reopening, or two scene instances keep
independent state. Match validation to that scenario and preserve existing game
feel unless changing it is requested. Numerical frame budgets and loading targets
come from the product/platform requirements, not this skill.

## Official lookup routes

- [Physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html)
  and the selected body class for movement/collision semantics.
- [Input event handling](https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html)
  for action mapping and propagation through UI and gameplay.
- [Scene organization](https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html)
  for reusable scene dependencies.
- [Containers](https://docs.godotengine.org/en/stable/tutorials/ui/gui_containers.html)
  and [GUI navigation](https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html)
  for layout and keyboard/controller focus.
- [Animation](https://docs.godotengine.org/en/stable/tutorials/animation/index.html),
  [audio](https://docs.godotengine.org/en/stable/tutorials/audio/index.html), and
  [rendering](https://docs.godotengine.org/en/stable/tutorials/3d/index.html)
  for the subsystem actually being changed.
- [Performance](https://docs.godotengine.org/en/stable/tutorials/performance/index.html)
  for profiling and platform-specific bottlenecks.

Consult [validation](debugging-testing-export.md) before running the project.
Screenshots can show layout and appearance; they do not prove input, animation,
audio, performance, or accessibility behavior.
