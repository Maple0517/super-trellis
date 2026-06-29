# Phase B Design: Personal Fork Distribution for Disciplined Trellis

**Date:** 2026-06-29
**Scope:** Maple's local Trellis fork distribution.
**Decision:** Productize the Pomotree-verified Trellis magic-mod into the Trellis template source so `trellis init` and `trellis update` generate the disciplined runtime by default.

---

## 1. Goal

Phase A proved the integration locally in Pomotree. Phase B turns that verified local runtime into the default output of this Trellis fork.

Target user experience:

```bash
trellis init
trellis update
```

A new or existing project should receive the disciplined Trellis runtime without manually copying Pomotree files.

This is a personal fork distribution, not an upstream-compatible PR.

---

## 2. Non-goals

- Do not preserve upstream default behavior for broad compatibility.
- Do not design for upstream PR acceptance.
- Do not create a second workflow beside `.trellis/workflow.md`.
- Do not keep Superpowers as a dependency or plugin.
- Do not use Pomotree app-specific rules as global Trellis defaults.
- Do not add a `--profile maple` layer unless a future need appears. The fork default is the profile.
- Do not rely on marketplace/registry as the main delivery path for runtime files.

---

## 3. Source of Truth

Phase B has two inputs:

1. **Golden fixture:** `/Users/maple/Documents/Pomotree`
   - Verified local Trellis runtime after Phase A.
   - Contains the desired workflow, skills, guides, channel agents, and platform agents.

2. **Distribution source:** `/Users/maple/Documents/trellis`
   - The Trellis fork that owns `packages/cli/src/templates/**`, configurators, migrations, tests, and built package output.

Rule: extract only generic Trellis runtime behavior from Pomotree. Do not copy Pomotree product rules, release workflow, app docs, or project-specific specs.

---

## 4. Distribution Strategy

Use the fork as the distribution source.

- Upstream Trellis remains a rebase/cherry-pick source only.
- This fork is allowed to diverge intentionally.
- Default templates are modified directly instead of adding an opt-in profile.
- Registry/marketplace may still distribute spec templates, but not the full runtime.

Why not registry only:

- Existing registry logic primarily installs `.trellis/spec` templates and selected workflow templates.
- This integration also changes `.agents/skills`, `.trellis/agents`, `.codex/agents`, `.claude/agents`, and platform-specific prompts.
- Those are generation/runtime templates, so the reliable path is the CLI template source.

---

## 5. Runtime Contract

Generated projects must receive these behaviors by default.

### 5.1 Workflow

`packages/cli/src/templates/trellis/workflow.md` must include:

- no-task triage limit before task creation,
- planning breadcrumb updates,
- in-progress and inline in-progress breadcrumbs,
- explicit debug routing before fixes,
- TDD gate visible in breadcrumbs,
- completion claim gate,
- review feedback routing,
- Visual Companion evaluation for frontend visual tasks,
- global step tracking guidance (`update_plan` / `TodoWrite`),
- finish-before-polish gate,
- existing dispatch context, JSONL, and sub-agent self-exemption rules preserved.

### 5.2 Skills

Common Trellis skills must absorb Phase A behavior:

| Skill template | Required Phase B content |
|---|---|
| `before-dev.md` | spec loading, update_plan/TodoWrite, TDD Iron Law, decision matrix, rationalizations, red flags, verify-RED, discard-and-restart, green verification |
| `brainstorm.md` | triage-only before task creation, repo evidence before questions, one question per turn, options before design, design approval, Visual Companion evaluation |
| `check.md` | completion claim gate, claim-to-evidence table, review gate, TDD evidence review, test coverage clarification, finish-before-polish |
| `break-loop.md` | explicit post-fix retrospective role, not first-stop debugging |
| `finish-work.md` | verify before finish, staged/unstaged hygiene, ignored Trellis runtime reporting, branch finish choices |
| `channel.md` if templated | Trellis-channel orchestration rules, not generic Superpowers subagent shell |
| `debug.md` | new skill: pre-fix systematic debugging with Iron Law, red flags, evidence phases, rationalization prevention, 3-fix stop rule |

