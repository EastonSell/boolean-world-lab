# Source and claim ledger

Reviewed 2026-10-27. This project does not reproduce or independently certify
OpenAI's proof. Known Tseitin gate-equivalence compilation and counting
self-reduction are used, not advertised as novel results.

## Primary source checked directly
https://github.com/openai/math/blob/main/lean/docs/378.md

This repository's formalization-scope note states that for fixed k>=2, exact
counting for canonically encoded k-CNF has time polynomial in encoding length
L times 2^{O_k(n(log log n)^2/sqrt(log n))}, and polynomial tape-space usage.
It separately attributes a sharper general-clause and sparse-clause bound to
the October 25 manuscript. Do not describe the sharper bound as Lean-verified
on the basis of this note. We did not run the Lean build.
The linked comparator is a statement artifact ending in `sorry`, not by itself
a checked proof of the theorem. Our formal-status description reports the
repository scope note, not an independent verification of the proof. Its literal
indices are unary: translating our O(N)-clause formula into that canonical
encoding can cost O(N^2) bits, still polynomial.

## Manuscript location
https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf

The manuscript was also read directly from its downloaded PDF text: Theorem 1.1
(page 2), its immediate self-reduction paragraph, and the introduction's declared-variable convention (page 1). Theorem 1.1 states time (n+m)^{O_k(1)} times
2^{O_k(n log log n/sqrt(log n))} to this manuscript and, for m<=Dn,
(n+m)^{O_{k,D}(1)} times 2^{O_{k,D}(n/sqrt(log n))}.
It permits shorter clauses by repeating literals, without adding variables.
The PDF is a separate source from the formalization scope note. Its complete
proof is not verified by this artifact. None of the Python code implements
these algorithms, and no empirical result here tests these bounds.

## Novelty and applicability
The elementary statements in PROOF.md are standard consequences of local gate
equivalences and rank-based self-reduction. Project-specific deliverables are
the explicit compiler, edge-case semantics, tests, and frozen evaluation.
A generic polynomial reduction would not justify preserving subexponential
complexity in the original instance parameter. We explicitly track N=n+g,
clause count, bit encoding length, and extra prefix clauses instead.
