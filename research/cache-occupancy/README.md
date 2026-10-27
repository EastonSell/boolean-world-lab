# Boolean-world cache occupancy research note

Local draft; no publication or literature-priority claim.

**Result:** sharp finite-(n,M,K) lower and upper bounds on expected prefix-cache entries, each attained simultaneously across all depths. The constructions are the first M binary words and their bit reversals. For a simple fixed/free-bit block family, reversing variable order changes expected cache entries by Theta(n) while preserving model count, probability and circuit size. This is a limitation of the baseline's uncompressed cache, not a new sampler or practical speedup.

- `PROOF.md`: statement, proof, scope and asymptotic separation.
- `PROTOCOL.md`: frozen pre-evaluation protocol; SHA256 recorded in results.
- `SOURCES.md`: primary-source inspection and explicit novelty limitations.
- `comparison_baseline.py`: fetched from EastonSell/boolean-world-lab at 23fc37a.
- `check_occupancy.py`: exact Fraction-based exhaustive checker with retained failure/error reporting.
- `check_occupancy_v1.py`: unchanged original checker.
- `AMENDMENT-v2.md`: reporting-only correction after independent review; no hypothesis/population changes.
- `results-v1.json`: original complete results, retained unchanged. Zero failures.
- `results-v2.json`: completed reporting-amended rerun: zero failures, no errors; scientific results exactly identical to v1.
- `fault-assertion.json`, `fault-exception.json`: intentional failures testing failure retention; not failed scientific hypotheses. Both correctly returned process exit 1.

## Original complete denominators
329,045 all-support/K envelope checks; 28,793 ordered-rank output traces through baseline `CachedSampler.unrank`; 1,096 exact trace expectations; 2,555 extremizer constructions; 1 empty-event boundary. No supports, rank traces, seeds or failed cases were dropped. Empty support is not assigned a conditional distribution. No random sampling or performance timing was used.

The baseline sampler is exercised with an independent table counter, deliberately isolating cache logic. These checks do not test its CNF compiler, its recursive counter speed, or production SAT samplers. The proof covers all admissible sizes; finite checks are bug-finding evidence, not the proof.

Run from this directory: `python check_occupancy.py results-new-name.json`. An existing output filename is refused. No dependencies or installs required.
