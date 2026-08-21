import { loadTerms } from "./term-data.mjs";

const terms = loadTerms();
for (const term of terms) {
  console.log(`${term.id}\t${term.term}\t${term.chapter}\t${term.sourceFile}`);
}
console.log(`\n${terms.length} terms`);
