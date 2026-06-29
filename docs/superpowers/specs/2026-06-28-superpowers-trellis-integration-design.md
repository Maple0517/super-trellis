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
| `executing-plans` | Phase 2.1 walkthrough and in-progress breadcrumb | Load plan, review it critically, execute step-by-step, stop on blockers, checkpoint progress. `trellis-continue` stays a resume/navigation skill. |
| `finishing-a-development-branch` | Phase 3.4, `trellis-finish-work` | Verify before merge/PR/cleanup, present integration choices, preserve evidence, then archive/journal through Trellis. |
| `receiving-code-review` | `trellis-check`, review handling sections | Understand feedback, verify against codebase, push back technically when wrong, no performative agreement. |
| `requesting-code-review` | `trellis-check`, Phase 2.2 | Request review after major tasks, high-risk changes, stuck states, and before merge; classify review findings by severity. |
| `systematic-debugging` | new pre-fix `trellis-debug`, bug/failure routing in workflow; `trellis-break-loop` only clarifies post-fix retrospective responsibility | Reproduce, read errors, inspect recent changes, find root cause before fixing, add regression prevention. |
| `test-driven-development` | `trellis-before-dev`, Phase 2.1 | Red/green/refactor for behavior changes; failing test, reproduction, or recorded substitute proof before implementation; if implementation precedes proof, discard it and restart from proof. |
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

## 5.5 Auxiliary Asset Integration

Superpowers skills include auxiliary prompts, references, scripts, and test documents beyond `SKILL.md`. These assets must be classified and handled explicitly; reading only the top-level skill files is not enough for maximum integration.

### Absorb into skills or `.trellis/spec/guides`

These should become Trellis-native guidance or references:

| Auxiliary asset | Trellis destination | Reason |
|---|---|---|
| `systematic-debugging/root-cause-tracing.md` | `trellis-debug` reference or `.trellis/spec/guides/debugging.md` | Core pre-fix investigation technique. |
| `systematic-debugging/condition-based-waiting.md` | testing/debugging guide | Directly useful for flaky tests and async verification. |
| `systematic-debugging/defense-in-depth.md` | debugging or validation guide | Prevents single-point fixes after invalid-data bugs. |
| `test-driven-development/testing-anti-patterns.md` | `trellis-before-dev` / `trellis-check` references | Strengthens test quality beyond the TDD gate. |
| `writing-skills/anthropic-best-practices.md` | `trellis-meta` reference | Directly improves Trellis skill authoring. |
| `writing-skills/persuasion-principles.md` | `trellis-meta` reference | Helps write skills that resist agent rationalization. |
| `writing-skills/testing-skills-with-subagents.md` | `trellis-meta` reference or skill-verification guide | Useful for validating Trellis skills under pressure. |

### Selectively absorb because the value is narrow

These are useful only in specific scenarios:

| Auxiliary asset | Selective use |
|---|---|
| `brainstorming/visual-companion.md` and browser companion scripts | Explicit evaluation required for frontend visual tasks; not mandatory to use, but mandatory to evaluate before design lock. Do not silently skip. |
| `systematic-debugging/test-*.md` pressure tests | Reuse as validation scenarios for `trellis-debug`, not as runtime skill text. |
| `writing-skills/examples/CLAUDE_MD_TESTING.md` | Reuse as examples for skill testing, not as Trellis runtime guidance. |
| `systematic-debugging/condition-based-waiting-example.ts` and `find-polluter.sh` | Keep as optional examples/scripts if a matching Trellis guide needs concrete fixtures. |
| `writing-skills/graphviz-conventions.dot` and `render-graphs.js` | Keep only for skill-documentation diagrams when Trellis meta docs need rendered examples. |

### Reference comparison against Trellis agents and channel runtime

These are prompt or agent-shape assets. They should be compared with existing Trellis channel/agent behavior and used to fill gaps, not copied blindly:

| Auxiliary asset | Comparison target |
|---|---|
| `brainstorming/spec-document-reviewer-prompt.md` | Trellis design/spec review flow. |
| `writing-plans/plan-document-reviewer-prompt.md` | Trellis `implement.md` review expectations. |
| `requesting-code-review/code-reviewer.md` | `trellis-check` and Trellis channel reviewer prompts. |
| `subagent-driven-development/implementer-prompt.md` | Trellis channel worker prompt shape. |
| `subagent-driven-development/spec-reviewer-prompt.md` | Trellis channel spec-review worker shape. |
| `subagent-driven-development/code-quality-reviewer-prompt.md` | Trellis channel code-quality review worker shape. |
| `using-superpowers/references/codex-tools.md`, `copilot-tools.md`, `gemini-tools.md` | Platform-specific Trellis hook/skill instructions. |
| all `agents/openai.yaml` files | Compare against Trellis agent definitions and platform template defaults; use only missing constraints, not raw agent wrappers. |

