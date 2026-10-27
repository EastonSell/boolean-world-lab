# Independent review and verification

A separate read-only agent inspected protocol, chronology amendment,
mathematical discussion, implementation, tests and raw study output.

- Independently ran `python -m unittest discover -s tests -v`: 9/9 passed.
- Verified all 16 unique predeclared horizon/event pairs retained.
- Verified closed-form accepted counts: unrestricted 2^(T+1), terminal memory
  true 2^T, all observations true 2, impossible 0.
- Verified every realized transcript has multiplicity 2 (unused input), and
  support size K/2; all reference and generated maps agree.
- Verified actual count-call totals: 1+K*(n+1), plus one impossible-event
  sample check when K=0.
- Protocol checksum matched; total wall 51.971430s; maximum process wall
  32.685016s; maximum reported RSS 17664 KiB. No correctness blocker found.
- Minor review fixes requested: place direct-run unittest entry point after
  all test classes; collect source hashes and CPU model in separate provenance
  metadata. The latter is post-run provenance, not a claim of prior source
  preregistration.

Parent study agent also ran the unchanged upstream Boolean World Lab suite:
5/5 tests passed. Those tests run against the original source copy, whose hash
matches the copied boolean_world.py noted in protocol.

Timings are one descriptive run, not statistical performance estimates.
The bounded pass is not a scalability result. In particular T=8 unrestricted
had forward full-support enumeration 0.001789636s versus count/unrank/replay
32.601429s, with both methods producing the same complete multiset contract.

Additional limitation: all supported transcripts in this chosen model have
multiplicity exactly two, solely from the unused input. It does not exercise
nonuniform transcript multiplicities, and its event counts have simple closed
forms. A later separately preregistered study should include partial/noisy
observations or many-to-one observation maps with unequal preimage counts,
as well as richer interventions. This suite is a tiny exactness/budget demo,
not a difficult inference benchmark.
