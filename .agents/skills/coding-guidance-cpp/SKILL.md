---
name: coding-guidance-cpp
description: C++ implementation and review skill. Use when writing, modifying, refactoring, or reviewing C++ code, especially modern C++17/20/23 code that needs strong ownership, type safety, and testable design. Portable across C++ repos and build systems.
---

# C++ Coding Guidance

This skill adds portable C++ implementation, refactoring, and review guidance.

## Adjacent Skills

This skill provides portable C++ engineering principles. Compose with:

- **Workflow:** **thinking** (planning), **recursive-thinking** (stress-testing),
  **security** (threat modeling)
- **Domain overlays:** **backend-guidance** (server-side code),
  **backend-systems-guidance** (stronger backend architecture, reliability, and
  trust-boundary work),
  **ui-guidance** (graphical UI/web frontend),
  **project-core-dev** (repo-specific build/test commands)

## When Not to Lean on This Skill

- non-C++ work
- legacy or bare-metal environments where modern C++ guidance must be adapted
  selectively
- pure architecture or process work with no C++ design or code judgment needed
- repo-specific style packs or platform policies that should be enforced by
  local `clang-tidy`, compiler, or overlay rules rather than a portable
  principle skill

## Boundary Contract

Keep this skill focused on portable C++ engineering judgment.

- Put repo-specific exception policy, warning policy, formatter choices, and
  include-order rules in repo config or repo docs
- Put style-pack rules from ecosystems such as Google, LLVM, Abseil, or
  platform/vendor bundles in repo config or overlays, not here
- Put library- or platform-specific API policy in repo config or a domain
  overlay
- When a rule is analyzer-shaped but not portable, keep it in `clang-tidy`
  config or the reference note rather than adding it to the main skill

## Implementation Workflow

1. Read the touched code, build shape, existing tests, and any nearby docs or
   shorthand notes before editing.
2. If the request is partially specified, infer the intended behavior from the
   existing code and tests. Ask only when multiple plausible C++ designs would
   change semantics.
3. Choose the narrowest change that solves the problem without hiding ownership,
   lifetime, or error-handling contracts.
4. Implement with simple, strongly typed interfaces and modern C++ defaults.
5. Add or update tests close to the changed behavior.
6. Run the narrowest relevant format, build, test, sanitizer, and analyzer
   targets the repo supports.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current behavior, invariants, side effects, and risky hotspots.
2. Break the refactor into small slices that preserve behavior.
3. Remove duplication, long functions, or muddled responsibilities one step at
   a time.
4. Keep tests passing after each slice; add characterization coverage first when
   behavior is unclear.
5. Stop when the code is simpler and safer.

## Review Workflow

When reviewing (not implementing), skip the implementation workflow and use this
instead:

1. Read the change in full before commenting.
2. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
3. Prioritize bugs and regressions, ownership and lifetime errors, exception or
   error-path holes, thread-safety issues, security risks, performance mistakes
   with real impact, and missing tests.
4. State findings with concrete evidence and the likely consequence.

## C++ Rules

Read these by failure theme, not as an exhaustive checklist.

### Construction, ownership, and lifetime

- Treat raw pointers and references as non-owning; never transfer ownership by
  raw pointer or reference
- Avoid `new` and `delete`; bind resource lifetime to object lifetime with RAII
- Prefer `std::unique_ptr` by default; use `std::shared_ptr` only for real
  shared lifetime and `std::weak_ptr` to break cycles
- Prefer values and stack allocation over heap allocation when ownership is
  simple
- Prefer rule-of-zero types; if you write a destructor or custom special member
  function, justify it
- Initialize objects into valid states immediately; construction should
  establish invariants instead of relying on later “remember to initialize”
  steps
- Do not store or return references, views, iterators, or pointers into
  temporaries or short-lived owners; when the lifetime proof is not obvious,
  return or store an owning value instead
- Treat moved-from objects as valid but semantically narrow; only destroy,
  reassign, or call operations whose post-move contract is explicit
- Do not cross async, callback, coroutine-suspend, or thread-handoff
  boundaries with borrowed state unless the lifetime proof is explicit

### Type, bounds, and representation safety

- Avoid unchecked bounds access; prefer `.at()`, iterators, range-for, or
  `std::span` when bounds are uncertain
