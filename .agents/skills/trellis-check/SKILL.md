---
name: trellis-check
description: "Comprehensive quality verification: spec compliance, lint, type-check, tests, cross-layer data flow, code reuse, and consistency checks. Use when code is written and needs quality verification, before committing changes, or to catch context drift during long sessions."
---

# Code Quality Check

Comprehensive quality verification for recently written code. Combines spec compliance, cross-layer safety, and pre-commit checks.

---

## Completion Claim Gate

Iron Law: every completion claim is unproven until fresh evidence says otherwise. Do not use completion or success language anywhere in this skill until this gate has passed.

Forbidden status words until the gate passes: "should", "probably", "seems to", "appears to", "looks good", "done", "fixed", "passing", "complete".

Before saying work is complete, fixed, passing, ready, or done:

1. Identify the command or direct evidence that proves the claim.
2. Run the full command freshly.
3. Read the output and exit code.
4. If the evidence fails, report the actual status and continue fixing.
5. If the evidence passes, state the claim with the proof command.

For bug-fix regression tests added after the fix, verify red-green: temporarily revert or disable the fix, confirm the regression test fails for the expected reason, restore the fix, and confirm it passes.

## Milestone Handoff

After verification passes, do not silently stop at a success claim. State the evidence and offer the next workflow step.

- If verification passed but intended work remains uncommitted, do not stop at an implementation summary. Offer the next step explicitly: review diff, commit now, or stop local.
- Active Trellis task: route to `trellis-update-spec`, commit, then ``finish-work` (Trellis command)`.
- No active Trellis task: offer structured integration choices: commit locally, push/PR, keep local only, continue with the next task, or stop here.
- Ask before pushing, opening a PR, running expensive extra checks, adding polish outside the agreed scope, or closing lifecycle state.

| Claim | Required evidence | Not sufficient |
|---|---|---|
| Tests pass | Fresh test command output with 0 relevant failures. | "Should pass", stale output, or partial test subset without scope reason. |
| Lint clean | Fresh lint command output with 0 relevant errors. | "No lint-looking changes" or uninspected warnings. |
| Build succeeds | Fresh build command exit 0. | Typecheck-only or previous build cache without current command. |
| Bug fixed | Reproduction or regression proof fails before the fix and passes after the fix. | Manual impression or test added after fix without red/green proof. |
| Review addressed | Each review item mapped to code evidence, fix evidence, or technical pushback. | Gratitude, agreement, or implementer self-report. |
| Requirements met | Acceptance criteria checked against artifacts and changed behavior. | Tests pass but requirements not re-read. |
| Agent completed | Actual diff, files, and commands inspected; implementer report is not sufficient. | Worker says DONE. |

Red flags — stop before claiming completion:

- Trusting an agent/worker report without reading diff and output.
- Relying on partial verification without saying why it is sufficient.
- Expressing satisfaction before evidence is complete.
- Ignoring warnings, skipped tests, or unrelated-looking failures.
- Feeling tired and wanting the work to be done.

Why this matters: completion claims are user trust contracts. A false "done" costs more than a slower, evidence-backed report.

Rationalization prevention:

| Rationalization | Reality |
|---|---|
| "It should pass." | Run it. |
| "Only a small change." | Small changes still break contracts. |
| "The agent said it passed." | Verify actual output yourself. |
| "I ran it earlier." | Claims need fresh evidence. |
| "One failing unrelated test is fine." | Identify and report unrelated evidence; do not hide it. |
| "Looks good visually." | Use direct visual evidence or browser output for UI claims. |
| "I am tired; done enough." | Fatigue is a red flag to slow down verification. |
| "Just this once." | Gate exceptions need user approval or recorded rationale. |

## Review Gate

Request review for high-risk, cross-layer, major feature, complex bugfix, pre-merge work, after each substantial subagent task, when stuck, before risky refactors, or after a complex bug fix. Do not force two separate reviewer agents by default; use the Trellis check path unless channel orchestration is explicitly chosen.

For symbol-level claims, cross-layer claims, caller/callee relationships, flow tracing, or impact-radius review, verify with CodeGraph when available. Use LeanCTX for fresh diff/status/test output, compressed logs, file reads, repo overview, routes, semantic search, and session memory. Do not claim CodeGraph unavailable until checking available tools or calling `codegraph_status`; if CodeGraph is unavailable, stale, or degraded, say so and use LeanCTX fresh reads or native search as fallback.

When receiving review feedback:

1. READ the full feedback before reacting.
2. UNDERSTAND the requested change in your own words.
3. VERIFY it against codebase reality.
4. EVALUATE whether it is correct, needed, and not speculative. If the suggestion adds "proper" behavior, grep for actual usage before implementing.
5. RESPOND with technical acknowledgment or technical pushback.
6. IMPLEMENT one item at a time and verify each fix.

Forbidden responses before technical evaluation: "You're absolutely right", "Great point", "Excellent feedback", "Thanks for catching this", and gratitude-only replies.

