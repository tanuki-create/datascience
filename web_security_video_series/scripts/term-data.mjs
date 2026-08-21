import fs from "node:fs";
import path from "node:path";

const projectRoot = path.resolve(new URL("..", import.meta.url).pathname);
const contentDir = path.join(projectRoot, "content");

export function getProjectRoot() {
  return projectRoot;
}

export function loadTerms() {
  if (!fs.existsSync(contentDir)) {
    return [];
  }

  const files = fs
    .readdirSync(contentDir)
    .filter((file) => file.endsWith(".json"))
    .sort();

  const terms = [];
  for (const file of files) {
    const fullPath = path.join(contentDir, file);
    const parsed = JSON.parse(fs.readFileSync(fullPath, "utf8"));
    const records = Array.isArray(parsed) ? parsed : parsed.terms;
    if (!Array.isArray(records)) {
      throw new Error(`${file} must contain an array or { "terms": [] }`);
    }
    for (const record of records) {
      terms.push({ ...record, sourceFile: file });
    }
  }

  const seen = new Set();
  return terms.map((term, index) => {
    const id = term.id || slugify(term.term || `term-${index + 1}`);
    if (seen.has(id)) {
      throw new Error(`Duplicate term id: ${id}`);
    }
    seen.add(id);
    return normalizeTerm({ ...term, id });
  });
}

export function findTerm(id) {
  const terms = loadTerms();
  return terms.find((term) => term.id === id);
}

export function normalizeTerm(term) {
  const visualBeats = Array.isArray(term.visual_beats) ? term.visual_beats : [];
  return {
    id: term.id,
    chapter: term.chapter || "Web Security",
    term: term.term || term.id,
    expanded: term.expanded || "",
    origin: term.origin || "",
    lower_layer: term.lower_layer || "",
    hook: term.hook || `${term.term || term.id}はどの境界が壊れる話？`,
    narration: term.narration || "",
    visual_beats: visualBeats.map((beat) =>
      typeof beat === "string"
        ? { text: beat, visual: beat }
        : {
            text: beat.text || beat.screen_text || beat.title || "",
            visual: beat.visual || beat.visual_idea || beat.diagram || beat.idea || "",
          },
    ),
    key_takeaway: term.key_takeaway || "",
    keywords: Array.isArray(term.keywords) ? term.keywords : [],
    duration: Number(term.duration || 22),
    sourceFile: term.sourceFile,
  };
}

export function slugify(value) {
  return String(value)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function validateTerm(term) {
  const required = [
    "id",
    "chapter",
    "term",
    "origin",
    "lower_layer",
    "hook",
    "narration",
    "key_takeaway",
  ];
  const missing = required.filter((field) => !String(term[field] || "").trim());
  const problems = [];
  if (missing.length > 0) {
    problems.push(`missing: ${missing.join(", ")}`);
  }
  if (term.visual_beats.length < 3) {
    problems.push("visual_beats must have at least 3 items");
  }
  return problems;
}