### Do not absorb

These should not become Trellis runtime behavior:

| Auxiliary asset | Reason |
|---|---|
| `systematic-debugging/CREATION-LOG.md` | Historical skill-creation record, not runtime guidance. |
| Raw visual companion server implementation | Useful only if Trellis deliberately adds a visual companion feature later. |
| Superpowers platform wrapper details that conflict with Trellis hooks | Trellis owns platform hook and context injection semantics. |
| Superpowers worktree and duplicate lifecycle wrappers inside auxiliary agent configs | Trellis task/workspace/finish lifecycle remains authoritative. |

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

- task-creation consent before substantive brainstorming; `no_task` state stays at triage depth only,
- repo evidence before questions,
- one question at a time,
- recommended answer with trade-off,
- 2-3 approaches before settling,
- design approval before implementation plan,
- explicit Visual Companion evaluation for frontend visual, layout-heavy, or interaction-heavy work,
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
- expose `trellis-debug` in the in-progress breadcrumb because breadcrumbs are the only per-turn mandatory channel,
- execute the plan step-by-step,
- use the platform's native step-tracking tool (`update_plan` on Codex, `TodoWrite` on Claude Code) to keep progress visible,
- stop and ask when blocked,
- run verification at each planned checkpoint,
- when the planned scope and acceptance criteria are verified, move to Phase 3; do not suggest new polish or follow-up work before offering the finish flow,
- for multi-agent work, use Trellis channel orchestration and return summaries to the main session.

### 6.4 Phase 2.2: Quality check

Quality check should absorb review and verification behavior:

- no completion claim without fresh proof,
- review required for high-risk work,
- review feedback must be verified, not blindly accepted,
- critical findings block progress,
- important findings block merge unless explicitly deferred,
- minor findings can be logged,
- when checks are green for the planned scope, the next step is Phase 3 (spec update, commit, finish); additional polish or follow-up work is a new scope decision and requires user approval.

### 6.5 Phase 3: Finish

Phase 3 should absorb branch-finish discipline without replacing Trellis finish:

- verify full intended test suite before commit/merge/PR,
- present local merge / PR / leave branch / discard choices when relevant,
- before staging or committing, inspect staged files separately from unstaged files; unstage unrelated paths before the work commit,
- do not archive task before work commits are handled,
- if `.trellis/` or platform directories are gitignored, archive and journal writes may remain local; report that state instead of forcing `git add -f`,
- use Trellis archive and session journal as the final source of truth.

---

## 7. Target Trellis Skill Changes

### 7.1 `trellis-start`

Add Superpowers-style routing semantics:

- classify task before action,
- process skill before implementation skill,
- simple-task fast path allowed,
- complex/high-risk tasks require task workflow,
- if user refuses task creation, shrink scope or stay in explanation mode,
- in `no_task` state, keep complex work at triage depth only; do not expand into brainstorm or implementation planning before the task exists,
- frontend visual, layout-heavy, or interaction-heavy work must explicitly evaluate Visual Companion during planning or review,
- on Codex, complex work should keep a short global `update_plan` current across planning, implementation, and verification.

### 7.2 `trellis-brainstorm`

Strengthen with Superpowers brainstorming:

- task-creation consent before substantive brainstorming; `no_task` state stays at triage depth,
- context evidence before user questions,
- one question per turn,
- recommended answer and trade-off in each question,
- 2-3 options before design,
- design approval gate,
- explicit Visual Companion evaluation for frontend visual tasks; do not silently skip,
- decomposition of too-large scopes,
- design self-review before plan writing.

### 7.3 `trellis-before-dev`

Strengthen with:

- applicable spec loading,
- TDD gate authority: Iron Law, decision matrix, verify-RED, discard-and-restart violation consequence, rationalizations, red flags,
- impact/risk check,
- behavior-change test expectation,
- bugfix route into pre-fix `trellis-debug` when root cause is unclear.

TDD is split by reader:

