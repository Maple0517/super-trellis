# Superpowers → Trellis Local Integration Design

**Date:** 2026-06-28
**Scope:** Local Trellis fork / local magic-mod version only.
**Decision:** Maximize absorption of Superpowers strengths while preserving Trellis as the only project-management workflow.

---

## 1. Goal

Upgrade Trellis from:

> project-management framework + foundational skills

into:

> project-management framework + deeply integrated Superpowers-grade execution, planning, review, debugging, and routing kernel.

This is not a documentation-only patch. The integration must change Trellis workflow semantics, skill responsibilities, phase gates, planning artifact contracts, review expectations, and agent orchestration rules.

---

## 2. Non-goals

- Do not create a second workflow beside `.trellis/workflow.md`.
- Do not copy Superpowers file locations as-is when Trellis already has task artifacts.
- Do not force every small request into a Trellis task.
- Do not absorb `using-git-worktrees` as a Trellis default.
- Do not preserve Superpowers branding or wrappers when the underlying method can become native Trellis behavior.
- Do not make this upstream-compatible unless it falls out naturally; this is for local magic-mod Trellis.

---

## 3. Current Architecture Comparison

### 3.1 Trellis today

Trellis owns durable project structure:

- `.trellis/workflow.md` as the single phase guide.
- `.trellis/tasks/` for active and archived task state.
- `.trellis/spec/` for package and layer guidelines.
- `.trellis/workspace/` for developer journals and session records.
- `trellis-channel` for durable multi-agent collaboration.
- Skills such as `trellis-start`, `trellis-brainstorm`, `trellis-before-dev`, `trellis-check`, `trellis-break-loop`, `trellis-finish-work`, and `trellis-meta`.

Trellis strength: project memory, task lifecycle, specs, hooks, platform templates, and persistent collaboration.

Trellis weakness: weaker hard gates, weaker execution-plan contract, weaker anti-rationalization rules, weaker review discipline, and less precise guidance on when to stop and ask.

### 3.2 Superpowers today

Superpowers owns strong operating discipline:

- mandatory process-skill selection before action,
- brainstorm before creative implementation,
- complete written implementation plans,
- TDD red/green/refactor,
- systematic debugging before fixes,
- verification before completion claims,
- review request/reception etiquette,
- checkpointed execution,
- subagent orchestration patterns,
- skill authoring standards.

Superpowers strength: behavioral rigor and agent anti-drift rules.

Superpowers weakness in this repo: it can form a parallel workflow with its own artifacts, worktree assumptions, branch-finish lifecycle, and subagent execution model unless absorbed carefully.

---

## 4. Integration Principle

Absorb Superpowers strengths at the highest Trellis-native level possible:

1. If a Superpowers strength can become a Trellis workflow rule, put it in `.trellis/workflow.md`.
2. If it maps naturally to an existing Trellis skill, merge it into that skill.
3. If it conflicts with Trellis runtime architecture but is valuable, add an adapted Trellis-native path and adjust routing.
4. If Trellis already has an equivalent or the Superpowers outer shell would create a second lifecycle, do not absorb that part.

The unit of absorption is not always a whole skill. A single Superpowers skill may contribute:

- routing semantics,
- gates,
- artifact requirements,
- execution model,
- review behavior,
- verification behavior,
- or text that should be rejected because it duplicates Trellis lifecycle.

---

## 5. Three-Class Skill Classification

### Class 1: Valuable but architecturally conflicting; add adapted Trellis-native support and adjust routing

These are not copied directly. They require Trellis-aware adaptation because they collide with `trellis-channel`, active task context, Codex inline mode, or Trellis task ownership.

| Superpowers skill | Conflict | Trellis-native absorption |
|---|---|---|
| `dispatching-parallel-agents` | Superpowers assumes generic parallel subagents; Trellis has durable `trellis-channel` and project/forum/thread state. | Convert into a Trellis channel orchestration mode: independent domains, explicit context bundle per worker, wait on Trellis events, integrate summaries through `trellis-check`. |
| `subagent-driven-development` | Fresh subagent per task can lose active task context and conflicts with Codex inline preference. | Convert into an optional Phase 2 execution strategy for complex implement plans. Use Trellis task artifacts as the context source and `trellis-channel` as the durable coordination layer. |

Class 1 requires real routing changes, not just doc text:

- workflow must define when orchestration is allowed,
- `trellis-channel` must be the preferred substrate,
- Codex inline remains the default for normal work,
- context injection must reference task artifacts and applicable specs,
- review checkpoints must return to the main session before proceeding.

### Class 2: Directly integrate into existing Trellis workflow and skills

These skills should become native Trellis behavior.

