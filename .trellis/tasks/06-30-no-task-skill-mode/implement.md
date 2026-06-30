# No-task skill mode implementation

## Scope

Implement dual-mode Trellis discipline skills so selected skills may run without an active task, while preserving task-only lifecycle features and a single workflow.

This task owns:

- `workflow.md` no-task routing redesign
- no-task bounded mode for `trellis-brainstorm`
- no-task fallback logic for `trellis-before-dev`
- no-task fallback logic for `trellis-check`
- no-task wording updates for `trellis-debug`, `trellis-update-spec`, `trellis-session-insight`, and `trellis-meta` where needed
- regression markers/tests for the new no-task behavior

This task does not own:

- making `trellis-break-loop`, `trellis-finish-work`, `trellis-continue`, or `trellis-channel` no-task capable
- adding a second workflow
- creating durable no-task planning artifacts

## Implementation steps

1. Update workflow routing and guardrails.
   - Rewrite `[workflow-state:no_task]` in `packages/cli/src/templates/trellis/workflow.md`.
   - Replace “skip Trellis for this session” with dual-mode no-task discipline routing.
   - Add explicit bounded-complexity language for no-task brainstorming.
   - Add upgrade-trigger references in `no_task` routing and guardrails.

2. Add dual-mode contract to `trellis-brainstorm`.
   - Keep existing task mode intact.
   - Add no-task mode behavior: evidence gathering, scope narrowing, recommendations, no artifact creation.
   - Add hard stop before full implementation planning for complex work.

3. Add no-task fallback to `trellis-before-dev`.
   - Keep task-artifact path intact when a task exists.
   - Add fallback input rules when no task exists: request, changed area, spec indexes, guides.
   - Preserve TDD/proof gate with no weakening.

4. Add no-task fallback to `trellis-check`.
   - Keep task-artifact path intact when a task exists.
   - Add fallback verification path using current diff, request scope, changed files, and specs.
   - Preserve completion gate and pre-commit milestone handoff.

5. Add wording updates to no-task-friendly skills.
   - `trellis-debug`: explicitly allowed without task; mention escalation on persistent/complex work.
   - `trellis-update-spec`: ask for approval before no-task `.trellis/spec` writes.
   - `trellis-session-insight`: clarify no-task usage and no-task persistence limits.
   - `trellis-meta`: clarify no-task usage for Trellis self-customization.

6. Protect task-only boundaries.
   - Confirm `trellis-break-loop`, `trellis-finish-work`, `trellis-continue`, and `trellis-channel` remain task-only by wording and routing.
   - Adjust workflow routing text if needed so they are not offered in no-task mode.

7. Add regression markers/tests.
   - Extend `packages/cli/test/templates/disciplined-runtime.test.ts`.
   - Add markers for:
     - no-task discipline routing
     - bounded no-task brainstorm
     - no-task fallback in before-dev/check
     - explicit approval before no-task spec writes
     - task-only boundaries

8. Validate.
   - Run targeted template tests.
   - If shared wording changes introduce platform-neutral placeholder concerns, run any additional template resolver tests that fail.
   - Build the CLI template bundle after test pass.

## Validation commands

```bash
pnpm --filter @mindfoldhq/trellis test -- packages/cli/test/templates/disciplined-runtime.test.ts packages/cli/test/templates/trellis.test.ts
pnpm --filter @mindfoldhq/trellis build
```

If shared template wording affects platform-neutral resolution:

```bash
pnpm --filter @mindfoldhq/trellis test -- packages/cli/test/configurators/shared.test.ts packages/cli/test/templates/codex.test.ts packages/cli/test/templates/trae.test.ts
```

## Risk points

- `workflow.md` may still contain stale “skip Trellis” language in one block if only one breadcrumb is updated.
- Shared skill wording can break platform-neutral template tests if platform-specific command syntax leaks into common templates.
- `trellis-brainstorm` is the easiest place to accidentally create a second workflow if no-task mode is not bounded tightly.
- `trellis-before-dev` / `trellis-check` must not silently require task artifacts after the rewrite, or no-task mode will be fake.
- `trellis-update-spec` must not auto-write in no-task mode.

## Rollback points

- After step 1, `workflow.md` should already clearly separate no-task discipline from task mode. If that separation becomes confusing, revert the routing rewrite before touching skills.
- After steps 2-5, rerun targeted tests before adding more markers. If tests fail due to shared syntax leakage, fix placeholders before proceeding.
