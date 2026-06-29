# Superpowers Trellis Phase A Local Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. This plan is Phase A only: make the target project local Trellis install at `/Users/maple/Documents/Pomotree` obey the integrated workflow. Do not dispatch implement/check sub-agents from this Codex inline session unless the user changes that constraint.

**Goal:** Integrate Superpowers-grade discipline into the target project local Trellis runtime in `/Users/maple/Documents/Pomotree` without touching template productization.

**Architecture:** Phase A edits only files currently read by Pomotree: `.trellis/workflow.md`, `.agents/skills/trellis-*`, `.trellis/agents/*`, and `.trellis/spec/guides/*`. Phase B template/init/update work is split into `docs/superpowers/plans/2026-06-28-superpowers-trellis-phase-b-template-productization.md`.

**Tech Stack:** Markdown workflow/skill/agent files, Trellis phase extraction via `.trellis/scripts/get_context.py`, local grep/frontmatter smoke checks, Git base-SHA review range.

---

## Pomotree Inline Experiment Feedback

The Pomotree Codex inline feature run exposed runtime gaps that this plan must close:

- Complex work in `no_task` state must stay at triage depth only. Substantive brainstorming, option trees, repeated product decisions, and implementation planning start after task creation.
- Frontend visual, layout-heavy, or interaction-heavy work must explicitly evaluate Visual Companion during planning or review. It is not mandatory, but silently skipping the decision is a gap.
- Codex complex work should keep a short global `update_plan` current across planning, implementation, and verification so progress remains visible.
- When planned scope, acceptance criteria, and relevant checks are green, the next step is Phase 3. Do not recommend new polish or follow-up work as the default next step before offering finish/commit/archive.
- Selective commit discipline must guard against pre-existing staged changes. Before committing, inspect staged files separately from unstaged files and unstage unrelated files before the work commit.
- If Trellis runtime files are ignored locally, archive/journal writes may remain local. This is acceptable for a local-only setup, but the finish flow must report it instead of forcing `git add -f`.

---

## Gap-Audit Corrections To Apply Before Phase B

The 2026-06-29 gap audit is useful, but it judges some Trellis-native adaptations against Superpowers' original shell. Treat its findings as follows.

### Must fix in Phase A local runtime

- **Visual Companion runnable chain:** current Pomotree runtime only asks whether Visual Companion would help. Add a Trellis-native runnable fallback because Superpowers is no longer a runtime dependency.
- **Verification anti-drift:** `trellis-check` has a Completion Claim Gate, but needs stronger verification-before-completion discipline: Iron Law, rationalization table, red flags, and a richer claim/evidence table.
- **Review feedback discipline:** `trellis-check` has READ/UNDERSTAND/VERIFY/EVALUATE/RESPOND/IMPLEMENT, but needs source-specific handling, unclear-feedback handling, implementation order, pushback criteria, and technical response patterns.
- **Writing-plan structure:** planning quality bars exist, but `implement.md` needs a concrete structure: file map first, goal/architecture/tech-stack summary when useful, bite-sized steps, exact commands, expected outputs, and verification checkpoints.
- **Debugging guide executability:** `trellis-debug` has the discipline, but `debugging-guide.md` needs runnable examples or recipes for root-cause tracing, condition-based waiting, defense-in-depth, and polluter search.
- **TDD explanatory layer:** TDD gates are strong, but add concise `Why Order Matters`, bugfix/debugging integration, and checklist refinements such as output cleanliness.
- **Platform-agent parity:** Codex remains inline by default and Claude Code remains subagent by default, but platform agent files still need the same compact status, TDD, review, and verification protocols as the channel agents.
- **Channel worker prompt template:** `trellis-channel` has orchestration rules, but needs a copyable worker prompt template with scope, goal, constraints, expected output, verification, and blocker fields.
- **Brainstorming quality controls:** absorb the useful parts only: one-question cadence, concrete 2-3 choice questions when appropriate, PRD/spec self-review, and planning checklist tracking. Do not copy Superpowers' artifact shell.
- **Writing-plan structure:** absorb the useful plan shape: file map first, Goal/Architecture/Tech Stack summary, task-by-task file lists, 2-5 minute checkbox steps, exact commands, expected output, and self-review for spec coverage, placeholder scan, and type/signature consistency.
- **Debug/TDD executable examples:** keep Trellis skills compact, but put small runnable examples and recipes into guides so the rules are executable, not just slogans.

### Auxiliary File Absorption Ledger

This ledger is for auditability only. Do not recreate these Superpowers files as a parallel runtime tree. Each source file is split into the Trellis location where its reader needs it.

| Source auxiliary file | Handling | Trellis destination | Reason |
|---|---|---|---|
| `systematic-debugging/condition-based-waiting-example.ts` | Absorb | `.trellis/spec/guides/debugging-guide.md` | Technique/example used during failure investigation; too long for `trellis-debug`. |
| `systematic-debugging/find-polluter.sh` | Absorb as script recipe | `.trellis/scripts/find-polluter.sh` + `debugging-guide.md` | Executable helper is useful; script belongs in scripts, usage belongs in guide. |
| `brainstorming/visual-companion.md` + scripts | Selectively absorb | `trellis-visual-companion` + `.trellis/workspace/visual-companion/` fallback | Need runnable visual review chain, but not Superpowers server/runtime dependency. |
| `systematic-debugging/test-pressure-1.md` | Selectively absorb | `verification-scenarios.md` + `debugging-guide.md` pressure scenarios | Tests integration behavior; not a per-turn runtime gate. |
| `systematic-debugging/test-pressure-2.md` | Selectively absorb | `verification-scenarios.md` + `debugging-guide.md` pressure scenarios | Same. |
| `systematic-debugging/test-pressure-3.md` | Selectively absorb | `verification-scenarios.md` + `debugging-guide.md` pressure scenarios | Same. |
| `systematic-debugging/test-academic.md` | Reference only | Optional self-test note in `verification-scenarios.md` | Useful for validating the skill, too academic for runtime rules. |
| `brainstorming/spec-document-reviewer-prompt.md` | Absorb checklist | `trellis-brainstorm` PRD/spec self-review | Planning artifact reviewer belongs before design lock. |
| `writing-plans/plan-document-reviewer-prompt.md` | Absorb checklist | `trellis-brainstorm` planning quality bar | `implement.md` quality is decided during planning. |
| `requesting-code-review/code-reviewer.md` | Absorb checklist | `trellis-check` + `.trellis/agents/check.md` | Review behavior belongs after implementation / review feedback; skip git SHA dispatch shell. |
| `subagent-driven-development/implementer-prompt.md` | Absorb agent rules | `.trellis/agents/implement.md` + platform implement agents | Execution/status/no-nesting rules belong to implement agents. |
| `subagent-driven-development/spec-reviewer-prompt.md` | Absorb stage | `.trellis/agents/check.md` spec-compliance stage + optional channel reviewer | Keep one Trellis check path but preserve spec-first review. |
| `subagent-driven-development/code-quality-reviewer-prompt.md` | Absorb stage | `.trellis/agents/check.md` code-quality stage + optional channel reviewer | Preserve quality review without forcing two reviewer agents. |
| GitHub thread reply guidance inside review prompts | Selective/optional | `trellis-check` PR-context subsection | Useful only when handling PR threads; not a mandatory local gate. |

### Auxiliary File Placement Rationale

Place auxiliary Superpowers files by reader and trigger point, not by source folder:

- Debugging technique examples belong in `.trellis/spec/guides/debugging-guide.md` because agents need them while investigating a failure, not every turn.
- Debugging pressure tests belong in `docs/superpowers/plans/verification-scenarios.md` because they verify the integration and should not become runtime gates.
- TDD Good/Bad examples belong in `.trellis/spec/guides/testing-guide.md` because `trellis-before-dev` should stay compact while the guide teaches test design.
- Spec and plan reviewer prompts become checklists inside `trellis-brainstorm` because they review planning artifacts before implementation approval.
- Code reviewer prompts become `trellis-check` and check-agent rules because they run after implementation or when receiving review feedback.
- Implementer prompts become implement-agent rules because they govern execution behavior, status reporting, and no nested subagents.
- Spec-reviewer and code-quality-reviewer prompts become two stages inside the check agent; Trellis keeps one default check path instead of forcing two reviewer agents.
- GitHub reply guidance is optional PR-context behavior inside review rules, not a mandatory local runtime gate.

### Do not treat as gaps

