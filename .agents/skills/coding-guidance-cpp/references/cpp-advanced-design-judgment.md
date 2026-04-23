# C++ Advanced Design Judgment

Load this reference when the C++ task needs deeper API, error-model, header,
concurrency, or advanced-language-feature judgment than the main skill should
carry by default.

## Advanced feature selection

- Use C++20 or C++23 features when they make contracts clearer, not to signal
  modernity.
- Use `consteval` only when every call must be a compile-time evaluation.
- Use concepts to constrain templates when the constraint is part of the public
  contract; avoid them for local cleverness.
- Use ranges when they improve readability; avoid long adaptor pipelines that
  hide cost or control flow.
- Use `std::span` and `std::string_view` for non-owning parameters only when
  the caller can satisfy the lifetime contract clearly.
- Use forwarding references only when perfect forwarding is the actual
  contract; otherwise prefer plain overloads, values, or `const&`.
- Use coroutines only when the repo already embraces them or when they simplify
  asynchronous control flow more than callback, future, or thread-based
  alternatives.
- In coroutine code, avoid captured or reference state that may outlive the
  source scope, and do not suspend while holding locks or other scoped guards.
- Do not introduce template metaprogramming, custom allocators, or exotic
  zero-cost abstractions unless measurement or reuse pressure justifies them.

## Error and contract model

- Pick one primary error model per subsystem: exceptions, status-return, or
  `std::expected`; cross-model adapters should be explicit at boundaries.
- Use exceptions for exceptional failures only when the repo and call graph are
  already built around exception safety.
- Prefer return-value error models where failure is routine, expected, or part
  of normal control flow.
- Mark destructors, `swap`, and move operations `noexcept` when that matches
  reality; throwing moves silently degrade container behavior and can weaken
  strong exception guarantees.
- State ownership, nullability, lifetime, and thread-safety contracts in the
  type system when possible, and in comments only when the type system cannot
  express them cleanly.
- Public APIs should make invalid states hard to represent and expensive states
  visible to callers.
- Prefer parse and conversion APIs that report failure explicitly; unchecked
  string-to-number and narrowing paths are common production defects.

## Headers and interfaces

- Minimize header surface; prefer forward declarations when they reduce stable
  dependencies without obscuring the contract.
- Do not put heavy includes, macros, or implementation-only dependencies in
  public headers without a clear reason.
- Keep inline and template-heavy code in headers only when required by the
  language or justified by measurement.
- Be deliberate with namespace-scope initialization; prefer `constexpr`,
  `constinit`, or function-local statics over cross-translation-unit dynamic
  initialization.
- Prefer free functions or narrow interfaces over large classes that force
  unnecessary rebuild and dependency coupling.
- Be explicit when ABI stability, plugin boundaries, or C interop constrain the
  design.
- Treat rebuild surface, transitive include fan-out, and template instantiation
  cost as design costs, not just build-system problems.
- Avoid anonymous namespaces, non-inline definitions, and hidden state in
  headers when those choices change linkage or duplicate objects across
  translation units.
- Keep include ordering, guards, and dependency direction consistent with repo
  conventions; header hygiene is part of correctness, not just style.

## Concurrency and synchronization

- Make thread ownership and synchronization strategy explicit; "probably
  thread-safe" is not a contract.
- Prefer message passing, task ownership, or data partitioning before shared
  mutable state.
- Protect invariants, not individual fields; lock scope should match the real
  consistency boundary.
- Use atomics only when the memory-ordering contract is understood and simpler
  locking would not be clearer.
- Treat coroutine, callback, and thread handoff points as lifetime hazards.
- Do not use async-signal-unsafe functions, cancellation modes, or wake-up
  assumptions that break library contracts under contention or interruption.

## APIs and abstraction

- Functions should do one thing, stay at one level of abstraction, and justify
  more than two meaningful parameters.
- Treat boolean flag parameters as a design smell; split behavior or introduce
  a parameter object when that makes the contract clearer.
- Prefer composition and value semantics over inheritance unless polymorphism is
  the actual domain model.
- Avoid config-bag APIs where many weakly related booleans, enums, or strings
  simulate a missing type.
- Make ownership and mutation visible at API boundaries; hidden allocation,
  caching, or global state is a design smell in clean-looking code.
- Be suspicious of abstractions that look tidy but add virtual dispatch,
  allocation, copies, or lifetime coupling without a clear benefit.
- Be suspicious of public template abstractions that improve local elegance but
  increase compile time, error verbosity, or rebuild cost across the repo.
- Prefer moving implementation detail out of headers when doing so preserves the
  contract and reduces dependency drag.
- Prefer parameter names and call sites that communicate semantics directly;
  ambiguous names, magic literals, and comment-only argument meaning are review
  smells.
