# Resolved conjecture: resource-preserving conditional Boolean worlds

**Status:** proved here by an elementary mathematical argument, with executable
finite checks; not a Lean formalization and not a claim of a new theorem.
The conjecture is the conjunction H1–H3 frozen in PROTOCOL.md. This artifact's
contribution is a precise, auditable implementation and its boundary conditions.

## Statement
Let C be an acyclic circuit with n independent uniform input bits, g gates,
and one event-output wire. Each gate is AND, OR, XOR (fan-in two), NOT (fan-in
one), or a Boolean constant. All gates and inputs are explicitly represented.
There is a CNF F with N=n+g declared variables, at most 4g+1 clauses of width
**at most** 3, and a bijection between the accepted n-bit worlds and models of F.
Consequently P(event)=#F/2^n. For #F>0, exact conditional uniform generation
requires one initial count and at most n prefix counts plus a uniform integer
rank in [0,#F). The included sampler makes one redundant initial count via
unrank, hence n+2 actual count calls; the mathematical procedure needs n+1.
When #F=0 conditional generation is undefined and must fail explicitly.

## Proof of parsimonious compilation
Introduce one variable for each gate output. For z=AND(a,b), use
(-z OR a), (-z OR b), (z OR -a OR -b). For OR, reverse the roles by
(z OR -a), (z OR -b), (-z OR a OR b). For NOT use (z OR a),
(-z OR -a). For XOR use (a OR b OR -z), (-a OR -b OR -z),
(a OR -b OR z), (-a OR b OR z). A constant uses the unit clause z or -z.
Each group is equivalent to its gate equality by its truth table; this remains
true for repeated input references. Assert the event output with one unit clause.

Fix an input assignment. Topological order determines each gate value uniquely.
The resulting extension satisfies all gate clauses. Conversely any satisfying
extension must have precisely those values by induction through the gate order.
It survives the final clause if and only if the event is true. Thus projection
onto input variables is a bijection, including when input bits are unused.
There are N variables and at most four clauses per gate plus one output clause.
Literal-index encoding costs O((n+g+1) log(n+g+2)) bits, not necessarily linear
bit length. This is a linear *variable/clause* reduction. The syntax requires
at least one wire; n=0 is supported by constant-containing circuits.

## Proof of counting and unranking
A fixed prefix partitions accepted worlds into the disjoint next-bit-zero and
next-bit-one sets, with sizes c0 and c1. A rank r in [0,c0+c1) selects bit zero
and retains r if r<c0; otherwise it selects bit one and replaces r by r-c0.
Inductively r remains a valid rank within the selected prefix. After n steps,
each accepted input has exactly one rank, in lexicographic order, and every rank
produces an accepted input. Therefore a uniform integer rank gives exactly
probability 1/#F to each accepted world. No floating-point probability or rounded
branch decision is used. A uniform rank can be drawn with rejection from ceil(log2
#F) fair bits, with fewer than two trials in expectation (and zero bits for #F=1).
This is exact distributional sampling in expected time, not worst-case bounded
random-bit consumption. Seeded Python PRNG runs are reproducible diagnostics;
mathematical exactness assumes an ideal uniform integer source.

The reference counter branches on an unfixed occurring variable, summing its
two disjoint cases. An empty clause yields zero. No remaining clauses means
all remaining declared variables are free, yielding 2^remaining. These base cases
and induction prove its exactness, including free variables and inconsistent
prefixes. It is still an exponential reference algorithm.

## Conditional asymptotic consequence, not implemented here
Using the external exact-counting theorem described in SOURCES.md, the encoding
and O(n) prefix counts imply subexponential time in **N=n+g**, up to polynomial
encoding factors, and polynomial space for counting, exact event probabilities,
and expected-time conditional sampling. Prefix conditions add at most n unit
clauses, so total clauses are <=4g+1+n<=4N+1. For N>=1 this is <=5N, a fixed
sparsity constant. All formulas remain width at most three. For a canonical
encoding, duplicate clauses/literals can be removed and tautologies dropped
while retaining the declared variable universe. No fresh unconstrained padding
variables are permitted. Unit/binary clauses are allowed in width-at-most-3 CNF.

The formal-scope bound transfers with exponent O(N(log log N)^2/sqrt(log N));
the sharper manuscript's sparse bound would transfer with O(N/sqrt(log N)).
These are asymptotic statements for sufficiently large N. They do not imply
subexponential time in n alone for arbitrary g, and do not provide usable
constants or demonstrate a practical speedup. Source validation and the theorem
itself are external dependencies; our tiny Python tests do not establish them.

## False tempting variants, with witnesses
1. **Divide by 2^N:** n=1 and z=NOT(x), event z, gives #F=1, N=2.
   Correct event probability is 1/2, not 1/4. Auxiliary variables are not randomness.
2. **One-way gate constraints preserve counts:** n=1, z=AND(x,x), event x.
   Keeping only z=>x and asserting x admits two extensions (z=false/true)
   instead of the single extension z=true required by gate equality.
3. **Ignore unused inputs:** event x1 among eight fair bits accepts 128 worlds,
   not one. Its denominator is 256. Projection without multiplicity changes counts.
4. **Condition on zero probability:** FALSE event has zero count, hence no
   probability distribution proportional to accepted-world indicators exists.