- Do not absorb `using-git-worktrees` as a default workflow.
- Do not recreate Superpowers' `docs/superpowers/specs` and `docs/superpowers/plans` artifact shell; Trellis keeps `prd.md`, `design.md`, and `implement.md`.
- Do not restore Superpowers bootstrap, skill-tool mapping, or platform adaptation docs as runtime dependencies.
- Do not force Codex into subagent mode. Codex default is inline unless the user explicitly requests workers/channel.
- Do not force Claude Code into inline mode. Claude Code default remains subagent-capable unless the user asks for inline.
- Do not require two separate reviewer agents by default. Trellis `trellis-check` may remain a single two-stage reviewer unless channel orchestration is explicitly chosen.
- Do not absorb model-tier routing, announcement/opening-statement conventions, or the raw git-SHA review dispatch shell.
- Do not preserve emotionally coercive Superpowers wording. Absorb rational discipline, not scare-copy.
- Do not treat every audit simplification as a bug. If Trellis already has a native mechanism, strengthen that mechanism instead of recreating the Superpowers mechanism.

---

## Phase A Scope

Keep:

- Pomotree local `.trellis/workflow.md`,
- Pomotree local `.agents/skills/`,
- Pomotree local `.trellis/agents/check.md` and `.trellis/agents/implement.md`,
- Pomotree local `.trellis/spec/guides/`,
- Pomotree local `.trellis/spec/cli/backend/workflow-state-contract.md` if present,
- readable Superpowers reference source at `/Users/maple/.codex/plugins/cache/openai-curated-remote/superpowers/5.1.4/skills` when the global plugin install is absent.

Defer to Phase B:

- `packages/cli/src/templates/**`,
- `packages/cli/src/configurators/shared.ts`,
- generated platform copies,
- fresh `trellis init` / `trellis update` validation,
- registry or marketplace distribution.

---

## Files And Responsibilities

### Plan artifacts

- Modify: `/Users/maple/Documents/trellis/docs/superpowers/specs/2026-06-28-superpowers-trellis-integration-design.md`
- Modify: `/Users/maple/Documents/trellis/docs/superpowers/plans/2026-06-28-superpowers-trellis-integration.md`
- Create: `/Users/maple/Documents/trellis/docs/superpowers/plans/2026-06-28-superpowers-trellis-phase-b-template-productization.md`

These plan/design documents are execution inputs. Keep them out of Phase A runtime commits unless the user asks for a separate docs commit.

### Current local workflow

- Modify: `/Users/maple/Documents/Pomotree/.trellis/workflow.md`
- Modify: `/Users/maple/Documents/Pomotree/.trellis/spec/cli/backend/workflow-state-contract.md`

### Current local skills

- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-start/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-brainstorm/SKILL.md`
- Create: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-visual-companion/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-before-dev/SKILL.md`
- Create: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-debug/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-continue/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-check/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-break-loop/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-channel/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-finish-work/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-meta/SKILL.md`
- Optional local link: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-session-insight/SKILL.md`

### Current local channel agents

- Modify: `/Users/maple/Documents/Pomotree/.trellis/agents/implement.md`
- Modify: `/Users/maple/Documents/Pomotree/.trellis/agents/check.md`

### Current local guides

- Modify: `/Users/maple/Documents/Pomotree/.trellis/spec/guides/index.md`
- Create: `/Users/maple/Documents/Pomotree/.trellis/spec/guides/debugging-guide.md`
- Create: `/Users/maple/Documents/Pomotree/.trellis/spec/guides/testing-guide.md`
- Create: `/Users/maple/Documents/Pomotree/.trellis/scripts/find-polluter.sh`

---

### Task 1: Protect scope and record base SHA

**Files:**
- Read: Git status and current HEAD
- Modify: no source files

- [ ] **Step 1: Confirm working tree scope**

Run:

```bash
git status --short
git rev-parse HEAD
```

Expected:

- Record the base SHA as `<base_sha>` for Task 8.
- Existing unrelated dirty files may be present.
- Do not stage or revert unrelated files.

- [ ] **Step 2: Commit boundary rule**

Use this rule for every later task:

```text
Only stage files changed by the current task. Review final implementation with <base_sha>..HEAD, not HEAD~N..HEAD.
Commit only if the user has approved committing. If not approved, stop after verification and report changed/staged files.
```

---

### Task 1A: Classify and route Superpowers auxiliary assets

**Files:**
- Modify: `/Users/maple/Documents/trellis/docs/superpowers/specs/2026-06-28-superpowers-trellis-integration-design.md`
- Modify: `/Users/maple/Documents/trellis/docs/superpowers/plans/2026-06-28-superpowers-trellis-integration.md`
- Read primary source: `/Users/maple/.codex/plugins/cache/openai-curated-remote/superpowers/5.1.4/skills/**/*.md`
- Read primary source: `/Users/maple/.codex/plugins/cache/openai-curated-remote/superpowers/5.1.4/skills/**/scripts/*`
- Read if present: `/Users/maple/.codex/plugins/cache/openai-curated-remote/superpowers/5.1.4/skills/**/agents/openai.yaml`
- Compare legacy local install only if present: `/Users/maple/.agents/plugins/superpowers/skills/**/*.md`

- [ ] **Step 1: Inventory auxiliary files**

Run:

```bash
find /Users/maple/.codex/plugins/cache/openai-curated-remote/superpowers/5.1.4/skills -type f ! -name SKILL.md -print | sort
find /Users/maple/.codex/plugins/cache/openai-curated-remote/superpowers/5.1.4/skills -path '*/agents/openai.yaml' -print | sort
test ! -d /Users/maple/.agents/plugins/superpowers/skills || find /Users/maple/.agents/plugins/superpowers/skills -type f ! -name SKILL.md -print | sort
```

Expected:

- Primary source contains Markdown references, prompts, scripts, examples, and tests.
- Primary source may contain zero `agents/openai.yaml`.
- Fallback snapshot contains `agents/openai.yaml` files for comparison only.

- [ ] **Step 2: Apply four-class auxiliary handling**

Use this matrix:

```text
Absorb into skill or guide:
- systematic-debugging/root-cause-tracing.md -> trellis-debug + debugging-guide.md
- systematic-debugging/condition-based-waiting.md -> debugging-guide.md
- systematic-debugging/defense-in-depth.md -> debugging-guide.md
- test-driven-development/testing-anti-patterns.md -> testing-guide.md + trellis-check
- writing-skills/anthropic-best-practices.md -> trellis-meta
- writing-skills/persuasion-principles.md -> trellis-meta
- writing-skills/testing-skills-with-subagents.md -> trellis-meta

Selectively absorb:
- brainstorming/visual-companion.md and brainstorming/scripts/* -> explicit evaluation required for frontend visual tasks; not mandatory to use, but mandatory to evaluate before design lock
- systematic-debugging/test-*.md -> pressure-test scenarios for trellis-debug
- systematic-debugging/condition-based-waiting-example.ts and find-polluter.sh -> examples in debugging-guide.md
- writing-skills/examples/CLAUDE_MD_TESTING.md -> trellis-meta example reference
- writing-skills/graphviz-conventions.dot and render-graphs.js -> optional documentation diagrams only

Reference comparison:
- brainstorming/spec-document-reviewer-prompt.md -> trellis-brainstorm design review gap check
- writing-plans/plan-document-reviewer-prompt.md -> implement.md plan review gap check
- requesting-code-review/code-reviewer.md -> trellis-check and .trellis/agents/check.md gap check
- subagent-driven-development/implementer-prompt.md -> .trellis/agents/implement.md gap check
- subagent-driven-development/spec-reviewer-prompt.md -> trellis-channel review worker guidance
- subagent-driven-development/code-quality-reviewer-prompt.md -> .trellis/agents/check.md gap check
- using-superpowers/references/codex-tools.md, copilot-tools.md, gemini-tools.md -> platform comparison only
- agents/openai.yaml fallback snapshot -> compare model/tool assumptions only

For each Reference comparison file, extract the top 3 actionable checklist items and route them to the concrete task below: spec reviewer -> Task 3 brainstorm self-review; plan reviewer -> Task 3 planning quality bar; code reviewer -> Task 5 Review Gate/check agent; implementer prompt -> Task 4 implement agents; spec reviewer prompt -> Task 5 spec-compliance review stage; code-quality reviewer prompt -> Task 5 code-quality review stage. If no gap is found, record `no action needed` in the task notes. Review workers must verify independently by reading artifacts and code; they must not trust implementer self-reports.

Do not absorb:
- systematic-debugging/CREATION-LOG.md
- raw visual companion server runtime
- Superpowers worktree/task/finish lifecycle wrappers
- platform wrapper details that conflict with Trellis hooks
```

