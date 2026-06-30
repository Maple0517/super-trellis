# Harden Codex inline plan execution — Design

## Architecture

The source of truth for generated project workflow text is `packages/cli/src/templates/trellis/workflow.md`.

The dogfood project also carries a generated local copy at `.trellis/workflow.md`. This task updates both files with equivalent `[workflow-state:in_progress-inline]` language so the current workspace and future generated workspaces behave the same way.

## Current Behavior

Inline mode injects the `[workflow-state:in_progress-inline]` block when Codex runs with `codex.dispatch_mode=inline`. The block currently says to read `prd.md -> design.md -> implement.md`, but it does not require ordered execution of `implement.md`.

Implement-agent surfaces already contain stronger plan discipline:

- `.trellis/agents/implement.md`: execute `implement.md` step-by-step and stop if instructions are unclear or verification fails.
- `.codex/agents/trellis-implement.toml`: review `implement.md` critically, then execute steps in order.

## Target Behavior

The inline breadcrumb should state that `implement.md` is an ordered execution contract when present.

The main session should:

1. Read `prd.md`, `design.md`, and `implement.md`.
2. Review `implement.md` against current code/spec reality before coding.
3. Keep one current top-level implement step active at a time.
4. Run the proof/check named by that step before moving on.
5. Stop for unclear instructions, failed gates, or required user decisions.
6. Batch, reorder, or merge steps only after stating the reason first.

## Boundaries

This is a workflow/prompt behavior change only.

No change to:

- `codex.dispatch_mode` default.
- hook selection logic.
- task status mapping.
- implement/check sub-agent definitions except as reference behavior.
- Superpowers upstream skills.

## Verification Strategy

Add or update template tests so the generated workflow template protects the new inline plan-discipline strings.

Run targeted test:

```bash
pnpm --filter @mindfoldhq/trellis test -- test/templates/trellis.test.ts
```

Expected result: the Trellis template test file passes.

If the template test command is unavailable or too broad in this environment, run:

```bash
pnpm --filter @mindfoldhq/trellis test
```

Expected result: CLI test suite passes.