| Superpowers skill | Trellis integration target | Absorbed essence |
|---|---|---|
| `using-superpowers` | `.trellis/workflow.md`, `trellis-start` | Choose the right process before acting; process skills before implementation skills; anti-rationalization against skipping workflow. |
| `brainstorming` | `trellis-brainstorm`, Phase 1.1 | Explore repo context first, ask one question at a time, propose 2-3 approaches, present design for approval, decompose oversized scopes. |
| `writing-plans` | Phase 1 planning artifacts, especially `implement.md` | Bite-sized implementation steps, exact files, exact commands, expected output, no placeholders, self-review of plans. |
| `executing-plans` | Phase 2.1, `trellis-continue` | Load plan, review it critically, execute step-by-step, stop on blockers, checkpoint progress. |
| `finishing-a-development-branch` | Phase 3.4, `trellis-finish-work` | Verify before merge/PR/cleanup, present integration choices, preserve evidence, then archive/journal through Trellis. |
| `receiving-code-review` | `trellis-check`, review handling sections | Understand feedback, verify against codebase, push back technically when wrong, no performative agreement. |
| `requesting-code-review` | `trellis-check`, Phase 2.2 | Request review after major tasks, high-risk changes, stuck states, and before merge; classify review findings by severity. |
| `systematic-debugging` | `trellis-break-loop`, bugfix routing in workflow | Reproduce, read errors, inspect recent changes, find root cause before fixing, add regression prevention. |
| `test-driven-development` | `trellis-before-dev`, Phase 2.1 | Red/green/refactor for behavior changes; failing test before implementation when practical; no generated-code shortcut without test ownership. |
| `verification-before-completion` | `trellis-check`, Phase 3 | Identify proof command, run it fresh, read output, only then claim completion. |
| `writing-skills` | `trellis-meta`, skill authoring guidance | Skill trigger clarity, frontmatter quality, when to create skills, reference/script/template split, skill self-verification. |

Class 2 should change actual Trellis skill instructions and workflow detail. It is insufficient to add a short note saying “use Superpowers discipline.”

### Class 3: Do not absorb, or absorb only as a small optional note

| Superpowers part | Reason |
|---|---|
| `using-git-worktrees` as a workflow default | Trellis local workflow already has task/workspace semantics; forced worktree creation is not desired for this local magic-mod version. |
| Superpowers task lifecycle shell | Trellis already owns task creation, active task, archive, and journal. |
| Superpowers file-location conventions for specs/plans | Trellis already owns `prd.md`, `design.md`, `implement.md`; only the quality bar should transfer. |
| Generic subagent dispatch shell | Trellis should use `trellis-channel` or platform-native inline mode, not generic parallel dispatch as the default. |
| Branch cleanup as a standalone finish lifecycle | Trellis Phase 3 remains the finish lifecycle; branch integration becomes one step inside it. |
| Any rule that requires full design/plan for trivial requests | Trellis must keep simple-task fast path while retaining necessary checks. |

---

## 6. Target Trellis Workflow Changes

### 6.1 Request triage

Add a richer triage matrix to `.trellis/workflow.md`:

| Request class | Task needed | Required Superpowers-derived gates |
|---|---:|---|
| Conversation / explanation | No | Evidence check if factual. |
| Trivial edit | No by default | Scope check, no unrelated edits, verification if behavior changes. |
| Small implementation | Optional | Mini-plan, applicable specs, focused verification. |
| Complex feature | Yes | Brainstorm, design, implement plan, verification plan. |
| Bug / regression | Optional or yes by risk | Systematic debugging, repro, root cause, regression proof. |
| High-risk / cross-layer | Yes | Design approval, TDD/regression, review gate, completion evidence. |
| Multi-agent candidate | Yes | Channel orchestration plan, context bundle, review checkpoints. |

### 6.2 Phase 1: Plan

Phase 1 should absorb Superpowers planning quality:

- repo evidence before questions,
- one question at a time,
- recommended answer with trade-off,
- 2-3 approaches before settling,
- design approval before implementation plan,
- `implement.md` with bite-sized tasks,
- exact files and commands,
- no placeholder language,
- self-review before starting Phase 2.

Trellis artifacts remain:

- `prd.md` for product/acceptance scope,
- `design.md` for architecture and decision record,
- `implement.md` for execution plan.

Superpowers `docs/superpowers/plans` style is not adopted as the durable Trellis task artifact format. Its rigor is transplanted into `implement.md`.

### 6.3 Phase 2: Execute

Phase 2 should absorb execution rigor:

- start with `trellis-before-dev`,
- load applicable specs,
- decide whether TDD is required,
- for bugfixes, run systematic debugging before patching,
- execute the plan step-by-step,
- stop and ask when blocked,
- run verification at each planned checkpoint,
- for multi-agent work, use Trellis channel orchestration and return summaries to the main session.

### 6.4 Phase 2.2: Quality check

Quality check should absorb review and verification behavior:

- no completion claim without fresh proof,
- review required for high-risk work,
- review feedback must be verified, not blindly accepted,
- critical findings block progress,
- important findings block merge unless explicitly deferred,
- minor findings can be logged.

### 6.5 Phase 3: Finish

Phase 3 should absorb branch-finish discipline without replacing Trellis finish:

- verify full intended test suite before commit/merge/PR,
- present local merge / PR / leave branch / discard choices when relevant,
- do not archive task before work commits are handled,
- use Trellis archive and session journal as the final source of truth.

---

## 7. Target Trellis Skill Changes

### 7.1 `trellis-start`

