# 技术设计 — No Task Skill Mode

## Overview

This task adds a dual-mode contract to Trellis discipline skills:

- **task mode** — existing behavior with an active Trellis task and task artifacts
- **no-task mode** — no active task, but Trellis discipline still runs automatically from prompt intent

The design keeps a single Trellis workflow. It does **not** create a second no-task workflow, and it does **not** permit no-task mode to grow its own durable planning artifacts. The only durable write allowed in no-task mode is `.trellis/spec`, and only after explicit user approval.

## Source Of Truth

The implementation must change template sources, not generated project copies.

Primary source files:

- `packages/cli/src/templates/trellis/workflow.md`
- `packages/cli/src/templates/common/skills/brainstorm.md`
- `packages/cli/src/templates/common/skills/before-dev.md`
- `packages/cli/src/templates/common/skills/check.md`
- `packages/cli/src/templates/common/skills/debug.md`
- `packages/cli/src/templates/common/skills/update-spec.md`

Validation surface:

- `packages/cli/test/templates/disciplined-runtime.test.ts`
- `packages/cli/test/templates/trellis.test.ts`
- any platform-neutral/template resolver tests that fail when shared wording leaks platform-specific command syntax

Generated local project copies (`.agents/skills`, `.claude/skills`, `.trellis/workflow.md`) should be refreshed through `pnpm --filter @mindfoldhq/trellis build` + `trellis update`, not edited as the primary implementation surface.

## Core Contract

### No-task mode

No-task mode means:

- there is no active task
- discipline skills may still auto-route from prompt intent
- no task artifacts are required
- no durable no-task planning/note file may be created
- complexity may be narrowed, but not promoted into full implementation planning for complex work

No-task mode is **pure discipline mode**, not a lightweight task system.

### Task mode

Task mode remains the existing Trellis path:

- active task required
- planning artifacts (`prd.md`, `design.md`, `implement.md`) allowed/required by scope
- `continue`, `finish-work`, archive, journal, and channel remain task-bound

### Upgrade rule

No-task mode may start work, but must return to task-creation consent when any hard upgrade trigger is hit. Upgrade is not optional once a trigger is met.

## Workflow changes

### `workflow.md` no-task routing

Current behavior:

- small work can skip Trellis entirely
- complex work in `no_task` is triage only
- substantive brainstorming starts only after task creation

Target behavior:

- plain conversation can still remain outside Trellis discipline
- small inline work without a task still auto-routes `trellis-brainstorm`, `trellis-before-dev`, `trellis-debug`, `trellis-check`, or `trellis-update-spec` based on prompt intent
- complex work may use bounded no-task brainstorming for evidence gathering, direction narrowing, and recommendation
- once bounded no-task brainstorming hits an upgrade trigger, the agent must ask to create a task before continuing deeper

### Guardrail rewrite

The current guardrail:

- “Complex work in `no_task` state is triage only; substantive brainstorming starts only after task creation.”

must be replaced with a dual-mode rule:

- no-task discipline is allowed
- complex no-task brainstorming is bounded
- full implementation planning still requires task mode

## Skill groups

### Task-only skills

Remain task-only by wording and routing:

- `trellis-break-loop`
- `trellis-finish-work`
- `trellis-continue`
- `trellis-channel`

These skills either depend directly on lifecycle state or are intentionally kept task-bound by user decision.

### Wording/routing-only changes

These skills mostly need dual-mode wording, not heavy logic changes:

- `trellis-debug`
- `trellis-update-spec`
- `trellis-session-insight`
- `trellis-meta`

Expected change shape:

- clarify they may operate without an active task
- remove any hidden assumption that task artifacts exist
- state no-task constraints where relevant

### Real fallback logic required

These skills need real execution-path changes, not only wording:

- `trellis-brainstorm`
- `trellis-before-dev`
- `trellis-check`

These currently assume task artifacts exist and therefore need explicit no-task input rules.

## Skill-by-skill design

### `trellis-brainstorm`

#### Task mode

Keep current behavior:

- create/use task
- update `prd.md`
- for complex work create/update `design.md` and `implement.md`

#### No-task mode

New bounded mode:

