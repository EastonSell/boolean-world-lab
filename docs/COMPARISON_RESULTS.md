# Results: exact sampling is not free, and rejection can fail to finish

## What was established
The frozen 135-cell comparison produced **all 405 method rows**, with no
invariant failures. Ten unit tests passed. The original five tests are retained;
five new tests check literal accounting by hand, every prefix of small worlds,
exhaustive rank bijections, repeated-cache reuse, and boundary cases.

Both exact methods completed **108/108 possible-event batches** and identified
**27/27 impossible-event batches**. Capped rejection completed **96/108**
possible-event batches; it exhausted its 4,096-proposal budget in the other 12,
and in all 27 impossible-event batches. An exhausted rejection budget is NOT
an impossibility certificate. The requested denominator was 3,645 samples for
EACH method, including 729 requests under impossible evidence. Conditional and
enumeration produced 2,916 samples each; rejection produced 2,529, retaining
partial outputs in every capped row. No cell or failure was dropped.

## All-row work totals (setup included)

| Method | Complete / impossible / capped batches | Outputs / requested | Measured work |
|---|---:|---:|---|
| Cached conditional | 108 / 27 / 0 | 2,916 / 3,645 | 6,993 count calls; 849,731 recursive visits; 25,546,130 literal inspections |
| Direct enumeration | 108 / 27 / 0 | 2,916 / 3,645 | 196,560 input evaluations; 922,752 gate evaluations |
| Rejection | 96 / 0 / 39 | 2,529 / 3,645 | 176,853 input evaluations; 682,480 gate evaluations; 1,536,948 generated input bits |

These operation types are **not equivalent**. The table does not establish a
runtime ranking. Exact count calls hide substantial work; the raw file includes
clause scans, empty-clause checks, restriction calls and compilation literals.
All methods start fresh in each cell; this includes setup repeated across seeds
and batch sizes. Validation/oracle checking outside a baseline is not charged to
its work counters; enumeration's full enumeration is charged to that baseline.
Sample tuple hashes, not a histogram-based claim of exact randomness, accompany
each row. Returned samples were checked individually against circuit evaluation.

## Rare-event results — every seed and batch size
All-true evidence accepts exactly one of 2**n inputs. Each entry below lists
rejection outputs for seeds 0,1,2; every requested batch and seed is shown.

| n | Requested per seed | Returned per seed | Completed batches / 3 |
|---:|---:|---|---:|
| 4 | 1 | 1, 1, 1 | 3 |
| 4 | 16 | 16, 16, 16 | 3 |
| 4 | 64 | 64, 64, 64 | 3 |
| 8 | 1 | 1, 1, 1 | 3 |
| 8 | 16 | 16, 11, 16 | 2 |
| 8 | 64 | 18, 11, 19 | 0 |
| 12 | 1 | 0, 0, 1 | 1 |
| 12 | 16 | 0, 0, 2 | 0 |
| 12 | 64 | 0, 0, 2 | 0 |

Both exact methods returned the full requested batch in all 27 all-true cells.
All certain, first-bit and parity batches completed under all three methods.
All impossible batches had zero outputs under every method. These statements
cover the entire grid, not a favorable subset.

At n=12, K=64, rejection's **uncapped expected** proposal count is 262,144,
whereas the experiment caps at 4,096. This analytic expectation is not the
observed capped count. Cached conditional uses 13 count calls for every one of
these singleton-evidence batches, independent of seed: one root and twelve
cached zero-child counts. The measured calls still cost 38,016 literal
inspections per cell. Direct enumeration evaluates 4,096 inputs and 45,056 gates
per cell, then reuses its one accepted tuple. These numbers illustrate the
tradeoff, not a common-unit speedup.

## Counterweight: moderate-probability evidence
For n=12 parity, K=64, seed=0, cached counting used 392 count calls and
3,883,388 literal inspections; direct enumeration evaluated 4,096 inputs and
45,056 gates; rejection completed after 118 input evaluations and 1,298 gates.
Parity has probability 1/2. Thus rarity alone is not the whole story, and
count-guided sampling is not automatically the practical choice. This row is an
illustration; all parity rows remain in the raw results. No runtime claim follows
from contrasting literal inspections with gates.

## Mathematical result and limits
The elementary [cache theorem](AMORTIZATION.md) gives at most
**1+min(Kn,2**n−1)** count calls for K samples, or one call for impossible evidence.
It preserves exactness under ideal uniform ranks, and exposes both query cost
and storage rather than treating an exact counter as free. This is an auditable
extension of known self-reduction, not a novel counting-complexity result.
The sampler stores prefix tuples, while enumeration stores accepted tuples;
these are storage proxies, not measured bytes. Python allocation, PRNG internal
work and much bookkeeping are excluded. There is no wall-time benchmark or
asymptotic empirical validation here. Seeded PRNG results do not prove ideal
independence. This code does not implement OpenAI's external counting algorithm.

## Reproduce and provenance
```sh
python -m unittest discover -s tests -v
python -m py_compile boolean_world.py comparison.py compare.py
python compare.py
```
- Protocol committed before implementation: `995c9d8`.
- Implementation committed before evaluation: `a9ac2829b02c10335b7a3f9463fe56e5467ba2a4`.
- Protocol SHA-256: `8a9e4065c03d8db9ea85a1894f01878b5756917bc6a68bcaacf136e60ff50e56`.
- Runtime: Python 3.12.14, standard library only.
- Machine-readable data: [comparison.json](../results/comparison.json), including
  exact source hashes, every method/cell, all denominators, statuses and work.
- The runner records validation exceptions and exits nonzero; no failed cell can
  silently produce a successful complete report.
- Re-execution at a later documentation commit changes only the recorded source
  commit provenance; compare `rows`, summaries and source hashes for reproduction.

This report and the code require independent review before publication.
