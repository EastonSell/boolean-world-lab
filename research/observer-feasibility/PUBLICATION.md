# Publication provenance and limits

This is an additive, independently reviewed snapshot of a local bounded
observer-world feasibility study, published on 2026-10-27. Original package
files are retained byte-for-byte and listed in SOURCE_SHA256.json.

Read the original protocol together with docs/PROTOCOL-AMENDMENT-1.md: the
protocol preceded the 16-case evaluation but not initial implementation or
small development tests. This is not pre-implementation preregistration or
independently public preregistration. The source-hash snapshot was collected
after execution. No historical commits or stronger attestation are invented.

All 16 predeclared cases are retained, including four impossible events.
The independent review found no correctness blocker and records nine new tests
and five unchanged upstream tests. Publication additionally checks the current
repository's full eleven-test baseline suite and the nine new tests.

## Negative performance result

For the original 8-tick unrestricted case, the same complete transcript-multiset
contract took about 32.60 seconds for compile/count/unrank/replay versus
0.00179 seconds for forward enumeration. The method was not faster here.
These are one-run, host-specific measurements, not portable performance
estimates, deployment comparisons, or extrapolations to realistic worlds.
All transcript preimages have multiplicity two and event counts have simple
closed forms; this is not a difficult inference benchmark.

The observer is a memory/feedback program, not a claim of consciousness.
The study is neither evidence that actual reality is simulated nor a result
about arbitrary physical-universe simulation. No novelty or practical speedup
is claimed.

## Safe reproduction

The retained runner overwrites results/study.json. Preserve the original by
copying this directory elsewhere before running it; do not run it in the
retained evidence directory if you want to keep the original measurements.
The publication verifier reran in a separate temporary copy and compared
exact scientific outputs, not timing or host metadata.
