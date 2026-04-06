---
name: backend-guidance
description: Overlay for server-side networked code — HTTP handlers, gRPC services, message consumers. Use alongside the repo's implementation skill when implementing or reviewing backend logic.
---

# Backend Guidance

This is a composable overlay, not a standalone workflow.
Use alongside the repo's implementation skill (e.g. **coding-guidance-cpp**, **project-core-dev**)
when the change touches backend code.

Use this as the thin default backend overlay for ordinary backend work.
If the task includes service-boundary refactors, repository or transaction work,
queue or webhook reliability, stronger testing expectations, or explicit
trust-boundary hardening, prefer `backend-systems-guidance`.

## When to use

The repo has server-side networked code: HTTP route handlers, gRPC service
methods, message/event consumers, or similar request-processing pipelines.

## Not for

HTTP client code, CLI tools that make outbound requests, batch processors, or
offline data pipelines. These do not have the handler/service/boundary shape
this skill addresses.

## Rules

- Keep handlers thin in responsibility, not by literal line count — parse
  input, call a service function, map transport concerns, serialize output. If
  a handler starts owning business decisions, extract that logic into a service
  or core module.
- Keep business logic testable without transport — no HTTP context, no gRPC
  metadata leaking into domain functions.
- Isolate data access behind an interface when it simplifies testing. Do not
  add an abstraction layer when the data access is trivial or test-only.
- Validate and sanitize external input at the boundary, before it reaches
  business logic. Internal calls between trusted modules do not need redundant
  validation.
- Keep boundary-only concerns at the edge: authentication, authorization,
  request decoding, transport-specific error mapping, and idempotency checks
  where applicable.
- Use dependency injection where it makes tests simpler — not as a default
  architectural pattern.

## Decision Heuristics

- **Handler size:** if a handler is hard to read in one screen or mixes
  transport concerns with business decisions, it is doing too much. Extract the
  logic; keep the handler as glue.
- **Test smell:** if testing a function requires standing up a server or faking
  a transport layer, the function has a boundary problem. Move the logic
  inward.
- **Validation placement:** validate once, at the outer edge. If you find
  validation scattered across layers, consolidate it at the boundary.

## Validation

A backend change is done when (in addition to the base implementation skill's
validation):

- handlers delegate to testable service functions
- business logic tests run without transport dependencies
- external input is validated at the boundary
- transport-specific error handling stays at the boundary instead of leaking
  into domain logic
