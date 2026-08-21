import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { getProjectRoot } from "./term-data.mjs";

const projectRoot = getProjectRoot();
const termId = process.argv[2] || process.env.TERM_ID;

if (!termId) {
  throw new Error("Usage: npm run render:term -- <term-id>");
}

const build = spawnSync("node", ["scripts/build-index.mjs", termId], {
  cwd: projectRoot,
  stdio: "inherit",
});
if (build.status !== 0) {
  process.exit(build.status ?? 1);
}

fs.mkdirSync(path.join(projectRoot, "renders"), { recursive: true });
const output = path.join("renders", `${termId}.mp4`);
const render = spawnSync(
  "npx",
  ["--yes", "hyperframes@0.6.33", "render", "--quality", "draft", "--fps", "30", "--output", output],
  { cwd: projectRoot, stdio: "inherit" },
);

process.exit(render.status ?? 1);
