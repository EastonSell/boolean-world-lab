# Boolean World Lab

An auditable **reference** implementation of fair-bit Boolean worlds:
compile an explicit event circuit parsimoniously to width-at-most-3 CNF,
count accepted worlds, compute exact event probabilities, and sample exactly
from the conditional distribution using integer-rank self-reduction.

**Resolved claim:** the compiler preserves counts with N=n+g variables and
at most 4g+1 clauses; rank unranking is a bijection to accepted inputs.
[Proof, assumptions, counterexamples and asymptotic boundary](docs/PROOF.md).
This is a verified small-instance application of known techniques, **not a new
counting theorem or a practical subexponential solver**. The external theorem
is distinguished from its manuscript refinements in [SOURCES](docs/SOURCES.md).

## Run (Python 3.10+, no dependencies)
```sh
python -m unittest discover -s tests -v
python evaluate.py
```
The complete deterministic readout is [results/evaluation.json](results/evaluation.json).
The [protocol](docs/PROTOCOL.md) was committed before implementation/evaluation.

```python
from boolean_world import World, all_true
w = World(all_true(8))
assert w.count() == 1
assert str(w.probability()) == '1/256'
assert w.sample() == (True,) * 8
print(w.cnf.dimacs())
```

## Boundaries
- Inputs must be independent fair bits. Outputs are deterministic acyclic gates.
- All declared input bits count, including unused ones. Gate auxiliaries do not
  enter the probability denominator.
- Impossible evidence raises `ImpossibleEvent`; no fallback samples are invented.
- The counter is exponential Python reference code: only small instances.
  Deep formulas can hit Python's recursion limit; this is not a scalable solver API.
- Exactness is a distributional statement under a uniform integer RNG;
  `random.Random(seed)` is useful for tests, not cryptographic or physical randomness.
- No empirical speedup, physical-world universality, or theorem novelty is claimed.
- Quantum amplitude/sign cancellation is a distinct problem, not represented here.

## Repeated-sampling comparison
The [preregistered full-grid comparison](docs/COMPARISON_PROTOCOL.md) now compares
cached count-guided sampling, direct enumeration, and capped rejection.
[Results and limits](docs/COMPARISON_RESULTS.md) include all 405 method rows,
partial outputs and failures; [the elementary amortization proof](docs/AMORTIZATION.md)
accounts for repeat-query reuse without treating an exact counter as free.
Run `python compare.py` (standard library only). This is a reference comparison,
not a runtime-speedup claim or the external subexponential counting algorithm.

## Cache occupancy analysis

[Sharp occupancy bounds and variable-order limitations](research/cache-occupancy/PUBLICATION.md)
extend the uncompressed-cache analysis. Exact finite checks, original and amended
evidence, and provenance are retained; literature novelty is unestablished.