- inspect repository evidence first
- clarify intent one question at a time when needed
- offer recommendations and scope narrowing
- do **not** create `prd.md`
- do **not** create `design.md` / `implement.md`
- for complex work, stop at “direction + recommendation + ask again to create task”

Key rule:

- no-task brainstorm may help choose direction
- it may not become durable or implementation-level planning

### `trellis-before-dev`

#### Task mode

Keep current behavior:

- read `prd.md`, `design.md`, `implement.md`
- discover relevant specs
- apply TDD/proof gate before writing code

#### No-task mode

Fallback inputs:

- current user request
- files about to be changed or current diff target area
- `.trellis/spec/guides/index.md`
- relevant package/layer spec indexes

Behavior:

- still mandatory before coding when prompt intent says “about to implement”
- still enforce TDD/proof gate fully
- does not block on missing task artifacts

### `trellis-check`

#### Task mode

Keep current behavior:

- read task artifacts
- read relevant specs
- run checks
- apply completion/milestone gates

#### No-task mode

Fallback inputs:

- current request / stated scope
- current diff
- changed paths
- relevant specs
- fresh verification command output

Behavior:

- run verification without requiring `prd.md`, `design.md`, `implement.md`
- still enforce completion gate
- still enforce milestone handoff
- if verification passes and changes are uncommitted, must explicitly offer `review diff / commit now / stop local`

### `trellis-debug`

No-task wording should explicitly allow:

- bug investigation before any task exists
- root-cause analysis based on reproduction and evidence

If the bug becomes persistent, multi-stage, or needs durable context, it must trigger task creation.

### `trellis-update-spec`

No-task mode allowed, but:

- no automatic write
- the skill may recommend a spec update
- it must ask and receive explicit user approval before writing `.trellis/spec`

### `trellis-session-insight`

No-task mode requires only wording clarification:

- session recall is allowed without a task
- any write-back destination still follows the no-task persistence rules

### `trellis-meta`

No-task mode requires only wording clarification:

- Trellis self-customization may happen without an active task when the user is making small framework edits
- larger architectural changes may still choose task mode

## Automatic routing

No-task skill routing must be automatic from prompt intent, not explicit skill invocation.

Implications:

- `workflow.md` no-task breadcrumb must no longer instruct the agent to skip Trellis after task refusal
- descriptions and routing text must make it clear that discipline skills may still fire in no-task mode
- the agent should not require the user to name skills such as `trellis-check`

## Upgrade triggers

The PRD’s six upgrade triggers become the canonical no-task → task escalation contract.

Implementation consequence:

- `workflow.md` should mention that no-task mode is valid only until an upgrade trigger is hit
- affected skills (`trellis-brainstorm`, `trellis-before-dev`, `trellis-check`, `trellis-debug`) should each reference escalation when their local work reveals one of those triggers

## Testing strategy

Add regression markers proving:

- `workflow.md` no longer says “skip Trellis for this session” after task refusal
- `workflow.md` explicitly allows no-task discipline routing
- `trellis-brainstorm` contains a no-task bounded mode
- `trellis-before-dev` contains a no-task fallback
- `trellis-check` contains a no-task fallback
- `trellis-update-spec` requires explicit approval before no-task spec writes
- task-only skills remain clearly task-only

Run:

- targeted template tests
- shared template resolver tests if shared skill wording introduces platform-specific command strings

## Risks

### Risk 1: No-task mode becomes a second workflow

Mitigation:

- forbid durable non-task planning artifacts
- bound no-task brainstorming depth
- enforce upgrade triggers

### Risk 2: Automatic routing becomes too weak

Mitigation:

- rewrite `workflow.md` no-task breadcrumb clearly
- add fallback logic in the three skills that truly need it

### Risk 3: Automatic routing becomes too permissive

Mitigation:

- keep task-only skills task-only
- keep hard upgrade triggers explicit
- require explicit consent for no-task `.trellis/spec` writes

### Risk 4: Shared skill wording breaks platform resolver tests

Mitigation:

- use neutral command placeholders like `{{CMD_REF:finish-work}}` when needed
- rerun template tests after every wording pass
