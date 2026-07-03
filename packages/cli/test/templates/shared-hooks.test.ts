import { describe, expect, it } from "vitest";
import {
  SHARED_HOOKS_BY_PLATFORM,
  getSharedHookScripts,
  getSharedHookScriptsForPlatform,
  type SharedHookPlatform,
} from "../../src/templates/shared-hooks/index.js";

const ALL_HOOK_FILES = [
  "session-start.py",
  "inject-shell-session-context.py",
  "inject-workflow-state.py",
  "inject-subagent-context.py",
] as const;

describe("shared-hooks capability table", () => {
  it("every capability-table entry names a real shared-hook file", () => {
    const realFiles = new Set(getSharedHookScripts().map((h) => h.name));
    for (const [platform, hooks] of Object.entries(
      SHARED_HOOKS_BY_PLATFORM,
    )) {
      for (const hook of hooks) {
        expect(
          realFiles.has(hook),
          `${platform} declares ${hook} but no such file exists under shared-hooks/`,
        ).toBe(true);
      }
    }
  });

  it("every shared-hook file is distributed to at least one platform", () => {
    const distributed = new Set<string>();
    for (const hooks of Object.values(SHARED_HOOKS_BY_PLATFORM)) {
      for (const h of hooks) distributed.add(h);
    }
    for (const hook of getSharedHookScripts()) {
      expect(
        distributed.has(hook.name),
        `${hook.name} exists under shared-hooks/ but no platform installs it — dead template`,
      ).toBe(true);
    }
  });

  it("statusline.py is not distributed by default", () => {
    const realFiles = new Set(getSharedHookScripts().map((h) => h.name));
    expect(realFiles.has("statusline.py")).toBe(false);
    for (const [platform, hooks] of Object.entries(
      SHARED_HOOKS_BY_PLATFORM,
    )) {
      expect(
        (hooks as readonly string[]).includes("statusline.py"),
        `${platform} must not install the generated statusline.py hook by default`,
      ).toBe(false);
    }
  });

  it("inject-subagent-context.py is restricted to class-1 push-based platforms", () => {
    // Class-2 (pull-based) platforms load context via agent-definition prelude,
    // not a hook-mutated prompt.
    const class2 = new Set(["codex", "copilot", "gemini", "qoder", "trae"]);
    for (const [platform, hooks] of Object.entries(
      SHARED_HOOKS_BY_PLATFORM,
    )) {
      const has = hooks.includes("inject-subagent-context.py");
      if (class2.has(platform))
        expect(
          has,
          `${platform} is class-2 pull-based and must not ship inject-subagent-context.py`,
        ).toBe(false);
    }
  });

  it("codex + copilot do not take the shared session-start.py (they bundle their own)", () => {
    expect(SHARED_HOOKS_BY_PLATFORM.codex).not.toContain("session-start.py");
    expect(SHARED_HOOKS_BY_PLATFORM.copilot).not.toContain("session-start.py");
  });

  it("inject-shell-session-context.py goes to Cursor only", () => {
    for (const [platform, hooks] of Object.entries(
      SHARED_HOOKS_BY_PLATFORM,
    )) {
      const has = hooks.includes("inject-shell-session-context.py");
      if (platform === "cursor") expect(has).toBe(true);
      else
        expect(
          has,
          `${platform} declares inject-shell-session-context.py but does not use Cursor beforeShellExecution`,
        ).toBe(false);
    }
  });

  it("kiro registers session-start, workflow-state, and subagent-context hooks", () => {
    // Kiro wires per-turn + spawn hooks on both surfaces (CLI agent
    // userPromptSubmit/agentSpawn + IDE .kiro.hook promptSubmit), so it ships
    // the same trio as other agent-capable push-based platforms.
    expect([...SHARED_HOOKS_BY_PLATFORM.kiro].sort()).toEqual(
      [
        "inject-subagent-context.py",
        "inject-workflow-state.py",
        "session-start.py",
      ].sort(),
    );
  });

  it("getSharedHookScriptsForPlatform returns exactly the declared set per platform", () => {
    for (const platform of Object.keys(
      SHARED_HOOKS_BY_PLATFORM,
    ) as SharedHookPlatform[]) {
      const names = getSharedHookScriptsForPlatform(platform)
        .map((h) => h.name)
        .sort();
      const expected = [...SHARED_HOOKS_BY_PLATFORM[platform]].sort();
      expect(names).toEqual(expected);
    }
  });

  it("shared-hooks directory only contains files enumerated by ALL_HOOK_FILES", () => {
    // Guards against a new shared hook being added without the capability
    // table being updated.
    const actual = new Set(getSharedHookScripts().map((h) => h.name));
    const expected = new Set(ALL_HOOK_FILES);
    expect(actual).toEqual(expected);
  });

  it("shared hooks do not read legacy .current-task state", () => {
    for (const hook of getSharedHookScripts()) {
      expect(
        hook.content,
        `${hook.name} must use the session-scoped active task resolver`,
      ).not.toContain(".current-task");
      expect(hook.content).not.toContain("global fallback");
    }
  });

  it("shared session-start.py injects compact task artifact guidance", () => {
    const sessionStart = getSharedHookScripts().find(
      (h) => h.name === "session-start.py",
    );
    expect(sessionStart, "session-start.py is missing from shared-hooks/").toBeDefined();
    const content = sessionStart ? sessionStart.content : "";
    expect(content).toContain("<trellis-workflow>");
    expect(content).toContain("Task context order");
    expect(content).toContain("jsonl entries -> `prd.md`");
    expect(content).toContain("Lightweight task can request start review with PRD-only");
    expect(content).toContain("complex task must add");
    expect(content).not.toContain("Status: READY");
    expect(content).not.toContain("<workflow>");
  });

  it("shared session-start.py reflects no-task consent and legacy completed-state discipline", () => {
    const sessionStart = getSharedHookScripts().find(
      (h) => h.name === "session-start.py",
    );
    expect(sessionStart, "session-start.py is missing from shared-hooks/").toBeDefined();
    const content = sessionStart ? sessionStart.content : "";
    expect(content).toContain("No-task direct work is explicit opt-in only");
    expect(content).toContain("consent question is blocking");
    expect(content).toContain("Status: LEGACY COMPLETED");
    expect(content).toContain("legacy completed task state");
    expect(content).not.toContain("Status: COMPLETED\\n");
  });

  it("shared sub-agent hook prompts mirror disciplined implement/check/research contracts", () => {
    const subagentHook = getSharedHookScripts().find(
      (h) => h.name === "inject-subagent-context.py",
    );
    expect(
      subagentHook,
      "inject-subagent-context.py is missing from shared-hooks/",
    ).toBeDefined();
    const content = subagentHook ? subagentHook.content : "";

    expect(content).toContain("No implementation code before failing proof");
    expect(content).toContain("If you wrote implementation before proof, delete it and start over");
    expect(content).toContain("route back to the main session for `trellis-debug`");
    expect(content).toContain("Status must be exactly one of: DONE, DONE_WITH_CONCERNS, BLOCKED, NEEDS_CONTEXT");

    expect(content).toContain("Reviewer/Fixer Boundary");
    expect(content).toContain("Mechanical issues only");
    expect(content).toContain("Do not self-fix behavior, design, test strategy, requirement mismatches, or implementation logic");
    expect(content).toContain("return those findings to the main session so it can dispatch `trellis-implement`");
    expect(content).toContain("Completion Claim Gate");
    expect(content).toContain("Review Gate");

    expect(content).toContain("Every research output MUST end up as a file under");
    expect(content).toContain("{{TASK_DIR}}/research/");
    expect(content).toContain("If no active task is set, ask the user where to write output");
    expect(content).toContain("Use the platform-exposed structural tool");

    expect(content).not.toContain("Fix issues yourself, don't just report");
    expect(content).not.toContain("Fix issues directly, don't just report");
    expect(content).not.toContain("find and explain information");
    expect(content).not.toContain("mcp__exa__web_search_exa");
  });
});
