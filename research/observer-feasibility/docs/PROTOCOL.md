# Bounded observer-world protocol v1

Frozen before new implementation or evaluation, 2026-10-27 UTC. This is an
isolated extension of Boolean World Lab, not a new public repository. Copied
boolean_world.py SHA256: 33d4ee6eb34c68df30f310856a4537e297e8a284de05c75620c2a55f5e2fa3fc.
No empirical outcomes informed these hypotheses. Freeze this file's SHA256 in
results before evaluation; any later change is a labeled amendment.

## Question and limits
Can a host reproduce the complete observable histories of a specified finite
world by count-conditioned generation as well as by forward execution, within
an explicitly bounded budget? This tests a finite computational construction,
not conscious observers, physical realism, universal simulation efficiency,
P=NP, the external ETH result, or whether reality is simulated.

## Fixed miniature world
For horizon T in {2,4,6,8}, a tape has n=T+1 independent fair bits. The last bit
is deliberately unused but retains multiplicity. Start x=0,m=0. For t=0..T-1:
  x_new = x XOR u[t] XOR m
  m_new = m XOR x_new
  log (x_new,m_new); replace x,m with x_new,m_new.
An observer here means this explicit memory-bearing, sensing, feedback-capable
finite-state component; no inference about consciousness is licensed. Its
memory affects the next world state, not merely a passive transcript.
Events: unrestricted; terminal m=1; every logged x=1; impossible (FALSE).
The 4 horizons x 4 events give exactly 16 predeclared cases; retain all cases.
The event circuit unrolls the same transitions with gate equalities. No
auxiliary variable contributes to the prior denominator 2^(T+1).

## Hypotheses, outputs and baselines
H1: The reference CNF count equals independent direct tape enumeration for
all 16 cases. Report exact numerator, denominator, fraction, nonzero support
size of transcripts, and tape multiplicity per transcript.
H2: Enumerating every integer conditional rank, decoding the tape and replaying
it gives exactly the same transcript multiplicity map as forward enumeration
restricted to the event. This finite exhaustive test does not rely on a PRNG
or an empirical histogram passing a weak statistical test.
H3: The impossible event has count zero and explicit ImpossibleEvent rather
than a fabricated sample. Conditional probability on it is undefined.
H4 (budgeted engineering claim): Each case completes within 60 wall seconds
and 512 MiB address-space limit, whole study within 10 minutes, on one existing
CPU process per case. Record overruns and exceptions as failed/unfinished
cases, never delete them or change limits to call the original claim passed.

Two matched contracts: (A) exact event count/probability, comparing brute-force
forward enumeration against compile plus exact count; (B) complete conditional
transcript multiset, comparing forward enumeration with filtering against
compile/count plus all-rank unranking and replay. This is deliberately NOT a
comparison of one forward sample against a global count, nor a speedup claim.
Record compilation, count, all-rank generation/replay and baseline durations
separately, plus end-to-end totals. State caching policy and repetitions;
single-run timings are descriptive, not stable performance estimates.
Report n, gates g, N=n+g, clauses, actual count-call totals if instrumented,
host CPU/platform/Python, limits, process peak RSS and its platform units.
Distinguish observed peak RSS from enforced virtual-address-space limit.

## Acceptance and failure
H1-H3 require exact integer/multiset equality for every completed case, with
16/16 explicit denominator. One mismatch fails that hypothesis. H4 fails
if any limit is exceeded; a timeout is not evidence that the world is
inconsistent. Diagnostic fixes must retain original failed output and rerun
under the same frozen cases and budget, labeling implementation revisions.
No selection of only favorable horizons, rare events or variable orders.
These tests establish behavior on this suite, not correctness for all worlds.

## Research boundary and next questions
An efficient SAT decision/witness algorithm, even under P=NP, is not a known
replacement for arbitrary exact #SAT or signed counting. An ETH-refuting
subexponential upper bound is not a polynomial-time bound and supplies no
usable small constants by itself. Count-conditioned generation changes how a
specified distribution is computed, not which physical universe exists.
Rare events must be reported as k/2^n before conditioning; conditioned support
is not a typicality statement. Constraints/event/prior are frozen above.
Only fair-bit priors are implemented; nonuniform priors need weighted counting.
Quantum signed paths require separate nonnegative Born prefix probabilities
from signed interference sums, not treating negative path weights as chances.