Acknowledging correct feedback after verification: use `Fixed: <brief technical description>` or `Accepted: <reason and planned change>`. Do not perform gratitude or agreement as a substitute for technical response.

Finding severity:
- Critical: fix before continuing.
- Important: fix before merge unless explicitly deferred by the user.
- Minor: record or fix if cheap.

Source-specific handling:
- User/partner feedback: clarify intent when ambiguous, then implement or push back technically.
- External PR/review feedback: verify against code and requirements; do not accept style churn or speculative architecture without evidence.
- Automated review: reproduce the finding locally or explain why it is not applicable.

Implementation order: blocking correctness/security/data-loss items first, then simple safe fixes, then complex design changes. Batch unclear items and ask instead of guessing.

Push back when feedback is factually wrong, conflicts with requirements, adds unused abstraction, breaks existing behavior, or is not worth the scope. State the evidence and propose the smaller alternative. If you pushed back and later find your pushback was wrong, correct it explicitly: `Correction: my earlier pushback was wrong because <evidence>. Fixed: <brief description>.`

If you feel uncomfortable pushing back, say so and show the evidence instead of silently accepting the suggestion.

Common mistakes:
- Accepting feedback without reading the relevant code.
- Implementing the broadest possible interpretation.
- Thanking or agreeing before verification.
- Treating style preference as correctness.
- Ignoring unclear feedback instead of clarifying.
- Changing unrelated code while addressing review.
- Reporting fixed without a fresh check.

GitHub/PR thread replies, when applicable: reply inline only after the item is fixed or technically rejected; include the evidence command or file reference; keep the reply short and technical.

YAGNI check: before adding a "proper" abstraction, grep for actual usage and report whether the usage justifies it.

Code-reviewer prompt absorption: inspect diff and requirements, separate spec compliance from quality, verify tests/commands directly, classify severity, and produce actionable findings with file evidence. Do not absorb the git-SHA dispatch shell.

## Step 1: Identify What Changed

```bash
git diff --name-only HEAD
git status
```

## Step 2: Read Task Artifacts and Applicable Specs

If a current task exists, read the task artifacts in order:

- `prd.md`
- `design.md` if present
- `implement.md` if present

If no active task exists, use the current user request, the current diff, changed paths, and the code area being edited as the temporary scope contract.

```bash
python3 ./.trellis/scripts/get_context.py --mode packages
```

For each changed package/layer, read the spec index and follow its **Quality Check** section:

```bash
cat .trellis/spec/<package>/<layer>/index.md
```

Read the specific guideline files referenced — the index is a pointer, not the goal.

No-task fallback: verification still runs fully even when task artifacts do not exist. In that case, requirements checks must be grounded in the current request, current diff, and fresh command evidence.

No-task escalation: if verification reveals a hard upgrade trigger — persistent planning, multi-stage or multi-session work, lifecycle features, structured decomposition, elevated risk/scope, or durable context injection beyond the current conversation — report the evidence and ask to create a Trellis task before continuing deeper.

## Step 3: Run Project Checks

Run the project's lint, type-check, and test commands. Fix any failures before proceeding.

## Step 4: Review Against Checklist

### Code Quality

- [ ] Linter passes?
- [ ] Type checker passes (if applicable)?
- [ ] Tests pass?
- [ ] No debug logging left in?
- [ ] No suppressed warnings or type-safety bypasses?

### Test Coverage

These are post-implementation verification checks. The TDD Decision Matrix in `trellis-before-dev` governs whether a failing test, reproduction, or substitute proof must exist before implementation begins. Use `.trellis/spec/guides/testing-guide.md` to catch testing anti-patterns.

- [ ] New function → unit test added?
- [ ] Bug fix → regression test added?
- [ ] Changed behavior → existing tests updated?

### Spec Sync

- [ ] Does `.trellis/spec/` need updates? (new patterns, conventions, lessons learned)

> "If I fixed a bug or discovered something non-obvious, should I document it so future me won't hit the same issue?" → If YES, update the relevant spec doc.

## Step 5: Cross-Layer Dimensions (if applicable)

Skip this step if your change is confined to a single layer.

### A. Data Flow (changes touch 3+ layers)

- [ ] Read flow traces correctly: Storage → Service → API → UI
- [ ] Write flow traces correctly: UI → API → Service → Storage
- [ ] Types/schemas correctly passed between layers?
- [ ] Errors properly propagated to caller?

### B. Code Reuse (modifying constants, creating utilities)

- [ ] Searched for existing similar code before creating new?
  ```bash
  grep -r "pattern" src/
  ```
- [ ] If 2+ places define same value → extracted to shared constant?
- [ ] After batch modification, all occurrences updated?

### C. Import/Dependency (creating new files)

- [ ] Correct import paths (relative vs absolute)?
- [ ] No circular dependencies?

### D. Same-Layer Consistency

- [ ] Other places using the same concept are consistent?

---

## Step 6: Report and Fix

Report violations found and fix them directly. Re-run project checks after fixes.