- [ ] **Step 3: Record classification**

Expected:

- Design and plan state that auxiliary files beyond `SKILL.md` are handled.
- No source-file commit is needed for this classification task; later source-changing tasks commit the actual local files.

---

### Task 2: Update local workflow routing and breadcrumbs without losing existing constraints

**Files:**
- Modify: `/Users/maple/Documents/Pomotree/.trellis/workflow.md`
- Modify: `/Users/maple/Documents/Pomotree/.trellis/spec/cli/backend/workflow-state-contract.md`
- Test: `/Users/maple/Documents/Pomotree/.trellis/scripts/get_context.py`

- [ ] **Step 1: Add Pomotree-local Superpowers integration contract**

In `.trellis/workflow.md`, insert after `## Core Principles`:

```markdown
## Superpowers Integration Contract

Trellis remains the only project-management workflow. Superpowers contributes gates, artifact quality bars, review behavior, debugging discipline, and orchestration patterns; it does not create a second lifecycle.

Violating the letter of a gate is violating the spirit of the gate. Do not bypass a gate because the task looks simple, the fix looks obvious, or a previous command probably passed.

Simple work may skip task creation, but it may not skip relevant evidence, scope, or verification discipline. Complex and high-risk work uses Trellis tasks and progressively stronger gates.
```

- [ ] **Step 2: Extend Request Triage and Active Task Routing**

In `.trellis/workflow.md`, update `### Request Triage` so bug/failure rows route to `trellis-debug` before patching:

```markdown
Bug, regression, failed verification, or unexpected behavior: reproduce and route to `trellis-debug` before patching; create a Trellis task when risk or scope is non-trivial.
Complex task: ask whether you may create a Trellis task and enter planning. Before task creation, limit yourself to lightweight triage, repo evidence gathering, and task-creation consent. Do not expand into a real option tree, multi-round product brainstorming, or implementation planning before the task exists.
```

Then update `### Active Task Routing` without removing existing platform blocks. Add `trellis-debug` to both route groups:

```markdown
- Bug, failure, failed verification, or unexpected behavior -> `trellis-debug` before patching.
- Repeated debugging after a fix -> `trellis-break-loop`; spec updates -> `trellis-update-spec`.
```

Expected:

- `trellis-break-loop` remains post-fix retrospective.
- `trellis-debug` is reachable before patching.

- [ ] **Step 3: Extend planning breadcrumbs, do not replace them**

In `[workflow-state:planning]`, keep existing lines about lightweight/complex artifacts, parent/child tasks, and jsonl curation. Add:

```markdown
Design Gate: inspect evidence before asking, ask one question at a time, present 2-3 approaches for real design choices, and get user approval before implementation planning.
Frontend visual/interaction work: explicitly evaluate whether Visual Companion would improve design exploration or review. Use it when layout, visual hierarchy, information density, or interaction shape is hard to judge from text alone.
Plan Quality Gate: complex `implement.md` starts with file map + Goal/Architecture/Tech Stack, then task-by-task exact files, 2-5 minute checkbox steps, concrete commands, expected outputs, verification checkpoints, no placeholders, and self-review for spec coverage/type consistency.
Tracking Gate: for complex work in Codex, keep a short global `update_plan` in sync across planning, implementation, and verification so task progress remains visible.
```

In `[workflow-state:planning-inline]`, keep existing inline-mode line and add:

```markdown
Design Gate: inspect evidence before asking, ask one question at a time, present 2-3 approaches for real design choices, and get user approval before implementation planning.
Frontend visual/interaction work: explicitly evaluate whether Visual Companion would improve design exploration or review. Use it when layout, visual hierarchy, information density, or interaction shape is hard to judge from text alone.
Plan Quality Gate: complex `implement.md` starts with file map + Goal/Architecture/Tech Stack, then task-by-task exact files, 2-5 minute checkbox steps, concrete commands, expected outputs, verification checkpoints, no placeholders, and self-review for spec coverage/type consistency.
Tracking Gate: for complex work in Codex, keep a short global `update_plan` in sync across planning, implementation, and verification so task progress remains visible.
```

- [ ] **Step 4: Extend in-progress breadcrumbs, do not replace them**

In `[workflow-state:in_progress]`, keep existing lines about Agent tools, main-session dispatch, sub-agent self-exemption, dispatch prompt, and jsonl read order. Change the Flow line to include debug:

```markdown
Flow: `trellis-before-dev` -> [`trellis-debug` if bug/failure/unexpected behavior] -> `trellis-implement` -> `trellis-check` -> `trellis-update-spec` -> commit (Phase 3.4) -> `/trellis:finish-work`.
Before implementation: apply the TDD Decision Matrix in `trellis-before-dev`; if proof was skipped, the exception must be recorded before code is written.
Before completion claims: run the Completion Claim Gate in `trellis-check`.
Review feedback: route directly to the review reception section of `trellis-check`.
Tracking: for complex work in Codex, keep a short global `update_plan` current as phases advance.
Finish gate: when the planned scope and acceptance criteria are verified, move to Phase 3. Do not suggest new work or polish before offering the finish flow.
Plan execution gate: at Phase 2 start, read `implement.md`, review it critically against current code/spec reality, then execute steps in order. Continue through the plan while unblocked; stop for failed gates, unclear instructions, or user decisions.
```

In `[workflow-state:in_progress-inline]`, keep existing inline dispatch ban and read-order lines. Change the Flow line and add:

```markdown
Flow: `trellis-before-dev` -> [`trellis-debug` if bug/failure/unexpected behavior] -> edit -> `trellis-check` -> validation -> `trellis-update-spec` -> commit (Phase 3.4) -> `/trellis:finish-work`.
Before implementation: apply the TDD Decision Matrix in `trellis-before-dev`; if proof was skipped, the exception must be recorded before code is written.
Before completion claims: run the Completion Claim Gate in `trellis-check`.
Review feedback: route directly to the review reception section of `trellis-check`.
Tracking: for complex work in Codex, keep a short global `update_plan` current as phases advance.
Finish gate: when the planned scope and acceptance criteria are verified, move to Phase 3. Do not suggest new work or polish before offering the finish flow.
Plan execution gate: at Phase 2 start, read `implement.md`, review it critically against current code/spec reality, then execute steps in order. Continue through the plan while unblocked; stop for failed gates, unclear instructions, or user decisions.
```

- [ ] **Step 5: Update Guardrails**

In `### Guardrails`, add:

```markdown
- Complex work in `no_task` state is triage only; substantive brainstorming starts only after task creation.
- Frontend visual or interaction-heavy work must explicitly evaluate whether Visual Companion should be used during planning or review.
- Behavior changes and bug fixes need a failing test, reproduction, or recorded substitute proof before implementation.
- Bugs, failures, and unexpected behavior route to `trellis-debug` before patching.
- Completion and success claims require fresh proof through `trellis-check`.
- Review feedback must be verified against code reality before it is accepted.
- In Codex, complex work should keep a short global `update_plan` current so progress remains visible across phases.
```

- [ ] **Step 6: Update jsonl curation guidance for bugfix tasks**

In Phase 1.3 context curation, after the spec/research bullets, add:

```markdown
- **Debug references** — for bugfix tasks, include `.trellis/spec/guides/debugging-guide.md` and `.trellis/spec/guides/testing-guide.md` when those guides are relevant to the failure or regression proof.
```

- [ ] **Step 7: Update workflow-state contract invariants**

In `.trellis/spec/cli/backend/workflow-state-contract.md`, extend the Test invariant paragraph so it mentions:

```text
in-progress keeps debug routing, TDD proof, completion claim gate, review feedback routing, and commit reachability visible in the breadcrumb.
```

Also list these regression-test expectations in the contract:

```text
- workflow.md [workflow-state:in_progress] mentions `trellis-debug`
- workflow.md [workflow-state:in_progress] mentions TDD proof before implementation
- workflow.md [workflow-state:in_progress] mentions Completion Claim Gate
- workflow.md [workflow-state:in_progress] mentions review feedback routing
- workflow.md [workflow-state:in_progress] mentions the finish gate before new work/polish
- workflow.md [workflow-state:in_progress] still mentions commit (Phase 3.4)
```

- [ ] **Step 8: Verify phase extraction**

Run:

```bash
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 1.1 --platform codex
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1 --platform codex
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.2 --platform codex
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.4 --platform codex
```

Expected:

- Each command exits 0.
- Existing dispatch/self-exemption/jsonl breadcrumb constraints remain visible.
- New debug/TDD/completion/review gates are visible.
- No-task triage, Visual Companion evaluation, update_plan tracking, and finish-before-polish rules are visible in the relevant extracted text.

