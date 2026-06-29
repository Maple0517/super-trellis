import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, "../../../..");

function read(relativePath: string): string {
  return fs.readFileSync(path.join(repoRoot, relativePath), "utf-8");
}

describe("disciplined Trellis runtime templates", () => {
  const markers: Array<[string, string]> = [
    ["packages/cli/src/templates/common/skills/before-dev.md", "NO IMPLEMENTATION CODE BEFORE FAILING PROOF"],
    ["packages/cli/src/templates/common/skills/before-dev.md", "Why Order Matters"],
    ["packages/cli/src/templates/common/skills/debug.md", "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"],
    ["packages/cli/src/templates/common/skills/debug.md", "Post-Fix Handoff"],
    ["packages/cli/src/templates/common/skills/check.md", "Completion Claim Gate"],
    ["packages/cli/src/templates/common/skills/check.md", "Milestone Handoff"],
    ["packages/cli/src/templates/common/skills/check.md", "Review Gate"],
    ["packages/cli/src/templates/common/skills/check.md", "Not sufficient"],
    ["packages/cli/src/templates/common/skills/check.md", "Rationalization prevention"],
    ["packages/cli/src/templates/common/skills/check.md", "Correction: my earlier pushback"],
    ["packages/cli/src/templates/common/skills/brainstorm.md", "Visual Companion"],
    ["packages/cli/src/templates/common/skills/brainstorm.md", "Planning Quality Bar"],
    ["packages/cli/src/templates/common/skills/brainstorm.md", "PRD / Spec Self-Review"],
    ["packages/cli/src/templates/common/skills/visual-companion.md", "Trellis Visual Companion"],
    ["packages/cli/src/templates/common/skills/visual-companion.md", "Runnable Fallback"],
    ["packages/cli/src/templates/common/skills/visual-companion.md", "python3 -m http.server 8765"],
    ["packages/cli/src/templates/markdown/spec/guides/debugging-guide.md.txt", "waitForCondition"],
    ["packages/cli/src/templates/markdown/spec/guides/debugging-guide.md.txt", "Polluter Search"],
    ["packages/cli/src/templates/markdown/spec/guides/testing-guide.md.txt", "keeps retrying until a transient operation succeeds"],
    ["packages/cli/src/templates/markdown/spec/guides/testing-guide.md.txt", "New public behavior or risky boundary"],
    ["packages/cli/src/templates/markdown/spec/guides/superpowers-verification-scenarios.md.txt", "Audit-only"],
    ["packages/cli/src/templates/trellis/workflow.md", "trellis-before-dev"],
    ["packages/cli/src/templates/trellis/workflow.md", "trellis-debug"],
    ["packages/cli/src/templates/trellis/workflow.md", "After `trellis-debug` proves the local fix"],
    ["packages/cli/src/templates/trellis/workflow.md", "Milestone Handoff Discipline"],
    ["packages/cli/src/templates/trellis/workflow.md", "No active task after commit"],
    ["packages/cli/src/templates/trellis/workflow.md", "Completion Claim Gate"],
    ["packages/cli/src/templates/trellis/workflow.md", "Review feedback"],
    ["packages/cli/src/templates/trellis/agents/implement.md", "Implementer Status Protocol"],
    ["packages/cli/src/templates/trellis/agents/implement.md", "DONE_WITH_CONCERNS"],
    ["packages/cli/src/templates/trellis/agents/check.md", "Two-Stage Review Protocol"],
    ["packages/cli/src/templates/trellis/agents/check.md", "Run review in two stages"],
    ["packages/cli/src/templates/codex/agents/trellis-implement.toml", "No implementation code before failing proof"],
    ["packages/cli/src/templates/codex/agents/trellis-implement.toml", "multi_agent = false"],
    ["packages/cli/src/templates/codex/agents/trellis-check.toml", "Verify TDD evidence existed before implementation"],
    ["packages/cli/src/templates/codex/agents/trellis-check.toml", "enabled = false"],
    ["packages/cli/src/templates/claude/agents/trellis-implement.md", "No implementation code before failing proof"],
    ["packages/cli/src/templates/claude/agents/trellis-check.md", "Verify proof existed before implementation"],
    ["packages/cli/src/templates/common/bundled-skills/trellis-channel/SKILL.md", "Copyable Worker Prompt Template"],
    ["packages/cli/src/templates/common/commands/finish-work.md", "Final handoff"],
    ["packages/cli/src/templates/markdown/spec/guides/debugging-guide.md.txt", "POLLUTER_CANDIDATE"],
  ];

  for (const [file, marker] of markers) {
    it(`${file} contains ${marker}`, () => {
      expect(read(file)).toContain(marker);
    });
  }
});
