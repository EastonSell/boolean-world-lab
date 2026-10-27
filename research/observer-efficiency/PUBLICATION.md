# Publication provenance and interpretation

Published as an additive snapshot after independent review on 2026-10-27.
The reviewed archive SHA-256 is
`dc4e23b1962fb013ea6ef699f00c60b1d85b165806020a5072cf7a7ebc644bf1`.
Its files are preserved unchanged; MANIFEST.sha256.json verifies the original
package, including all 57 baseline files from fbee23a. Retained README wording
about no publication describes its pre-publication state.

FREEZE.json records a local pre-evaluation source/protocol freeze. It is not an
independently public preregistration. Prior negative results and existing cache
code informed this targeted engineering change; no blind-discovery claim is made.
This snapshot does not fabricate historical commits or alter original evidence.

All 48 method-cells and 16 exact-map comparisons are retained, including eight
impossible probes and cases where caching loses. In the original single-run
T=8 unrestricted full-multiset comparison, original 42.967516 s became cached
0.958916 s, while contemporaneous forward enumeration took 0.00207139 s.
The approximately 44.81x reduction does not mean the cache beats forward: it
remained approximately 462.93x slower in that observation. Timings are one-shot,
host-specific measurements, not statistical or deployment performance estimates.

This reuses a known prefix-count caching principle. It is not an implementation
of the external ETH algorithm, a new solver, or evidence about actual reality
being simulated. Counting, cache storage, and exhaustive output remain
worst-case exponential; see PROTOCOL.md and RESULTS.md for accounting caveats.

Use the README reproduction instructions on a separate copy to retain original
results. The publication verifier reran all 48 method-cells in a separate copy
and compared scientific outputs/work counters, without pooling timings.