- [ ] **Step 9: Commit local workflow changes**

Run:

```bash
git add .trellis/workflow.md .trellis/spec/cli/backend/workflow-state-contract.md
git commit -m "docs: integrate superpowers gates into local trellis workflow"
```

---

### Task 3: Update local start and brainstorm skills

**Files:**
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-start/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-brainstorm/SKILL.md`
- Create: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-visual-companion/SKILL.md`

- [ ] **Step 1: Replace or merge `trellis-start` quick reference**

Replace the existing `## Skill routing (quick reference)` table, or merge into it without duplication:

```markdown
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
   Before the task exists, keep complex work at triage depth only: evidence gathering, one-sentence direction checks, and task-creation consent. Do not expand into a real brainstorm, option tree, or implementation plan before creating the task.
9. Frontend visual redesign, layout-heavy, or interaction-heavy work -> explicitly evaluate whether Visual Companion should be used during planning or review.
10. In Codex, complex work -> keep a short global `update_plan` current across planning, implementation, and verification.
11. Gate bypass language ("too simple", "just this once", "I already know", "probably fine") -> stop and apply the relevant Trellis gate.
```

- [ ] **Step 2: Add design gate to `trellis-brainstorm`**

Add near the existing interview/evidence rules:

```markdown
## Design Gate

Before implementation planning, converge on a design. Inspect project evidence first, ask one question at a time, recommend an answer with trade-offs, then present 2-3 approaches when there is a real design choice. After the user selects or approves the design, write or update the Trellis planning artifacts.

Do not use this skill for substantive brainstorming before the task exists. In `no_task` state, stay at triage depth only; once the conversation needs a real option tree, planning artifacts, or repeated product decisions, create the task first.

When the task is frontend-visual in nature, do not silently skip Visual Companion. Explicitly decide whether it would add signal. If the answer is no, proceed without it; if the answer is yes, recommend using it before design lock.

If the scope contains multiple independent subsystems, decompose it before planning implementation. Each sub-project must produce independently testable work.
```

- [ ] **Step 3: Add planning quality bar and Visual Companion runnable fallback**

In `trellis-brainstorm`, add a `## Planning Quality Bar` requiring: file map first; Goal/Architecture/Tech Stack header; `### Task N` sections with `**Files:**`; 2-5 minute checkbox steps; exact commands with expected output; and self-review for spec coverage, placeholder scan, and type/signature consistency. Ban placeholders such as TBD, TODO, "implement later", "add appropriate error handling", "write tests for the above", and "similar to previous task".

Add a PRD/spec self-review checklist before design lock, absorbing `brainstorming/spec-document-reviewer-prompt.md` without copying the prompt: placeholder scan, contradiction scan, ambiguity scan, missing acceptance-criteria scan, user-decision trace, and scope-boundary check. Fix issues inline before asking for implementation approval.

Add an implement-plan reviewer checklist, absorbing `writing-plans/plan-document-reviewer-prompt.md`: file map exists before tasks, every requirement maps to a task, every task has exact files and verification, steps are 2-5 minute single actions, no placeholders, type/signature names stay consistent across tasks, and rollback/stop points are explicit.

Also require preference questions to use 2-3 concrete choices with a recommended option when appropriate, while preserving one-question-per-message.

Create `.agents/skills/trellis-visual-companion/SKILL.md` as a Trellis-native fallback: create `.trellis/workspace/visual-companion/index.html`, serve it with `python3 -m http.server 8765`, give the user `http://localhost:8765/`, capture accepted visual decisions into task artifacts, and fall back to the HTML file path if a local server/browser is unavailable.

- [ ] **Step 4: Verify local routing text**

Run:

```bash
grep -R "Routing Discipline" .agents/skills/trellis-start/SKILL.md
grep -R "trellis-debug" .agents/skills/trellis-start/SKILL.md
grep -R "triage depth only" .agents/skills/trellis-start/SKILL.md .agents/skills/trellis-brainstorm/SKILL.md
grep -R "Visual Companion" .agents/skills/trellis-start/SKILL.md .agents/skills/trellis-brainstorm/SKILL.md
grep -R "trellis-visual-companion" .agents/skills/trellis-brainstorm/SKILL.md .agents/skills/trellis-visual-companion/SKILL.md
grep -R "Planning Quality Bar" .agents/skills/trellis-brainstorm/SKILL.md
grep -R "placeholder scan" .agents/skills/trellis-brainstorm/SKILL.md
grep -R "missing acceptance-criteria" .agents/skills/trellis-brainstorm/SKILL.md
grep -R "implement-plan reviewer" .agents/skills/trellis-brainstorm/SKILL.md
grep -R "update_plan" .agents/skills/trellis-start/SKILL.md
grep -R "Design Gate" .agents/skills/trellis-brainstorm/SKILL.md
```

- [ ] **Step 5: Commit local routing skills**

Run:

```bash
git add .agents/skills/trellis-start/SKILL.md .agents/skills/trellis-brainstorm/SKILL.md .agents/skills/trellis-visual-companion/SKILL.md
git commit -m "docs: strengthen local trellis routing and brainstorming"
```

---

### Task 4: Add local TDD, debug, continue, and implement-agent discipline

**Files:**
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-before-dev/SKILL.md`
- Create: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-debug/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-continue/SKILL.md`
- Modify only to clarify pre/post responsibility: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-break-loop/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.trellis/agents/implement.md`
- Modify: `/Users/maple/Documents/Pomotree/.codex/agents/trellis-implement.toml`
- Modify: `/Users/maple/Documents/Pomotree/.claude/agents/trellis-implement.md`
- Modify: `/Users/maple/Documents/Pomotree/.trellis/spec/guides/index.md`
- Create: `/Users/maple/Documents/Pomotree/.trellis/spec/guides/debugging-guide.md`
- Create: `/Users/maple/Documents/Pomotree/.trellis/spec/guides/testing-guide.md`

- [ ] **Step 1: Add TDD Iron Law and Decision Matrix to `trellis-before-dev`**

Add:

```markdown
## Iron Law

NO IMPLEMENTATION CODE BEFORE FAILING PROOF.

Proof means a failing test, reproduction, or executable acceptance check. Write implementation before proof? Delete it and start over. No exceptions without user permission or a recorded task-artifact reason before implementation.

## TDD Decision Matrix

Before writing implementation code, decide whether the change needs proof first.

| Change type | Required proof |
|---|---|
| New behavior | Failing test or explicit executable acceptance check before implementation. |
| Bug fix | Reproduction or regression test before fix. |
| Refactor | Existing tests pass before and after; add tests if behavior boundaries are weak. |
| Docs-only | Render/link/spell or targeted review check. |
| Config or workflow behavior | Small scripted check or command output proving the changed path. |

Gate: after writing a failing test or reproduction, run it and verify it fails for the expected reason before implementation. If it passes immediately, it is not a valid failing test.

Gate: if implementation code is written before the failing test, reproduction, user-approved substitute proof, or recorded exception in the task artifact, discard that implementation and restart from proof. Do not keep the discarded implementation as reference and do not adapt it into the test. If a failing test is genuinely impractical, record the reason and substitute proof location before writing implementation code.

Green verification: after the minimal implementation, run the new proof and the relevant existing tests. Output must be clean enough to support the claim.

Common rationalizations:

| Rationalization | Reality |
|---|---|
| "I'll test after." | Tests-after prove what code does; tests-first prove desired behavior. |
| "Tests after achieve the same goals." | Tests-after answer "what does this do?"; tests-first answer "what should this do?" |
| "I manually checked it." | Manual checks are not durable regression proof. |
| "Deleting work is wasteful." | Keeping pre-proof implementation pollutes the test and weakens the gate. |
| "Too simple to test." | Simple code breaks. Test takes 30 seconds. |
| "Keep it as reference." | You will adapt it. That is testing after. Delete means delete. |
| "Need to explore first." | Throw away exploration and restart from proof. |
| "The test is hard to write." | Hard to test often means hard to use. Simplify the design. |
| "TDD will slow me down." | TDD is faster than debugging unproven code. |
| "Manual test is faster." | Manual checks do not prove edge cases and cannot be rerun reliably. |
| "Existing code has no tests." | Improve the boundary you touch; add tests where behavior risk exists. |

## Why Order Matters

