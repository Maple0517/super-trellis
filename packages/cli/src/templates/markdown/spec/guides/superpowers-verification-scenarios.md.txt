# Superpowers Integration Verification Scenarios

Audit-only. Use these scenarios to verify the local Trellis integration. They are not mandatory runtime gates.

## Debugging Pressure Scenarios

- Symptom moves after one fix: return to root-cause tracing; do not stack patches.
- Failure crosses UI/API/storage: collect evidence at every boundary before hypothesizing.
- Test passes alone but fails in suite: run polluter search and inspect shared state, clocks, network mocks, global caches, filesystem artifacts, database rows, and environment variables.
- Academic/artificial debugging drills are optional self-tests for the debugging skill, not project runtime rules.

## Planning Scenarios

- Complex request in `no_task`: stay at triage depth and ask for task creation before substantive brainstorming.
- Complex planning: `implement.md` starts with file map and Goal/Architecture/Tech Stack, then exact bite-sized tasks with expected outputs.
- Frontend visual task: Visual Companion is explicitly evaluated and can create a local HTML fallback.

## TDD / Verification Scenarios

- Behavior change: proof exists before implementation.
- Bug fix: reproduction/regression proof fails before fix and passes after.
- Completion claim: success language is blocked until fresh evidence passes.
- Output cleanliness: warnings, skipped tests, or unrelated failures are explained, not hidden.

## Review / Agent Scenarios

- Review feedback: source-specific handling, implementation order, pushback, unclear feedback, and YAGNI checks exist.
- Check agent: review is two-stage, spec compliance first and code quality second.
- Implement/check agents: status protocol and no-nested-subagent guard exist.
- Channel workers: prompt template includes scope, constraints, expected output, verification, blockers, and status enum.
