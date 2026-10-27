# Measured result: prefix reuse removes repeated counting, but forward remains faster

48/48 method-cells completed; all 16/16 counts and complete transcript-multiset maps match; all 8/8 impossible-event probes raised ImpossibleEvent. No evaluation errors, timeouts or skipped cells. Total wall time: 71.826 s, maximum method-process wall: 43.046 s, maximum process RSS: 17,792 KiB. The 512 MiB address-space limit was enforced separately.

**Primary T=8 unrestricted contract:** original 42.967516 s → cached 0.958916 s, a **44.81× reduction** on this run. Contemporaneous independent forward took 0.00207139 s: cached remains **462.93× slower**. Historical 32.601 s versus 0.001790 s remains retained, not overwritten or pooled. Count-only times were 0.0376093 s original, 0.0349371 s cached, 0.000765373 s forward; reuse is primarily an exhaustive-rank benefit, not a major initial-count improvement.

512/512 accepted tape assignments produce 256 transcripts with multiplicity 2 each. Input prior has 9 bits (denominator 512), compiled CNF has 35 variables, 26 gates, 99 clauses, 291 literal occurrences. Original made 5,121 actual count calls; cached made 512. Both replayed 512 ranks × 8 ticks = 4,096 ticks. Cached held 511 proper prefixes, 3,586 tuple slots; owned shallow cache-object estimate 67,892 bytes. Whole-process peak RSS was 14,720 KiB cached versus 17,792 KiB original and 13,184 KiB forward; these are not isolated allocator/cache measurements.

## All predefined cases

| T | Event | Accepted/prior | Forward multiset s | Original s | Cached s | Original/cached | Cached/forward |
|---|---|---:|---:|---:|---:|---:|---:|
| 2 | none | 8/8 | 0.0000091 | 0.0077942 | 0.0030172 | 2.58 | 329.97 |
| 2 | terminal_memory_true | 4/8 | 0.0000091 | 0.0125011 | 0.0020989 | 5.96 | 230.04 |
| 2 | all_observations_true | 2/8 | 0.0000106 | 0.0025866 | 0.0044301 | 0.58 | 416.52 |
| 2 | impossible | 0/8 | 0.0000061 | 0.0002347 | 0.0002464 | 0.95 | 40.07 |
| 4 | none | 32/32 | 0.0000284 | 0.1857668 | 0.0169019 | 10.99 | 595.28 |
| 4 | terminal_memory_true | 16/32 | 0.0000276 | 0.0938001 | 0.0172019 | 5.45 | 622.54 |
| 4 | all_observations_true | 2/32 | 0.0000322 | 0.0199058 | 0.0060087 | 3.31 | 186.84 |
| 4 | impossible | 0/32 | 0.0000170 | 0.0070214 | 0.0027238 | 2.58 | 160.55 |
| 6 | none | 128/128 | 0.0001296 | 2.5080588 | 0.1697056 | 14.78 | 1309.10 |
| 6 | terminal_memory_true | 64/128 | 0.0001148 | 1.2503031 | 0.1145573 | 10.91 | 998.30 |
| 6 | all_observations_true | 2/128 | 0.0001894 | 0.0796207 | 0.0301402 | 2.64 | 159.11 |
| 6 | impossible | 0/128 | 0.0001660 | 0.0117538 | 0.0100217 | 1.17 | 60.37 |
| 8 | none | 512/512 | 0.0020714 | 42.9675156 | 0.9589160 | 44.81 | 462.93 |
| 8 | terminal_memory_true | 256/512 | 0.0023447 | 17.5491867 | 0.7116404 | 24.66 | 303.51 |
| 8 | all_observations_true | 2/512 | 0.0009975 | 0.4751407 | 0.1316881 | 3.61 | 132.02 |
| 8 | impossible | 0/512 | 0.0005242 | 0.0300198 | 0.0322701 | 0.93 | 61.57 |

One observation per method-cell. No confidence intervals, crossover claim, or claim of beating forward. This deliberately simple benchmark is not representative of hard inference; cache storage and exhaustive output remain exponential. Work units are CNF calls and explicit compile/replay/cache units, not a complete instruction-level census. See README.md and PROTOCOL.md for exact exclusions and proof.
