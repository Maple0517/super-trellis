# Harden Codex inline plan execution

## Goal

Codex inline mode must treat `implement.md` as an ordered execution contract, not just background context.

When a Trellis task has `prd.md`, `design.md`, and `implement.md`, the inline main session should execute the implementation plan step-by-step with the same plan discipline already present in implement-agent/sub-agent paths.

## Background

- Codex inline mode is selected by `.trellis/config.yaml` through the Codex dispatch behavior setting. The documented default is `inline`.
- Inline mode currently injects `.trellis/workflow.md` block `[workflow-state:in_progress-inline]`.
- That inline block loads `prd.md -> design.md -> implement.md` as context, but does not explicitly say that `implement.md` is the sequential execution contract.
- The stronger rule already exists in implement-agent surfaces:
  - `.trellis/agents/implement.md`: when `implement.md` exists, execute it step-by-step and stop if instructions are unclear or verification fails.
  - `.codex/agents/trellis-implement.toml`: read `implement.md`, review it critically, then execute steps in order.
- Observed failure mode: inline execution can batch multiple implement steps at once because the main-session breadcrumb lacks the Superpowers-style executing-plan discipline.

## Requirements

- R1: Strengthen Codex inline workflow guidance so `implement.md` is treated as a sequential execution contract.
- R2: Require inline execution to review `implement.md` critically before coding and raise blockers before starting when instructions are unclear or conflict with code/spec reality.
- R3: Require inline execution to keep a visible current-step cursor, normally one top-level step in progress at a time.
- R4: Require per-step proof/check behavior where the plan specifies verification.
- R5: Allow batching/reordering only when the agent states the reason first, such as inseparable atomic edits, dependency correction, failed verification, or user override.
- R6: Keep existing inline constraints intact: no implement/check sub-agent dispatch, TDD gate, debug gate, `trellis-check`, `trellis-update-spec`, and finish handoff.
- R7: Keep sub-agent / channel implement behavior aligned with inline behavior where the same plan-discipline language applies.
- R8: Apply the fix to both the local dogfood workflow file and the upstream Trellis workflow template so future generated projects inherit the behavior.

## Acceptance Criteria

- [ ] The inline workflow-state block explicitly says `implement.md` is the ordered execution contract.
- [ ] The inline workflow-state block requires critical review of `implement.md` before implementation.
- [ ] The inline workflow-state block requires one active plan step at a time unless batching/reordering is justified first.
- [ ] The inline workflow-state block requires stopping for unclear instructions, failed gates, or user decisions instead of guessing.
- [ ] Existing TDD, debug, check, spec-update, and finish gates remain present in the inline block.
- [ ] The local dogfood `.trellis/workflow.md` and upstream `packages/cli/src/templates/trellis/workflow.md` carry equivalent inline plan-discipline language.
- [ ] Verification confirms the affected workflow/template output matches the intended inline behavior.

## Out of Scope

- Changing Codex default dispatch mode.
- Re-enabling implement/check sub-agents for inline mode.
- Redesigning the whole Trellis task lifecycle.
- Changing Superpowers upstream skills.

## Decisions

- Scope: fix both local dogfood `.trellis/workflow.md` and upstream `packages/cli/src/templates/trellis/workflow.md`.
- Execution mode: keep Codex inline behavior; do not re-enable implement/check sub-agent dispatch.
