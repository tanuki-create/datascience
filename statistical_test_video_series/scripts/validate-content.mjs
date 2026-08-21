import { loadTerms, validateTerm } from "./term-data.mjs";

const terms = loadTerms();
let failed = 0;

for (const term of terms) {
  const problems = validateTerm(term);
  if (problems.length > 0) {
    failed += 1;
    console.error(`${term.id}: ${problems.join("; ")}`);
  }
}

if (failed > 0) {
  throw new Error(`${failed} term records need fixes.`);
}

console.log(`Content OK: ${terms.length} terms`);
