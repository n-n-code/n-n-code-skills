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

Choose deliberately: `require` stops the current test or subtest. Sibling
`t.Run` cases still execute. A flat loop without subtests stops with its parent,
so subtests can preserve independent failure reports.

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
| `assert.InDelta(t, expected, actual, delta)` | Approximate numeric results with a justified absolute tolerance. Exact equality is valid for exact contracts. |
| `assert.InEpsilon(t, expected, actual, epsilon)` | Relative float comparison. |
| `assert.Len(t, collection, n)` | Length check without caring about contents. |
| `assert.Empty` / `assert.NotEmpty` | Zero-value / non-zero-value check. |

### Struct equality — assert only what the test claims

Compare the whole struct when the full value is promised. Use selected fields
when the test covers only those fields. Include generated and defaulted fields
when they are part of the claim; the fixture need not have set them directly.

```go
// Appropriate when the entire value is the contract.
assert.Equal(t, want, got)

// Appropriate when only these fields belong to the claim.
assert.Equal(t, "alice", got.Name)
assert.Equal(t, 30, got.Age)
assert.True(t, got.CreatedAt.After(before))
```

Make promised fields deterministic where useful (for example, inject time).
Do not zero out a meaningful field merely to make a comparison pass.

## Error Assertions

Prefer the wrap-aware helpers.

```go
assert.ErrorIs(t, err, ErrNotFound)
assert.ErrorAs(t, err, &validationErr)
```

- `ErrorIs` = sentinel equivalence via `errors.Is`.
- `ErrorAs` = typed unwrap via `errors.As`, binds to a typed variable.
- `assert.NoError(t, err)` and `require.NoError(t, err)` for the happy path.
- `assert.Error(t, err)` is sufficient when failure presence is the contract.
  Add `ErrorIs`, `ErrorAs`, or message checks only for the promised semantics.

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

Use panic assertions for a documented panic contract, or a regression asserting
that supported input does not panic. Changing production error behavior is a
separate compatibility decision, not an automatic consequence of test review.

## Async / Readiness Assertions

Use bounded eventual assertions when eventual state is the contract. Prefer
explicit completion signals or supported virtual-time testing when available.

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

- Budget: choose it from the operation's expected behavior and test environment;
  the numbers below are illustrative, not a universal timing policy.
- Tick: balance responsiveness and work per poll. Bound the callback's own I/O
  and synchronize shared state; the assertion timeout cannot cancel arbitrary
  work inside the callback.
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