If a skill currently exists only in generated local `.agents/skills` but not `packages/cli/src/templates/common/skills`, add or register it in the same mechanism used by bundled Trellis skills.

### 5.3 Guides

Template guides must include:

- `debugging-guide.md`: root-cause tracing, condition-based waiting, defense in depth, polluter search, multi-component tracing, elusive-root-cause guidance.
- `testing-guide.md`: TDD proof gate, mocking rules, anti-patterns, Good Tests, Good/Bad examples, regression red-green, When Stuck, TDD verification checklist, completion evidence.
- `index.md`: links to both guides with clear use cases.

### 5.4 Channel agents

`packages/cli/src/templates/trellis/agents/implement.md` must include:

- proof gates,
- TDD execution gate,
- plan execution discipline,
- debug route on failures,
- branch guard,
- no commit/push/merge,
- structured status: `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`.

`packages/cli/src/templates/trellis/agents/check.md` must include:

- independent verification of implementer output,
- spec compliance before code quality,
- TDD evidence review,
- completion claim gate,
- review feedback gate,
- self-fix boundary,
- verification report format.

### 5.5 Platform agents

At minimum, synchronize the same compact execution/evidence gates into:

- `packages/cli/src/templates/codex/agents/trellis-implement.toml`
- `packages/cli/src/templates/codex/agents/trellis-check.toml`
- `packages/cli/src/templates/claude/agents/trellis-implement.md`
- `packages/cli/src/templates/claude/agents/trellis-check.md`

For other platform agent templates, choose one of two explicit policies:

1. **Full parity now:** update every platform agent template.
2. **Codex/Claude first:** document that other platforms lag until separately validated.

Recommendation: Codex/Claude first, because those are the tested paths. Add grep regression tests so future expansion is mechanical.

---

## 6. Template Registration

Phase B must inspect and update the actual generation path before editing.

Expected targets:

- `packages/cli/src/templates/common/skills/*.md`
- `packages/cli/src/configurators/shared.ts`
- platform configurators under `packages/cli/src/configurators/*.ts` if they map skill names or generated filenames,
- `packages/cli/src/templates/trellis/workflow.md`
- `packages/cli/src/templates/trellis/agents/*.md`
- `packages/cli/src/templates/{codex,claude}/agents/*`
- `packages/cli/src/templates/markdown/spec/guides/*.md.txt`
- tests under `packages/cli/test/**`.

New generated skill requirement:

- `trellis-debug` must have valid frontmatter.
- The generated skill name and description must be trigger-oriented, not a workflow summary.
- Platform skill copies must be generated consistently with existing Trellis skill naming conventions.

---

## 7. Update Semantics

Existing projects running `trellis update` should receive the new disciplined runtime through normal template update/conflict behavior.

Rules:

- Preserve Trellis-protected project data: `.trellis/tasks`, `.trellis/workspace`, project specs, and user local edits.
- Do not silently overwrite user-modified files; rely on existing conflict flow.
- Template hash tracking must recognize new template contents.
- If a generated file is ignored by the project repo, still update it on disk; git tracking is the project owner's decision.

Pomotree-specific note: Pomotree currently ignores `.trellis`, `.agents`, `.codex`, `.claude`; Phase B should still update those runtime files locally. Git status visibility is not the source of truth.

---

## 8. Validation Strategy

Phase B is done only when generated projects prove the runtime exists.

### 8.1 Static regression tests

Add or extend tests to assert generated files contain:

- `NO IMPLEMENTATION CODE BEFORE FAILING PROOF`,
- `trellis-debug`,
- `NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST`,
- `Completion Claim Gate`,
- `Review Gate`,
- `Visual Companion`,
- `update_plan`,
- `Additional polish is a new scope decision` or equivalent finish-before-polish rule,
- `No implementation code before failing proof` in Codex/Claude implement agents,
- `Verify proof existed before implementation` in Codex/Claude check agents,
- `DONE_WITH_CONCERNS` in implement agents.

### 8.2 Fresh init smoke

