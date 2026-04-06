# Backend Systems Guidance Trigger Evals

Use these prompts to spot over-triggering and boundary drift between
`backend-guidance` and `backend-systems-guidance`.

## Expected `backend-guidance`

- "Fix this HTTP handler so it stops doing auth checks inline and just calls the service."
- "Clean up this gRPC method and move input parsing to the boundary."
- "Review this small message consumer and make sure transport concerns stay at the edge."

## Expected `backend-systems-guidance`

- "Add idempotent webhook handling with retries, timeout rules, and integration tests."
- "Refactor this endpoint stack into controller, service, and repository layers and check for N+1 queries."
- "Review this backend change for auth gaps, transaction boundaries, outbound request safety, and missing tests."

## Expected Neither

- "Tune this HTTP client retry policy for outbound SDK calls."
- "Threat-model our auth system and list likely attack paths."
- "Set up Kubernetes deployment manifests and production dashboards."

## Manual Simulation Summary

Prompts used:

- positive-obvious: "Refactor this endpoint stack into controller, service, and repository layers and check for N+1 queries."
- positive-paraphrased: "This backend change touches retries, auth, and webhook deduplication. Use the stronger backend overlay."
- negative-adjacent: "Tune this HTTP client retry policy for outbound SDK calls."

What passed:

- obvious multi-layer backend work points clearly to `backend-systems-guidance`
- paraphrased reliability and trust-boundary work still triggers the stronger
  overlay
- outbound-client-only work stays out of scope

Residual risk:

- backend review requests may still need judgment when they are narrow enough to
  fit `backend-guidance`
- if the stronger overlay grows more review-specific, re-check whether a
  companion review overlay would be cleaner
