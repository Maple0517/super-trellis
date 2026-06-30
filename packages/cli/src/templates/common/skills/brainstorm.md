# Trellis Brainstorm

## Non-Negotiable Interview Contract

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

## Non-Negotiable Evidence Rule

If a question can be answered by exploring the codebase, explore the codebase instead.

This is mandatory. Before asking the user a question, first check whether the answer is already available in code, tests, configs, docs, existing specs, or task history.

Do not ask the user to confirm facts that the repository can answer. Ask only for product intent, preference, scope, risk tolerance, or decisions that remain ambiguous after inspection.

---

Use this skill to clarify requirements, scope, and trade-offs. In task mode, it turns the user's request into planning artifacts. In no-task mode, it stays bounded to evidence gathering, direction narrowing, and recommendation.

## Preconditions

Resolve the mode before taking action:

This skill has two modes:

- **Task mode**: task exists or the user approved task creation. Use the full planning flow and write planning artifacts.
- **No-task mode**: no active task exists and the user declined task creation. Use bounded brainstorming only: inspect repo evidence, narrow direction, recommend scope, and ask one question at a time when needed. Do not create planning artifacts and do not expand into full implementation planning.

In no-task mode, once the conversation needs a real option tree, repeated product decisions, durable planning, or implementation-level sequencing, stop and ask again to create a Trellis task.

Hard upgrade triggers:
1. The work needs persistent planning or durable decision records such as `prd.md`, `design.md`, or `implement.md`.
2. The work spans multiple stages, multiple sessions, or otherwise will not naturally finish inside the current inline pass.
3. The work needs task lifecycle features such as `trellis-continue`, `trellis-finish-work`, archive, or journal recording.
4. The work needs structured decomposition or coordination such as parent/child task trees, explicit dependency management, or `trellis-channel`.
5. Risk or scope increases to the point that explicit planning, rollback thinking, or code-level implementation sequencing is needed.
6. Future agents or sessions will need durable context injection beyond the current conversation, such as task artifacts, JSONL manifests, curated research files, or stable handoff context.

In task mode, if no task exists yet, create one:

```bash
TASK_DIR=$(python3 ./.trellis/scripts/task.py create "<short task title>" --slug <slug>)
```

Use a concise title from the user's request. Use a slug without a date prefix. `task.py create` adds the `MM-DD-` directory prefix automatically.

`task.py create` creates the default `prd.md`. Update that file with the current understanding before asking follow-up questions.

## Planning Flow

1. Capture the user's request and initial known facts in `prd.md`.
2. Inspect available evidence before asking questions:
   - code, tests, fixtures, and configs
   - README files, docs, existing specs, and domain notes
   - related Trellis tasks, research files, and session history when present
3. Separate what you found into:
   - confirmed facts
   - product intent still needed from the user
   - scope or risk decisions still needed from the user
   - likely out-of-scope items
4. Ask the single highest-value remaining question.
5. Include your recommended answer with the question.
6. After each user answer, update `prd.md` before continuing.
7. For complex tasks, create or update `design.md` and `implement.md` before implementation starts.
8. Before final review or `task.py start`, run the PRD convergence pass below.
9. For frontend visual, layout-heavy, or interaction-heavy work, explicitly evaluate whether Visual Companion would improve design exploration or review. If yes, recommend it before locking the design.

Do not invent a project-specific product/spec hierarchy. If the repository already has product, domain, or spec docs, use them. If it does not, proceed with the evidence that exists.

## No-task Mode

When no active task exists and the user declined task creation:

1. Inspect repository evidence first.
2. Clarify scope, direction, and trade-offs one question at a time when needed.
3. Recommend the smallest viable direction.
4. Do not create or update `prd.md`.
5. Do not create `design.md` or `implement.md`.
6. Do not expand into full implementation planning for complex work.
7. If work needs persistent planning, multi-stage execution, durable context, or lifecycle tracking, stop and ask again to create a Trellis task.
8. If any hard upgrade trigger appears, stop bounded brainstorming and ask to create a Trellis task before deeper planning.

## Question Rules

Ask only one question per message.

Each question must include:

- the decision needed
- why the answer matters
- your recommended answer
- the trade-off if the user chooses differently

Do not ask process questions such as whether to search, inspect files, or continue brainstorming. Do the evidence work directly. Ask the user only when the remaining issue is a product decision, preference, scope boundary, or risk tolerance choice.

## Thinking Framework: First Principles Analysis

When requirements are vague, solutions feel over-engineered, or you're about to add complexity "because everyone does" — decompose to fundamental truths before reasoning upward.

### Step 1: Restate the Problem

Strip away implementation details to one sentence.

> Bad: "We need to add Redis caching to the user profile endpoint"
> Good: "User profile data takes too long to load"

### Step 2: List Fundamental Truths

What is absolutely true (not opinion or convention)?

| Category | Examples |
|----------|----------|
| **Physical constraints** | Network latency ≥ 0, disk I/O has limits |
| **Business rules** | "Users must see their own data" |
| **Technical invariants** | "Data must be consistent" |
| **User needs** | "The user wants X within Y seconds" |

### Step 3: Challenge Assumptions

For each component of the current plan:

- **Fact or convention?** "We always use REST" — why?
- **What if we removed this?** If nothing breaks, it's unnecessary.
- **Solving the actual problem or a symptom?** Trace the causal chain.
- **Who benefits from this complexity?** If "nobody", simplify.

