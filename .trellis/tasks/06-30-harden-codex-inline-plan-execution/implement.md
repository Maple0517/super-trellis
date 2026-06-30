# Harden Codex inline plan execution — Implementation Plan

## File Map

- Modify: `packages/cli/src/templates/trellis/workflow.md`
  - Upstream template for generated `.trellis/workflow.md`.
  - Add explicit inline plan execution discipline to `[workflow-state:in_progress-inline]`.
- Modify: `.trellis/workflow.md`
  - Dogfood local workflow file currently injected into this Codex session.
  - Mirror the same inline plan discipline as the upstream template.
- Modify: `packages/cli/test/templates/trellis.test.ts`
  - Add regression coverage for `[workflow-state:in_progress-inline]` plan discipline.
- Read/check: `.trellis/spec/cli/backend/workflow-state-contract.md`
  - Verify the change still respects the workflow-state runtime contract.

## Header

**Goal:** Make Codex inline execution follow `implement.md` step-by-step instead of treating it as loose context.

**Architecture:** Patch the inline breadcrumb in both the upstream workflow template and the local dogfood workflow copy. Protect the new behavior with a template-level Vitest assertion that extracts `in_progress-inline` and checks for plan-discipline strings.

**Tech Stack:** Markdown workflow templates, TypeScript Vitest template tests, pnpm.

## Tasks

### Task 1: Add failing template test for inline plan discipline

**Files:**

- Modify: `packages/cli/test/templates/trellis.test.ts`

- [ ] **Step 1: Add helper usage for `in_progress-inline`**

Insert a new test near the existing workflow breadcrumb tests:

```ts
  it("[codex-inline] workflow.md in_progress-inline treats implement.md as ordered execution contract", () => {
    const block = workflowStateBreadcrumb("in_progress-inline");
    expect(block).toContain("implement.md");
    expect(block).toContain("ordered execution contract");
    expect(block).toContain("review it critically");
    expect(block).toContain("one top-level implement step");
    expect(block).toContain("Do not batch, reorder, or skip");
    expect(block).toContain("Stop for unclear instructions");
  });
```

- [ ] **Step 2: Run the targeted test and confirm it fails**

Run:

```bash
pnpm --filter @mindfoldhq/trellis test -- test/templates/trellis.test.ts
```

Expected: FAIL because the current `in_progress-inline` block does not contain the new contract strings.

### Task 2: Patch upstream workflow template inline block

**Files:**

- Modify: `packages/cli/src/templates/trellis/workflow.md`

- [ ] **Step 1: Replace the loose inline context line with explicit plan discipline**

In `[workflow-state:in_progress-inline]`, replace:

```md
Context: `prd.md` -> `design.md` -> `implement.md`, plus relevant spec/research loaded by skills.
```

with:

```md
Plan discipline: `implement.md`, when present, is the ordered execution contract. At Phase 2 start, read `prd.md` -> `design.md` -> `implement.md`, review it critically against current code/spec reality, and surface blockers before coding.
Step cursor: keep exactly one current top-level implement step in progress; complete that step's proof/check before moving to the next step.
Step changes: Do not batch, reorder, or skip implement steps unless you first state the reason, such as inseparable atomic edits, dependency correction, failed verification, or user override.
Stop points: Stop for unclear instructions, failed gates, or required user decisions instead of guessing.
Context: relevant spec/research loaded by skills.
```

- [ ] **Step 2: Preserve existing inline gates**

Confirm the block still contains:

```md
Flow: `trellis-before-dev` -> [`trellis-debug` if bug/failure/unexpected behavior] -> edit -> `trellis-check` -> `trellis-update-spec` -> Phase 3.
Quality: apply the TDD Decision Matrix in `trellis-before-dev` before writing code.
Do not dispatch implement/check sub-agents in inline mode.
```

### Task 3: Mirror the patch into local dogfood workflow

**Files:**

- Modify: `.trellis/workflow.md`

- [ ] **Step 1: Apply the same inline block text**

Make `.trellis/workflow.md` `[workflow-state:in_progress-inline]` match the upstream template language from Task 2.

- [ ] **Step 2: Verify no accidental sub-agent-mode change**

Run:

```bash
rg -n "workflow-state:in_progress-inline|Plan discipline|Do not dispatch implement/check" .trellis/workflow.md packages/cli/src/templates/trellis/workflow.md
```

Expected: both workflow files include `Plan discipline`; both still include `Do not dispatch implement/check sub-agents in inline mode`.

### Task 4: Run verification

**Files:**

- Test: `packages/cli/test/templates/trellis.test.ts`
- Check: `packages/cli/src/templates/trellis/workflow.md`
- Check: `.trellis/workflow.md`

- [ ] **Step 1: Run targeted template test**

Run:

```bash
pnpm --filter @mindfoldhq/trellis test -- test/templates/trellis.test.ts
```

Expected: PASS.

- [ ] **Step 2: Run typecheck if test touched TypeScript**

Run:

```bash
pnpm --filter @mindfoldhq/trellis typecheck
```

Expected: PASS.

- [ ] **Step 3: Review diff for scope**

Run:

```bash
git diff -- .trellis/tasks/06-30-harden-codex-inline-plan-execution packages/cli/src/templates/trellis/workflow.md .trellis/workflow.md packages/cli/test/templates/trellis.test.ts
```

Expected: diff only contains planning artifacts, inline workflow text, and the regression test.

## Self-Review

- Spec coverage: R1-R8 map to Tasks 1-4.
- Placeholder scan: no unresolved marker instructions.
- Stop points: failed test, unclear workflow wording, or disagreement between dogfood and upstream template blocks.
- Rollback point: revert only the three implementation files if verification fails; keep task artifacts unless the task is abandoned.
