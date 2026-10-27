# Frozen conditional-sampling comparison — 2026-10-27

This protocol is frozen before implementing or evaluating this comparison.
It extends (does not replace) the original correctness protocol. It is an
engineering study of elementary reference algorithms, not an implementation,
validation, or claimed speedup of the external OpenAI counting theorem.

## Questions and fixed design
H1: Memoizing zero-child counts across rank-unranking requests preserves the
exact conditional distribution and reduces repeated count requests. For K
requests with n inputs it needs one root count and at most
min(K*n, 2**n-1) distinct zero-child counts. Impossible evidence needs only the
root count and returns failure. This counts oracle calls, NOT oracle cost.
H2: Rare evidence increases rejection demand: for M>0 accepted worlds out of
2**n, uncapped rejection needs K*2**n/M proposals in expectation. Fixed-budget
failure must not be silently dropped. Enumerating all 2**n inputs is a competing
baseline with reusable accepted-world storage, not merely a correctness oracle.
No hypothesis that conditional counting is faster is preregistered.

Full Cartesian grid: n in {4,8,12}; family in {certain,impossible,first_bit,
all_true,parity}; requested K in {1,16,64}; seed in {0,1,2}: 135 cells, each with
all three methods. Parity means XOR of all inputs. Certain/impossible use one
constant gate; first_bit declares n inputs and no gates; all_true uses the
existing constructor. All cells appear, including impossible/capped failures.

Conditional: one fresh instance/cache per cell, cached root count, count the
zero-child subtree once per encountered parent prefix, draw uniform integer
ranks with Python Random(seed). No solver optimization beyond memoization.
Enumeration: independently interpret every input, store accepted tuples, then
select uniform list indices. Include all setup cost, even for K=1.
Rejection: independent Random(seed), generate n fair PRNG bits per proposal,
evaluate circuit, accept up to K, hard cap 4096 proposals per cell. Do NOT use
the enumeration oracle to shortcut impossible evidence. Partial samples stay
in the result with status budget_exhausted. Finite PRNG tests do not prove exact
sampling; proof assumes ideal uniform randomness.

## Fixed accounting and analysis
Report per cell n,g,N,clause count,M,2**n,K,seed,method,status,produced and all
work counters. CNF work: count calls, recursive visits, restriction calls,
clauses scanned, literal inspections (explicit membership and filtering loops).
Circuit work: evaluated inputs, evaluated gates, generated input bits. Rank
requests and cached-prefix count are separate. Counter setup, including every
root and prefix count, is included. Compilation reports emitted literals; it is
not equated to literal scans or gate evaluations. Do not add unlike operations
into an invented single speed metric. Wall time is not a primary endpoint.
Enumeration accepted-list size and conditional prefix-cache entries are explicit
storage proxies, not byte-accurate peak memory. PRNG internal work, Python tuple
allocations, recursion and bookkeeping are not fully captured; no total runtime
or memory superiority claim is allowed.

Report exact rational uncapped rejection expectation where M>0; undefined for
M=0. Empirical summaries include every cell, exact status counts, proposals and
outputs, and method-specific setup/work totals. Exhaustively verify unranking
bijection on small independent circuits before the comparison; verify every
returned sample satisfies evidence, oracle counts agree, conditional and
enumeration samples match under same seed/index convention, and cache bounds
hold. Any failed invariant or unexpected exception fails the entire run and is
retained as a failure, not excluded. No tuning or selective reruns after results.
Independent review is required before publication. No publication by runner.