- Tests written after implementation tend to confirm what exists; tests written first define what should exist.
- Manual checks are observations, not durable regression contracts.
- Deleting pre-proof implementation prevents the test from being shaped by the solution.
- TDD is a gate for behavior, bug fixes, risky boundaries, and claims that need proof; it is not ceremony for every line.
- Bug found means: write or identify failing proof first, then debug and fix. Never fix a bug without a reproduction, regression test, or recorded substitute proof.

## Red Flags — STOP and Start Over

- Code before test.
- Test after implementation.
- Test passes immediately.
- Can't explain why the proof failed.
- Tests added "later".
- Rationalizing "just this once".
- "I already manually tested it."
- "Tests after achieve the same purpose."
- "It's about spirit, not ritual."
- "Keep as reference" or "adapt existing code."
- "Already spent hours; deleting is wasteful."
- "TDD is dogmatic; I'm being pragmatic."
- "This is different because..."

All of these mean: delete implementation code and restart from proof.
```

- [ ] **Step 2: Create `trellis-debug` with anti-rationalization architecture**

Create `/Users/maple/Documents/Pomotree/.agents/skills/trellis-debug/SKILL.md`:

```markdown
---
name: trellis-debug
description: Use when encountering a bug, test failure, build failure, runtime error, unexpected behavior, or failed verification.
---

# Trellis Debug

Use this skill before proposing or writing a fix. `trellis-break-loop` handles post-fix retrospective analysis after repeated debugging.

## Iron Law

NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

Violating the letter of this process is violating the spirit of debugging. If implementation starts before reproduction, evidence, and a written testable hypothesis, discard the speculative fix and restart from investigation.

## Red Flags

STOP and return to evidence gathering when you notice:

- "Quick fix for now."
- "Just try changing X."
- "I see the problem, let me fix it" before reproduction or root-cause evidence.
- "It's probably X" without evidence.
- A second speculative patch without a falsified hypothesis.
- Pressure to patch because the failure looks small.

## Systematic Debugging Phases

1. Capture the complete failure: command, output, file paths, line numbers, assertion text, environment, and current git diff.
2. Reproduce the issue consistently, or record exactly why reproduction is not yet possible.
3. Gather multi-component evidence before hypothesizing when the failure crosses layers. Trace the data flow from input to failing output.
4. Pattern analysis: find a working example, compare it to the failing path, identify the first meaningful difference, and check relevant docs or specs.
5. Write one smallest testable hypothesis in the notes or task artifact.
6. Test the hypothesis with the smallest evidence-gathering command or instrumentation.
7. Apply the smallest root-cause fix only after evidence supports the hypothesis.
8. Prove the fix with the reproduction, regression test, or command output.
9. Capture durable prevention through `trellis-update-spec` when the lesson is reusable.

## Rationalization Prevention

| Rationalization | Reality |
|---|---|
| "This is obvious." | Obvious fixes still need root-cause evidence. |
| "One quick fix first." | Quick fixes create false confidence and hide the real failure. |
| "The test failure points right at it." | Error locations are symptoms until traced to cause. |
| "I can reason it out." | Reasoning without reproduction is guessing. |
| "Adding logs is slower." | Evidence gathering is faster than repeated patches. |
| "This is too small for the process." | Small bugs still have causes and regression risks. |
| "The first patch almost worked." | Almost working is evidence the hypothesis is incomplete. |
| "Three fixes failed but the next one is simple." | After 3 failed fixes, stop patching and re-question assumptions. |

## Stop Rule

After 3 failed fixes, stop patching. Re-check reproduction, architecture, assumptions, and recent changes. Ask for review or use `trellis-break-loop` after the immediate failure is stabilized.
```

- [ ] **Step 3: Create local debugging guide**

Create `.trellis/spec/guides/debugging-guide.md`:

```markdown
# Debugging Guide

## Root-Cause Tracing

Trace from the failing output back to the first incorrect input or state transition.

1. Mark the observed failure.
2. Identify the data or control path that produced it.
3. Add temporary evidence at boundaries: caller input, callee output, persisted state, external response, and transformed value.
4. Compare a working path to the failing path.
5. Stop at the first point where expected and actual diverge.

## Condition-Based Waiting

Do not use fixed sleeps when a test can wait for a condition. Poll for the actual state with a timeout, then report the last observed state on failure. Use a helper like this and adapt names to the project test framework:

    export async function waitForCondition<T>(options: {
      read: () => Promise<T> | T;
      ok: (value: T) => boolean;
      timeoutMs?: number;
      intervalMs?: number;
      label?: string;
    }): Promise<T> {
      const timeoutMs = options.timeoutMs ?? 5000;
      const intervalMs = options.intervalMs ?? 100;
      const start = Date.now();
      let last: T | undefined;

      while (Date.now() - start < timeoutMs) {
        last = await options.read();
        if (options.ok(last)) return last;
        await new Promise((resolve) => setTimeout(resolve, intervalMs));
      }

      throw new Error(
        `Timed out waiting for ${options.label ?? "condition"}; last observed=${JSON.stringify(last)}`
      );
    }

Example use:

    await waitForCondition({
      label: "saved todo to appear",
      read: () => screen.queryByText("Buy milk"),
      ok: (node) => node !== null,
    });

## Defense In Depth

When bad data can enter through multiple boundaries, fix the root source and add validation at the trust boundary. Avoid a display-only guard that leaves invalid state alive. Show the intended layers as: source input validation -> domain invariant -> persistence constraint -> display fallback.

## Polluter Search

For order-dependent tests, isolate the smallest preceding test or setup step that changes shared state. Reset shared state at the source, not in every affected test. Use `.trellis/scripts/find-polluter.sh` for candidate bisection when available.

## Pressure Scenarios

- Symptom moves after one fix: return to root-cause tracing; do not stack patches.
- Failure crosses UI/API/storage: collect evidence at every boundary before hypothesizing.
- Test passes alone but fails in suite: run polluter search and inspect shared state, clocks, network mocks, global caches, and filesystem artifacts.
- Absorb `test-pressure-1.md`, `test-pressure-2.md`, and `test-pressure-3.md` as scenario ideas here. Keep `test-academic.md` as optional self-test/reference, not a runtime rule.
```

- [ ] **Step 4: Create polluter search helper**

Create `.trellis/scripts/find-polluter.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
TARGET="$1"
shift
for candidate in "$@"; do
  echo "checking polluter: $candidate -> $TARGET"
  if ! pnpm test "$candidate" "$TARGET"; then
    echo "POLLUTER_CANDIDATE=$candidate"
    exit 1
  fi
done
echo "no polluter found in provided candidates"
```

Run: `chmod +x .trellis/scripts/find-polluter.sh`

- [ ] **Step 5: Create local testing guide**

Create `.trellis/spec/guides/testing-guide.md`:

```markdown
# Testing Guide

## Test Quality Checks

- Test behavior, not mock implementation details.
- Do not add test-only production methods unless the design already needs that seam.
- Understand the real dependency before mocking it.
- Complete mocks enough to fail for the same reason the real dependency would fail.
- Treat integration tests as first-class when behavior crosses layers.

## Good Tests

| Quality | Good | Bad |
|---|---|---|
| Minimal | One behavior. "and" in the name means split it. | `test('validates email and domain and whitespace')` |
| Clear | Name describes user-visible behavior. | `test('test1')` |
| Shows intent | Demonstrates the desired API or outcome. | Obscures behavior behind setup or implementation details. |

Add this Good/Bad code comparison so the guide is not placeholder-only:

Good behavior test:

    test("retries the operation until it succeeds", async () => {
      let attempts = 0;
      const result = await retryOperation(async () => {
        attempts += 1;
        if (attempts < 3) throw new Error("temporary failure");
        return "ok";
      });

      expect(result).toBe("ok");
      expect(attempts).toBe(3);
    });

Bad implementation-detail test:

    test("calls retry helper", async () => {
      const retry = vi.fn().mockResolvedValue("ok");
      await runWithRetry(retry);
      expect(retry).toHaveBeenCalled();
    });

Why bad: it proves a mock was called, not that retry behavior works under failure.

## Regression Test Red-Green

For bug fixes where a regression test is added:

1. Run the test against the broken behavior and verify it fails for the expected reason.
2. Apply the fix.
3. Run the test and verify it passes.
4. If the test was added after the fix, temporarily revert or disable the fix, verify the test fails, then restore the fix and verify it passes.

## When Stuck

| Problem | Signal | Action |
|---|---|---|
| Don't know how to test | Requirement is unclear | Write the wished-for API and assertion first. |
| Test too complicated | Design is too complicated | Simplify the interface. |
| Must mock everything | Code is too coupled | Move the mock to an external boundary or use dependency injection. |
| Test setup huge | Too many dependencies | Extract helpers; if still complex, simplify design. |

