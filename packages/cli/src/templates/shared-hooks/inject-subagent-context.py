#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Platform Sub-Agent Context Injection Hook

Injects task-specific context when sub-agents (implement, check, research) are spawned.

Core Design Philosophy:
- Hook is responsible for injecting all context, subagent works autonomously with complete info
- Each agent has a dedicated jsonl file defining its context
- No resume needed, no segmentation, behavior controlled by code not prompt

Trigger: PreToolUse (before Task tool call)

Context Source: Trellis active task resolver points to task directory
- implement.jsonl - Implement agent dedicated context
- check.jsonl     - Check agent dedicated context
- prd.md          - Requirements document
- design.md       - Technical design for complex tasks
- implement.md    - Execution plan for complex tasks
- codex-review-output.txt - Code Review results
"""
from __future__ import annotations

# IMPORTANT: Suppress all warnings FIRST
import warnings
warnings.filterwarnings("ignore")

import json
import os
import sys
from pathlib import Path
from typing import Any

# IMPORTANT: Force stdout to use UTF-8 on Windows
# This fixes UnicodeEncodeError when outputting non-ASCII characters
if sys.platform.startswith("win"):
    import io as _io
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    elif hasattr(sys.stdout, "detach"):
        sys.stdout = _io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# =============================================================================
# Path Constants (change here to rename directories)
# =============================================================================

DIR_WORKFLOW = ".trellis"
DIR_SPEC = "spec"
FILE_TASK_JSON = "task.json"

# =============================================================================
# Subagent Constants (change here to rename subagent types)
# =============================================================================

AGENT_IMPLEMENT = "trellis-implement"
AGENT_CHECK = "trellis-check"
AGENT_RESEARCH = "trellis-research"

# Agents that require a task directory
AGENTS_REQUIRE_TASK = (AGENT_IMPLEMENT, AGENT_CHECK)
# All supported agents
AGENTS_ALL = (AGENT_IMPLEMENT, AGENT_CHECK, AGENT_RESEARCH)


def find_repo_root(start_path: str) -> str | None:
    """
    Find git repo root from start_path upwards

    Returns:
        Repo root path, or None if not found
    """
    current = Path(start_path).resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return str(current)
        current = current.parent
    return None


def _detect_platform(input_data: dict) -> str | None:
    if isinstance(input_data.get("cursor_version"), str):
        return "cursor"
    env_map = {
        "CLAUDE_PROJECT_DIR": "claude",
        "CURSOR_PROJECT_DIR": "cursor",
        "CODEBUDDY_PROJECT_DIR": "codebuddy",
        "FACTORY_PROJECT_DIR": "droid",
        "GEMINI_PROJECT_DIR": "gemini",
        "QODER_PROJECT_DIR": "qoder",
        "KIRO_PROJECT_DIR": "kiro",
        "COPILOT_PROJECT_DIR": "copilot",
    }
    for env_name, platform in env_map.items():
        if os.environ.get(env_name):
            return platform
    script_parts = set(Path(sys.argv[0]).parts)
    if ".claude" in script_parts:
        return "claude"
    if ".cursor" in script_parts:
        return "cursor"
    if ".gemini" in script_parts:
        return "gemini"
    if ".qoder" in script_parts:
        return "qoder"
    if ".codebuddy" in script_parts:
        return "codebuddy"
    if ".factory" in script_parts:
        return "droid"
    if ".kiro" in script_parts:
        return "kiro"
    return None


def get_current_task(repo_root: str, input_data: dict) -> str | None:
    """Resolve current task directory through the unified active task resolver."""
    scripts_dir = Path(repo_root) / DIR_WORKFLOW / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    try:
        from common.active_task import resolve_active_task  # type: ignore[import-not-found]
    except Exception:
        return None

    active = resolve_active_task(
        Path(repo_root),
        input_data,
        platform=_detect_platform(input_data),
    )
    return active.task_path


def read_file_content(base_path: str, file_path: str) -> str | None:
    """Read file content, return None if file doesn't exist"""
    full_path = os.path.join(base_path, file_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None
    return None


def read_directory_contents(
    base_path: str, dir_path: str, max_files: int = 20
) -> list[tuple[str, str]]:
    """
    Read all .md files in a directory

    Args:
        base_path: Base path (usually repo_root)
        dir_path: Directory relative path
        max_files: Max files to read (prevent huge directories)

    Returns:
        [(file_path, content), ...]
    """
    full_path = os.path.join(base_path, dir_path)
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        return []

    results = []
    try:
        # Only read .md files, sorted by filename
        md_files = sorted(
            [
                f
                for f in os.listdir(full_path)
                if f.endswith(".md") and os.path.isfile(os.path.join(full_path, f))
            ]
        )

        for filename in md_files[:max_files]:
            file_full_path = os.path.join(full_path, filename)
            relative_path = os.path.join(dir_path, filename)
            try:
                with open(file_full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    results.append((relative_path, content))
            except Exception:
                continue
    except Exception:
        pass

    return results


def read_jsonl_entries(base_path: str, jsonl_path: str) -> list[tuple[str, str]]:
    """
    Read all file/directory contents referenced in jsonl file

    Schema:
        {"file": "path/to/file.md", "reason": "..."}
        {"file": "path/to/dir/", "type": "directory", "reason": "..."}
        {"_example": "..."}          # seed row — skipped (no `file` field)

    Rows without a ``file`` field (e.g. the self-describing seed line written
    by ``task.py create`` before the agent has curated entries) are skipped
    silently. If the resulting entry list is empty, a stderr warning is
    emitted so the operator can debug missing context.

    Returns:
        [(path, content), ...]
    """
    full_path = os.path.join(base_path, jsonl_path)
    if not os.path.exists(full_path):
        print(
            f"[inject-subagent-context] WARN: {jsonl_path} not found — "
            f"sub-agent will receive only task artifacts",
            file=sys.stderr,
        )
        return []

    results = []
    saw_real_entry = False
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                    file_path = item.get("file") or item.get("path")
                    entry_type = item.get("type", "file")

                    if not file_path:
                        # Seed / comment row — skip silently
                        continue

                    saw_real_entry = True
                    if entry_type == "directory":
                        # Read all .md files in directory
                        dir_contents = read_directory_contents(base_path, file_path)
                        results.extend(dir_contents)
                    else:
                        # Read single file
                        content = read_file_content(base_path, file_path)
                        if content:
                            results.append((file_path, content))
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass

    if not saw_real_entry:
        print(
            f"[inject-subagent-context] WARN: {jsonl_path} has no curated "
            f"entries (only seed / empty) — sub-agent will receive only "
            f"task artifacts. See workflow.md planning artifact guidance.",
            file=sys.stderr,
        )

    return results




def get_agent_context(repo_root: str, task_dir: str, agent_type: str) -> str:
    """
    Get context from {agent_type}.jsonl for the specified agent.
    Only reads implement.jsonl or check.jsonl (the two JSONL files the task system creates).
    """
    context_parts = []

    agent_jsonl = f"{task_dir}/{agent_type}.jsonl"
    for file_path, content in read_jsonl_entries(repo_root, agent_jsonl):
        context_parts.append(f"=== {file_path} ===\n{content}")

    return "\n\n".join(context_parts)


def get_implement_context(repo_root: str, task_dir: str) -> str:
    """
    Complete context for Implement Agent

    Read order:
    1. All files in implement.jsonl (spec/research manifests)
    2. prd.md (requirements)
    3. design.md if present (technical design)
    4. implement.md if present (execution plan)
    """
    context_parts = []

    # 1. Read implement.jsonl
    base_context = get_agent_context(repo_root, task_dir, "implement")
    if base_context:
        context_parts.append(base_context)

    # 2. Requirements document
    prd_content = read_file_content(repo_root, f"{task_dir}/prd.md")
    if prd_content:
        context_parts.append(f"=== {task_dir}/prd.md (Requirements) ===\n{prd_content}")

    # 3. Technical design for complex tasks
    design_content = read_file_content(repo_root, f"{task_dir}/design.md")
    if design_content:
        context_parts.append(
            f"=== {task_dir}/design.md (Technical Design) ===\n{design_content}"
        )

    # 4. Execution plan for complex tasks
    implement_plan_content = read_file_content(repo_root, f"{task_dir}/implement.md")
    if implement_plan_content:
        context_parts.append(
            f"=== {task_dir}/implement.md (Execution Plan) ===\n{implement_plan_content}"
        )

    return "\n\n".join(context_parts)


def get_check_context(repo_root: str, task_dir: str) -> str:
    """
    Context for Check Agent: check.jsonl + task artifacts.
    """
    context_parts = []

    for file_path, content in read_jsonl_entries(repo_root, f"{task_dir}/check.jsonl"):
        context_parts.append(f"=== {file_path} ===\n{content}")

    prd_content = read_file_content(repo_root, f"{task_dir}/prd.md")
    if prd_content:
        context_parts.append(f"=== {task_dir}/prd.md (Requirements) ===\n{prd_content}")

    design_content = read_file_content(repo_root, f"{task_dir}/design.md")
    if design_content:
        context_parts.append(
            f"=== {task_dir}/design.md (Technical Design) ===\n{design_content}"
        )

    implement_plan_content = read_file_content(repo_root, f"{task_dir}/implement.md")
    if implement_plan_content:
        context_parts.append(
            f"=== {task_dir}/implement.md (Execution Plan) ===\n{implement_plan_content}"
        )

    return "\n\n".join(context_parts)


def get_finish_context(repo_root: str, task_dir: str) -> str:
    """
    Context for Finish phase: reuses check.jsonl + prd.md
    (Finish is a final check, same context source.)
    """
    return get_check_context(repo_root, task_dir)



def build_implement_prompt(original_prompt: str, context: str) -> str:
    """Build complete prompt for Implement"""
    return f"""<!-- trellis-hook-injected -->
# Implement Agent Task

You are the Implement Agent in the Trellis Multi-Agent Pipeline.

## Your Context

All the information you need has been prepared for you:

{context}

---

## Your Task

{original_prompt}

---

## Workflow

1. **Understand specs** - All dev specs are injected above, understand them.
2. **Review task artifacts** - Read requirements, technical design if present, and execution plan if present. Treat `implement.md`, when present, as the ordered execution contract.
3. **Apply the TDD execution gate** - No implementation code before failing proof: a failing test, reproduction, or executable acceptance check.
4. **Execute one step at a time** - Review `implement.md` critically against current code/spec reality, surface blockers before coding, and keep one top-level plan step in progress unless you state why batching/reordering is required.
5. **Implement the smallest change** - Write the smallest code that makes the proof pass, following specs and task artifacts.
6. **Verify** - Run the new proof and relevant existing tests before reporting status.
7. **Report status** - Use the status protocol below and list modified/created files.

## TDD Execution Gate

- No implementation code before failing proof: a failing test, reproduction, or executable acceptance check.
- Run the proof and verify it fails for the expected reason before coding.
- If you wrote implementation before proof, delete it and start over; do not keep it as reference.
- If a bug, failed test, or unexpected behavior appears, route back to the main session for `trellis-debug` instead of speculative patching.
- Write the smallest code that makes proof pass, then run the proof and relevant existing tests.

## Status Protocol

Status must be exactly one of: DONE, DONE_WITH_CONCERNS, BLOCKED, NEEDS_CONTEXT.

- DONE: implementation and relevant verification completed for the requested scope.
- DONE_WITH_CONCERNS: code changed but risks, partial verification, or follow-up check remains.
- BLOCKED: cannot proceed safely because a gate failed or user decision is required.
- NEEDS_CONTEXT: required artifacts, specs, or task direction are missing.

## Important Constraints

- Do NOT execute git commit, only code modifications
- Do NOT execute git push, git merge, or branch-changing commands
- Do NOT spawn nested implement/check sub-agents; return BLOCKED or NEEDS_CONTEXT if another worker or decision is needed
- Follow all dev specs injected above
- When the planned scope and acceptance criteria are verified, report status and hand control back to the main session; do not propose extra polish as the next step"""


def build_check_prompt(original_prompt: str, context: str) -> str:
    """Build complete prompt for Check"""
    return f"""<!-- trellis-hook-injected -->
# Check Agent Task

You are the Check Agent in the Trellis Multi-Agent Pipeline (code and cross-layer checker).

## Your Context

All check specs and dev specs you need:

{context}

---

## Your Task

{original_prompt}

---

## Workflow

1. **Get changes** - Run `git diff --name-only` and `git diff` to get code changes
2. **Spec compliance first** - Check changes against prd.md, design.md if present, implement.md if present, and acceptance criteria.
3. **Code quality second** - Inspect implementation quality, tests, lint/typecheck, security/regression risk, and maintainability.
4. **TDD evidence review** - Verify proof existed before implementation and RED/GREEN evidence is real.
5. **Mechanical self-fix only** - Fix only clearly mechanical issues.
6. **Run verification** - Run project's relevant lint, typecheck, build, or test commands.
7. **Report status** - Use the status protocol below and cite evidence.

## Reviewer/Fixer Boundary

Mechanical issues only: you may self-fix lint nits, formatting, missing or incorrect imports, obvious type annotations, trivial dead branches, obvious typos, and deterministic command failures whose fix does not change product behavior.

Do not self-fix behavior, design, test strategy, requirement mismatches, or implementation logic. For those findings, cite file/line evidence and return those findings to the main session so it can dispatch `trellis-implement` for the next implementation pass.

If a finding is not clearly mechanical, treat it as non-mechanical. Your status for non-mechanical findings is DONE_WITH_CONCERNS, not DONE.

## Completion Claim Gate

Before saying work is complete, fixed, passing, ready, or done: identify the proving command/evidence, run it freshly, read output and exit code, and only then state the claim with the proof. Do not trust implementer self-reports.

## Review Gate

When reviewing feedback, read it fully, verify it against codebase reality, evaluate correctness and scope, then accept, fix, or push back technically with evidence. Do not use gratitude or agreement as a substitute for technical evaluation.

## TDD Evidence Review

- Verify proof existed before implementation: failing test, reproduction, executable acceptance check, or recorded substitute proof.
- Verify RED failed for the expected reason and GREEN passed after the change.
- Check tests exercise real behavior, not mock behavior or implementation details.

## Status Protocol

Status must be exactly one of: DONE, DONE_WITH_CONCERNS, BLOCKED, NEEDS_CONTEXT.

## Important Constraints

- Mechanical issues only
- Must execute complete checklist in check specs
- Pay special attention to impact radius analysis (L1-L5)
- Additional polish is a new scope decision; do not recommend new work before the finish flow is offered"""


def build_finish_prompt(original_prompt: str, context: str) -> str:
    """Build complete prompt for Finish (final check before PR)"""
    return f"""<!-- trellis-hook-injected -->
# Finish Agent Task

You are performing the final Trellis finish check before commit, push, PR, archive, or stop-local handoff.

## Your Context

Finish checklist and requirements:

{context}

---

## Your Task

{original_prompt}

---

## Workflow

1. **Review changes** - Run `git diff --name-only` to see all changed files
	2. **Verify task artifacts** - Check requirements in prd.md and, when present, design.md / implement.md
3. **Completion Claim Gate** - Identify proving command/evidence, run it freshly, read output and exit code, and only then use success language
4. **Spec sync** - Analyze whether changes introduce new patterns, contracts, or conventions
   - If new pattern/convention found: read target spec file → update it → update index.md if needed
   - If infra/cross-layer change: follow the 7-section mandatory template from update-spec.md
   - If pure code fix with no new patterns: skip this step
5. **Run final checks** - Execute relevant lint, typecheck, build, test, or direct acceptance checks
6. **Finish handoff** - Report evidence and ask the main session/user for the next lifecycle step when it changes scope or external state

## Important Constraints

- You MAY update spec files when gaps are detected (use update-spec.md as guide)
- MUST read the target spec file BEFORE editing (avoid duplicating existing content)
- Do NOT update specs for trivial changes (typos, formatting, obvious fixes)
- If critical CODE issues found, report them clearly (fix specs, not code)
- Verify all acceptance criteria in prd.md are met
- Verify design.md and implement.md constraints when those files are present
- Additional polish is a new scope decision and needs user approval
- Do not create commits, pushes, PRs, archives, or cleanup actions yourself unless the caller explicitly requested that lifecycle action"""



def get_research_context(repo_root: str, task_dir: str | None) -> str:
    """
    Context for Research Agent — project structure overview for spec directories.

    `task_dir` kept for signature parity with get_implement_context / get_check_context
    so the dispatcher can call them uniformly.
    """
    _ = task_dir
    context_parts = []

    # 1. Project structure overview (dynamically discover spec directories)
    spec_path = f"{DIR_WORKFLOW}/{DIR_SPEC}"
    spec_root = Path(repo_root) / DIR_WORKFLOW / DIR_SPEC

    # Build spec tree dynamically
    tree_lines = [f"{spec_path}/"]
    if spec_root.is_dir():
        pkg_dirs = sorted(d for d in spec_root.iterdir() if d.is_dir())
        for i, pkg_dir in enumerate(pkg_dirs):
            is_last = i == len(pkg_dirs) - 1
            prefix = "└── " if is_last else "├── "
            layers = sorted(d.name for d in pkg_dir.iterdir() if d.is_dir())
            layer_info = f" ({', '.join(layers)})" if layers else ""
            tree_lines.append(f"{prefix}{pkg_dir.name}/{layer_info}")

    spec_tree = "\n".join(tree_lines)

    project_structure = f"""## Project Spec Directory Structure

```
{spec_tree}
```

To get structured package info, run: `python3 ./{DIR_WORKFLOW}/scripts/get_context.py --mode packages`

## Search Tips

- Spec files: `{spec_path}/**/*.md`
- Code structure: use the platform-exposed structural tool when available; otherwise use plain-text search/read tools
- External references: use the platform-exposed URL/document reader when available"""

    context_parts.append(project_structure)

    return "\n\n".join(context_parts)


def build_research_prompt(original_prompt: str, context: str) -> str:
    """Build complete prompt for Research"""
    return f"""<!-- trellis-hook-injected -->
# Research Agent Task

You are the Research Agent in the Multi-Agent Pipeline (search researcher).

## Core Principle

**You do one thing: find, explain, and persist information.**

Conversations get compacted; files do not. Every research output MUST end up as a file under `{{TASK_DIR}}/research/`. Returning findings only through chat is a failure.

## Project Info

{context}

---

## Your Task

{original_prompt}

---

## Workflow

1. **Resolve current task** - Run `python3 ./.trellis/scripts/task.py current --source`. If no active task is set, ask the user where to write output; do NOT guess.
2. **Plan search** - List search steps for complex queries
3. **Execute search** - Execute multiple independent searches in parallel when useful
4. **Persist each topic** - Write each distinct topic to `{{TASK_DIR}}/research/<topic-slug>.md`
5. **Report paths only** - Return file paths plus one-line summaries and critical caveats

## Search Tools

| Tool | Purpose |
|------|---------|
| Platform structural tool | Use the platform-exposed structural tool for file/module/symbol/flow questions; use Codex CodeGraph only when that tool is actually exposed, and use Claude Code gortex only on Claude Code. |
| Plain text search | Use the platform's grep/search tool for regex or exact text search. |
| Read | Read current file bytes and task artifacts. |
| URL/docs tool | Use whatever URL/document reader is exposed by the platform when external references are required. |

## Strict Boundaries

**Only allowed**: Describe what exists, where it is, how it works, and persist research notes under `{{TASK_DIR}}/research/`

**Forbidden** (unless explicitly asked):
- Suggest improvements
- Criticize implementation
- Recommend refactoring
- Modify code files, specs, workflow files, platform config, or unrelated task directories

## Report Format

Reply with ONLY:
- List of research files written
- One-line summary per file
- Any critical caveats the main agent needs immediately"""


def _string_value(value: Any) -> str:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped
    return ""


def _extract_subagent_name(value: Any) -> str:
    """Extract a sub-agent name from common platform encodings.

    Cursor's native Task args encode custom sub-agents as a protobuf oneof,
    which can appear in hook JSON as either ``{"custom": {"name": "..."}}``
    or ``{"type": {"case": "custom", "value": {"name": "..."}}}``.
    """
    direct = _string_value(value)
    if direct:
        return direct

    if not isinstance(value, dict):
        return ""

    for key in ("name", "subagent_type_name", "subagentTypeName"):
        direct = _string_value(value.get(key))
        if direct:
            return direct

    custom = value.get("custom")
    if isinstance(custom, dict):
        custom_name = _string_value(custom.get("name"))
        if custom_name:
            return custom_name

    oneof = value.get("type")
    if isinstance(oneof, dict):
        case_name = _string_value(oneof.get("case"))
        if case_name == "custom":
            nested_value = oneof.get("value")
            if isinstance(nested_value, dict):
                custom_name = _string_value(nested_value.get("name"))
                if custom_name:
                    return custom_name
        if case_name:
            return case_name

    case_name = _string_value(value.get("case"))
    if case_name == "custom":
        nested_value = value.get("value")
        if isinstance(nested_value, dict):
            custom_name = _string_value(nested_value.get("name"))
            if custom_name:
                return custom_name
    if case_name:
        return case_name

    for agent_name in AGENTS_ALL:
        if agent_name in value:
            return agent_name

    return ""


def _extract_subagent_type(tool_input: dict) -> str:
    for key in (
        "subagent_type",
        "subagentType",
        "subagent_type_name",
        "subagentTypeName",
        "agent_type",
        "agentType",
        "name",
    ):
        agent_name = _extract_subagent_name(tool_input.get(key))
        if agent_name:
            return agent_name
    return ""


def _parse_hook_input(input_data: dict) -> tuple[str, str, dict]:
    """Parse hook input across different platform formats.

    Returns (subagent_type, original_prompt, tool_input).
    Handles:
    - Claude Code / Qoder / CodeBuddy / Droid: tool_name=Task|Agent, tool_input.subagent_type
    - Cursor: tool_name=Task|Subagent, tool_input.subagent_type
    - Copilot CLI: toolName=task (camelCase key, lowercase value)
    - Gemini CLI: tool_name IS the agent name (BeforeTool matcher already filtered)
    - Kiro: agentSpawn hook, agent_name field at top level
    """
    tool_input = input_data.get("tool_input", {})

    # Standard format: Task/Agent tool with subagent_type
    tool_name = input_data.get("tool_name", "") or input_data.get("toolName", "")
    if tool_name.lower() in ("task", "agent", "subagent"):
        return (
            _extract_subagent_type(tool_input),
            tool_input.get("prompt", ""),
            tool_input,
        )

    # Kiro: agentSpawn hook passes agent_name at top level
    agent_name = input_data.get("agent_name", "")
    if agent_name:
        return agent_name, tool_input.get("prompt", input_data.get("prompt", "")), tool_input

    # Gemini CLI: BeforeTool where tool_name IS the agent name
    # (matcher already ensured it's one of our agents)
    if tool_name in AGENTS_ALL:
        return tool_name, tool_input.get("prompt", ""), tool_input

    # Copilot CLI: toolName field (camelCase), value might be the agent name
    tool_name_camel = input_data.get("toolName", "")
    if tool_name_camel in AGENTS_ALL:
        return tool_name_camel, input_data.get("toolArgs", ""), tool_input

    return "", "", tool_input


def main():
    if os.environ.get("TRELLIS_HOOKS") == "0" or os.environ.get("TRELLIS_DISABLE_HOOKS") == "1":
        sys.exit(0)

    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    subagent_type, original_prompt, tool_input = _parse_hook_input(input_data)
    cwd = input_data.get("cwd", os.getcwd())

    # Only handle subagent types we care about
    if subagent_type not in AGENTS_ALL:
        sys.exit(0)

    # Find repo root
    repo_root = find_repo_root(cwd)
    if not repo_root:
        sys.exit(0)

    # Get current task directory (research doesn't require it)
    task_dir = get_current_task(repo_root, input_data)

    # implement/check need task directory
    if subagent_type in AGENTS_REQUIRE_TASK:
        if not task_dir:
            sys.exit(0)
        # Check if task directory exists
        task_dir_full = os.path.join(repo_root, task_dir)
        if not os.path.exists(task_dir_full):
            sys.exit(0)

    # Check for [finish] marker in prompt (check agent with finish context)
    is_finish_phase = "[finish]" in original_prompt.lower()

    # Get context and build prompt based on subagent type
    if subagent_type == AGENT_IMPLEMENT:
        assert task_dir is not None  # validated above
        context = get_implement_context(repo_root, task_dir)
        new_prompt = build_implement_prompt(original_prompt, context)
    elif subagent_type == AGENT_CHECK:
        assert task_dir is not None  # validated above
        if is_finish_phase:
            # Finish phase: use finish context (lighter, focused on final verification)
            context = get_finish_context(repo_root, task_dir)
            new_prompt = build_finish_prompt(original_prompt, context)
        else:
            # Regular check phase: use check context (full specs for self-fix loop)
            context = get_check_context(repo_root, task_dir)
            new_prompt = build_check_prompt(original_prompt, context)
    elif subagent_type == AGENT_RESEARCH:
        # Research can work without task directory
        context = get_research_context(repo_root, task_dir)
        new_prompt = build_research_prompt(original_prompt, context)
    else:
        sys.exit(0)

    if not context:
        sys.exit(0)

    # Return updated input — use a multi-format output that covers all platforms.
    # Most platforms ignore unrecognized fields, so we include multiple formats.
    # The platform picks whichever fields it understands.
    updated = {**tool_input, "prompt": new_prompt}
    output = {
        # Claude Code / Qoder / CodeBuddy / Droid format
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": updated,
        },
        # Cursor format
        "permission": "allow",
        "updated_input": updated,
        # Gemini format
        "updatedInput": updated,
    }

    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