- Avoid silent narrowing conversions; use explicit casts or narrowing helpers
- Avoid signed/unsigned comparison traps; use `std::cmp_*`, `std::in_range`,
  or a deliberate common type when integer domains differ
- Prefer compile-time checking to runtime checking when the type system can
  express the rule
- Avoid C-style casts; use `static_cast`, `const_cast`, `reinterpret_cast`, and
  `dynamic_cast` deliberately
- Prefer `std::bit_cast` or byte-wise copy for object-representation
  reinterpretation; do not use `reinterpret_cast` where aliasing or lifetime
  rules make the behavior fragile
- Avoid raw memory APIs, `memset`/`memcpy` tricks, or pointer arithmetic on
  non-trivial, polymorphic, or lifetime-sensitive types
- Use `const` and `constexpr` by default; mutability should be the exception
- Prefer `enum class` over plain enums and `nullptr` over `NULL`
- Prefer `std::array` over C arrays, `std::string_view` for non-owning strings,
  and `std::span` for non-owning ranges when lifetime rules are clear

### API contracts and call-site clarity

- Do not mix exception and error-code styles inconsistently inside one path
- Do not ignore must-check results from allocation, parsing, synchronization,
  numeric conversion, or OS/library APIs when failure changes behavior
- Use `[[nodiscard]]` when ignoring a result is likely a bug
- Prefer explicit constructors, conversions, and named types when ownership,
  units, or semantics would otherwise be implicit
- Avoid forwarding, overload, and default-argument combinations that make calls
  ambiguous or silently select the wrong overload
- Treat virtual dispatch boundaries as bug-prone: use `override`, avoid near
  misses, and do not rely on shadowing or signature accidents
- Keep declarations and definitions consistent across headers and sources:
  parameter names, qualifiers, defaults, and ownership cues should not drift
- Be suspicious of adjacent same-type parameters; named types, parameter
  objects, or strong typedefs are often clearer than comments
- Prefer interfaces that make argument order hard to misuse and bool/int/string
  sentinels hard to confuse
- Prefer APIs that encode units, domains, and nullability in types rather than
  relying on comments, magic values, or positional conventions

### Headers, globals, and build surface

- Avoid `using namespace std` in headers
- Keep warnings at zero in repo-owned code
- Keep macros narrow, parenthesized, side-effect-safe, and out of API shaping;
  prefer language features unless a macro is the least-bad tool
- Avoid reserved identifiers, namespace pollution, and definitions in headers
  that quietly change ODR or rebuild behavior
- Prefer include sets that are minimal and explicit; unused includes, include
  cycles, and transitive-include dependence are design smells
- Use `constinit` for non-local static or thread-local objects that must not
  rely on dynamic initialization
- Prefer compile-time constants, local statics, or explicit startup wiring over
  hidden global initialization side effects

### Concurrency, async, and testability

- Prefer structured thread ownership and explicit cancellation over detached
  threads or ad hoc stop flags; `std::jthread` and `std::stop_token` are good
  defaults when the codebase already uses standard thread primitives
- Assume container modifications may invalidate iterators, references, pointers,
  and views unless the container contract says otherwise
- Prefer seams that keep core logic testable without real threads, clocks,
  filesystem, process state, or ambient globals when the domain does not
  require those dependencies

### Expressive modern defaults

- Prefer vocabulary types such as `std::optional`, `std::variant`, and
  `std::expected` when they encode real domain states better than sentinels or
  ad hoc conventions
- Prefer standard algorithms and ranges over open-coded loops when they make the
  intent clearer
- Prefer standard library and language replacements for deprecated,
  legacy-C-leaning, or handwritten utilities when the replacement is clearer
  and already acceptable in the repo toolchain

### Advanced feature selection

- Use C++20 or C++23 features when they make contracts clearer, not to signal
  modernity
- Use `consteval` only when every call must be a compile-time evaluation
- Use concepts to constrain templates when the constraint is part of the public
  contract; avoid them for local cleverness
- Use ranges when they improve readability; avoid long adaptor pipelines that
  hide cost or control flow
- Use `std::span` and `std::string_view` for non-owning parameters only when
  the caller can satisfy the lifetime contract clearly