## TDD Verification Checklist

- [ ] Proof existed before implementation.
- [ ] New public behavior or risky boundary has proof; do not mechanically require a test for every private helper.
- [ ] Proof failed for the expected reason.
- [ ] Implementation was the smallest change that made proof pass.
- [ ] New proof passes after implementation.
- [ ] Relevant existing tests pass.
- [ ] Tests exercise real behavior, not mock behavior.
- [ ] Any substitute proof is user-approved or recorded before implementation.
- [ ] Output is pristine enough to support the claim: no ignored errors, unrelated failures, or "probably fine" warnings.

## Debugging Integration

When a bug is found, first create or identify a failing proof, then use `trellis-debug` to investigate root cause. The proof must fail before the fix and pass after the fix unless a user-approved or recorded substitute proof is used.
```

- [ ] **Step 6: Register guides**

In `.trellis/spec/guides/index.md`, add:

```markdown
| [Debugging Guide](./debugging-guide.md) | Root-cause tracing, async waiting, and defense-in-depth checks | Bugs, failed tests, runtime errors, repeated fixes |
| [Testing Guide](./testing-guide.md) | TDD proof quality, regression red-green, and testing anti-patterns | Behavior changes, bug fixes, and post-implementation checks |
```

- [ ] **Step 7: Add debug route to `trellis-continue`**

In Step 3 route list, add near `status=in_progress`:

```markdown
- `status=in_progress` + current turn reports a bug, failure, failed verification, or unexpected behavior → load `trellis-debug` before patching, then resume **2.1**.
```

- [ ] **Step 8: Clarify `trellis-break-loop`**

Add near the top of `trellis-break-loop`:

```markdown
`trellis-debug` handles pre-fix investigation when a bug, failure, or unexpected behavior first appears. This skill handles post-fix retrospective analysis after repeated debugging or repeated failed fixes. Do not use this skill as the first stop before gathering root-cause evidence.
```

- [ ] **Step 9: Update `.trellis/agents/implement.md`**

Add to Core Responsibilities:

```markdown
5. **Respect proof gates** — behavior changes and bug fixes need a failing test, reproduction, or recorded substitute proof before implementation code.
6. **Follow the plan** — when `implement.md` exists, execute it step-by-step and stop if instructions are unclear or verification fails.
7. **Protect branches** — verify you are not on `main` or `master` before editing. If on a protected branch without explicit user consent, report `BLOCKED`.
```

Add to Workflow before implementation:

```markdown
Before coding, apply the TDD Decision Matrix from `trellis-before-dev`. Run the failing test or reproduction and verify it fails for the expected reason. If a bug, failure, or unexpected behavior appears, route back to the main session for `trellis-debug` instead of speculative patching.
When the planned scope and acceptance criteria are verified, route back to Phase 3. Do not recommend new polish or follow-up work as the next step before the finish flow is offered.
```

Add a compact TDD execution gate and implementer-prompt absorption to `.trellis/agents/implement.md`, `.codex/agents/trellis-implement.toml`, and `.claude/agents/trellis-implement.md` (`subagent-driven-development/implementer-prompt.md` maps here):

```markdown
- No implementation code before failing proof: a failing test, reproduction, or executable acceptance check.
- Run the proof and verify it fails for the expected reason before coding.
- Do not spawn nested implement/check subagents; return BLOCKED or NEEDS_CONTEXT to the main session if another worker is needed.
- If implementation was written before proof, delete it and start over; do not keep it as reference.
- Write the smallest code that makes proof pass, then run the proof and relevant existing tests.
- Full gate: `.agents/skills/trellis-before-dev/SKILL.md`; test quality: `.trellis/spec/guides/testing-guide.md`.
```

Add to Report Format:

```markdown
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT

- DONE: implementation completed and verification evidence is included.
- DONE_WITH_CONCERNS: implementation completed, but correctness, scope, or risk concerns remain.
- BLOCKED: implementation cannot continue without a decision or failed prerequisite.
- NEEDS_CONTEXT: missing context prevents correct implementation.
```

- [ ] **Step 10: Verify local debug/TDD files**

Run:

```bash
grep -R "TDD Decision Matrix" .agents/skills/trellis-before-dev/SKILL.md
grep -R "NO IMPLEMENTATION CODE BEFORE FAILING PROOF" .agents/skills/trellis-before-dev/SKILL.md
grep -R "Red Flags" .agents/skills/trellis-before-dev/SKILL.md
grep -R "Good Tests" .trellis/spec/guides/testing-guide.md
grep -R "retries the operation until it succeeds" .trellis/spec/guides/testing-guide.md
grep -R "Why bad" .trellis/spec/guides/testing-guide.md
grep -R "TDD Verification Checklist" .trellis/spec/guides/testing-guide.md
grep -R "New public behavior or risky boundary" .trellis/spec/guides/testing-guide.md
grep -R "Why Order Matters" .agents/skills/trellis-before-dev/SKILL.md
grep -R "Debugging Integration" .trellis/spec/guides/testing-guide.md
grep -R "Pressure Scenarios" .trellis/spec/guides/debugging-guide.md
test -x .trellis/scripts/find-polluter.sh
grep -R "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST" .agents/skills/trellis-debug/SKILL.md
grep -R "Pattern analysis" .agents/skills/trellis-debug/SKILL.md
grep -R "Rationalization Prevention" .agents/skills/trellis-debug/SKILL.md
grep -R "current turn reports a bug" .agents/skills/trellis-continue/SKILL.md
grep -R "trellis-debug" .agents/skills/trellis-continue/SKILL.md
grep -R "Respect proof gates" .trellis/agents/implement.md
grep -R "No implementation code before failing proof" .codex/agents/trellis-implement.toml .claude/agents/trellis-implement.md .trellis/agents/implement.md
grep -R "Protect branches" .trellis/agents/implement.md
grep -R "DONE_WITH_CONCERNS" .trellis/agents/implement.md
grep -R "Do not spawn nested" .trellis/agents/implement.md .codex/agents/trellis-implement.toml .claude/agents/trellis-implement.md
grep -R "Debugging Guide" .trellis/spec/guides/index.md
grep -R "Testing Guide" .trellis/spec/guides/index.md
```

Expected:

- `trellis-debug` frontmatter has `name: trellis-debug` and trigger-only description.
- TDD verify-RED and Green verification are present.
- Channel implement agent cannot bypass proof, plan, branch, or status-reporting discipline.

- [ ] **Step 11: Commit local execution/debug changes**

Run:

```bash
git add .agents/skills/trellis-before-dev/SKILL.md .agents/skills/trellis-debug/SKILL.md .agents/skills/trellis-continue/SKILL.md .agents/skills/trellis-break-loop/SKILL.md .trellis/agents/implement.md .codex/agents/trellis-implement.toml .claude/agents/trellis-implement.md .trellis/spec/guides/index.md .trellis/spec/guides/debugging-guide.md .trellis/spec/guides/testing-guide.md .trellis/scripts/find-polluter.sh
git commit -m "docs: add local trellis tdd and debug gates"
```

---

### Task 5: Add local verification, review, check-agent, and finish gates

**Files:**
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-check/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-finish-work/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.trellis/agents/check.md`
- Modify: `/Users/maple/Documents/Pomotree/.codex/agents/trellis-check.toml`
- Modify: `/Users/maple/Documents/Pomotree/.claude/agents/trellis-check.md`

- [ ] **Step 1: Add Completion Claim Gate to `trellis-check`**

Add near the top:

```markdown
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
```

- [ ] **Step 2: Add Review Gate to `trellis-check`**

Add:

```markdown
## Review Gate

Request review for high-risk, cross-layer, major feature, complex bugfix, pre-merge work, after each substantial subagent task, when stuck, before risky refactors, or after a complex bug fix. Do not force two separate reviewer agents by default; use the Trellis check path unless channel orchestration is explicitly chosen.

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

Absorb `requesting-code-review/code-reviewer.md` as checklist items, not as its git-SHA dispatch shell: inspect diff and requirements, separate spec compliance from quality, verify tests/commands directly, classify severity, and produce actionable findings with file evidence.
```

- [ ] **Step 3: Clarify Test Coverage**

In the existing Test Coverage checklist, add:

```markdown
These are post-implementation verification checks. The TDD Decision Matrix in `trellis-before-dev` governs whether a failing test, reproduction, or substitute proof must exist before implementation begins. Use `.trellis/spec/guides/testing-guide.md` to catch testing anti-patterns.
```

