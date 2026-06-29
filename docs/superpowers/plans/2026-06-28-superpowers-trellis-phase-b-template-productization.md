# Phase B Personal Fork Distribution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Maple's Trellis fork generate the Pomotree-verified disciplined runtime by default through `trellis init` and `trellis update`.

**Architecture:** Treat Pomotree as the golden fixture and Trellis `packages/cli/src/templates/**` as the distribution source. Copy only generic runtime behavior into default templates, register missing generated assets, and add regression tests that prevent future upstream rebases from dropping discipline gates.

**Tech Stack:** TypeScript CLI templates, Vitest tests, Markdown/TOML/Python generated files, Trellis init/update template hash flow.

---

## Preconditions

- Phase A local runtime in `/Users/maple/Documents/Pomotree` is the golden fixture.
- Work in `/Users/maple/Documents/trellis` only for Phase B source changes.
- Do not copy Pomotree product rules, release workflow, app docs, or project-specific specs.
- Do not preserve upstream default behavior for PR acceptance; this is a personal fork distribution.
- Do not add `--profile maple`; the fork default is the profile.
- Commit only if the user explicitly approves committing.

## Phase A Delta To Productize

Phase A has evolved beyond the original local integration. Phase B must now productize these additional generic assets from Pomotree:

- `trellis-visual-companion` skill and its local HTML/server fallback semantics.
- `trellis-brainstorm` Planning Quality Bar, PRD/spec self-review checklist, implement-plan reviewer checklist, and 2-3 option preference rule.
- `testing-guide.md` additions: Why Order Matters, Red/Green/Refactor, retry Good/Bad TypeScript examples, public behavior/risky boundary proof, output-pristine rule, and Debugging Integration.
- `debugging-guide.md` additions: `waitForCondition<T>` code, Polluter Search, Pressure Scenarios, and optional academic self-test note.
- `find-polluter.sh` shell recipe remains in `debugging-guide.md`; do not add a `.sh` script template because existing Trellis regression tests require generated scripts to be Python-only.
- `superpowers-verification-scenarios.md` as audit-only guide material, not a normal runtime gate.
- `trellis-check` additions: Not Sufficient column, red flags, rationalization table, short Why This Matters, receiving-review acknowledgement/correction/common-mistake/GitHub-PR optional guidance, and code-reviewer prompt absorption.
- implement/check agent parity: Implementer Status Protocol, no nested subagent guard, Two-Stage Review Protocol, and status enum across Trellis/Codex/Claude agent templates.
- `trellis-channel` Copyable Worker Prompt Template.

Do not productize Pomotree-specific app rules, tasks, workspace state, ignored local metadata, or `.superpowers/`.

## Files

### Read

- `/Users/maple/Documents/Pomotree/.trellis/workflow.md`
- `/Users/maple/Documents/Pomotree/.agents/skills/trellis-*.md`
- `/Users/maple/Documents/Pomotree/.trellis/agents/implement.md`
- `/Users/maple/Documents/Pomotree/.trellis/agents/check.md`
- `/Users/maple/Documents/Pomotree/.codex/agents/trellis-implement.toml`
- `/Users/maple/Documents/Pomotree/.codex/agents/trellis-check.toml`
- `/Users/maple/Documents/Pomotree/.claude/agents/trellis-implement.md`
- `/Users/maple/Documents/Pomotree/.claude/agents/trellis-check.md`
- `/Users/maple/Documents/Pomotree/.trellis/spec/guides/debugging-guide.md`
- `/Users/maple/Documents/Pomotree/.trellis/spec/guides/testing-guide.md`
- `/Users/maple/Documents/Pomotree/.trellis/spec/guides/superpowers-verification-scenarios.md`
- `/Users/maple/Documents/Pomotree/.trellis/spec/guides/index.md`
- `/Users/maple/Documents/Pomotree/.agents/skills/trellis-visual-companion/SKILL.md`

### Modify or Create