### Step 4: Build Up from Truths

1. Start with the minimum viable mechanism satisfying all truths
2. Add complexity only when a specific truth demands it
3. Each addition must answer: "Which truth requires this?"

### Step 5: Validate

- Does the solution solve the original problem?
- What assumptions need verification?
- What's the simplest experiment to test this?

## Artifact Rules

`prd.md` records requirements and acceptance:

- goal and user value
- confirmed facts
- requirements
- acceptance criteria
- out of scope
- open questions that still block planning

`design.md` records technical design for complex tasks:

- architecture and boundaries
- data flow and contracts
- compatibility and migration notes
- important trade-offs
- operational or rollback considerations

`implement.md` records execution planning for complex tasks:

- ordered implementation checklist
- validation commands
- risky files or rollback points
- follow-up checks before `task.py start`

Lightweight tasks may have only `prd.md`. Complex tasks must have `prd.md`, `design.md`, and `implement.md` before `task.py start`.

`implement.md` is not a replacement for `implement.jsonl`. On sub-agent-dispatch workflows, `implement.jsonl` and `check.jsonl` must each contain at least one real spec/research entry before `task.py start`; the seed `_example` row does not count. Inline workflows skip this JSONL gate because Phase 2 loads context through `trellis-before-dev`.

## PRD Convergence Pass

Before declaring planning ready or running `task.py start`, rewrite `prd.md` once against the final structure described in the artifact rules above. This is not optional cleanup; it is the final planning gate.

The pass must be lossless:

- Collapse repeated facts into one authoritative section.
- Fold temporary brainstorm sections such as `What I already know`, `Assumptions`, and resolved `Open Questions` into Goal, Background, Requirements, Technical Notes, or Acceptance Criteria.
- Remove resolved open questions instead of leaving empty or already-answered sections.
- Merge parallel bug and requirement lists when they describe the same work; keep each defect's severity, evidence, and file:line anchors on the owning requirement.
- Preserve every file:line anchor, decision, constraint, requirement ID, and acceptance-criteria mapping.
- Keep only genuinely blocking open questions.

After the pass, read `prd.md` top to bottom and verify that no fact is repeated across sections unless the repetition adds new information.

## Quality Bar

Before declaring planning ready:

- `prd.md` contains testable acceptance criteria.
- `prd.md` has passed the PRD convergence pass: no unresolved temporary brainstorm sections, no duplicate facts across sections, and no lost anchors, decisions, or acceptance mappings.
- Repository-answerable questions have already been answered through inspection.
- Remaining open questions are genuinely about user intent or scope.
- Complex tasks have `design.md` and `implement.md`.
- Sub-agent-dispatch tasks have real curated entries in both `implement.jsonl` and `check.jsonl`; seed-only manifests are not ready.
- The user has reviewed the final planning artifacts or explicitly approved proceeding.
- No placeholder markers such as `TBD`, unresolved contradictions, or vague acceptance criteria remain.

Do not start implementation until the user approves or asks for implementation.

## Design Gate

Before implementation planning, converge on a design. Inspect project evidence first, ask one question at a time, recommend an answer with trade-offs, then present 2-3 approaches when there is a real design choice. After the user selects or approves the design, write or update the Trellis planning artifacts.

Do not begin implementation planning until the user has approved the design, regardless of perceived simplicity.

When the task is frontend-visual in nature, do not silently skip Visual Companion. Explicitly decide whether it would add signal. If the answer is no, proceed without it; if the answer is yes, recommend using it before design lock.

If the scope contains multiple independent subsystems, decompose it before planning implementation. Each sub-project must produce independently testable work.


## Planning Quality Bar

For complex work, write `implement.md` in this order:

1. File map: exact files to create, modify, and test; include each file's responsibility.
2. Header: Goal, Architecture, and Tech Stack.
3. Tasks: `### Task N: Name`, `**Files:**`, then checkbox steps.
4. Steps: one action each, sized for 2-5 minutes, with exact commands and expected output when verification is involved.
5. Self-review: spec coverage, placeholder scan, and type/signature consistency.

Do not write placeholders such as TBD, TODO, "implement later", "add appropriate error handling", "write tests for the above", or "similar to previous task".

When asking user preferences, prefer 2-3 concrete choices with a recommended option and tradeoff unless the user asked an open-ended question. Ask one question per message.

For frontend visual/layout/interaction work, explicitly evaluate `trellis-visual-companion`. If useful, run it before design lock or visual review; if not useful, record why text-only review is enough.

### PRD / Spec Self-Review

Before design lock, absorb the spec-reviewer checklist without copying the original Superpowers prompt:

- Placeholder scan: no TBD/TODO/unresolved markers.
- Contradiction scan: requirements do not conflict with each other or existing project constraints.
- Ambiguity scan: every acceptance criterion is testable.
- Missing acceptance-criteria scan: every important requirement has at least one acceptance criterion.
- User-decision trace: major choices record the selected option and tradeoff.
- Scope-boundary check: out-of-scope work is explicit.

Fix issues inline before asking for implementation approval.

### Implement Plan Reviewer Checklist

Absorb the plan-reviewer checklist into Trellis planning:

- File map exists before tasks.
- Every requirement maps to a task.
- Every task has exact files and verification.
- Steps are 2-5 minute single actions.
- No placeholders or "similar to previous task" shortcuts.
- Type, function, file, and status names stay consistent across tasks.
- Rollback points, stop points, and user-decision blockers are explicit.
