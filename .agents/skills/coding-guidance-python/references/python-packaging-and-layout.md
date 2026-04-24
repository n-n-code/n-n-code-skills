# Packaging and layout

Use this reference only when the Python task affects distribution, package
layout, imports across package boundaries, or published CLI entrypoints.

## Use when

- editing `pyproject.toml`, `setup.cfg`, package metadata, package data, or
  console scripts
- moving modules across import boundaries or deciding between flat and `src/`
  layout
- changing a distributable library, plugin, CLI, or typed package contract

Do not load this reference for ordinary single-module bug fixes that do not
touch imports, packaging metadata, or published entrypoints.

## Rules

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
