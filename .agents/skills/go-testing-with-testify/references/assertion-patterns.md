# Testify Assertion Patterns

Reference for `assert` / `require` usage. The SKILL.md names the rules; this
file shows the concrete shapes and the boundary cases. Load on demand.

## `assert` vs `require`

Both packages expose the same surface; the difference is failure behavior:

- `assert.Foo(t, …)` records a failure and continues. Subsequent
  assertions still run. Use for independent output checks in a row.
- `require.Foo(t, …)` records a failure and calls `t.FailNow()`. The test
  stops immediately. Use for preconditions whose failure makes the rest of
  the test meaningless.
- `require.*` must be called from the goroutine running the test. It is not a
  safe shortcut inside background goroutines.

Rule of thumb per line:

- `require.NoError(t, err)` on the call under test when the next line reads
  the return value. A nil receiver panic is worse than a stopped test.
- `require.NoError(t, setup(...))` on setup helpers.
- `assert.Equal(t, wantName, got.Name)` / `assert.Equal(t, wantAge, got.Age)`
  as independent checks — you want both failures visible, not the first one
  hiding the second.

Do not default to `require` for every line. A suite of `require` calls in a
table-driven test short-circuits on the first failing row's first failing
assertion, so you get one failure report instead of the map of real damage.

## Equality Assertions

Use the most specific one that matches the claim.

| Assertion | Use when |
| --- | --- |
| `assert.Equal(t, expected, actual)` | Values are deeply equal and the diff format is fine. |
| `assert.EqualValues` | Rarely; cross-type numeric comparison. Prefer converting types explicitly. |
| `assert.Same(t, expected, actual)` | Pointer identity matters (same instance, not equal value). |
| `assert.NotSame` | Explicitly separate instances. |
| `assert.ElementsMatch(t, expected, actual)` | Slice contents equal, order is incidental. |
| `assert.Subset(t, super, sub)` | `sub` is contained in `super` in any order. |
| `assert.Contains(t, haystack, needle)` | Substring, map key, or slice membership. |
| `assert.JSONEq(t, expectedJSON, actualJSON)` | JSON strings are structurally equal. |
| `assert.YAMLEq` | YAML strings are structurally equal. |
| `assert.InDelta(t, expected, actual, delta)` | Floats. Never `Equal` on floats. |
| `assert.InEpsilon(t, expected, actual, epsilon)` | Relative float comparison. |
| `assert.Len(t, collection, n)` | Length check without caring about contents. |
| `assert.Empty` / `assert.NotEmpty` | Zero-value / non-zero-value check. |

### Struct equality — assert only what the test claims

Comparing whole structs with `assert.Equal` is convenient and brittle. A
harmless new field cascades into every unrelated test failing.

```go
// Brittle: any new field breaks unrelated tests.
assert.Equal(t, want, got)

// Better: assert on the fields the test claims.
assert.Equal(t, "alice", got.Name)
assert.Equal(t, 30, got.Age)
assert.True(t, got.CreatedAt.After(before))
```

When the test *does* claim "entire struct matches", isolate the fields that
are deterministic (e.g., zero out `CreatedAt` or inject a clock) so the
struct match is honest.

## Error Assertions

Prefer the wrap-aware helpers.

```go
assert.ErrorIs(t, err, ErrNotFound)
assert.ErrorAs(t, err, &validationErr)
```

- `ErrorIs` = sentinel equivalence via `errors.Is`.
- `ErrorAs` = typed unwrap via `errors.As`, binds to a typed variable.
- `assert.NoError(t, err)` and `require.NoError(t, err)` for the happy path.
- `assert.Error(t, err)` is a weak oracle on its own; always pair with
  `ErrorIs` / `ErrorAs` or a specific message when message is the contract.

### String-match errors — the narrow allowed use

```go
// Allowed only when the message itself is the public contract.
assert.EqualError(t, err, "user: email must not be empty")

// Preferred for internal errors.
var vErr *ValidationError
if assert.ErrorAs(t, err, &vErr) {
    assert.Equal(t, "email", vErr.Field)
    assert.Equal(t, "required", vErr.Rule)
}
```

### Panics

```go
assert.Panics(t, func() { mustParse("bad") })
assert.PanicsWithError(t, "parse: bad", func() { mustParse("bad") })
assert.NotPanics(t, func() { safeParse("ok") })
```

Only use panic assertions for code that documents panic as its contract
(typically `Must*` helpers). Otherwise, convert to an error return.

## Async / Readiness Assertions

Eventual consistency is the only place sleeps sneak into tests. Replace
them.

