import fs from "node:fs";
import path from "node:path";
import { getProjectRoot, loadTerms } from "./term-data.mjs";
import { renderHtml } from "./render-template.mjs";

const projectRoot = getProjectRoot();
const outputRoot = path.join(projectRoot, "generated_html");
const terms = loadTerms();

if (terms.length === 0) {
  throw new Error("No terms found. Add content/*.json first.");
}

fs.mkdirSync(outputRoot, { recursive: true });
for (const term of terms) {
  const dir = path.join(outputRoot, term.id);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, "index.html"), renderHtml(term));
}

console.log(`Generated ${terms.length} HTML compositions in ${outputRoot}`);
