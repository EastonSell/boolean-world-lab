# Frozen occupancy protocol v1
Frozen 2026-10-27 before implementation or evaluation. Target baseline: EastonSell/boolean-world-lab 23fc37a, CachedSampler with one zero-child count per visited prefix, no eviction or shortcut. Work is isolated; no publication authorized by this protocol.

## Hypotheses
H1: For nonempty S subset {0,1}^n, M=|S| and K IID uniform samples with replacement, expected cache size is sum over depths d<n and prefixes u of 1-(1-m_u/M)^K. Root count is additional, so expected total count calls is 1+this value, including K=0. Empty event performs one root count and rejects sampling.
H2: At each depth let b=2^d, L=2^(n-d), q,r=divmod(M,L), a,s=divmod(M,b), and f(t)=1-(1-t/M)^K. The sharp lower and upper expected cache bounds are respectively sums of q*f(L)+f(r) and (b-s)*f(a)+s*f(a+1). Interpret f(0)=0 also when K=0. Lexicographically first M words attain every lower term; reversing each word's n bits attains every upper term.
H3: With n=2m, M=K=2^m, fixed-first versus fixed-last blocks have expected-cache ratio Theta(m), despite equal model count, acceptance probability, and gate count under variable renaming.

## Fixed evaluation, denominators, and analysis
1. Exhaustively enumerate every nonempty subset for n=0..4 and K in [0,1,2,3,8]. Check exact Fraction-valued H1 expression lies in H2 bounds; report total instances, failures and all failure witnesses.
2. For n=0..3 every nonempty subset, and K=0..3, enumerate every ordered rank tuple in [0,M)^K, execute baseline CachedSampler.unrank using an independent table prefix counter, and compare exact trace-averaged cache size/count calls against H1. Check returned sequence equals requested lexicographic ranks. Retain all failures; table counter deliberately isolates cache logic and does not test compiler/counter performance.
3. For n=0..8 and M=1..2^n, K in [0,1,2,3,8], check both extremizer constructions attain respective bounds using exact arithmetic.
4. Report illustrative block examples m=1..10 at K=2^m using exact analytic expressions, not simulation or runtime evidence. No hypothesis selection, tuning, p-values, omitted failed seeds, time claims, practical efficacy claims or claim of literature novelty.
5. No Monte Carlo, installs, external jobs or paid compute. Preserve protocol SHA256 in results. Publish only after independent proof/code review. If a computation fails, retain its record and explicitly amend protocol before rerun; never overwrite a failed result.

## Prior art boundary
Occupancy expectations, concavity/majorization, bit reversal, prefix tries, cached counting and exact self-reduction are known techniques. The proposed contribution is the explicit simultaneous extremal envelope and variable-order counterexample for this cache model; literature novelty is UNESTABLISHED. This is not an improved sampling algorithm, runtime guarantee, or result about SPUR/d-DNNF/component caches.
