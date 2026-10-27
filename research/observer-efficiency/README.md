# Observer prefix-count reuse: a large overhead reduction, not a fast simulator

This isolated follow-on starts from **fbee23a9de99eedcf116320445241debec5bd835**. All 57 baseline files were checked against GitHub Git-blob hashes; original source, historical failures, protocols and results remain untouched in `baseline/`.

The targeted change reuses the exact root count and each visited prefix's false-child count across rank requests. This is the already-known caching principle in the repository's `comparison.py`, applied to the observer study; it is not a new solver. `PROTOCOL.md` gives the proof, hypotheses, fixed cases, timing contracts, budgets and limitations, frozen with source hashes in `FREEZE.json` before evaluation.

## Scope and accounting

The contract is **complete accepted transcript multiset with exact multiplicity**, over all T+1 fair input bits. It is not merely one sample, or merely a count. Timings include compilation, initial count, cache construction, all rank decoding, forward replay and Counter construction. No cross-case reuse. Count-only contracts are reported separately. The redundant unused input bit remains in the probability denominator; deterministic gate auxiliaries do not.

Each of 16 cases runs three methods in fresh processes, serially: 48 planned method-cells. One repetition only: timings are host-specific descriptive observations, not a statistical performance estimate. Original/candidate order alternates by case; this does not eliminate machine-load effects. Candidate initialization performs the root count internally, so its initialization time includes counting; use `count_contract_s` and `multiset_contract_s` for valid comparisons, not initialization alone.

Work counters report actual CNF solves, cache requests/hits/entries/key slots, rank requests, forward tape enumerations/replay ticks, and compiled clauses/literals. These are explicit work units, **not exhaustive machine-instruction counts**; recursive CNF visits/literal scans are not instrumented. Peak RSS covers the whole child process (Python/CNF/output/cache), not incremental cache cost. The object-size estimate covers owned cache containers/keys/integers, not allocator/process overhead. Wall and CPU times and the 512 MiB virtual-address-space cap are separately recorded.

## Reproduce without overwriting evidence

Run `python -m unittest test_cached -v`. To reproduce the full evaluation, copy this directory elsewhere, keep baseline and FREEZE.json intact, and remove **only that new copy's** `results.jsonl` and `summary.json` before `python evaluate_reuse.py`. Existing output is refused, rather than overwritten. Do not run the historical baseline runner inside retained baseline evidence.

`results.jsonl` preserves all outcomes; `summary.json` reports all fixed denominators. `tdd-red.log` retains the missing-feature failure, `tdd-green.log` the new passing tests; `baseline-tests.log` and `observer-tests.log` record inherited test suites.

## Limits

Caching reduces repeated work but can use exponential memory; reference CNF counting remains exponential. Exhaustive output remains exponential in input bits. This benchmark's transcript multiplicities are uniformly two and its event counts have simple closed forms, so it is not difficult-inference evidence. No claim about consciousness, universe simulation, quantum simulation, P=NP, external ETH proof verification or implementation of the external asymptotic algorithm. No installations, paid resources, merges or publication were performed. Independent review is required before publication.
