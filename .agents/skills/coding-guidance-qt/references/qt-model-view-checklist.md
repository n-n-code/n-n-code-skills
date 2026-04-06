# Qt Model View Checklist

Open this reference when the task touches `QAbstractItemModel`,
`QAbstractProxyModel`, selection models, custom roles, resets, or view/model
interaction bugs.

## Core rules

- Treat `data()`, `flags()`, `headerData()`, role names, and index validity as
  compatibility-facing contracts
- Use the correct `begin*/end*` pair for structural changes; do not emit data
  change signals as a substitute for inserts, removes, or moves
- Use model reset only when the model contract truly resets; prefer narrower
  notifications when the structure is still meaningfully stable
- Keep selection state, current index, and persistent index assumptions explicit
  when rows move, reset, or disappear

## Review hotspots

- `dataChanged` emitted where rows were inserted, removed, or moved
- indexes created or consumed without validating parent, row, column, or model
- custom roles added without stable names or without updating the view path that
  depends on them
- view code caching model-derived state that becomes stale after reset or move
- delegates or views depending on side effects in `data()` or paint-time logic

## Validation

- verify the affected view path with inserts, removes, updates, and empty-model
  cases
- confirm selection/current-index behavior after reset, move, or deletion
- add deterministic model tests where the contract is subtle or previously
  broken
