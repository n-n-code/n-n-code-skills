# Testify Mocking Patterns

Reference for deciding between hand-written fakes and `testify/mock`, then
using `mock` precisely when it is the right tool.

## Fake First

Prefer a hand-written fake when the interface is narrow and owned by the code
under test.

```go
type fakeMailer struct {
    sent []Message
    err  error
}

func (f *fakeMailer) Send(ctx context.Context, msg Message) error {
    f.sent = append(f.sent, msg)
    return f.err
}
```

Why this wins:

- compiler-checked against the real interface
- easy to inspect resulting state
- survives refactors better than a chain of `On(...).Return(...)`
- keeps the test honest when behavior matters more than call choreography

## When `testify/mock` Earns Its Keep

Use `testify/mock` when the test genuinely needs at least one of:

- call-count assertions (`Once`, `Twice`, `Times`)
- optional calls (`Maybe`)
- argument matching that depends on selected fields (`MatchedBy`)
- controlled mutation of pointer arguments (`Run`)
- explicit ordering (`InOrder`, `NotBefore`)
- a wide interface where a fake would be longer than the behavior under test

Keep the mocked interface owned and narrow where possible.

## Basic Shape

```go
type paymentGatewayMock struct {
    mock.Mock
}

func (m *paymentGatewayMock) Charge(ctx context.Context, in ChargeRequest) error {
    args := m.Called(ctx, in)
    return args.Error(0)
}

func TestChargeUser(t *testing.T) {
    gateway := new(paymentGatewayMock)
    gateway.On("Charge", mock.Anything, ChargeRequest{UserID: "u1", Amount: 10}).
        Return(nil).
        Once()

    err := svc.ChargeUser(context.Background(), "u1", 10)
    require.NoError(t, err)
    gateway.AssertExpectations(t)
}
```

Always assert expectations before the test returns. If multiple mocks are in
play, `mock.AssertExpectationsForObjects(t, a, b, c)` checks all of them, and
the testify docs note that calls may have occurred in any order unless you add
an explicit ordering rule.

## Argument Matching

Prefer exact arguments when the full value is the claim. Reach for looser
matching only when exact equality would couple the test to irrelevant fields.

```go
repo.On("Save", mock.MatchedBy(func(u User) bool {
    return u.Email == "alice@example.com" && u.ID != ""
})).Return(nil)
```

Use:

- `mock.Anything` when an argument truly does not matter
- `mock.AnythingOfType("string")` when type matters but value does not
- `mock.MatchedBy(...)` when only selected properties matter

Do not hide important contract details behind `mock.Anything`.

## Pointer Mutation With `Run`

`Run` exists for methods that mutate a pointer argument before returning.

```go
decoder.On("Decode", mock.AnythingOfType("*Payload")).
    Return(nil).
    Run(func(args mock.Arguments) {
        p := args.Get(0).(*Payload)
        p.ID = "p1"
        p.Email = "alice@example.com"
    })
```

Use this narrowly. If most of the mock's value is "pretend to be a decoder",
the code usually wants a fake instead.

## Optional, Counted, And Ordered Calls

```go
cache.On("Get", "u1").Return(User{}, ErrMiss).Once()
cache.On("Set", "u1", mock.Anything).Return(nil).Maybe()
```

- `Once`, `Twice`, `Times(n)` constrain call count
- `Maybe` makes a call optional
- `InOrder(...)` constrains a sequence only when order itself is the contract
- `NotBefore(...)` is the more local dependency rule when one call must not
  happen before another

Order assertions are expensive. Add them only when order is semantically part
of the behavior, not because the current implementation happens to call methods
in a certain sequence.

## HTTP And Repository Boundaries

Prefer a real boundary when it is cheap:

- HTTP client code -> `httptest.NewServer`
- repository code -> real DB in a cheap local harness or container
- filesystem code -> `t.TempDir()`

`testify/mock` is usually worse than those options when the seam is already
concrete and inexpensive to exercise for real.

For concrete harness shapes, see
[real-boundary-patterns.md](real-boundary-patterns.md).

## Anti-patterns

- mocking the system under test
- mocking third-party types directly instead of wrapping them
- `mock.Anything` on every argument, which turns the expectation into noise
- asserting call order when the contract does not require it
- using `Run` to reproduce most of a collaborator's real behavior
- forgetting `AssertExpectations(t)` and then trusting the test

## Practical Review Questions

- Would a fake be shorter and clearer here?
- Are we matching only the arguments that matter to the claim?
- Is call order actually part of the contract?
- Are we mocking an owned interface or a third-party type we should wrap?
- Would `httptest.NewServer` or a real dependency be cheaper and more honest?