- [ ] **Step 4: Update `.trellis/agents/check.md`**

Add to Core Responsibilities:

```markdown
7. **Enforce completion gate** — do not report success until fresh verification evidence has passed.
8. **Enforce review gate** — verify review feedback against code reality before accepting it.
9. **Verify independently** — do not trust implementer self-reports; read the actual diff, artifacts, and relevant code.
```

Add to Workflow before report:

```markdown
Run review in two stages even when using one check agent, absorbing `subagent-driven-development/spec-reviewer-prompt.md` and `subagent-driven-development/code-quality-reviewer-prompt.md`: first spec/acceptance compliance against PRD/design/implement, then code quality including lint/typecheck/tests/security/regression risk.

Before reporting success, run the relevant verification freshly and read the output. Do not use "should", "probably", "seems to", "done", "fixed", "passing", or "complete" unless the evidence supports the claim. When reviewing external feedback, check actual code usage before implementing speculative suggestions. Verify findings independently from the implementer report by reading the diff and code.
When checks are green for the planned scope, do not recommend new work as the next step. Move to Phase 3: spec update judgment, commit, and finish/archive. Additional polish is a new scope decision and needs user approval.
```

Add compact TDD evidence review to `.trellis/agents/check.md`, `.codex/agents/trellis-check.toml`, and `.claude/agents/trellis-check.md`:

```markdown
- Do not trust implementer self-reports; inspect the actual diff, artifacts, and relevant code.
- Verify proof existed before implementation: failing test, reproduction, executable acceptance check, or recorded substitute proof.
- Verify RED failed for the expected reason and GREEN passed after the change.
- Check tests exercise real behavior, not mock behavior or implementation details.
- Full gate: `.agents/skills/trellis-before-dev/SKILL.md`; test quality: `.trellis/spec/guides/testing-guide.md`.
```

- [ ] **Step 5: Add Branch Finish Discipline to `trellis-finish-work`**

Add:

```markdown
## Branch Finish Discipline

Before archive or journal finalization, ensure work commits and verification are handled. If the work lives on a branch, present the relevant integration choices: local merge, push/PR, keep branch as-is, or discard.

Safety rules:
- If required tests fail, stop and report the failing evidence.
- Discard requires explicit user confirmation.
- Do not remove worktrees, workspace dirs, or harness-owned branches unless provenance is known.
- Do not archive task work while current-task code changes remain uncommitted.
- Before staging or committing, inspect staged files separately from unstaged files. If unrelated paths are already staged, unstage them before the work commit.
- If `.trellis/` or platform directories are ignored, archive and journal writes may remain local. Report that state instead of forcing ignored files into Git.

Trellis archive and session journal remain the final lifecycle steps.
```

- [ ] **Step 6: Verify local check/finish gates**

Run:

```bash
grep -R "Completion Claim Gate" .agents/skills/trellis-check/SKILL.md
grep -R "Forbidden status words" .agents/skills/trellis-check/SKILL.md
grep -R "Review Gate" .agents/skills/trellis-check/SKILL.md
grep -R "testing-guide.md" .agents/skills/trellis-check/SKILL.md
grep -R "Additional polish is a new scope decision" .agents/skills/trellis-check/SKILL.md .trellis/agents/check.md
grep -R "Enforce completion gate" .trellis/agents/check.md
grep -R "two stages" .trellis/agents/check.md
grep -R "Required evidence" .agents/skills/trellis-check/SKILL.md
grep -R "Not sufficient" .agents/skills/trellis-check/SKILL.md
grep -R "Red flags" .agents/skills/trellis-check/SKILL.md
grep -R "Why this matters" .agents/skills/trellis-check/SKILL.md
grep -R "Rationalization prevention" .agents/skills/trellis-check/SKILL.md
grep -R "Source-specific handling" .agents/skills/trellis-check/SKILL.md
grep -R "Implementation order" .agents/skills/trellis-check/SKILL.md
grep -R "Push back" .agents/skills/trellis-check/SKILL.md
grep -R "Fixed: <brief technical description>" .agents/skills/trellis-check/SKILL.md
grep -R "Correction: my earlier pushback" .agents/skills/trellis-check/SKILL.md
grep -R "Common mistakes" .agents/skills/trellis-check/SKILL.md
grep -R "GitHub/PR thread replies" .agents/skills/trellis-check/SKILL.md
grep -R "code-reviewer.md" .agents/skills/trellis-check/SKILL.md
grep -R "Verify independently" .trellis/agents/check.md
grep -R "Branch Finish Discipline" .agents/skills/trellis-finish-work/SKILL.md
grep -R "inspect staged files separately" .agents/skills/trellis-finish-work/SKILL.md
```

- [ ] **Step 7: Commit local verification/review/finish changes**

Run:

```bash
git add .agents/skills/trellis-check/SKILL.md .agents/skills/trellis-finish-work/SKILL.md .trellis/agents/check.md
git commit -m "docs: add local trellis verification and review gates"
```

---

### Task 6: Adapt local channel and meta skills

**Files:**
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-channel/SKILL.md`
- Modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-meta/SKILL.md`
- Optional modify: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-session-insight/SKILL.md`

- [ ] **Step 1: Add Trellis-native orchestration rules to `trellis-channel`**

Add:

```markdown
## Superpowers-Derived Orchestration Rules

Use channel orchestration only when work splits into independent domains or needs durable peer review. Do not use workers to avoid understanding the task.

Before spawning or coordinating workers:

1. Define each independent domain.
2. Provide a self-contained context bundle from Trellis task artifacts, relevant specs, and exact files.
3. Define expected output: findings, changed files, verification, and blockers.
4. Use `--kind done` / `--kind turn_finished` for worker completion detection, not user-defined tags.
5. Main session reviews and integrates worker output before proceeding.

After workers complete, read each summary, verify that worker changes do not conflict, spot-check the actual code or artifact changes, and run the relevant full verification before claiming integration success.

Do not use workers when tasks have sequential dependencies, require shared mutable state, need full-system reasoning in one context, or inline execution would be faster.

For Codex inline sessions, inline execution remains the default unless the user explicitly requests workers or the workflow classifies the task as a multi-agent candidate.

Copyable worker prompt template fields:
- Active task: <task path>
- Worker role: <implement|check|research|review>
- Scope: <exact files, subsystem, or question>
- Goal: <one verifiable outcome>
- Constraints: <do not edit outside scope; do not spawn nested workers; obey TDD/debug/review gates>
- Context to read first: <prd/design/implement/spec files>
- Expected output: changed files or findings, verification commands run, evidence, blockers, concerns
- Status enum: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
```

- [ ] **Step 2: Add skill-authoring rules to `trellis-meta`**

Add:

```markdown
## Skill Authoring Quality Bar

Create or modify Trellis skills only when the behavior will be reused, the trigger is clear, and documentation is better than automation. Skill descriptions must describe when to use the skill, not summarize workflow steps. Keep `SKILL.md` focused; move heavy references, command catalogs, and examples into reference files. Verify a skill by checking trigger, workflow, references, and local effective copies.
```

- [ ] **Step 3: Optionally link session insight to debug**

If `trellis-session-insight` already has a debugging trigger section, add:

```markdown
When debugging a familiar bug, use session insight to find prior evidence, then route current investigation through `trellis-debug` before patching.
```

- [ ] **Step 4: Verify channel/meta text**

Run:

```bash
grep -R "Superpowers-Derived Orchestration Rules" .agents/skills/trellis-channel/SKILL.md
grep -R "turn_finished" .agents/skills/trellis-channel/SKILL.md
grep -R "Do not use workers" .agents/skills/trellis-channel/SKILL.md
grep -R "After workers complete" .agents/skills/trellis-channel/SKILL.md
grep -R "Copyable worker prompt template" .agents/skills/trellis-channel/SKILL.md
grep -R "Status enum" .agents/skills/trellis-channel/SKILL.md
grep -R "Skill Authoring Quality Bar" .agents/skills/trellis-meta/SKILL.md
```

- [ ] **Step 5: Commit local channel/meta changes**

Run:

```bash
git add .agents/skills/trellis-channel/SKILL.md .agents/skills/trellis-meta/SKILL.md
git add .agents/skills/trellis-session-insight/SKILL.md 2>/dev/null || true
git commit -m "docs: adapt superpowers orchestration into local trellis"
```

---

### Task 7: Local verification scenarios and smoke checks

**Files:**
- Create: `/Users/maple/Documents/trellis/docs/superpowers/plans/verification-scenarios.md`
- Modify source files only if a local check already exists and can be extended without template productization

- [ ] **Step 1: Create scenario checklist**

Create `docs/superpowers/plans/verification-scenarios.md`:

```markdown
# Superpowers Trellis Phase A Verification Scenarios