- `trellis-before-dev` is the gate authority: no implementation code before failing proof.
- `.trellis/spec/guides/testing-guide.md` is the test-quality authority: Good Tests, Good/Bad examples, When Stuck, mocking anti-patterns, regression red-green, and verification checklist.
- Workflow breadcrumbs and implement/check agents carry compact execution rules plus references to those two authorities.

### 7.4 `trellis-check`

Strengthen with:

- verification-before-completion gate,
- proof command selection,
- review-request rules,
- review-reception rules,
- no positive completion language until evidence exists.

### 7.5 `trellis-debug`

Create as the pre-fix systematic debugging skill:

- reproduce first,
- read full error output,
- obey the Iron Law: no fixes without root-cause investigation first,
- stop on red flags such as quick fixes, speculative patching, or "I see the problem" without evidence,
- inspect recent changes,
- form and test hypotheses,
- fix root cause,
- add regression proof,
- capture reusable lesson into specs when warranted.

### 7.6 `trellis-break-loop`

Keep as post-fix retrospective:

- clarify that `trellis-debug` handles pre-fix investigation,
- classify why repeated fixes failed after the bug is fixed,
- propose durable prevention after evidence exists.

### 7.7 `trellis-channel`

Adapt Class 1 Superpowers orchestration:

- independent-domain detection,
- worker context bundle requirements,
- dispatcher wait semantics,
- implementer/reviewer checkpoint pattern,
- main-session integration responsibilities.

### 7.8 `trellis-finish-work`

Strengthen with branch completion discipline:

- verify before finish choices,
- handle branch/PR/merge decision before archive,
- distinguish dirty files from current task vs other work,
- keep archive/journal as Trellis finalization.

### 7.9 `trellis-meta`

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

## 10.5 Pomotree Inline Experiment Feedback

A full Codex inline feature run on the Pomotree project (Next.js + Tauri, frontend UI redesign) exposed runtime gaps that the integration must close:

| Finding | Gap | Required fix |
|---|---|---|
| Agent brainstormed deeply before task creation | `no_task` state had no triage depth limit | Enforce triage-only before task creation in `trellis-start`, `trellis-brainstorm`, workflow breadcrumbs, and guardrails |
| Visual Companion was never offered for a frontend UI task | Visual Companion classified as "optional"; agent silently skipped | Change to explicit evaluation required for frontend visual tasks in `trellis-brainstorm`, `trellis-start`, and breadcrumbs |
| No Codex step-tracking popup during implementation | Agent did not call `update_plan`; user had no progress visibility | Add `update_plan` / `TodoWrite` integration to `trellis-start`, `trellis-before-dev`, breadcrumbs, and guardrails |
| Agent suggested "visual polish" after implement.md was complete | No finish gate to transition from Phase 2 to Phase 3 | Add finish gate: when planned scope and acceptance criteria are verified, move to Phase 3 before suggesting new work |
| Commit included pre-existing staged files | Agent did not inspect staged vs unstaged separately | Add staged-file hygiene to `trellis-finish-work` safety rules |
| Trellis archive/journal writes remained local | `.trellis/` was gitignored; agent tried to force-add | Report local state instead of forcing `git add -f` |
| Platform-level implement/check agents missed TDD gates | `.trellis/agents/*` was updated, but `.codex/agents/*` and `.claude/agents/*` still had old prompts | Sync compact TDD execution/evidence gates into platform agents |
| TDD absorption was only a skeleton | Core proof gate existed, but Superpowers anti-drift pieces were thin | Add Iron Law, rationalizations, red flags, Good Tests, Good/Bad examples, When Stuck, and verification checklist |

All findings are encoded as runtime rules in the workflow, skills, guides, and local platform/channel agents.

---

## 11. Design Self-Review

- Placeholder scan: no placeholder markers or vague future-fill language remain.
- Scope check: focused on local Trellis magic-mod integration, not publishing or upstreaming.
- Conflict check: Trellis remains the only workflow; Superpowers outer task/finish lifecycle is not imported.
- Max-integration check: plan requires workflow, skills, artifacts, review, execution, debugging, and channel routing changes; it is not a few added sentences.
- Classification check: all 14 Superpowers skills are accounted for across the three classes.
- Pomotree experiment check: no-task triage depth, Visual Companion evaluation, platform step-tracking, finish-before-polish gate, staged-file hygiene, and ignored-runtime reporting are all encoded as runtime rules.
- TDD absorption check: gate authority and test-quality authority are separated; platform/channel agents get compact execution/evidence rules and references, not duplicated long tutorials.
