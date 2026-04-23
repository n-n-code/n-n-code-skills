# Go Performance And Modules

Load this reference for package/module layout, dependency decisions, generated
code, release metadata, profiling, hot-path allocation work, or build-surface
changes.

## Packages

- Keep packages cohesive and small enough that their exported names form a clear
  vocabulary.
- Split by responsibility or user boundary, not by file length.
- Avoid generic package names such as `util`, `common`, `helper`, and `misc`.
  Name packages for what they provide.
- Avoid import cycles by moving shared contracts to a lower package or splitting
  responsibilities, not by adding late globals or vague common packages.
- Keep `internal/` packages for code that should not become public API by
  accident.
- Avoid `init` for non-trivial wiring. Prefer explicit construction in `main`,
  tests, or dependency setup.
- Call `os.Exit` or `log.Fatal` only in `main`, preferably through a `run()`
  function that returns an error.

## Modules And Dependencies

- Keep `go.mod` and `go.sum` changes minimal and explain dependency additions.
- Run `go mod tidy` only when module files should change.
- Treat `replace`, `retract`, workspace `go.work`, vendoring, and private module
  settings as build-contract changes.
- Do not leak local paths into shared module files.
- Do not add a dependency for tiny helpers the standard library already covers.
- Consider license, binary size, supply-chain, and transitive dependency cost
  before adding modules.
- Use `go mod verify`, `go mod why`, or the repo's dependency audit path when a
  module change is suspicious or release-facing.

## Build Tags And Generation

- Use build tags deliberately and test tagged variants when behavior depends on
  them.
- Keep `go generate` directives deterministic and scoped.
- Track generator tool dependencies with the repo's established pattern, often
  a `tools.go` file guarded by a `tools` build tag.
- Do not commit generated output unless the repo normally commits generated
  output for that generator.
- Keep generated code, vendored code, and app-owned code boundaries explicit.

## Release Metadata

- Preserve or add version/build metadata only through the repo's build pipeline.
- Avoid ad hoc `ldflags` or generated version files that make local builds
  unreproducible.
- Treat CLI flags, file formats, metrics, log field names, and wire schemas as
  compatibility boundaries.

## Configuration

- Do not hardcode environment-specific configuration in libraries or deep
  packages.
- Parse env, flags, and config files at process boundaries.
- Validate configuration once and pass typed configuration inward.
- Prefer explicit constructor parameters or config structs for required
  settings. Use functional options for public or extensible constructors with
  several optional settings.

## Performance Workflow

1. State the performance claim and the suspected bottleneck.
2. Establish a baseline with benchmarks, `pprof`, execution traces, allocation
   profiles, or production telemetry.
3. Make the narrowest change that addresses the measured bottleneck.
4. Re-run the same measurement and compare before/after signal.
5. Keep the change only when the gain matters and the readability or complexity
   cost is justified.

## Performance Rules

- Optimize after measurement, except for obvious algorithmic, allocation, or I/O
  mistakes on hot paths.
- Use `pprof`, execution traces, or benchmark profiles to identify CPU, heap,
  goroutine, mutex, block, and allocation bottlenecks before reshaping code for
  performance.
- Preallocate slices and maps when the approximate size is known.
- Use `strings.Builder` for repeated string construction, `strings.Join` for
  joining slices, and `strconv` instead of `fmt` for hot primitive conversions.
- Prefer values over pointers when copying is cheap and mutation or nil is not
  part of the contract.
- Avoid reflection in hot paths or public data plumbing unless it materially
  reduces complexity and the cost is measured or irrelevant.
- Use `sync.Pool` only for frequently allocated temporary objects on measured
  hot paths; reset pooled values before putting them back.
