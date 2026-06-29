# Trellis Debug

Use this skill before proposing or writing a fix. `trellis-break-loop` handles post-fix retrospective analysis after repeated debugging.

## Iron Law

NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

Violating the letter of this process is violating the spirit of debugging. If implementation starts before reproduction, evidence, and a written testable hypothesis, discard the speculative fix and restart from investigation.

## Red Flags

STOP and return to evidence gathering when you notice:

- "Quick fix for now."
- "Just try changing X."
- "I see the problem, let me fix it" before reproduction or root-cause evidence.
- "It's probably X" without evidence.
- A second speculative patch without a falsified hypothesis.
- Pressure to patch because the failure looks small.

## Systematic Debugging Phases

1. Capture the complete failure: command, output, file paths, line numbers, assertion text, environment, and current git diff.
2. Reproduce the issue consistently, or record exactly why reproduction is not yet possible.
3. Gather multi-component evidence before hypothesizing when the failure crosses layers. Trace the data flow from input to failing output.
4. Pattern analysis: find a working example, compare it to the failing path, identify the first meaningful difference, and check relevant docs or specs.
5. Write one smallest testable hypothesis in the notes or task artifact.
6. Test the hypothesis with the smallest evidence-gathering command or instrumentation.
7. Apply the smallest root-cause fix only after evidence supports the hypothesis.
8. Prove the fix with the reproduction, regression test, or command output.
9. Capture durable prevention through `trellis-update-spec` when the lesson is reusable.

## Rationalization Prevention

| Rationalization | Reality |
|---|---|
| "This is obvious." | Obvious fixes still need root-cause evidence. |
| "One quick fix first." | Quick fixes create false confidence and hide the real failure. |
| "The test failure points right at it." | Error locations are symptoms until traced to cause. |
| "I can reason it out." | Reasoning without reproduction is guessing. |
| "Adding logs is slower." | Evidence gathering is faster than repeated patches. |
| "This is too small for the process." | Small bugs still have causes and regression risks. |
| "The first patch almost worked." | Almost working is evidence the hypothesis is incomplete. |
| "Three fixes failed but the next one is simple." | After 3 failed fixes, stop patching and re-question assumptions. |

## Stop Rule

After 3 failed fixes, stop patching. Re-check reproduction, architecture, assumptions, and recent changes. Ask for review or use `trellis-break-loop` after the immediate failure is stabilized.