Create a temporary project and run the local fork's `trellis init`.

Verify generated files:

```bash
rg "NO IMPLEMENTATION CODE BEFORE FAILING PROOF" .agents .trellis .codex .claude
rg "trellis-debug" .agents .trellis
rg "No implementation code before failing proof" .codex/agents .claude/agents .trellis/agents
rg "Verify proof existed before implementation" .codex/agents .claude/agents .trellis/agents
```

### 8.3 Update smoke

Create or reuse a temporary project initialized from the old template, then run local fork `trellis update`.

Verify:

- generated runtime files receive the disciplined rules,
- user-modified files are not overwritten silently,
- `.trellis/config.yaml` registry settings remain valid,
- template hash state is updated as expected.

### 8.4 Package checks

Run the repo's normal checks after implementation:

```bash
pnpm typecheck
pnpm test
```

If full tests are too expensive during iteration, run targeted template/configurator tests first and full tests before finalizing.

---

## 9. Rollout Plan

1. Record current Trellis fork base SHA.
2. Diff Pomotree golden runtime against Trellis template source.
3. Copy generic behavior into template source with minimal rewrites.
4. Register `trellis-debug` and new guides.
5. Synchronize Codex/Claude platform agent templates.
6. Add regression tests for disciplined markers.
7. Run targeted tests.
8. Run fresh init smoke.
9. Run update smoke.
10. Run full checks.
11. Install/link the fork locally.
12. Use the fork on one new non-Pomotree project before treating it as stable.

---

## 10. Local Installation Options

Preferred during development:

```bash
pnpm install
pnpm build
npm link
```

Then in target projects:

```bash
trellis init
trellis update
```

Alternative later:

- publish under a private npm scope,
- install from a Git URL,
- keep a local shell alias pointing to the built CLI.

The fork should expose itself clearly in `trellis --version` or release notes if version metadata is easy to adjust. This is optional for Phase B but useful to avoid confusing upstream Trellis with Maple Trellis.

---

## 11. Rebase Policy

Upstream is a source of patches, not the design owner.

When rebasing/cherry-picking upstream:

1. Re-run static regression tests for all disciplined markers.
2. Re-run fresh init smoke if template files changed.
3. Re-run update smoke if update/migration/configurator logic changed.
4. Compare Pomotree golden runtime to generated output if behavior seems to drift.

If upstream changes conflict with the disciplined runtime, preserve the disciplined runtime unless the upstream change fixes a concrete bug or compatibility issue.

---

## 12. Risks

| Risk | Mitigation |
|---|---|
| Template drift from Pomotree | Keep Pomotree as golden fixture; add marker tests. |
| Platform drift | Codex/Claude first; explicit parity policy for other platforms. |
| Overwriting local user edits on update | Use existing template hash/conflict flow; test modified-file update. |
| Too much duplicated TDD text | Long rules live in `trellis-before-dev` and `testing-guide`; agents get compact rules plus references. |
| Upstream rebase removes gates | Static regression tests fail fast. |
| Superpowers dependency sneaks back | Do not include `superpowers:*` references in runtime files; keep methods native Trellis. |

---

## 13. Acceptance Criteria

- `trellis init` from this fork generates the disciplined runtime by default.
- `trellis update` from this fork updates existing projects through normal conflict-safe flow.
- Generated projects include `trellis-debug`.
- Generated workflow breadcrumbs expose debug routing, TDD gate, completion gate, review routing, update_plan tracking, and finish-before-polish.
- Generated Codex and Claude implement/check agents contain compact TDD execution/evidence gates.
- Generated testing/debugging guides contain Phase A content.
- Tests or smoke checks prove all critical markers exist.
- No runtime file requires the Superpowers plugin.

---

## 14. Open Decisions

1. Whether to update every non-Codex/Claude platform agent in Phase B or leave them explicitly lagging.
2. Whether to rename the fork's CLI/version string to distinguish it from upstream.
3. Whether to keep `docs/superpowers/*` as design history or rename future docs away from Superpowers now that the plugin is uninstalled.
