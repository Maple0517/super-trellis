---
name: trellis-debug
description: "Pre-fix root-cause investigation for bugs, test failures, build failures, runtime errors, unexpected behavior, and failed verification. Use when encountering a failure before proposing or writing a fix."
---

# Trellis Debug

Use this skill before proposing or writing a fix. It may be used with or without an active Trellis task. `trellis-break-loop` handles post-fix retrospective analysis after repeated debugging and remains task-only.

## Iron Law

NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

Violating the letter of this process is violating the spirit of debugging. If implementation starts before reproduction, evidence, and a written testable hypothesis, discard the speculative fix and restart from investigation.

## Tool Routing

For code-level root cause tracing, use CodeGraph before text search when tracing symbols, callers, callees, module flow, or impact radius. Use LeanCTX for current logs, command output, fresh file bytes, repo overview, semantic search, and compressed test/build output. Do not claim CodeGraph unavailable until checking available tools or calling `codegraph_status`; if CodeGraph is unavailable, stale, or degraded, say so and fall back to LeanCTX fresh reads or native search.

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

## Post-Fix Handoff

After the local reproduction, regression proof, or substitute proof passes, do not stop at "fixed".

Offer the next workflow step:

1. Run broader verification through `trellis-check`.
2. Decide whether the lesson should go to `trellis-update-spec`.
3. If the same bug or fix loop happened 3+ times, use `trellis-break-loop`.
4. If checks are enough for the task scope, move to the finish/commit decision.

Ask the user whether to continue with broader verification when the checks are non-trivial or expensive.

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

No-task escalation: if no active task exists and a hard upgrade trigger appears — persistent planning, multi-stage or multi-session debugging, lifecycle features, structured decomposition, elevated risk/scope, durable context injection beyond the current conversation, or repeated-fix analysis — stop and ask to create a Trellis task before deeper work.
