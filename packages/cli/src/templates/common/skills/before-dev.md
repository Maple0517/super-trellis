Read the relevant development guidelines before starting your task.

Execute these steps:

1. **Resolve task mode vs no-task mode**:
   - If a current task exists, read task artifacts:
     - `prd.md` for requirements and acceptance criteria
     - `design.md` if present for technical design
     - `implement.md` if present for execution order and validation plan
   - If no active task exists, use the current user request, the files or package area you are about to change, and the current diff target area as the temporary scope contract.

2. **Discover packages and their spec layers**:
   ```bash
   python3 ./.trellis/scripts/get_context.py --mode packages
   ```

3. **Identify which specs apply** based on:
   - Which package you're modifying (e.g., `cli/`, `docs-site/`)
   - What type of work (backend, frontend, unit-test, docs, etc.)
   - Any spec/research paths referenced by the task artifacts when a task exists
   - The current request and changed area when no task exists

4. **Read the spec index** for each relevant module:
   ```bash
   cat .trellis/spec/<package>/<layer>/index.md
   ```
   Follow the **"Pre-Development Checklist"** section in the index.

5. **Read the specific guideline files** listed in the Pre-Development Checklist that are relevant to your task. The index is NOT the goal — it points you to the actual guideline files (e.g., `error-handling.md`, `conventions.md`, `mock-strategies.md`). Read those files to understand the coding standards and patterns.

6. **Always read shared guides**:
   ```bash
   cat .trellis/spec/guides/index.md
   ```

7. Understand the coding standards and patterns you need to follow, then proceed with your development plan. No-task mode still requires the same proof and TDD gates before implementation.

8. **Register implementation steps** via the platform's step-tracking tool (`update_plan` on Codex, `TodoWrite` on Claude Code) before writing code, so the user sees progress visually.

This step is **mandatory** before writing any code.

## Iron Law

NO IMPLEMENTATION CODE BEFORE FAILING PROOF.

Proof means a failing test, reproduction, or executable acceptance check. Write implementation before proof? Delete it and start over. No exceptions without user permission or a recorded task-artifact reason before implementation.

## TDD Decision Matrix

Before writing implementation code, decide whether the change needs proof first.

| Change type | Required proof |
|---|---|
| New behavior | Failing test or explicit executable acceptance check before implementation. |
| Bug fix | Reproduction or regression test before fix. |
| Refactor | Existing tests pass before and after; add tests if behavior boundaries are weak. |
| Docs-only | Render/link/spell or targeted review check. |
| Config or workflow behavior | Small scripted check or command output proving the changed path. |

Gate: after writing a failing test or reproduction, run it and verify it fails for the expected reason before implementation. If it passes immediately, it is not a valid failing test.

Gate: if implementation code is written before the failing test, reproduction, user-approved substitute proof, or recorded exception in the task artifact, discard that implementation and restart from proof. Do not keep the discarded implementation as reference and do not adapt it into the test. If a failing test is genuinely impractical, record the reason and substitute proof location before writing implementation code.

Green verification: after the minimal implementation, run the new proof and the relevant existing tests. Output must be clean enough to support the claim.

Common rationalizations:

| Rationalization | Reality |
|---|---|
| "I'll test after." | Tests-after prove what code does; tests-first prove desired behavior. |
| "Tests after achieve the same goals." | Tests-after answer "what does this do?"; tests-first answer "what should this do?" |
| "I manually checked it." | Manual checks are not durable regression proof. |
| "Deleting work is wasteful." | Keeping pre-proof implementation pollutes the test and weakens the gate. |
| "Too simple to test." | Simple code breaks. Test takes 30 seconds. |
| "Keep it as reference." | You will adapt it. That is testing after. Delete means delete. |
| "Need to explore first." | Fine. Throw away exploration and restart from proof. |
| "The test is hard to write." | Hard to test often means hard to use. Simplify the design. |
| "TDD will slow me down." | TDD is faster than debugging unproven code. |
| "Manual test is faster." | Manual checks do not prove edge cases and cannot be rerun reliably. |
| "Existing code has no tests." | Improve the boundary you touch; add tests where behavior risk exists. |

## Why Order Matters

- Tests written after implementation tend to confirm what exists; tests written first define what should exist.
- Manual checks are observations, not durable regression contracts.
- Deleting pre-proof implementation prevents the test from being shaped by the solution.
- TDD is a gate for behavior, bug fixes, risky boundaries, and claims that need proof; it is not ceremony for every line.
- Bug found means: write or identify failing proof first, then debug and fix. Never fix a bug without a reproduction, regression test, or recorded substitute proof.

## Red Flags — STOP and Start Over

- Code before test.
- Test after implementation.
- Test passes immediately.
- Can't explain why the proof failed.
- Tests added "later".
- Rationalizing "just this once".
- "I already manually tested it."
- "Tests after achieve the same purpose."
- "It's about spirit, not ritual."
- "Keep as reference" or "adapt existing code."
- "Already spent hours; deleting is wasteful."
- "TDD is dogmatic; I'm being pragmatic."
- "This is different because..."

All of these mean: delete implementation code and restart from proof.
