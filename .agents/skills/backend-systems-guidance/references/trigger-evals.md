# Backend Systems Guidance Trigger Evals

Use these prompts to spot over-triggering and boundary drift between
`backend-guidance` and `backend-systems-guidance`.

## Expected `backend-guidance`

- "Fix this thin HTTP handler so it authenticates at ingress, delegates shared authorization to the existing service policy, and maps domain errors."
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

## Static Prediction Record

These are description-and-instruction predictions, not observed host routing.

| Case | Expected primary | Expected companions | Selection to avoid | Surface | Method | Context | Comparison | Result | Failure class | Residual risk |
|---|---|---|---|---|---|---|---|---|---|---|
| "Refactor this endpoint stack into controller, service, and repository layers and check for N+1 queries." | `backend-systems-guidance` | matching implementation skill | `backend-guidance` alone | activation | static prediction | N/A | none | pass | N/A | host routing not observed |
| "This backend change touches retries, authorization, and webhook deduplication." | `backend-systems-guidance` | matching implementation skill | `backend-guidance` alone | activation | static prediction | N/A | none | pass | N/A | host routing not observed |
| "Tune this HTTP client retry policy for outbound SDK calls." | matching client or implementation guidance | none | both backend overlays | activation | static prediction | N/A | none | pass | N/A | host routing not observed |
| "Review this protected endpoint for authorization bypasses, but do not edit files." | `security` | matching backend overlay when implementation structure matters | mutating backend workflow | activation | static prediction | N/A | none | pass | N/A | host routing not observed |

Residual risk:

- backend review requests may still need judgment when they are narrow enough to
  fit `backend-guidance`
- if the stronger overlay grows more review-specific, re-check whether a
  companion review overlay would be cleaner
