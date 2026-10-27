# Repeated exact conditional sampling: cost is not just oracle-call count

This is an elementary extension of the original proof, not a new counting
complexity theorem. Let a finite fair-bit circuit have n inputs and M accepted
inputs. Assume an exact counter and an ideal uniform integer random source.

## Cache bound and exactness
For M>0, compute M once. For each requested sample draw a fresh independent
uniform rank in [0,M). During unranking cache the zero-child count by its parent
prefix. Reusing a deterministic exact count cannot change any branch decision,
so the original rank-to-world bijection still gives independent uniform
conditional samples. Independence here is conditional on the fixed circuit;
PRNG seeds are reproducibility diagnostics, not an ideal-randomness proof.

Across K samples, at most Kn parent-prefix visits occur. The full binary tree
has 1+2+...+2**(n-1)=2**n-1 internal nodes. Hence the total number of exact count
calls is at most 1+min(Kn,2**n-1), including the initial count. A sharper
instance-dependent bound replaces 2**n-1 by the number of internal prefixes
having an accepted descendant; the sampler visits only these. For M=1 only n
such prefixes can be visited regardless of K. For n=0 the cache is empty and a
successful sample is the empty tuple. For M=0 the root count suffices to report
undefined conditioning; no conditional sample exists.

These bounds do NOT count the cost of solving a count query. The reference
counter can take exponential work for a single query. Memoization also uses
storage: Python stores a prefix tuple and a count per entry, not one free bit.

## Competing costs
For rejection, each independent proposal succeeds with p=M/2**n. For M>0,
linearity of expectation over K geometric waiting times gives E[T]=K/p.
For M=0 no finite expected completion time exists. A cap B returns a full batch
exactly when Binomial(B,p)>=K; discarding failures selects a different reported
population. The benchmark includes every capped failure and partial output.

Direct enumeration evaluates all 2**n inputs once, stores M accepted tuples,
and draws uniform indices for repeated requests. It is also exact. This can be
preferable on small instances and must not be hidden behind an oracle-only
label. Reference conditional counting, enumeration and rejection operate on
different primitives: clause/literal scans and gate evaluations are reported
separately. No universal runtime crossover follows from oracle-call counts or
this finite benchmark. The comparison does not implement the externally cited
subexponential counting algorithm.
