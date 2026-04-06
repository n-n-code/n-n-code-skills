# Clang-Tidy-derived guidance for `coding-guidance-cpp`

This note records how the current `clang-tidy` catalog at
<https://clang.llvm.org/extra/clang-tidy/checks/list.html> was triaged for this
principle skill.

Use it to keep the skill aligned with the tool without turning the main
`SKILL.md` into an analyzer index.

## Goal

Extract portable engineering guidance from the full check list while keeping
repo-local style policy, platform quirks, and library-pack rules out of the
default skill.

## What belongs in the principle skill

These check families reinforce portable C++ guidance and should shape the main
skill wording:

- `bugprone-*`: dangling handles, unchecked optional/status access, suspicious
  arithmetic, overload mistakes, swapped arguments, use-after-move, macro
  hazards, raw-memory misuse, dangerous static initialization, signal-handler
  mistakes
- `cppcoreguidelines-*`: ownership, bounds, initialization, special members,
  slicing, varargs avoidance, globals, narrowing, virtual-destructor safety,
  coroutine hazards
- `modernize-*`: safer language/library defaults such as `override`,
  `nullptr`, `[[nodiscard]]`, `noexcept`, member initializers, safer factory
  functions, constrained templates, and standard replacements for deprecated
  constructs
- `performance-*`: avoid accidental copies, hidden reallocations, ineffective
  moves, slow string and container patterns, and obviously inefficient
  algorithms
- `misc-*`: header definitions, include cycles, identifier confusion,
  const-correctness, recursion, hostile RAII/coroutine interactions, custom
  `new`/`delete` pitfalls
- `portability-*`: non-portable headers and constructs, assembler usage,
  pragma-specific assumptions, allocator and template patterns with toolchain
  or ABI risk
- `readability-*`: argument clarity, complexity, brace consistency, implicit
  bool conversion, magic numbers, declaration isolation, redundant casts, and
  smart-pointer misuse at call sites
- CERT and HIC++ aliases: useful because they cluster around real correctness
  and safety concerns, but most are already covered by the families above

## What should stay out of the principle skill

These families are real, but too repo-, platform-, framework-, or vendor-
specific to bake into portable default guidance:

- `abseil-*`, `boost-*`: library-pack conventions for repos that depend on
  those ecosystems
- `altera-*`, `mpi-*`, `openmp-*`: specialized parallel or accelerator domains
- `android-*`, `darwin-*`, `fuchsia-*`, `linuxkernel-*`, `zircon-*`: OS- or
  platform-specific policy
- `google-*`, `llvm-*`: style-pack and ecosystem-specific conventions
- `objc-*`: Objective-C specific
- `clang-analyzer-*`: valuable when available, but they represent a different
  analyzer layer than portable C++ coding guidance

For these, prefer repo-local `clang-tidy` config, a domain overlay, or explicit
project documentation.

## Signals worth emphasizing in future revisions

The full catalog strongly suggests these themes deserve explicit wording in the
main skill:

- construction and initialization correctness
- borrowed-lifetime hazards across async and coroutine boundaries
- overload and parameter-list designs that invite swapped or ambiguous calls
- header hygiene as a correctness and build-surface concern
- macro and identifier discipline
- unchecked conversions, parsing, and status-return paths
- modern replacements for deprecated or C-leaning constructs when the repo can
  support them
- performance guidance framed as “avoid obvious cost leaks,” not “micro-opt by
  default”

## Easy-to-miss checks worth remembering

These are not separate principles, but they are good reminders because they
reveal failure modes that teams often underweight:

- swapped or easily-swappable arguments: a signal to redesign the API, not just
  annotate call sites
- default-argument and overload interactions: small convenience features can
  quietly turn into ambiguous or wrong-call hazards
- coroutine capture and suspend-with-lock hazards: async code often fails at
  lifetime and scope boundaries, not in the happy-path logic
- dynamic or throwing static initialization: startup order and initialization
  side effects deserve the same design scrutiny as normal runtime code
- raw-memory operations on non-trivial types: “fast” low-level code is often
  just undefined behavior with a familiar shape
- ineffective move patterns and hidden copies: performance reviews should look
  for semantic cost leaks before algorithm heroics
- suspicious string, numeric-conversion, and status-access paths: parsing and
  boundary code remain a dense source of production defects

## Maintenance rule

When the clang-tidy catalog grows:

1. Check whether a new family exposes a portable semantic issue or only a repo-
   specific policy.
2. If it is portable and high-signal, fold the principle into `SKILL.md`.
3. If it is narrow, move it into repo config, a domain overlay, or leave it in
   this reference note.
4. Prefer consolidating by design issue, not by adding one bullet per analyzer
   check.
