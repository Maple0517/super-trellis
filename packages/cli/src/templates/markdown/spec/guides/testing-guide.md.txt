# Testing Guide

Use this guide with `trellis-before-dev` and `trellis-check` when writing tests, changing behavior, fixing bugs, adding mocks, or verifying completion.

## TDD Proof Gate

Behavior changes and bug fixes need proof before implementation:

1. Write the failing test, reproduction, or executable acceptance check.
2. Run it and verify it fails for the expected reason.
3. Implement the smallest change that makes it pass.
4. Run the new proof and relevant existing tests.

If proof is genuinely impractical, record the reason and substitute proof location before writing implementation code.

## Why Order Matters

- Tests written after implementation tend to confirm what exists; tests written first define what should exist.
- Manual checks are observations, not durable regression contracts.
- Deleting pre-proof implementation prevents the test from being shaped by the solution.
- TDD is a gate for behavior, bug fixes, risky boundaries, and claims that need proof; it is not ceremony for every line.
- Bug found means: write or identify failing proof first, then debug and fix. Never fix a bug without a reproduction, regression test, or recorded substitute proof.

## Red / Green / Refactor

1. RED: write the smallest proof of desired behavior and verify it fails for the expected reason.
2. GREEN: write the smallest implementation that makes the proof pass.
3. REFACTOR: clean structure while keeping the proof and relevant existing tests green.
4. OUTPUT: verification output must be pristine enough to support the claim; do not hide warnings, skipped tests, or unrelated-looking failures.

Bugfix example:

```typescript
test("keeps retrying until a transient operation succeeds", async () => {
  let attempts = 0;

  const result = await retryOperation(async () => {
    attempts += 1;
    if (attempts < 3) throw new Error("temporary failure");
    return "ok";
  });

  expect(result).toBe("ok");
  expect(attempts).toBe(3);
});
```

Bad mock-only example:

```typescript
test("calls retry helper", async () => {
  const retry = vi.fn().mockResolvedValue("ok");
  await runWithRetry(retry);
  expect(retry).toHaveBeenCalled();
});
```

Why bad: it proves a mock was called, not that retry behavior works under failure.

## Mocking Rules

Tests must verify real behavior, not mock behavior.

- Never assert that a mock exists unless the mock itself is the intended product behavior.
- Do not add production methods only for tests. Put cleanup and setup helpers in test utilities.
- Do not mock a dependency before understanding its side effects.
- Mock the slow or external boundary, not the higher-level behavior the test needs.
- Mock response objects should match the real shape closely enough that downstream consumers are exercised.

Before adding a mock, answer:

1. What side effects does the real dependency have?
2. Does this test depend on any of those side effects?
3. Is there a lower-level boundary that can be mocked instead?

## Anti-Patterns

Avoid:

- Tests that pass because a mock element exists.
- Tests that duplicate implementation details instead of asserting behavior.
- Test-only production APIs.
- Partial mocks that omit fields real code consumes.
- "Tests later" after implementation.
- Arbitrary sleeps for async behavior.
- Green tests that were never observed failing before the fix.

## Good Tests

| Quality | Good | Bad |
|---|---|---|
| Minimal | One behavior. "and" in the name means split it. | `test('validates email and domain and whitespace')` |
| Clear | Name describes user-visible behavior. | `test('test1')` |
| Shows intent | Demonstrates the desired API or outcome. | Obscures behavior behind setup or implementation details. |

Good behavior test:

```typescript
test('rejects an empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

Bad implementation-detail test:

```typescript
test('calls validator', async () => {
  const validator = vi.fn();
  await submitForm({ email: '' }, { validator });
  expect(validator).toHaveBeenCalled();
});
```

## Regression Proof

For bug fixes, prefer a regression test or reproduction that fails before the fix and passes after it.

If the regression test was created after the fix, verify red-green when practical:

1. Temporarily disable or revert the fix.
2. Confirm the proof fails for the expected reason.
3. Restore the fix.
4. Confirm the proof passes.

If red-green is unsafe or too expensive, record the substitute evidence and why it is enough.

## When Stuck

| Problem | Signal | Action |
|---|---|---|
| Don't know how to test | Requirement is unclear | Write the wished-for API and assertion first. |
| Test too complicated | Design is too complicated | Simplify the interface. |
| Must mock everything | Code is too coupled | Move the mock to an external boundary or use dependency injection. |
| Test setup huge | Too many dependencies | Extract helpers; if still complex, simplify design. |

## TDD Verification Checklist

- [ ] Proof existed before implementation.
- [ ] New public behavior or risky boundary has proof; do not mechanically require a test for every private helper.
- [ ] Proof failed for the expected reason.
- [ ] Implementation was the smallest change that made proof pass.
- [ ] New proof passes after implementation.
- [ ] Relevant existing tests pass.
- [ ] Tests exercise real behavior, not mock behavior.
- [ ] Any substitute proof is user-approved or recorded before implementation.
- [ ] Output is pristine enough to support the claim: no ignored errors, hidden warnings, or unexplained unrelated failures.

## Completion Evidence

A completion claim needs fresh evidence:

- Test claim: command output with relevant failures at zero.
- Lint claim: fresh lint command output.
- Build claim: fresh build command exit 0.
- Bug-fix claim: reproduction or regression evidence.
- Review claim: each item mapped to code evidence, fix evidence, or technical pushback.

Do not use success language before reading the evidence.


## Debugging Integration

When a bug is found, first create or identify a failing proof, then use `trellis-debug` to investigate root cause. The proof must fail before the fix and pass after the fix unless a user-approved or recorded substitute proof is used.
