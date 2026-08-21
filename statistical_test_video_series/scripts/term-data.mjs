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
      terms.push(normalizeTerm({ ...record, sourceFile: file }));
    }
  }

  const seen = new Set();
  for (const term of terms) {
    if (seen.has(term.id)) {
      throw new Error(`Duplicate term id: ${term.id}`);
    }
    seen.add(term.id);
  }

  return terms;
}

export function findTerm(id) {
  return loadTerms().find((term) => term.id === id);
}

export function normalizeTerm(term) {
  const visualBeats = Array.isArray(term.visual_beats) ? term.visual_beats : [];
  const assumptions = Array.isArray(term.assumptions)
    ? term.assumptions
    : String(term.assumptions || "")
        .split(/[、,]/)
        .map((item) => item.trim())
        .filter(Boolean);

  return {
    id: term.id || slugify(term.term || "statistical-test"),
    chapter: term.chapter || "統計検定",
    term: term.term || "",
    short_name: term.short_name || term.term || "",
    hypothesis: normalizeHypothesis(term.hypothesis),
    use_when: term.use_when || "",
    assumptions,
    lower_layer: normalizeLowerLayer(term.lower_layer),
    hook: term.hook || "",
    narration: term.narration || "",
    visual_beats: visualBeats.map((beat) => ({
      text: beat.text || beat.screen_text || beat.title || "",
      visual: beat.visual || beat.diagram || beat.visual_idea || "",
    })),
    key_takeaway: term.key_takeaway || "",
    keywords: Array.isArray(term.keywords) ? term.keywords : [],
    formula: term.formula || "",
    duration: Number(term.duration || 24),
    sourceFile: term.sourceFile,
  };
}

function normalizeHypothesis(value) {
  if (typeof value === "string") {
    return { h0: value, h1: "" };
  }
  return {
    h0: value?.h0 || value?.null || value?.H0 || "",
    h1: value?.h1 || value?.alternative || value?.H1 || "",
  };
}

function normalizeLowerLayer(value) {
  if (!value) {
    return "";
  }
  if (typeof value === "string") {
    return value;
  }
  return [value.one_layer_down, value.mechanism, value.contrast]
    .filter(Boolean)
    .join(" ");
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
    "short_name",
    "use_when",
    "lower_layer",
    "hook",
    "narration",
    "key_takeaway",
    "formula",
  ];
  const problems = [];
  const missing = required.filter((field) => !String(term[field] || "").trim());
  if (missing.length > 0) {
    problems.push(`missing: ${missing.join(", ")}`);
  }
  if (!term.hypothesis.h0) {
    problems.push("hypothesis.h0 is required");
  }
  if (term.assumptions.length === 0) {
    problems.push("assumptions must have at least 1 item");
  }
  if (term.visual_beats.length !== 4) {
    problems.push("visual_beats must have exactly 4 items");
  }
  return problems;
}