- Use forwarding references only when perfect forwarding is the actual contract;
  otherwise prefer plain overloads, values, or `const&`
- Use coroutines only when the repo already embraces them or when they simplify
  asynchronous control flow more than callback, future, or thread-based
  alternatives
- In coroutine code, avoid captured or reference state that may outlive the
  source scope, and do not suspend while holding locks or other scoped guards
- Do not introduce template metaprogramming, custom allocators, or exotic
  zero-cost abstractions unless measurement or reuse pressure justifies them

### Design judgment - error and contract model

- Pick one primary error model per subsystem: exceptions, status-return, or
  `std::expected`; cross-model adapters should be explicit at boundaries
- Use exceptions for exceptional failures only when the repo and call graph are
  already built around exception safety
- Prefer return-value error models where failure is routine, expected, or part
  of normal control flow
- Mark destructors, `swap`, and move operations `noexcept` when that matches
  reality; throwing moves silently degrade container behavior and can weaken
  strong exception guarantees
- State ownership, nullability, lifetime, and thread-safety contracts in the
  type system when possible, and in comments only when the type system cannot
  express them cleanly
- Public APIs should make invalid states hard to represent and expensive states
  visible to callers
- Prefer parse and conversion APIs that report failure explicitly; unchecked
  string-to-number and narrowing paths are common production defects

### Design judgment - headers and interfaces

- Minimize header surface; prefer forward declarations when they reduce stable
  dependencies without obscuring the contract
- Do not put heavy includes, macros, or implementation-only dependencies in
  public headers without a clear reason
- Keep inline and template-heavy code in headers only when required by the
  language or justified by measurement
- Be deliberate with namespace-scope initialization; prefer `constexpr`,
  `constinit`, or function-local statics over cross-translation-unit dynamic
  initialization
- Prefer free functions or narrow interfaces over large classes that force
  unnecessary rebuild and dependency coupling
- Be explicit when ABI stability, plugin boundaries, or C interop constrain the
  design
- Treat rebuild surface, transitive include fan-out, and template instantiation
  cost as design costs, not just build-system problems
- Avoid anonymous namespaces, non-inline definitions, and hidden state in
  headers when those choices change linkage or duplicate objects across
  translation units
- Keep include ordering, guards, and dependency direction consistent with repo
  conventions; header hygiene is part of correctness, not just style

### Design judgment - concurrency and synchronization

- Make thread ownership and synchronization strategy explicit; “probably
  thread-safe” is not a contract
- Prefer message passing, task ownership, or data partitioning before shared
  mutable state
- Protect invariants, not individual fields; lock scope should match the real
  consistency boundary
- Use atomics only when the memory-ordering contract is understood and simpler
  locking would not be clearer
- Treat coroutine, callback, and thread handoff points as lifetime hazards
- Do not use async-signal-unsafe functions, cancellation modes, or wake-up
  assumptions that break library contracts under contention or interruption

### Design judgment - APIs and abstraction

- Functions should do one thing, stay at one level of abstraction, and justify
  more than two meaningful parameters
- Treat boolean flag parameters as a design smell; split behavior or introduce a
  parameter object when that makes the contract clearer
- Prefer composition and value semantics over inheritance unless polymorphism is
  the actual domain model
- Avoid “config bag” APIs where many weakly related booleans, enums, or strings
  simulate a missing type
- Make ownership and mutation visible at API boundaries; hidden allocation,
  caching, or global state is a design smell in “clean-looking” code
- Be suspicious of abstractions that look tidy but add virtual dispatch,
  allocation, copies, or lifetime coupling without a clear benefit
- Be suspicious of public template abstractions that improve local elegance but
  increase compile time, error verbosity, or rebuild cost across the repo
- Prefer moving implementation detail out of headers when doing so preserves the
  contract and reduces dependency drag
- Prefer parameter names and call sites that communicate semantics directly;
  ambiguous names, magic literals, and comment-only argument meaning are review
  smells

## Clang-Tidy-derived emphasis

Use the full `clang-tidy` catalog as a source of recurring failure modes, not as
a portable checklist to paste into every repo.

- Treat `bugprone`, `cppcoreguidelines`, `modernize`, `performance`, `misc`,
  `portability`, and the CERT/HIC++ aliases as high-signal prompts for code
  review and refactoring
