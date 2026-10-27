# Publication provenance

This additive snapshot was published after independent review on 2026-10-27.
The retained README and protocol describe their original local-draft status.
The protocol was locally frozen before evaluation according to the local work
record; it was not independently publicly preregistered. This directory had no
Git history, and this publication does not invent protocol or evaluation commits.

All original package files are preserved byte-for-byte; SOURCE_SHA256.json
records their hashes. The original v1 evidence, reporting-only v2 amendment,
v2 evidence and both deliberately injected reporting failures are retained.
The baseline comparison file differs from repository comparison.py at 23fc37a
only by one trailing blank line; boolean_world.py is byte-identical.

Independent review accepted the exact expectation, simultaneous lexicographic
and bit-reversal extrema, and linear-factor ratio of expected cache occupancies.
These are findings for this uncompressed prefix cache, not practical speedups,
new sampling algorithms, or established literature novelty.

The independent reviewer reproduced v1 in full and checked v2 provenance and
fault reporting; the publication verifier also reran v2 in full.
No failed scientific cases were omitted. Intentional reporting fault artifacts
are tests of error handling, not scientific counterexamples.

To reproduce without overwriting retained evidence:

```sh
cd research/cache-occupancy
python check_occupancy.py /tmp/occupancy-verification.json
```

The v2 script SHA-256 is
`d04345f1f36a68a1bca1d2001dabf1ac974043ca1d101ba1794f8fd52f7d075a`.
