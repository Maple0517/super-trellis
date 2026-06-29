# Debugging Guide

Use this guide with `trellis-debug` when a bug, failed verification, flaky test, runtime error, or unexpected behavior appears.

## Non-Negotiable Rule

No fixes before root-cause investigation. Reproduce the symptom, gather evidence, write a testable hypothesis, then patch the proven cause.

## Root-Cause Tracing

When the error appears deep in a call stack or async flow:

1. Record the symptom: command, output, stack trace, file, line, environment, and current diff.
2. Identify the immediate failing operation.
3. Trace callers, inputs, and data transformations backward until you find the first invalid assumption or value.
4. Fix at the source, not only at the symptom point.
5. Add targeted validation at the layer where the invalid value first enters.

Use temporary instrumentation only to gather evidence. Remove or gate noisy debug output before completion.

## Multi-Component Evidence

If a failure crosses layers, collect evidence at every boundary:

- Entry/input shape.
- State or storage write.
- Service or transformation output.
- API, event, or command payload.
- UI, CLI, or test assertion output.

Do not patch one layer until you know which boundary first diverges from the expected behavior.

## Condition-Based Waiting

For flaky async tests, wait for the condition you need, not an arbitrary delay.

Good waiting targets:

- Event exists.
- State becomes ready.
- Count reaches expected value.
- File or record appears.
- UI element becomes visible or actionable.

Timeouts are allowed only when they are testing real timing behavior or have a documented timing source. Otherwise, replace sleeps with condition polling and a clear timeout error.

Example helper:

```typescript
export async function waitForCondition<T>(options: {
  read: () => Promise<T> | T;
  ok: (value: T) => boolean;
  timeoutMs?: number;
  intervalMs?: number;
  label?: string;
}): Promise<T> {
  const timeoutMs = options.timeoutMs ?? 5000;
  const intervalMs = options.intervalMs ?? 100;
  const start = Date.now();
  let last: T | undefined;

  while (Date.now() - start < timeoutMs) {
    last = await options.read();
    if (options.ok(last)) return last;
    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }

  throw new Error(
    `Timed out waiting for ${options.label ?? "condition"}; last observed=${JSON.stringify(last)}`
  );
}

await waitForCondition({
  label: "saved todo to appear",
  read: () => screen.queryByText("Buy milk"),
  ok: (node) => node !== null,
});
```

## Defense In Depth

When invalid data caused the bug, make recurrence structurally harder:

1. Entry validation rejects impossible input.
2. Business logic validates operation-specific assumptions.
3. Environment guards protect dangerous contexts such as tests, temp dirs, production paths, or destructive commands.
4. Forensics capture enough context to debug future failures without guessing.

Do not add broad defensive checks that hide the failure. Prefer narrow checks with useful error messages.

## Pressure Checks

Stop and return to evidence gathering when you hear yourself thinking:

- "Quick fix first."
- "This is obvious."
- "The failure line tells me the cause."
- "I can just try changing X."
- "The next speculative patch should work."

After three failed fixes, stop patching. Re-check the reproduction, assumptions, architecture, and recent changes before continuing.


## Polluter Search

For order-dependent tests, isolate the smallest preceding test or setup step that changes shared state. Reset shared state at the source, not in every affected test. Use a shell recipe like this when candidate tests can be listed explicitly:

```bash
TARGET="path/to/failing.test.ts"
for candidate in path/to/candidate1.test.ts path/to/candidate2.test.ts; do
  echo "checking polluter: $candidate -> $TARGET"
  if ! pnpm test "$candidate" "$TARGET"; then
    echo "POLLUTER_CANDIDATE=$candidate"
    break
  fi
done
```

Check shared state, clocks, network mocks, global caches, filesystem artifacts, database rows, and environment variables.

## Pressure Scenarios

Absorb the systematic-debugging pressure scenarios as runtime reminders, not mandatory gates:

- Symptom moves after one fix: return to root-cause tracing; do not stack patches.
- Failure crosses UI/API/storage: collect evidence at every boundary before hypothesizing.
- Test passes alone but fails in suite: run polluter search and inspect shared state.
- Academic/artificial debugging drills are optional self-tests for the skill, not project runtime rules.
