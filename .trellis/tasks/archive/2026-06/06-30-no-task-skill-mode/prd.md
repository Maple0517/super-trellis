# Enable no-task skill mode

## Goal

Allow Trellis discipline skills to run without an active Trellis task, while preserving a single Trellis workflow and keeping task lifecycle features task-bound.

## Requirements

- Add a "no-task skill mode" design for Trellis so agents can use selected Trellis skills without creating or starting a Trellis task.
- Keep a single Trellis workflow. Do not introduce a second workflow for no-task usage.
- Preserve discipline in no-task mode. No-task usage must not weaken proof, debugging, verification, or handoff gates.
- Keep the following skills task-only:
  - `trellis-break-loop`
  - `trellis-finish-work`
  - `trellis-continue`
  - `trellis-channel`
- Redesign all other Trellis skills to allow no-task usage, with explicit behavior for when no active task exists.
- No-task mode must not automatically create or require task artifacts such as `prd.md`, `design.md`, `implement.md`, archive, or journal output.
- No-task mode must be pure-discipline mode: no additional durable non-task notes, planning files, or sidecar records. The only allowed durable write outside code changes is `.trellis/spec` through `trellis-update-spec`.
- No-task mode must still allow escalation into task mode when work becomes complex, persistent, multi-stage, or needs lifecycle tracking.
- Workflow routing in `no_task` state must stop meaning "skip Trellis entirely" and instead distinguish:
  - plain conversation
  - small inline work with Trellis discipline but no task
  - work that must be upgraded into a Trellis task
- No-task skill routing must be automatic based on prompt intent. The user must not need to explicitly name Trellis skills.
- Existing task mode behavior must remain intact for task-bound flows.
- No-task mode must upgrade back to task-creation consent when any hard upgrade trigger is hit.
- For complex work after the user declines task creation, no-task `trellis-brainstorm` may gather evidence, narrow direction, and recommend scope, but must not expand into full implementation planning.
- In no-task mode, `trellis-update-spec` may recommend writing `.trellis/spec`, but must ask for and receive explicit user approval before performing the write.

## Confirmed Facts

- Current `no_task` workflow language says small work can skip Trellis for the session.
- Current `trellis-brainstorm` explicitly assumes task creation and writes to `prd.md`.
- Current `trellis-before-dev` assumes current task artifacts exist and reads `prd.md`, `design.md`, and `implement.md`.
- Current `trellis-check` also assumes current task artifacts exist and reads them before verification.
- `trellis-debug`, `trellis-update-spec`, `trellis-session-insight`, and `trellis-meta` are conceptually easier to adapt to no-task mode than lifecycle-heavy skills.
- The user explicitly wants `trellis-channel` to remain task-only even though it is not a lifecycle skill.
- The user explicitly wants no-task skill routing to be automatic from prompt intent, not based on explicit user skill invocation.
- The user approves asking for consent before no-task `.trellis/spec` writes and only writing after explicit approval.

## Out Of Scope

- Adding a second workflow for no-task sessions.
- Changing `trellis-break-loop`, `trellis-finish-work`, `trellis-continue`, or `trellis-channel` into no-task-capable skills.
- Weakening TDD, debug, verification, or milestone handoff rules for no-task sessions.
- Solving every possible no-task UX edge case in one pass if a simpler first rollout can preserve discipline.

## Acceptance Criteria

- [ ] `workflow.md` defines no-task routing that still allows Trellis discipline skills without task creation.
- [ ] A clear task-mode vs no-task-mode contract exists for each affected skill.
- [ ] `trellis-brainstorm` supports a no-task mode that can clarify scope without requiring `prd.md`.
- [ ] `trellis-before-dev` supports a no-task fallback that reads repo specs and current request/context without task artifacts.
- [ ] `trellis-check` supports a no-task fallback that verifies against current request, diff, and specs without task artifacts.
- [ ] `trellis-debug`, `trellis-update-spec`, `trellis-session-insight`, and `trellis-meta` have explicit no-task wording where needed.
- [ ] The four task-only skills remain clearly task-only in wording and routing.
- [ ] No-task mode includes explicit upgrade triggers for when a Trellis task must be created.
- [ ] No-task mode auto-routes discipline skills from prompt intent without requiring explicit skill names.
- [ ] No-task mode does not create any durable note/planning file outside normal code changes and optional `.trellis/spec` updates.
- [ ] A stable set of hard upgrade triggers is defined so no-task mode cannot silently absorb task-worthy work.
- [ ] No-task `trellis-brainstorm` has a bounded complex-work mode: it may do direction narrowing and recommendations, but must not become full implementation planning.
- [ ] In no-task mode, `.trellis/spec` writes only happen after the agent asks and the user explicitly approves.
- [ ] Template tests or regression markers cover the new no-task behavior so it does not silently regress.

## Upgrade Triggers

No-task mode must stop and request Trellis task creation when any of the following becomes true:

1. The work needs persistent planning or durable decision records such as `prd.md`, `design.md`, or `implement.md`.
2. The work spans multiple stages, multiple sessions, or otherwise will not naturally finish inside the current inline pass.
3. The work needs task lifecycle features such as `trellis-continue`, `trellis-finish-work`, archive, or journal recording.
4. The work needs structured decomposition or coordination such as parent/child task trees, explicit dependency management, or `trellis-channel`.
5. Risk or scope increases to the point that explicit planning, rollback thinking, or code-level implementation sequencing is needed.
6. Future agents or sessions will need durable context injection beyond the current conversation, such as task artifacts, JSONL manifests, curated research files, or stable handoff context.

## Open Questions

- Which affected skills need only wording/routing changes, and which ones require real no-task fallback logic to operate safely?

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