- Simple explanation: no task required; factual repo claim uses evidence.
- Trivial edit: no task by default; behavior change still gets verification.
- Complex feature: task path requires brainstorm, design approval, and implement plan.
- Bugfix: `trellis-debug` route appears before patching.
- TDD violation: implementation before failing proof triggers discard-and-restart instruction.
- Verify-RED: failing test must fail for expected reason before implementation.
- Completion claim: success language is blocked until fresh proof exists.
- Review feedback: feedback is verified against code reality before acceptance.
- Anti-rationalization: "too simple for debugging" triggers evidence gathering.
- Resume debug: `trellis-continue` routes active in-progress failures to `trellis-debug`.
- Channel worker: `.trellis/agents/implement.md` and `check.md` contain the same gates.
- Finish flow: verification happens before commit/archive/journal language.
- No-task complex request: assistant stays at triage depth and asks for task creation before substantive brainstorming.
- Frontend visual task: Visual Companion is explicitly evaluated before design lock or visual review.
- Codex complex task: `update_plan` is maintained across planning, implementation, and verification.
- Checks green: assistant offers Phase 3 finish flow before suggesting extra polish or new work.
- Dirty staged state: unrelated staged files are detected and unstaged before the work commit.
- Ignored Trellis runtime: archive/journal writes are reported as local when `.trellis/` is ignored.
- Visual Companion runnable fallback: visual task can create HTML and serve it locally or report file fallback.
- Writing-plan quality: implement.md starts with file map and header, then exact bite-sized tasks with expected outputs.
- Debugging executable guide: condition wait, defense-in-depth, polluter search examples, and pressure scenario references exist.
- Review feedback: source-specific handling, implementation order, pushback, unclear feedback, and YAGNI checks exist.
- Completion verification: rationalization table blocks stale/partial/agent-reported evidence.
- Channel workers: prompt template includes scope, constraints, expected output, verification, blockers, and status enum.
- Auxiliary ledger: every non-writing-skills auxiliary file is mapped to skill, guide, agent, script, scenario, or reference-only rationale.
- Execution start: Phase 2 reads and critically reviews implement.md before coding, then continues while unblocked.
- Subagent path: platform agents include status protocol and no-nested-subagent recursion guard.
- Check agent: review is explicitly two-stage, spec compliance first and code quality second.
```

- [ ] **Step 2: Run local smoke checks**

Run:

```bash
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1 --platform codex
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.2 --platform codex
test -f .agents/skills/trellis-debug/SKILL.md
grep -R "^name: trellis-debug$" .agents/skills/trellis-debug/SKILL.md
grep -R "description: Use when encountering" .agents/skills/trellis-debug/SKILL.md
grep -R "trellis-debug" .trellis/workflow.md .agents/skills/trellis-start/SKILL.md .agents/skills/trellis-continue/SKILL.md
grep -R "triage depth only" .trellis/workflow.md .agents/skills/trellis-start/SKILL.md .agents/skills/trellis-brainstorm/SKILL.md
grep -R "Visual Companion" .trellis/workflow.md .agents/skills/trellis-start/SKILL.md .agents/skills/trellis-brainstorm/SKILL.md
grep -R "update_plan" .trellis/workflow.md .agents/skills/trellis-start/SKILL.md
grep -R "Additional polish is a new scope decision" .trellis/workflow.md .agents/skills/trellis-check/SKILL.md .trellis/agents/check.md
grep -R "Auxiliary File Absorption Ledger" /Users/maple/Documents/trellis/docs/superpowers/plans/2026-06-28-superpowers-trellis-integration.md
grep -R "spec-document-reviewer-prompt.md" /Users/maple/Documents/trellis/docs/superpowers/plans/2026-06-28-superpowers-trellis-integration.md
grep -R "code-quality-reviewer-prompt.md" /Users/maple/Documents/trellis/docs/superpowers/plans/2026-06-28-superpowers-trellis-integration.md
grep -R "Respect proof gates" .trellis/agents/implement.md
grep -R "Enforce completion gate" .trellis/agents/check.md
grep -R "two stages" .trellis/agents/check.md
grep -R "inspect staged files separately" .agents/skills/trellis-finish-work/SKILL.md
```

Expected:

- Commands exit 0.
- Local effective workflow, skills, and channel agents expose the new gates.
- Verification is not grep-only: phase extraction also runs.

- [ ] **Step 3: Run project checks**

Inspect package scripts, then run available checks. If `pnpm` scripts exist:

```bash
pnpm typecheck
pnpm test
```

Expected:

- Checks pass, or failures are clearly pre-existing/unrelated with evidence.

- [ ] **Step 4: Commit verification scenarios**

Run:

```bash
git add docs/superpowers/plans/verification-scenarios.md
git commit -m "docs: add local superpowers trellis verification scenarios"
```

---

### Task 8: Final local review and handoff

**Files:**
- Read: commits from `<base_sha>..HEAD`
- Read: git status
- Modify: no files unless review finds a concrete Phase A gap

- [ ] **Step 1: Review implementation range**

Run:

```bash
git log --oneline --decorate <base_sha>..HEAD
git diff --name-only <base_sha>..HEAD
```

Expected:

- Diff covers only Phase A local files and docs.
- No `packages/cli/src/templates/**` or `packages/cli/src/configurators/shared.ts` files are included.

- [ ] **Step 2: Confirm Superpowers coverage**

Use this checklist:

```text
Local Phase A integrated:
- using-superpowers -> workflow + trellis-start
- brainstorming -> trellis-brainstorm
- writing-plans -> workflow planning + implement.md quality bar
- executing-plans -> workflow Phase 2.1 + implement agent discipline
- systematic-debugging -> trellis-debug + debugging-guide
- test-driven-development -> trellis-before-dev + testing-guide + implement agent
- verification-before-completion -> trellis-check + check agent
- receiving-code-review -> trellis-check Review Gate
- requesting-code-review -> trellis-check Review Gate + check agent
- finishing-a-development-branch -> trellis-finish-work
- dispatching-parallel-agents -> trellis-channel
- subagent-driven-development -> trellis-channel + channel agents
- writing-skills -> trellis-meta
- brainstorming/visual-companion -> explicit evaluation gate for frontend visual tasks
- Pomotree inline feedback -> no-task triage limit, Codex update_plan tracking, finish-before-polish gate, staged-file hygiene

Local Phase A rejected/default-off:
- using-git-worktrees as default workflow
- duplicate Superpowers task/finish lifecycle shells
```

- [ ] **Step 3: Final status**

Run:

```bash
git status --short
```

Expected:

- Only unrelated pre-existing dirty files remain, or working tree is clean except known docs/session files.

- [ ] **Step 4: Report**

Report:

```text
Implemented Superpowers -> Trellis Phase A local integration.
Verified: <commands run>.
Commits: <commit hashes>.
Deferred Phase B: template/common-skill/shared.ts/init-update productization.
Unrelated dirty files left untouched: <list or none>.
```

---

## Plan Self-Review

- Phase A scope: Pomotree local Trellis install only.
- Phase B split: template productization moved to separate plan.
- Breadcrumb safety: existing dispatch/self-exemption/jsonl constraints are extended, not replaced.
- Channel runtime safety: `.trellis/agents/check.md` and `implement.md` receive the same core gates, status protocol, no-nesting guard, and two-stage review order.
- Debug strength: `trellis-debug` includes Iron Law, red flags, pattern analysis, written hypothesis, rationalization prevention, and stop rule.
- TDD strength: verify-RED, discard-before-proof violation, and Green verification are included.
- Completion strength: forbidden status words, Not Sufficient column, red flags, rationalization prevention, short Why This Matters, and regression red-green verification are included.
- Review strength: READ/UNDERSTAND/VERIFY/EVALUATE/RESPOND/IMPLEMENT, source-specific handling, implementation order, pushback criteria, unclear feedback handling, and YAGNI check are included.
- Auxiliary absorption: absorbed files have concrete destinations in skills, guides, runnable fallback scripts, agents, verification scenarios, or explicit reference-only notes; original auxiliary files are not recreated as a parallel runtime tree.
- Pomotree experiment feedback: no-task triage, Visual Companion evaluation, update_plan tracking, finish-before-polish, and staged-file hygiene are encoded as runtime rules.
- Placeholder scan: no placeholder markers, no optional-proof escape hatch, no vague future-fill instructions, and no stale Superpowers install path dependency remain.
