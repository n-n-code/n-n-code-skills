# Packaging and layout

Use this reference only when the Python task affects distribution, package
layout, imports across package boundaries, or published CLI entrypoints.

- Prefer `pyproject.toml` as the packaging configuration source of truth
- Treat import paths, console entrypoints, and published metadata as
  compatibility boundaries, not routine refactor detail
- Prefer `src/` layout for distributable libraries unless the repo has a clear
  reason not to
- For typed libraries, ship `py.typed` and keep runtime dependencies distinct
  from dev-only tooling
- After package-layout changes, verify imports from an installed or package-like
  context rather than trusting local source-tree imports alone
- After CLI packaging changes, run a narrow entrypoint smoke test so broken
  console-script wiring is caught early
