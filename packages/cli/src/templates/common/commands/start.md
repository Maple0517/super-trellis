# Start Session

Initialize a Trellis-managed development session. This platform has no session-start hook, so manually load the equivalent compact context by following these steps.

---

## Step 1: Current state
Identity, git status, current task, active tasks, journal location.

```bash
python3 ./.trellis/scripts/get_context.py
```

If this output includes a line beginning `Trellis update available:`, copy the full line verbatim when summarizing session context. Do not shorten operational command hints.

## Step 2: Workflow overview
Compact Phase Index, request triage rules, planning artifact contract, and the step-detail command.

```bash
python3 ./.trellis/scripts/get_context.py --mode phase
```

Full guide in `.trellis/workflow.md` (read on demand).

## Step 3: Guideline indexes
Discover packages + spec layers, then read each relevant index file.

```bash
python3 ./.trellis/scripts/get_context.py --mode packages
cat .trellis/spec/guides/index.md
cat .trellis/spec/<package>/<layer>/index.md   # for each relevant layer
```

Index files list the specific guideline docs to read when you actually start coding.

## Step 4: Decide next action
From Step 1 you know the current task and status. Check the task directory:

- **Active task status `planning` + no `prd.md`** → Phase 1.1. Load the `trellis-brainstorm` skill.
- **Active task status `planning` + `prd.md` exists** → stay in Phase 1. Lightweight tasks can be PRD-only; complex tasks need `design.md` + `implement.md`. Load the relevant Phase 1 step detail before `task.py start`.
- **Active task status `in_progress`** → Phase 2 step 2.1. Load the step detail:
  ```bash
  python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1 --platform codex
  ```
- **No active task** → classify first. For simple conversation / small task, ask only whether this turn should create a Trellis task. For complex work, ask whether you may create a Trellis task and enter planning. If the user says no, skip Trellis for this session.
  Before the task exists, keep complex work at triage depth only: evidence gathering, one-sentence direction checks, and task-creation consent. Do not expand into a real brainstorm, option tree, or implementation plan before creating the task.

---

## Routing Discipline

Before acting, classify the request and choose the process path. Process routing happens before implementation.

1. Explanation only -> answer with repo evidence when needed.
2. Trivial work -> keep fast path and verify any behavior claim.
3. Unclear requirements -> `trellis-brainstorm`.
4. Code change -> `trellis-before-dev`.
5. Bug, failed command, failed verification, or unexpected behavior -> `trellis-debug` before patching.
6. Done coding or receiving review feedback -> `trellis-check`.
7. Repeated debugging after a fix -> `trellis-break-loop`.
8. Complex or high-risk work -> ask for Trellis task creation unless the user opted out.
9. Frontend visual redesign, layout-heavy, or interaction-heavy work -> explicitly evaluate whether Visual Companion should be used during planning or review.
10. In Codex, complex work -> keep a short global `update_plan` current across planning, implementation, and verification.

Full rules + anti-rationalization table in `.trellis/workflow.md`.