- Fold only portable semantics into this principle skill; repo-specific naming,
  include order, formatter preferences, test-framework style, platform APIs,
  and library-pack rules belong in repo config or overlays
- If a repo ships `clang-tidy`, read its enabled checks before introducing new
  patterns; local suppressions and allowlists often document real constraints
- When multiple checks point at the same design issue, fix the design cause
  instead of satisfying each warning mechanically

## Resource map

- [references/clang-tidy-derived-guidance.md](references/clang-tidy-derived-guidance.md):
  triage of the current clang-tidy check catalog into portable principles,
  repo-level rules, and non-portable families that should stay out of this
  skill

## Decision Heuristics

Use these when the right choice is not obvious:

- **Scope check:** if a change touches more than 3 public interfaces, stop and
  plan before continuing; the change is bigger than it looks.
- **Ownership clarity:** if ownership is not obvious from the type signature,
  redesign the interface or add a one-line contract comment.
- **Error-model consistency:** do not mix exceptions, error codes, and
  `expected`-style returns within one subsystem unless the boundary is explicit.
- **Exception-safety pressure:** when mutating multi-step state, decide whether
  the operation offers no-fail, strong, or basic exception safety and structure
  the code to match.
- **Repo conventions:** if the repo has established rules for exceptions,
  containers, ownership types, or naming, follow them unless they create a
  correctness or safety problem.
- **Feature pressure:** do not introduce concepts, ranges, coroutines, or
  metaprogramming unless they make the code simpler for this repo's likely
  maintainers.
- **Interface pressure:** if a header starts dragging in broad dependencies or
  exposing implementation detail, narrow the interface before adding more code.
- **Build-surface pressure:** if a design pushes more logic, templates, or
  dependencies into public headers, justify the compile-time and rebuild cost.
- **Parameter pressure:** when adjacent parameters have the same type, or the
  function needs more than 2-3 meaningful inputs, prefer a named type or helper
  struct.
- **Lifetime pressure:** if a non-owning type crosses async, callback, return,
  or storage boundaries, prefer an owning type unless the lifetime proof is
  obvious from the interface.
- **Initialization pressure:** if correct behavior depends on a later
  “remember to initialize” step, move that requirement into construction or the
  type itself.
- **Call-site pressure:** if two arguments are easy to swap or a call needs
  comments to explain literals, redesign the API before adding more call sites.
- **Header pressure:** if a header starts accumulating definitions, globals,
  unnecessary includes, or hidden initialization, push behavior back behind a
  source boundary.
- **Testability pressure:** if a design forces tests to spin threads, sleep,
  touch the real filesystem, or patch globals just to exercise core logic,
  introduce a seam before adding more behavior.
- **Test setup size:** if test setup exceeds about 20 lines, extract a fixture
  only when the setup is reused or the test intent becomes unclear.
- **Narrowness vs. quality:** implement the narrowest change that solves the
  problem. When narrowness conflicts with correctness or safety, prefer
  correctness. When it conflicts with style alone, prefer narrowness unless the
  task is explicitly a cleanup.
- **Refactor boundary:** outside explicit refactor work, fix at most one small
  adjacent issue while you are in the file.
- **Abstraction threshold:** three similar code blocks or repeated API-shaping
  pain is a pattern; before extracting, check whether a free function, helper
  type, or composed object is the simpler move.
- **Performance rule:** optimize only after measurement, except for obvious
  ownership, allocation, or algorithmic mistakes on hot paths.
- **UB-sensitive optimization:** treat optimizations that rely on subtle
  lifetime, aliasing, or memory-order assumptions as high-risk until proven by
  evidence and tooling.

## Validation

A change is done when:

- the code compiles without new warnings, unless the repo explicitly treats a
  known warning set as baseline debt outside the change
- existing tests pass
- new or changed behavior has test coverage, or the lack of coverage is called
  out with a concrete reason
- the repo's formatter has been run
- configured static analyzers report no new findings
- available sanitizers are clean for the touched paths when the change affects
  memory safety, threading, or undefined-behavior risk
- performance-sensitive changes are measured instead of justified by intuition
- review findings at `Critical` and `Important` severity are addressed