```go
require.Eventually(t,
    func() bool {
        s, err := store.Status(ctx, id)
        return err == nil && s == StatusReady
    },
    2*time.Second,    // total budget
    10*time.Millisecond, // poll interval
    "status did not reach Ready",
)
```

- Budget: set it at 2–5× the p99 you expect. Too tight and you re-create
  the flake; too loose and every CI run pays for it.
- Tick: small enough that the total budget isn't dominated by the last
  wait. 10ms is a common floor.
- Message: name the invariant, not the poll. "status did not reach Ready"
  beats "eventually was false".

`EventuallyWithT` variant gives you a `*CollectT` to make multiple
assertions per iteration, each of which is retried together:

```go
require.EventuallyWithT(t, func(c *assert.CollectT) {
    s, err := store.Status(ctx, id)
    assert.NoError(c, err)
    assert.Equal(c, StatusReady, s)
}, 2*time.Second, 10*time.Millisecond)
```

Prefer this when the failure mode matters: with `Eventually` a returning
`false` collapses every reason into one boolean.

`assert.Never` is the negative companion when the claim is "this must not
happen within the observation window":

```go
assert.Never(t, func() bool {
    return worker.Stopped()
}, 200*time.Millisecond, 10*time.Millisecond)
```

### Even better: eliminate the wait

If the code under test exposes a synchronization hook — a returned channel,
a `Done()` method, a completion callback — wait on that instead of polling.
Polling is a last resort, not the default.

## Context and Timeouts

Never let a test run forever. Bound the context.

```go
baseCtx := context.Background() // Go 1.24+: use t.Context() when you want test-lifetime cancellation.
ctx, cancel := context.WithTimeout(baseCtx, 5*time.Second)
t.Cleanup(cancel)
result, err := svc.Do(ctx, req)
```

Use `t.Context()` as the base context on Go 1.24+ when cancellation should
follow test lifetime. On older Go versions, or when the module version is
unknown, keep examples on `context.Background()` plus `t.Cleanup(cancel)`.

## Helpers

Every assertion helper you write must call `t.Helper()` before asserting.

```go
func assertUser(t *testing.T, got *User, wantName string, wantAge int) {
    t.Helper()
    require.NotNil(t, got)
    assert.Equal(t, wantName, got.Name)
    assert.Equal(t, wantAge, got.Age)
}
```

Without `t.Helper()`, failure messages point inside the helper, not at the
call site. Readers then waste time scrolling through the helper source.

## Argument Order

`assert.Equal(t, expected, actual)`. Same for `NotEqual`, `ElementsMatch`,
`JSONEq`, `InDelta`. The diff format is "expected vs actual"; reversing the
order silently reverses the mental model without a test failure.

Reviewer tip: every call where `got` comes before `want` is a yellow flag.

## Assertion Object Helpers

`assert.New(t)` and `require.New(t)` are fine when the test makes many
assertions and the shorter receiver improves readability:

```go
assert := assert.New(t)
require := require.New(t)

require.NoError(err)
assert.Equal("alice", got.Name)
assert.Len(got.Roles, 2)
```

Do not introduce the object form just to save one package qualifier. Prefer the
plain package functions in short tests and when mixing helper wrappers makes the
receiver style harder to follow.

## Common Compositions

- **HTTP handler happy path:**

  ```go
  rr := httptest.NewRecorder()
  h.ServeHTTP(rr, req)

  require.Equal(t, http.StatusOK, rr.Code)
  assert.Equal(t, "application/json", rr.Header().Get("Content-Type"))
  assert.JSONEq(t, `{"id":"u1","name":"alice"}`, rr.Body.String())
  ```

- **Table-driven validation:**

  ```go
  cases := []struct {
      name    string
      in      Input
      wantErr error
  }{
      {"empty email", Input{}, ErrEmailRequired},
      {"invalid email", Input{Email: "x"}, ErrEmailFormat},
      {"ok", Input{Email: "a@b"}, nil},
  }
  for _, tc := range cases {
      t.Run(tc.name, func(t *testing.T) {
          err := Validate(tc.in)
          if tc.wantErr == nil {
              assert.NoError(t, err)
              return
          }
          assert.ErrorIs(t, err, tc.wantErr)
      })
  }
  ```

- **Struct field-by-field:**

  ```go
  got, err := svc.Create(ctx, in)
  require.NoError(t, err)

  assert.NotEmpty(t, got.ID)
  assert.Equal(t, in.Email, got.Email)
  assert.WithinDuration(t, time.Now(), got.CreatedAt, time.Second)
  ```
