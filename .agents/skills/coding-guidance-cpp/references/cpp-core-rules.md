# C++ Core Rules

Read this reference when a C++ task needs a detailed correctness or API-design
checklist beyond the critical defaults in `SKILL.md`.

## Construction, ownership, and lifetime

- Treat raw pointers and references as non-owning; never transfer ownership by
  raw pointer or reference.
- Avoid `new` and `delete`; bind resource lifetime to object lifetime with RAII.
- Prefer `std::unique_ptr` by default; use `std::shared_ptr` only for real shared
  lifetime and `std::weak_ptr` to break cycles.
- Prefer values and stack allocation when ownership is simple.
- Prefer rule-of-zero types; justify custom destructors or special members.
- Initialize objects into valid states and establish invariants during
  construction.
- Do not store or return references, views, iterators, or pointers into
  temporaries or short-lived owners. Use an owning value when the lifetime proof
  is unclear.
- Treat moved-from objects as valid but semantically narrow; destroy, reassign,
  or call only operations whose post-move contract is explicit.
- Do not cross callback, coroutine-suspend, async, or thread-handoff boundaries
  with borrowed state unless the lifetime proof is explicit.

## Type, bounds, and representation safety

- Avoid unchecked bounds access; prefer `.at()`, iterators, range-for, or
  `std::span` when bounds are uncertain.
- Avoid silent narrowing. Use deliberate casts or narrowing helpers.
- Avoid signed/unsigned comparison traps; use `std::cmp_*`, `std::in_range`, or
  a deliberate common type when integer domains differ.
- Prefer compile-time checking when the type system can express the rule.
- Avoid C-style casts; choose the C++ cast that exposes the intended operation.
- Prefer `std::bit_cast` or byte-wise copy for object-representation work. Do
  not use `reinterpret_cast` where aliasing or lifetime rules make behavior
  fragile.
- Avoid raw memory APIs, `memset` or `memcpy` tricks, and pointer arithmetic on
  non-trivial, polymorphic, or lifetime-sensitive types.
- Apply const-correctness deliberately. Use `constexpr` when compile-time
  evaluation is part of the contract and the repository target supports it.
- Prefer `enum class` over plain enums and `nullptr` over `NULL`.
- Prefer `std::array` over C arrays, `std::string_view` for non-owning strings,
  and `std::span` for non-owning ranges when their lifetimes are clear.

## API contracts and call-site clarity

- Do not mix exception and error-code styles inconsistently within one path.
- Do not ignore must-check results from allocation, parsing, synchronization,
  numeric conversion, or OS and library APIs when failure changes behavior.
- Use `[[nodiscard]]` when ignoring a result is likely a bug.
- Prefer explicit constructors, conversions, and named types when ownership,
  units, or semantics would otherwise be implicit.
- Avoid forwarding, overload, and default-argument combinations that make calls
  ambiguous or silently select the wrong overload.
- Use `override` at virtual boundaries and avoid signature near-misses.
- Keep declarations and definitions consistent across headers and sources,
  including qualifiers, defaults, parameter meaning, and ownership cues.
- Treat adjacent same-type parameters as call-site pressure. Use named types,
  parameter objects, or strong typedefs when they make misuse harder.
- Encode units, domains, nullability, and sentinel states in types rather than
  comments, magic values, or positional conventions.

## Headers, globals, and build surface

- Avoid `using namespace std` in headers.
- Keep warnings at zero in repository-owned code.
- Keep macros narrow, parenthesized, side-effect-safe, and out of API shaping;
  prefer language features unless a macro is the clearest available tool.
- Avoid reserved identifiers, namespace pollution, and definitions in headers
  that quietly alter ODR or rebuild behavior.
- Keep include sets minimal and explicit; avoid include cycles and dependence on
  transitive includes.
- Use `constinit` for non-local static or thread-local objects that must not rely
  on dynamic initialization.
- Prefer compile-time constants, local statics, or explicit startup wiring over
  hidden global initialization side effects.

## Concurrency, testability, and modern defaults

- Prefer structured thread ownership and explicit cancellation over detached
  threads or ad hoc stop flags. `std::jthread` and `std::stop_token` are useful
  when the repository already uses compatible standard primitives.
- Assume container mutation may invalidate iterators, references, pointers, and
  views unless the container contract says otherwise.
- Keep core logic testable without real threads, clocks, filesystems, process
  state, or ambient globals when the domain does not require them.
- Prefer `std::optional`, `std::variant`, and, when supported, `std::expected`
  when they encode domain states better than sentinels.
- Prefer standard algorithms and ranges over open-coded loops when they make
  intent clearer.
- Prefer standard language and library replacements for deprecated,
  legacy-C-leaning, or handwritten utilities when the toolchain supports them
  and the replacement is clearer.
