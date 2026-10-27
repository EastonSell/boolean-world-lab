# Post-evaluation robustness amendment

Independent review found that the runner built summary counter names from its
last successful sampler. If every cell failed before sampler creation, this
would raise UnboundLocalError instead of saving the planned failure artifact.
This does not affect the original run (all 135 cells succeeded), whose frozen
results/comparison.json and comparison-console.json remain byte-for-byte intact.

The amendment derives summary names from the Work schema directly, adds a test
forcing all 135 cells to fail, and allows a separate output filename so a
verification rerun cannot overwrite the original preregistered result. This is
a reporting robustness fix, not a changed hypothesis, grid, sampler, accounting
rule or analysis. The amended verification is saved separately in
results/comparison-amended.json and is compared with original rows and summaries.

Verification: all 405 method rows, summaries and validation results reproduced
exactly; both original evidence files match commit 1175960 byte-for-byte.
All 11 tests pass, including the new forced-total-failure regression; compilation
passes. The amended runner source was frozen at e18b260 before its verification
rerun. Independent re-review is required before publication.
