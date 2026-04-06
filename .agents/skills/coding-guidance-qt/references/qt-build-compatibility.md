# Qt Build Compatibility

Open this reference only when the task touches CMake, generated Qt build steps,
or real Qt5/Qt6 compatibility requirements.

## Use when

- the repo claims support for both Qt5 and Qt6
- `CMakeLists.txt` contains hard-coded `Qt5::` or `Qt6::` targets
- generated-code inputs such as moc, uic, or qrc are part of the failure
- a build works on one Qt version and fails on the other

## Core patterns

- Prefer version-driven discovery over hard-coded target families:

```cmake
find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core Widgets)
```

- Prefer version-driven targets:

```cmake
target_link_libraries(myapp
    Qt${QT_VERSION_MAJOR}::Core
    Qt${QT_VERSION_MAJOR}::Widgets
)
```

- In Qt6-first repos that are not already standardized on a stable local
  pattern, prefer Qt's helper commands such as
  `qt_standard_project_setup()` and `qt_add_executable()` over ad hoc Qt target
  setup.

- Treat moc, uic, and qrc changes as build-contract changes, not local cleanup.

## Review hotspots

- hard-coded `Qt5::` / `Qt6::` targets in a repo that claims both
- new hand-rolled CMake setup in a Qt6-first repo where Qt helper commands
  would be clearer and less error-prone
- generated headers or sources not regenerated after class-shape changes
- stale `Q_OBJECT` additions that compile only because one platform cached old
  generated files
- resource lookups that depend on the current working directory

## Validation

- configure and build each claimed Qt variant
- verify generated-code inputs are part of the build graph
- smoke-test the changed UI path on at least one affected platform