- `packages/cli/src/templates/trellis/workflow.md`
- `packages/cli/src/templates/common/skills/before-dev.md`
- `packages/cli/src/templates/common/skills/brainstorm.md`
- `packages/cli/src/templates/common/skills/visual-companion.md`
- `packages/cli/src/templates/common/skills/check.md`
- `packages/cli/src/templates/common/skills/break-loop.md`
- `packages/cli/src/templates/common/skills/debug.md`
- `packages/cli/src/templates/common/skills/finish-work.md` if missing or generated through another path
- `packages/cli/src/templates/common/bundled-skills/trellis-channel/SKILL.md`
- `packages/cli/src/templates/trellis/agents/implement.md`
- `packages/cli/src/templates/trellis/agents/check.md`
- `packages/cli/src/templates/codex/agents/trellis-implement.toml`
- `packages/cli/src/templates/codex/agents/trellis-check.toml`
- `packages/cli/src/templates/claude/agents/trellis-implement.md`
- `packages/cli/src/templates/claude/agents/trellis-check.md`
- `packages/cli/src/templates/markdown/spec/guides/debugging-guide.md.txt`
- `packages/cli/src/templates/markdown/spec/guides/testing-guide.md.txt`
- `packages/cli/src/templates/markdown/spec/guides/superpowers-verification-scenarios.md.txt`
- `packages/cli/src/templates/markdown/spec/guides/index.md.txt`
- `packages/cli/src/configurators/shared.ts`
- `packages/cli/test/templates/trellis.test.ts`
- `packages/cli/test/templates/codex.test.ts`
- `packages/cli/test/templates/claude.test.ts`
- `packages/cli/test/configurators/shared.test.ts`

---

### Task 1: Record scope and inspect generation paths

**Files:**
- Read: git status, current branch, template exports, configurator shared mapping
- Modify: none

- [ ] **Step 1: Record dirty baseline**

Run:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
```

Expected:

- Record current branch and base SHA in implementation notes.
- Existing unrelated dirty files are left untouched.

- [ ] **Step 2: Inspect template exports and skill registration**

Run:

```bash
rg -n "common/skills|SKILL_DESCRIPTIONS|wrapWithSkillFrontmatter|getAll.*Skills|workflowMdTemplate|implementAgentTemplate|checkAgentTemplate" packages/cli/src packages/cli/test
find packages/cli/src/templates/common -maxdepth 3 -type f | sort
```

Expected:

- Identify the exact files that export common skills, workflow template, Trellis agents, and platform agents.
- Confirm whether adding `common/skills/debug.md` only requires `SKILL_DESCRIPTIONS.debug`, or whether an index/export file must also change.
- Confirm `common/skills/` and `common/bundled-skills/` are separate generation mechanisms. Ordinary generated `trellis-*` skills use `common/skills/`; bundled skills such as `trellis-channel` use `common/bundled-skills/`.
- Resolve `find-polluter.sh` productization: existing Trellis script template tests require generated scripts to be Python-only, so do not add a shell script template; keep the shell recipe in `debugging-guide.md`.

- [ ] **Step 3: Inspect Pomotree golden markers**

Run:

```bash
rg -n "NO IMPLEMENTATION CODE BEFORE FAILING PROOF|trellis-debug|NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST|Completion Claim Gate|Review Gate|Visual Companion|trellis-visual-companion|Planning Quality Bar|waitForCondition|Not sufficient|Copyable Worker Prompt Template|Implementer Status Protocol|Two-Stage Review Protocol|update_plan|Additional polish is a new scope decision|DONE_WITH_CONCERNS" /Users/maple/Documents/Pomotree/.trellis /Users/maple/Documents/Pomotree/.agents /Users/maple/Documents/Pomotree/.codex /Users/maple/Documents/Pomotree/.claude
```

Expected:

- Markers exist in Pomotree.
- Any missing marker must be fixed in Pomotree first or explicitly excluded from Phase B.

---

### Task 2: Productize workflow template

**Files:**
- Read: `/Users/maple/Documents/Pomotree/.trellis/workflow.md`
- Modify: `packages/cli/src/templates/trellis/workflow.md`
- Test: `packages/cli/test/templates/trellis.test.ts`

- [ ] **Step 1: Compare workflow structure before merging**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import re
files = {
    "pomotree": Path("/Users/maple/Documents/Pomotree/.trellis/workflow.md"),
    "template": Path("packages/cli/src/templates/trellis/workflow.md"),
}
for name, path in files.items():
    text = path.read_text()
    states = re.findall(r"\[workflow-state:([^\]]+)\]", text)
    phases = re.findall(r"^###? Phase [^\n]+", text, re.M)
    print(name, path)
    print("states:", states)
    print("phases:", phases)
PY
diff -u packages/cli/src/templates/trellis/workflow.md /Users/maple/Documents/Pomotree/.trellis/workflow.md | sed -n '1,220p'
```

Expected:

- Decide the merge strategy before editing.
- If workflow-state blocks have the same status names, prefer replacing full `[workflow-state:STATUS]...[/workflow-state:STATUS]` blocks from Pomotree and then re-adding template-only invariants.
- If upstream changed status names, nesting, or required comments, stop and update the plan before editing.

- [ ] **Step 2: Copy generic workflow behavior**

Update `packages/cli/src/templates/trellis/workflow.md` from the Pomotree workflow while preserving template-only invariants already present in the Trellis source.

Template-only invariants to preserve:

