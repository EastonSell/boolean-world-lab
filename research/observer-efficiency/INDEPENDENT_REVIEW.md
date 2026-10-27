# Independent review — 2026-10-27

Verdict: no correctness or reporting blocker found for the narrow, descriptive prefix-reuse result. This is not evidence of a new counting algorithm or superiority to forward simulation.

Reviewed frozen PROTOCOL.md, cached_world.py, evaluate_reuse.py, test_cached.py, baseline World/CNF/observer implementation, completed results, summary and README. No evaluator or frozen implementation was edited. Independent checks ran after timed evaluation completed.

## Checks performed

- Recomputed all four FREEZE.json SHA-256 digests: match. Recomputed Git blob SHA-1 for all 57 retained baseline files: match verified base manifest.
- Confirmed prefix cache uses exact false-child completion counts and immutable circuit/CNF data; original lexicographic recurrence and invalid/impossible-rank behavior are retained. Root solve is included in candidate initialization, count-contract and multiset-contract timing, and actual solve accounting.
- Independently rebuilt accepted tapes and complete transcript Counters with forward execution for all 16 cases. All 48 method rows match exact counts, denominators, support and complete maps. All 48 distinct planned method-cells completed; no failures/timeouts are omitted.
- For every original/candidate row, checked actual solve formula, including impossible probe. Candidate solves equal one plus distinct visited proper prefixes; entries and tuple-key slots equal independently reconstructed prefix statistics. Requests equal solves plus hits. Rank requests and replay ticks match accepted tape count.
- All eight impossible-method probes report ImpossibleEvent. Every recorded cell wall time is below 60 seconds; suite wall time is 71.826 seconds against 600 seconds. Recorded peak RSS is below 512 MiB; separately, runner enforces a 512 MiB address-space cap (RSS is not a substitute for that cap).
- After completion, reran T=4 terminal_memory_true in fresh children for forward, original and cached. Exact maps, counts, denominators and all work counters reproduced. This is a selected-cell reproduction, not an independent full timing rerun.

## Interpretation and caveats

Multiset contracts are matched: candidate includes compile/count/all ranks/replay/Counter work; forward enumerates the full prior including the unused bit. Forward's separately timed count pass is not charged to its multiset pass, appropriately because the latter independently constructs all multiplicities and thereby supplies its count. The original and cached methods incur a Counted proxy call per measured CNF request; this instrumentation overhead is not separately estimated. Timing is one repetition per cell, host-specific and descriptive only. Root counting occurs during cached construction and must not be omitted by comparing initialization components incorrectly.

The cache-size number is a shallow unique-object accounting estimate, not incremental RSS or a complete allocator measurement. Work counters are selected algorithmic units, not machine instructions or recursive solver visit totals. All these limitations are documented. The cached method remains far slower than forward execution at T=8 unrestricted despite reducing original CNF calls from 5121 to 512.
