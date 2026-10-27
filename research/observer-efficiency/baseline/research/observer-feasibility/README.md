# Bounded observer-world feasibility study

An isolated, dependency-free extension of Boolean World Lab. A two-bit world
and memory-bearing feedback observer run for 2, 4, 6 or 8 ticks. We compare
independent forward tape enumeration with parsimonious Boolean compilation,
exact counting, and exhaustive conditional-rank decoding.

**Results:** all 16 predeclared cases completed; exact counts and complete
transcript multiplicities agreed in 16/16; all four impossible events raised
`ImpossibleEvent`. Nine unit/regression tests pass. The suite took 51.97 seconds;
maximum case wall time was 32.69 seconds, within 60 seconds/case and enforced
512 MiB address-space limits. One process ran at a time. These are single-run,
host-specific measurements, not stable performance estimates.

The method was **not faster** than forward execution here. For the 8-tick
unrestricted case, exact-count contracts took 0.000373 seconds forward versus
0.03027 seconds compile/count; complete transcript-multiset contracts took
0.001790 seconds forward versus 32.601 seconds compile/count/unrank/replay.
The latter made 5,121 actual count calls. Peak process RSS was 17,664 KiB,
distinct from the virtual-address-space cap. CPU: AMD EPYC 9V74 80-Core Processor.

## Reproduce

```sh
python -m unittest discover -s tests -v
python run_study.py
```

The runner checks the frozen protocol hash and launches each case in a fresh,
budget-limited process. Re-running overwrites `results/study.json`; preserve a
copy if comparing independent runs. No dependencies, installs or paid resources.

- `docs/PROTOCOL.md` and `docs/PROTOCOL.sha256`: frozen cases and acceptance rules.
- `docs/PROTOCOL-AMENDMENT-1.md`: timing disclosure; original
  protocol wording overstates pre-implementation freeze. The small development
  tests preceded freezing; the 16-case evaluation followed it.
- `results/study.json`: every case, full exact transcript maps, fractions,
  count calls, timings, limits and host metadata.
- `results/source-hashes.json`: explicitly post-execution source snapshot.
- `tdd-red.log`, `tdd-green.log`: initial missing-feature failures and final tests.

The rare all-observations-true events have prior probabilities 1/4, 1/16, 1/64,
and 1/256. Conditioned generation does not make these events typical under the
original prior. The unused input bit preserves multiplicity; gate auxiliaries
never enter the prior denominator.

## What this establishes—and does not

This establishes exact bounded emulation of this specified finite observer's
transcripts. “Observer” denotes a sensing/memory/feedback program, not a claim
of consciousness. It establishes neither physical-universe simulability nor
that reality is simulated. It does not prove P=NP, independently verify an ETH
result, implement a fast asymptotic algorithm, or demonstrate quantum simulation.
The provided Boolean counter is an exponential reference implementation.

All transcript preimages in this suite have size exactly two, solely because
of the unused input bit, and event counts have simple closed forms. It is not
a difficult inference benchmark or a test of unequal transcript multiplicities.
See `docs/FEASIBILITY.md` for the literature, general elementary equivalence
proof, host-resource accounting, quantum follow-on design and evidential limits;
`docs/REVIEW.md` records independent verification and remaining limitations.