- exact `[workflow-state:STATUS]...[/workflow-state:STATUS]` tag pairing,
- comments that describe workflow-state injection and test invariants,
- class-2 dispatch protocol wording required by existing tests,
- JSONL context guidance,
- sub-agent self-exemption / recursion guard guidance,
- marketplace native workflow mirror requirement,
- any existing platform block names required by `packages/cli/test/templates/trellis.test.ts`.

Required content:

- no-task triage-only rule before task creation,
- planning breadcrumb Design Gate,
- in-progress and in-progress-inline breadcrumbs,
- `trellis-before-dev -> [trellis-debug if bug/failure/unexpected behavior]` flow,
- TDD gate line: no implementation before failing proof; violation means discard implementation and restart from proof,
- completion claim gate in `trellis-check`,
- review feedback routing,
- Visual Companion evaluation for frontend visual tasks,
- global `update_plan` / `TodoWrite` tracking guidance,
- finish-before-polish gate,
- existing class-2 dispatch context, JSONL guidance, and sub-agent self-exemption.

- [ ] **Step 3: Preserve workflow mirror requirement**

If `packages/cli/test/templates/trellis.test.ts` requires `marketplace/workflows/native/workflow.md` to equal `workflowMdTemplate`, copy the same content to:

```bash
marketplace/workflows/native/workflow.md
```

Expected:

- `marketplace native workflow mirror matches the bundled workflow` still passes.

- [ ] **Step 4: Check workflow-state contract template**

Run:

```bash
rg -n "workflow-state-contract|INVARIANT \\(test/regression.test.ts\\)|workflow-state" packages/cli/src packages/cli/test .trellis/spec
```

Expected:

- If a workflow-state contract template or generated spec exists in `packages/cli/src/templates/**`, update it so the new breadcrumb gates are documented and tested.
- If no template exists, record `no template action` in implementation notes; do not create a dead file.

- [ ] **Step 5: Add workflow marker regression tests**

In `packages/cli/test/templates/trellis.test.ts`, add one focused test:

```ts
it("disciplined workflow breadcrumbs keep Phase A gates visible", () => {
  const inProgress = workflowStateBreadcrumb("in_progress");
  const inline = workflowStateBreadcrumb("in_progress-inline");
  for (const block of [inProgress, inline]) {
    expect(block).toContain("trellis-before-dev");
    expect(block).toContain("trellis-debug");
    expect(block).toContain("TDD gate");
    expect(block).toContain("Completion Claim Gate");
    expect(block).toContain("Review feedback");
    expect(block).toContain("finish flow");
  }
});
```

Adjust exact strings to match final template wording.

- [ ] **Step 6: Run workflow tests**

Run:

```bash
pnpm vitest run packages/cli/test/templates/trellis.test.ts
```

Expected:

- Test passes.
- If marketplace mirror fails, sync `marketplace/workflows/native/workflow.md` and rerun.

---

### Task 3: Productize common skills

