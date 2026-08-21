import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { getProjectRoot, loadTerms } from "./term-data.mjs";

const projectRoot = getProjectRoot();
const requestedIds = process.argv.slice(2).filter((arg) => !arg.startsWith("--"));
const allTerms = loadTerms();
const selected = requestedIds.length
  ? allTerms.filter((term) => requestedIds.includes(term.id))
  : allTerms;

if (selected.length === 0) {
  throw new Error("No matching terms to render.");
}

fs.mkdirSync(path.join(projectRoot, "renders"), { recursive: true });

const manifest = [];
for (const [index, term] of selected.entries()) {
  console.log(`\n[${index + 1}/${selected.length}] Rendering ${term.id} (${term.term})`);

  const build = spawnSync("node", ["scripts/build-index.mjs", term.id], {
    cwd: projectRoot,
    stdio: "inherit",
  });
  if (build.status !== 0) {
    process.exit(build.status ?? 1);
  }

  const output = path.join("renders", `${term.id}.mp4`);
  const render = spawnSync(
    "npx",
    ["--yes", "hyperframes@0.6.33", "render", "--quality", "draft", "--fps", "30", "--output", output],
    { cwd: projectRoot, stdio: "inherit" },
  );
  if (render.status !== 0) {
    process.exit(render.status ?? 1);
  }

  manifest.push({
    id: term.id,
    term: term.term,
    chapter: term.chapter,
    output: path.join(projectRoot, output),
  });
}

const manifestPath = path.join(projectRoot, "renders", "manifest.json");
fs.writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(`\nRendered ${manifest.length} videos.`);
console.log(`Manifest: ${manifestPath}`);