Add Superpowers-style routing semantics:

- classify task before action,
- process skill before implementation skill,
- simple-task fast path allowed,
- complex/high-risk tasks require task workflow,
- if user refuses task creation, shrink scope or stay in explanation mode.

### 7.2 `trellis-brainstorm`

Strengthen with Superpowers brainstorming:

- context evidence before user questions,
- one question per turn,
- recommended answer and trade-off in each question,
- 2-3 options before design,
- design approval gate,
- decomposition of too-large scopes,
- design self-review before plan writing.

### 7.3 `trellis-before-dev`

Strengthen with:

- applicable spec loading,
- TDD decision matrix,
- impact/risk check,
- behavior-change test expectation,
- bugfix route into `trellis-break-loop` when root cause is unclear.

### 7.4 `trellis-check`

Strengthen with:

- verification-before-completion gate,
- proof command selection,
- review-request rules,
- review-reception rules,
- no positive completion language until evidence exists.

### 7.5 `trellis-break-loop`

Strengthen with systematic debugging:

- reproduce first,
- read full error output,
- inspect recent changes,
- form and test hypotheses,
- fix root cause,
- add regression proof,
- capture reusable lesson into specs when warranted.

### 7.6 `trellis-channel`

Adapt Class 1 Superpowers orchestration:

- independent-domain detection,
- worker context bundle requirements,
- dispatcher wait semantics,
- implementer/reviewer checkpoint pattern,
- main-session integration responsibilities.

### 7.7 `trellis-finish-work`

Strengthen with branch completion discipline:

- verify before finish choices,
- handle branch/PR/merge decision before archive,
- distinguish dirty files from current task vs other work,
- keep archive/journal as Trellis finalization.

### 7.8 `trellis-meta`

Absorb `writing-skills`:

- when to create or edit a Trellis skill,
- skill frontmatter quality,
- trigger descriptions,
- reference files vs main SKILL.md split,
- skill self-verification.

---

## 8. Template and Code Touch Points

The implementation plan should touch template sources first, generated local copies second only when needed for the current checkout.

Likely source files and generated mirrors:

- `/Users/maple/Documents/trellis/.trellis/workflow.md`
- `/Users/maple/Documents/trellis/.agents/skills/trellis-start/SKILL.md`
- `/Users/maple/Documents/trellis/.agents/skills/trellis-brainstorm/SKILL.md`
- `/Users/maple/Documents/trellis/.agents/skills/trellis-before-dev/SKILL.md`
- `/Users/maple/Documents/trellis/.agents/skills/trellis-check/SKILL.md`
- `/Users/maple/Documents/trellis/.agents/skills/trellis-break-loop/SKILL.md`
- `/Users/maple/Documents/trellis/.agents/skills/trellis-channel/SKILL.md`
- `/Users/maple/Documents/trellis/.agents/skills/trellis-finish-work/SKILL.md`
- `/Users/maple/Documents/trellis/.agents/skills/trellis-meta/SKILL.md`
- `/Users/maple/Documents/trellis/packages/cli/src/templates/trellis/scripts/common/workflow_phase.py`
- `/Users/maple/Documents/trellis/packages/cli/src/configurators/workflow.ts`
- `/Users/maple/Documents/trellis/packages/cli/src/templates/codex/index.ts`

If the repo maintains platform-generated skill copies under `.claude/`, `.cursor/`, `.opencode/`, `.pi/`, and `.codex/`, the implementation must either update generation templates or consciously synchronize generated copies. It must not hand-edit one platform and leave others stale.

---

## 9. Error Handling and Escape Hatches

- User can explicitly skip task creation; the agent must then reduce scope or stay in non-task mode.
- User can override a recommended gate, but the assistant must state the skipped risk.
- If plan instructions are unclear, execution stops and asks instead of guessing.
- If verification fails, completion cannot be claimed.
- If subagent/channel workers diverge, main session reviews and integrates; worker output is not trusted blindly.
- If a Superpowers rule conflicts with Trellis task lifecycle, Trellis lifecycle wins and only the useful method is retained.

---

## 10. Verification Strategy for the Integration

The implementation should be verified with scenario tests or scripted dry runs covering:

1. Simple explanation request: no task, no heavy plan, evidence discipline preserved.
2. Small edit: no forced task, but specs and verification are required where relevant.
3. Complex feature: task creation path, brainstorm, design, implement plan.
4. Bugfix: systematic debugging route before patch.
5. High-risk cross-layer change: design approval, TDD/regression, review, verification.
6. Multi-agent candidate: channel orchestration selected instead of generic subagent shell.
7. Finish flow: verify before commit/archive/journal.

---

## 11. Design Self-Review

- Placeholder scan: no placeholder markers or vague future-fill language remain.
- Scope check: focused on local Trellis magic-mod integration, not publishing or upstreaming.
- Conflict check: Trellis remains the only workflow; Superpowers outer task/finish lifecycle is not imported.
- Max-integration check: plan requires workflow, skills, artifacts, review, execution, debugging, and channel routing changes; it is not a few added sentences.
- Classification check: all 14 Superpowers skills are accounted for across the three classes.