**Files:**
- Read: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-before-dev/SKILL.md`
- Read: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-brainstorm/SKILL.md`
- Read: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-visual-companion/SKILL.md`
- Read: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-check/SKILL.md`
- Read: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-break-loop/SKILL.md`
- Read: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-debug/SKILL.md`
- Read: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-finish-work/SKILL.md`
- Modify/Create: `packages/cli/src/templates/common/skills/*.md`
- Modify: `packages/cli/src/configurators/shared.ts`
- Test: `packages/cli/test/configurators/shared.test.ts`
- Test: platform template skill tests as needed

- [ ] **Step 1: Update existing common skills**

Update these templates with Pomotree's generic behavior, removing generated frontmatter if the common template source expects body-only Markdown:

```text
packages/cli/src/templates/common/skills/before-dev.md
packages/cli/src/templates/common/skills/brainstorm.md
packages/cli/src/templates/common/skills/check.md
packages/cli/src/templates/common/skills/break-loop.md
```

Required markers:

```text
NO IMPLEMENTATION CODE BEFORE FAILING PROOF
Red Flags — STOP and Start Over
Visual Companion
trellis-visual-companion
Planning Quality Bar
PRD / Spec Self-Review
Implement Plan Reviewer Checklist
Completion Claim Gate
Review Gate
Not sufficient
Rationalization prevention
Fixed: <brief technical description>
Correction: my earlier pushback
Common mistakes
GitHub/PR thread replies
Code-reviewer prompt absorption
Additional polish is a new scope decision
`trellis-debug` handles pre-fix investigation
```

- [ ] **Step 2: Add `trellis-visual-companion` common skill**

Create:

```text
packages/cli/src/templates/common/skills/visual-companion.md
```

Content must be body-only Markdown if `wrapWithSkillFrontmatter` adds frontmatter. Include:

```text
# Trellis Visual Companion
Runnable Fallback
.trellis/workspace/visual-companion/index.html
python3 -m http.server 8765
local browser/server fallback to file path
```

Register a trigger-oriented skill description if common skills require `SKILL_DESCRIPTIONS.visualCompanion` or equivalent.

- [ ] **Step 3: Add `trellis-debug` common skill**

Create:

```text
packages/cli/src/templates/common/skills/debug.md
```

Content must be body-only Markdown if `wrapWithSkillFrontmatter` adds frontmatter. Include:

```text
# Trellis Debug
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.
Red Flags
Systematic Debugging Phases
Rationalization Prevention
Stop Rule
```

- [ ] **Step 4: Register new skill descriptions**

In `packages/cli/src/configurators/shared.ts`, add:

```ts
debug:
  "Pre-fix root-cause investigation for bugs, test failures, build failures, runtime errors, unexpected behavior, and failed verification. Use when encountering a failure before proposing or writing a fix.",
visualCompanion:
  "Visual, layout, information-density, and interaction-shape exploration/review helper. Use when text-only planning or review is insufficient for frontend visual work.",
```

Description must be trigger-oriented, not a workflow summary.

- [ ] **Step 5: Confirm `finish-work` template path**

Run:

```bash
rg -n "finish-work|Finish Work|archive" packages/cli/src/templates packages/cli/src/configurators packages/cli/test
```

If `finish-work` is already generated from a different template path, update that path with Pomotree's finish discipline:

```text
verify before finish
staged vs unstaged hygiene
ignored Trellis runtime reporting
branch finish choices
```

If no `finish-work` template exists but generated projects currently receive it, inspect the generation code and update the actual source. Do not create a dead template.

- [ ] **Step 6: Add shared skill regression tests**

In `packages/cli/test/configurators/shared.test.ts` or the platform template test that resolves common skills, add assertions that resolved skills include:

```ts
expect(resolved).toContain("name: trellis-debug");
expect(resolved).toContain("NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST");
expect(resolved).toContain("NO IMPLEMENTATION CODE BEFORE FAILING PROOF");
expect(resolved).toContain("Completion Claim Gate");
expect(resolved).toContain("Visual Companion");
expect(resolved).toContain("trellis-visual-companion");
expect(resolved).toContain("Runnable Fallback");
expect(resolved).toContain("python3 -m http.server 8765");
expect(resolved).toContain("Planning Quality Bar");
expect(resolved).toContain("Not sufficient");
```

- [ ] **Step 7: Run skill tests**

Run:

```bash
pnpm vitest run packages/cli/test/configurators/shared.test.ts packages/cli/test/templates/codex.test.ts
```

Expected:

- `trellis-debug` resolves with valid frontmatter.
- No missing skill description error.

- [ ] **Step 8: Verify `trellis-debug` and `trellis-visual-companion` routing chain**

Run:

```bash
rg -n "trellis-debug|bug|failure|unexpected behavior" packages/cli/src/templates/common/skills packages/cli/src/templates/trellis/workflow.md packages/cli/src/templates/trellis/agents packages/cli/src/templates/codex/agents packages/cli/src/templates/claude/agents
```

Expected:

- `trellis-brainstorm` references `trellis-visual-companion` only for frontend visual/layout/interaction work; it is not a second workflow.
- `trellis-start` or equivalent startup/routing skill includes bug/failure route to `trellis-debug` when that skill is generated from templates.
- `trellis-continue` or equivalent resume guidance routes `status=in_progress` plus bug/failure to `trellis-debug` before patching, if that skill exists in template source.
- `trellis-break-loop` clearly says it is post-fix retrospective, not first-stop debugging.
- Workflow breadcrumbs include `trellis-debug`.
- Implement agents report debug need instead of speculative patching on failure.

---

### Task 4: Productize guides

**Files:**
- Read: `/Users/maple/Documents/Pomotree/.trellis/spec/guides/debugging-guide.md`
- Read: `/Users/maple/Documents/Pomotree/.trellis/spec/guides/testing-guide.md`
- Read: `/Users/maple/Documents/Pomotree/.trellis/spec/guides/superpowers-verification-scenarios.md`
- Read: `/Users/maple/Documents/Pomotree/.trellis/spec/guides/index.md`
- Create: `packages/cli/src/templates/markdown/spec/guides/debugging-guide.md.txt`
- Create: `packages/cli/src/templates/markdown/spec/guides/testing-guide.md.txt`
- Create: `packages/cli/src/templates/markdown/spec/guides/superpowers-verification-scenarios.md.txt`
- Modify: `packages/cli/src/templates/markdown/spec/guides/index.md.txt`
- Test: `packages/cli/test/templates/trellis.test.ts` or existing markdown/spec template tests

- [ ] **Step 1: Create debugging guide template**

Copy generic content from Pomotree into:

```text
packages/cli/src/templates/markdown/spec/guides/debugging-guide.md.txt
```

Required markers:

```text
Root-Cause Tracing
Condition-Based Waiting
Defense In Depth
Multi-Component Tracing
When Root Cause Is Elusive
waitForCondition<T>
Polluter Search
Pressure Scenarios
```

If Pomotree lacks `Multi-Component Tracing` or `When Root Cause Is Elusive`, add concise sections from Phase A design before productizing.

- [ ] **Step 2: Create testing guide template**

Copy generic content from Pomotree into:

```text
packages/cli/src/templates/markdown/spec/guides/testing-guide.md.txt
```

Required markers:

```text
TDD Proof Gate
Mocking Rules
Anti-Patterns
Good Tests
Regression Proof
When Stuck
TDD Verification Checklist
Completion Evidence
Why Order Matters
Red / Green / Refactor
keeps retrying until a transient operation succeeds
New public behavior or risky boundary
Output is pristine
```

- [ ] **Step 3: Productize verification scenarios and polluter helper**

Copy `superpowers-verification-scenarios.md` into the guide template tree as audit-only material. Its index description must say it is for runtime audits/regression checks, not normal implementation.

Keep the `find-polluter.sh` recipe in `debugging-guide.md` only. Do not add a shell script under `templates/trellis/scripts/` because current regression tests enforce Python-only generated scripts.

- [ ] **Step 4: Register guide links**

Update `packages/cli/src/templates/markdown/spec/guides/index.md.txt` to include:

```markdown
| [Debugging Guide](./debugging-guide.md) | Root-cause tracing, async waiting, and defense-in-depth checks | Bugs, failed tests, runtime errors, repeated fixes |
| [Testing Guide](./testing-guide.md) | TDD proof quality, regression red-green, and testing anti-patterns | Behavior changes, bug fixes, and post-implementation checks |
| [Superpowers Integration Verification Scenarios](./superpowers-verification-scenarios.md) | Audit-only scenario checklist for validating Trellis/Superpowers integration behavior | Runtime audits and regression checks; do not load during normal implementation |
```

- [ ] **Step 5: Add guide regression test**

Add a small test to an existing template test file that reads the guide templates directly and asserts the markers above exist.

- [ ] **Step 6: Run guide tests**

Run:

```bash
pnpm vitest run packages/cli/test/templates/trellis.test.ts
```

Expected:

- Guide marker tests pass.

---

### Task 5: Productize channel agents

**Files:**
- Read: `/Users/maple/Documents/Pomotree/.trellis/agents/implement.md`
- Read: `/Users/maple/Documents/Pomotree/.trellis/agents/check.md`
- Modify: `packages/cli/src/templates/trellis/agents/implement.md`
- Modify: `packages/cli/src/templates/trellis/agents/check.md`
- Test: `packages/cli/test/templates/trellis.test.ts`

- [ ] **Step 1: Update implement agent template**

Update `packages/cli/src/templates/trellis/agents/implement.md` with Pomotree's generic implement-agent discipline.

Required markers:

```text
Respect proof gates
Protect branches
TDD (mandatory for features and bugfixes)
No implementation code before failing proof
trellis-debug
DONE_WITH_CONCERNS
BLOCKED
NEEDS_CONTEXT
Implementer Status Protocol
Do not spawn nested
```

- [ ] **Step 2: Update check agent template**

Update `packages/cli/src/templates/trellis/agents/check.md` with Pomotree's generic check-agent discipline.

Required markers:

```text
Enforce completion gate
Enforce review gate
Verify independently
TDD evidence review
Verify proof existed before implementation
Spec compliance first
No completion claims without evidence
Two-Stage Review Protocol
Fixed: <brief technical description>
```

- [ ] **Step 3: Add Trellis agent regression tests**

In `packages/cli/test/templates/trellis.test.ts`, add assertions against `implementAgentTemplate` and `checkAgentTemplate`:

```ts
expect(implementAgentTemplate).toContain("No implementation code before failing proof");
expect(implementAgentTemplate).toContain("DONE_WITH_CONCERNS");
expect(checkAgentTemplate).toContain("Verify proof existed before implementation");
expect(checkAgentTemplate).toContain("Verify independently");
expect(checkAgentTemplate).toContain("Run review in two stages");
```

- [ ] **Step 4: Run Trellis agent tests**

Run:

```bash
pnpm vitest run packages/cli/test/templates/trellis.test.ts
```

Expected:

- Trellis agent marker tests pass.

---

### Task 6: Productize Codex and Claude platform agents

**Files:**
- Read: `/Users/maple/Documents/Pomotree/.codex/agents/trellis-implement.toml`
- Read: `/Users/maple/Documents/Pomotree/.codex/agents/trellis-check.toml`
- Read: `/Users/maple/Documents/Pomotree/.claude/agents/trellis-implement.md`
- Read: `/Users/maple/Documents/Pomotree/.claude/agents/trellis-check.md`
- Modify: `packages/cli/src/templates/codex/agents/trellis-implement.toml`
- Modify: `packages/cli/src/templates/codex/agents/trellis-check.toml`
- Modify: `packages/cli/src/templates/claude/agents/trellis-implement.md`
- Modify: `packages/cli/src/templates/claude/agents/trellis-check.md`
- Test: `packages/cli/test/templates/codex.test.ts`
- Test: `packages/cli/test/templates/claude.test.ts`

Scope note: these platform agent files are for dispatched platform sub-agent paths. Codex inline mode still gets its runtime discipline from `.trellis/workflow.md`, `.agents/skills/trellis-*`, and `.trellis/spec/guides/*`; Task 6 prevents the sub-agent path from lagging behind the inline path.

- [ ] **Step 1: Update Codex implement agent**

Add compact TDD execution gate, Implementer Status Protocol, and no-nested-subagent instruction to `packages/cli/src/templates/codex/agents/trellis-implement.toml`:

```text
TDD execution gate:
- No implementation code before failing proof: a failing test, reproduction, or executable acceptance check.
- Run the proof and verify it fails for the expected reason before coding.
- If you wrote implementation before proof, delete it and start over; do not keep it as reference.
- Write the smallest code that makes proof pass, then run the proof and relevant existing tests.
- Full gate: `.agents/skills/trellis-before-dev/SKILL.md`; test quality: `.trellis/spec/guides/testing-guide.md`.
- If a bug, failed test, or unexpected behavior appears, stop speculative patching and report that `trellis-debug` is needed.
```

- [ ] **Step 2: Update Codex check agent**

Add compact TDD evidence review, Two-Stage Review Protocol, status enum, and no-nested-subagent instruction to `packages/cli/src/templates/codex/agents/trellis-check.toml`:

```text
- Do not trust implementer self-reports; inspect the actual diff, artifacts, and relevant code.
- Verify TDD evidence existed before implementation: failing test, reproduction, executable acceptance check, or recorded substitute proof.
- Verify RED failed for the expected reason and GREEN passed after the change.
- Check tests exercise real behavior, not mock behavior or implementation details.
- Full gate: `.agents/skills/trellis-before-dev/SKILL.md`; test quality: `.trellis/spec/guides/testing-guide.md`.
```

- [ ] **Step 3: Update Claude implement/check agents**

Add the same compact execution/evidence gates to:

```text
packages/cli/src/templates/claude/agents/trellis-implement.md
packages/cli/src/templates/claude/agents/trellis-check.md
```

Place them near existing recursion guard/context/important sections so the agent reads them before workflow steps.

- [ ] **Step 4: Add Codex/Claude regression tests**

In `packages/cli/test/templates/codex.test.ts`, add:

```ts
expect(content).toContain("No implementation code before failing proof");
expect(content).toContain("Verify TDD evidence existed before implementation");
expect(content).toContain("Implementer Status Protocol");
expect(content).toContain("Two-Stage Review Protocol");
expect(content).toContain("multi_agent = false");
expect(content).toContain("enabled = false");
```

In `packages/cli/test/templates/claude.test.ts`, add equivalent assertions for the two Claude agent files.

- [ ] **Step 5: Run platform agent tests**

Run:

```bash
pnpm vitest run packages/cli/test/templates/codex.test.ts packages/cli/test/templates/claude.test.ts
```

Expected:

- Codex recursion guard tests still pass.
- New TDD marker tests pass.

---

### Task 7: Productize channel orchestration skill

**Files:**
- Read: `/Users/maple/Documents/Pomotree/.agents/skills/trellis-channel/SKILL.md`
- Modify: `packages/cli/src/templates/common/bundled-skills/trellis-channel/SKILL.md`
- Modify if needed: files under `packages/cli/src/templates/common/bundled-skills/trellis-channel/references/`
- Test: existing platform skill/template tests

- [ ] **Step 1: Update trellis-channel bundled skill**

Copy generic orchestration rules from Pomotree into `packages/cli/src/templates/common/bundled-skills/trellis-channel/SKILL.md`.

Required markers:

```text
Superpowers-Derived Orchestration Rules
Use channel orchestration only when work splits into independent domains or needs durable peer review
Do not use workers to avoid understanding the task
--kind done / --kind turn_finished
For Codex inline sessions, inline execution remains the default
Copyable Worker Prompt Template
Status enum: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
```

- [ ] **Step 2: Keep reference files minimal**

Only update reference files if Pomotree contains changed generic command guidance not already present in Trellis source. Do not copy noisy local notes.

- [ ] **Step 3: Run relevant template tests**

Run:

```bash
pnpm vitest run packages/cli/test/templates/codex.test.ts packages/cli/test/templates/claude.test.ts packages/cli/test/configurators/shared.test.ts
```

Expected:

- Bundled skill still resolves on supported platforms.

---

### Task 8: Add generated runtime regression test

**Files:**
- Modify: existing test file under `packages/cli/test/templates/` or create `packages/cli/test/templates/disciplined-runtime.test.ts`

- [ ] **Step 1: Add static marker test**

Create one test that reads template source files directly and checks the full disciplined marker set:

```ts
const markers = [
  ["packages/cli/src/templates/common/skills/before-dev.md", "NO IMPLEMENTATION CODE BEFORE FAILING PROOF"],
  ["packages/cli/src/templates/common/skills/debug.md", "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"],
  ["packages/cli/src/templates/common/skills/check.md", "Completion Claim Gate"],
  ["packages/cli/src/templates/common/skills/check.md", "Review Gate"],
  ["packages/cli/src/templates/common/skills/brainstorm.md", "Visual Companion"],
  ["packages/cli/src/templates/common/skills/brainstorm.md", "Planning Quality Bar"],
  ["packages/cli/src/templates/common/skills/visual-companion.md", "Trellis Visual Companion"],
  ["packages/cli/src/templates/markdown/spec/guides/debugging-guide.md.txt", "waitForCondition"],
  ["packages/cli/src/templates/markdown/spec/guides/testing-guide.md.txt", "keeps retrying until a transient operation succeeds"],
  ["packages/cli/src/templates/common/bundled-skills/trellis-channel/SKILL.md", "Copyable Worker Prompt Template"],
  ["packages/cli/src/templates/trellis/workflow.md", "update_plan"],
  ["packages/cli/src/templates/trellis/agents/implement.md", "DONE_WITH_CONCERNS"],
  ["packages/cli/src/templates/codex/agents/trellis-implement.toml", "No implementation code before failing proof"],
  ["packages/cli/src/templates/codex/agents/trellis-check.toml", "Verify TDD evidence existed before implementation"],
  ["packages/cli/src/templates/claude/agents/trellis-implement.md", "No implementation code before failing proof"],
  ["packages/cli/src/templates/claude/agents/trellis-check.md", "Verify proof existed before implementation"],
];
```

Use exact final strings after implementation.

- [ ] **Step 2: Run static marker test**

Run:

```bash
pnpm vitest run packages/cli/test/templates/disciplined-runtime.test.ts
```

Expected:

- All markers pass.

---

### Task 9: Fresh init smoke

**Files:**
- Modify: none in repo unless smoke reveals a bug
- Temp output: `/tmp/trellis-disciplined-init-smoke-*`

- [ ] **Step 1: Inspect package scripts**

Run:

```bash
cat package.json
cat packages/cli/package.json
```

Expected:

- Identify the correct local CLI invocation, such as `pnpm --filter @mindfoldhq/trellis-cli ...` or `pnpm trellis`.

- [ ] **Step 2: Build if needed**

Run the minimum build command needed for local CLI template changes to be visible.

Expected:

- Local CLI runs against current source or freshly built dist.

- [ ] **Step 3: Initialize temp project**

Run equivalent of:

```bash
SMOKE_DIR=$(mktemp -d /tmp/trellis-disciplined-init-smoke-XXXXXX)
trap 'rm -rf "$SMOKE_DIR"' EXIT
cd "$SMOKE_DIR"
git init
<local-trellis-cli> init -y --tools codex,claude
```

Expected:

- Init exits 0.
- `.trellis`, `.agents`, `.codex`, and `.claude` files are generated.

- [ ] **Step 4: Verify generated markers**

Run:

```bash
rg "NO IMPLEMENTATION CODE BEFORE FAILING PROOF" .agents .trellis .codex .claude
rg "trellis-debug" .agents .trellis
rg "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST" .agents .trellis
rg "No implementation code before failing proof" .codex/agents .claude/agents .trellis/agents
rg "Verify proof existed before implementation|Verify TDD evidence existed before implementation" .codex/agents .claude/agents .trellis/agents
rg "trellis-visual-companion|Planning Quality Bar|waitForCondition|Copyable Worker Prompt Template|Superpowers Integration Verification Scenarios" .agents .trellis .codex .claude
rg "find-polluter.sh|POLLUTER_CANDIDATE" .trellis/spec/guides/debugging-guide.md
```

Expected:

- Every command finds at least one generated file.
- Temporary smoke directory is removed by the shell trap after the smoke run.

---

### Task 10: Update smoke

**Files:**
- Modify: none in repo unless smoke reveals a bug
- Temp output: `/tmp/trellis-disciplined-update-smoke-*`

- [ ] **Step 1: Create old-style fixture**

Use the current published Trellis CLI or a saved pre-Phase-B checkout to initialize a temp project. If not available, create a minimal fixture by copying current generated files and removing one disciplined marker from a hash-tracked template file.

Expected:

- Fixture has `.trellis/.template-hashes.json` and generated runtime files.

- [ ] **Step 2: Run local fork update**

Run:

```bash
UPDATE_SMOKE_DIR=$(mktemp -d /tmp/trellis-disciplined-update-smoke-XXXXXX)
trap 'rm -rf "$UPDATE_SMOKE_DIR"' EXIT
cd "$UPDATE_SMOKE_DIR"
<local-trellis-cli> update
```

Expected:

- Update exits 0 or reports expected conflict prompts.
- It does not overwrite user-modified files silently.

- [ ] **Step 3: Verify updated markers**

Run the same marker `rg` commands from Task 9.

Expected:

- Disciplined runtime files are present after update.
- User-modified fixture file behavior matches existing update conflict rules.
- Temporary smoke directory is removed by the shell trap after the smoke run.

---

### Task 11: Full verification and handoff

**Files:**
- Read: git diff and test outputs
- Modify: no files unless verification finds a real issue

- [ ] **Step 1: Run targeted tests**

Run:

```bash
pnpm vitest run packages/cli/test/templates/trellis.test.ts packages/cli/test/templates/codex.test.ts packages/cli/test/templates/claude.test.ts packages/cli/test/configurators/shared.test.ts
```

Expected:

- All targeted tests pass.

- [ ] **Step 2: Run full checks**

Run:

```bash
pnpm typecheck
pnpm test
```

Expected:

- Full checks pass, or failures are clearly unrelated/pre-existing with evidence.

- [ ] **Step 3: Review final diff**

Run:

```bash
git diff --name-only
git diff --stat
```

Expected:

- Diff is limited to Phase B template, configurator, test, and doc files.
- No Pomotree product files are copied into Trellis templates.

- [ ] **Step 4: Reverse smoke on Pomotree**

Use Pomotree only after the template source and init/update smokes pass.

Run:

```bash
POMOTREE_BACKUP=$(mktemp -d /tmp/pomotree-trellis-runtime-backup-XXXXXX)
trap 'rm -rf "$POMOTREE_BACKUP"' EXIT
cd /Users/maple/Documents/Pomotree
cp -R .agents .trellis .codex .claude "$POMOTREE_BACKUP"/
# Note: copying `.claude` backs up `.claude/agents`, `.claude/skills`, hooks, commands, and settings together.
<local-trellis-cli> update
diff -ru "$POMOTREE_BACKUP/.agents" .agents | sed -n '1,220p' || true
diff -ru "$POMOTREE_BACKUP/.trellis" .trellis | sed -n '1,220p' || true
diff -ru "$POMOTREE_BACKUP/.codex" .codex | sed -n '1,220p' || true
diff -ru "$POMOTREE_BACKUP/.claude" .claude | sed -n '1,220p' || true
rg "NO IMPLEMENTATION CODE BEFORE FAILING PROOF|trellis-debug|No implementation code before failing proof|Verify proof existed before implementation|Verify TDD evidence existed before implementation" .agents .trellis .codex .claude
```

Expected:

- Pomotree still contains the disciplined markers after update.
- Differences are reviewed as template normalization, expected hash/update metadata, or real regressions.
- Do not require byte-for-byte equality when generated templates legitimately differ from Pomotree's manually edited golden fixture.
- Do not force-add ignored Pomotree runtime files to git.

- [ ] **Step 5: Report**

Report:

```text
Phase B personal fork distribution implemented.
Verified: <commands run>.
Fresh init smoke: <path + result>.
Update smoke: <path + result>.
Files changed: <summary>.
Remaining risks: <if any>.
```

---

## Plan Self-Review

- Spec coverage: covers workflow, common skills, visual companion, debug skill registration, guides, polluter helper, verification scenarios, channel agents, Codex/Claude agents, channel orchestration, tests, init smoke, update smoke.
- Scope check: personal fork default templates only; no upstream PR compatibility and no profile layer.
- Placeholder scan: no placeholder or future-fill markers.
- Risk control: existing dirty files are recorded first; Pomotree remains read-only golden fixture; generated file behavior is verified by fresh init/update smoke.
- YAGNI check: Codex/Claude platform parity first; Cursor, OpenCode, Gemini, Qoder, CodeBuddy, Copilot, Droid, Pi, Kiro, Antigravity, Devin, and other platform-specific agents are intentionally deferred until separately validated.
