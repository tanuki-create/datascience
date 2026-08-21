import fs from "node:fs";
import path from "node:path";
import { findTerm, getProjectRoot, loadTerms } from "./term-data.mjs";
import { renderHtml } from "./render-template.mjs";

const projectRoot = getProjectRoot();
const requestedId = process.argv[2] || process.env.TERM_ID;
const terms = loadTerms();

if (terms.length === 0) {
  throw new Error("No content JSON files found in content/.");
}

const term = requestedId ? findTerm(requestedId) : terms[0];
if (!term) {
  const ids = terms.map((item) => item.id).join(", ");
  throw new Error(`Unknown term id: ${requestedId}. Available: ${ids}`);
}

fs.writeFileSync(path.join(projectRoot, "index.html"), renderHtml(term));
console.log(`Built index.html for ${term.id} (${term.term})`);
