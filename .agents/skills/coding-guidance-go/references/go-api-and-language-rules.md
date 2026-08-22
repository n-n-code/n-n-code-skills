# Go API And Language Rules

Load this reference when a Go task materially changes API shape, exported
contracts, interface placement, naming, declarations, generics, or collection
semantics.

## Control flow and declarations

- Prefer clarity, simplicity, concision, maintainability, then local
  consistency.
- Keep the normal path unindented. Handle errors and special cases first; omit
  `else` after terminating control flow.
- Use `if` or `switch` initialization to reduce scope, but avoid `:=` shadowing
  that leaves an outer variable unchanged.
- Use `var` for intentional zero values and package-level declarations. Use
  `:=` for local values with obvious types.
- Always assign the result of `append`; the backing array may change.
- Decide whether nil and empty maps, slices, and channels are equivalent before
  exposing them, especially in wire formats.
- Copy slices and maps at API boundaries when caller mutation would violate
  invariants or returned state should be immutable to callers.

## Names and exported contracts

- Use MixedCaps identifiers, consistent initialisms such as `URL`, `ID`, and
  `HTTP`, and short receiver names that stay consistent across a type's methods.
- Avoid names that repeat package or receiver context: prefer `widget.New()` to
  `widget.NewWidget()` and `p.Name()` to `p.ProjectName()`.
- Document exported packages, types, functions, methods, constants, and
  variables with comments that start with the exported name and read as
  complete sentences.
- Treat exported identifiers, module paths, JSON, database, protobuf, and
  OpenAPI tags, CLI flags, file formats, metrics, and log fields as
  compatibility boundaries.

## Interfaces and generics

- Define interfaces at the consumer side unless the producer owns a stable
  abstraction used by many consumers.
- Keep interfaces as small as their consumer contract allows. Exposing methods
  the consumer does not need often hides a concrete type without adding a real
  abstraction.
- Accept interfaces and return concrete types by default. Return an interface
  when the implementation is intentionally hidden behind a stable standard or
  package-owned abstraction.
- Start with concrete code. Add generics only when multiple types share
  identical logic and interfaces do not model the behavior cleanly.
- Keep generic constraints minimal. Prefer standard constraints such as
  `comparable` or `cmp.Ordered` when supported; do not over-constrain unions.
