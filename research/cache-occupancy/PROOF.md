# Sharp cache occupancy envelope (research note; novelty unestablished)

Fix n>=0, nonempty S subset {0,1}^n, M=|S|, and K>=0 independent uniform draws with replacement. The cache has no eviction: for every visited parent prefix of length d<n it stores exactly one zero-child count. It does not skip deterministic branches, free suffixes or already known singleton models. Let C be its final number of entries. The initial total count is separate, hence total oracle calls Q=1+C. The cost of an oracle call, cache key storage, output writing and randomness are not bounded by Q.

## Exact instance formula
For a prefix u, let m_u be the number of words of S extending it. Its cache entry appears iff at least one draw extends u. For K>0 the probability is f(m_u), where f(t)=1-(1-t/M)^K. For K=0 define f(t)=0. Indicator linearity gives

E[C] = sum_{d=0}^{n-1} sum_{u in {0,1}^d} f(m_u).

No independence of prefix indicators is asserted or needed. This occupancy identity is standard, not a novelty claim.

## Globally sharp fixed-(n,M,K) bounds
For each d put b=2^d and L=2^(n-d), q=floor(M/L), r=M-qL, a=floor(M/b), and s=M-ab. Then

sum_{d<n} [q*f(L)+f(r)] <= E[C] <= sum_{d<n} [(b-s)*f(a)+s*f(a+1)].

Terms with a zero coefficient are omitted (so f(L) need never be evaluated when L>M and q=0). Both bounds are simultaneously attained at every depth by explicit single accepted sets: the lower by S_low={binary_n(j):0<=j<M}, and the upper by S_high={reverse(binary_n(j)):0<=j<M}.

### Proof
For K=0 the conclusion is immediate; K=1 gives f(t)=t/M and each level contributes exactly one. For K>=2, f is increasing and concave on [0,M]; equivalently its increments f(t+1)-f(t) are nonincreasing for integer t. At depth d the count vector has b integer entries, sum M, each in [0,L]. Moving one unit from a larger positive entry to a smaller entry whose difference is at least two cannot decrease the sum of f. Repeating terminates at counts a or a+1, with s of the latter: the stated maximum. Conversely, moving one unit from a smaller nonzero entry to a larger not-full entry cannot increase that sum. Repeating terminates at q full entries L and at most one residual r: the minimum. These arguments apply on the feasible interval [0,min(L,M)].

Levelwise inequalities alone would not prove simultaneous attainability, since neighboring levels must agree under binary refinement. For S_low, prefixes partition integer interval [0,2^n) into consecutive blocks of length L. Initial segment [0,M) fills q blocks completely and one block by r, at every depth. For S_high, its d-bit prefixes correspond bijectively to residues of j modulo b=2^d (bit reversal only permutes their names). Residue classes among integers 0..M-1 have sizes a or a+1, with exactly s larger classes, at every depth. Thus each construction obeys all binary-refinement constraints and attains the sum of its levelwise extrema. This proves global sharpness, not just separately feasible depth bounds.

n=0 yields an empty sum and one initial count. M=1 yields C=n for K>0; K=0 yields C=0. M=0 has no conditional law and is outside these formulas; the implementation rejects it after its root count.

## Linear-factor variable-order separation
Let m>=1, n=2m, M=K=2^m. Consider S_A=0^m{0,1}^m and S_B={0,1}^m0^m, obtained from one another solely by reversing variable order. The two displayed sets are not identical as labeled subsets; they represent the same constraint pattern after a coordinate permutation (or the same event read in two variable orders). Both are conjunctions fixing m bits, with identical gate counts after renaming. Define

T_m=sum_{j=0}^{m-1} 2^j [1-(1-2^(-j))^M],
D_m=M[1-(1-1/M)^M].

The exact expectations are E[C_A]=m+T_m and E[C_B]=T_m+m*D_m. In A, depths 0..m-1 contribute m and depths m..2m-1 contribute T_m. In B, depths 0..m-1 contribute T_m and each of the remaining m depths contributes D_m. These are the preceding global lower and upper extremizers for this M.

Since D_m >= (1-exp(-1))*M and T_m<=M-1, E[C_B]/E[C_A] >= (1-exp(-1))*m*M/(m+M-1) >= (1-exp(-1))*m/2. Also the j=m-1 term gives T_m >= (M/2)*(1-exp(-2)); therefore E[C_B]/E[C_A] <= (m+1)*M / [(M/2)*(1-exp(-2))] = O(m). The ratio is Theta(m)=Theta(n). Thus acceptance probability, input count, model count and gate count do not determine even the expected prefix-count call burden within a constant factor uniformly in n.

This is a limitation/counterexample for this uncompressed prefix cache, not a speedup claim. Detecting forced bits, reusing subproblems, compressed tries, d-DNNF compilation or component caching may erase this example. In particular, no lower bound on all exact samplers follows. Output writing alone takes Theta(nK) bits, which can dominate either oracle-count budget. No assertion about time crossover against rejection, SPUR, KUS or other production methods is supported.

## Differentiation and open novelty
The extension beyond baseline AMORTIZATION.md is an exact instance statistic, explicit globally sharp finite-parameter envelopes, and a variable-order counterexample with fixed support and circuit size. Occupancy linearity, concavity, bit reversal and cached sampling are established ideas. Their combination here is a proved application, not yet established as a novel theorem. Independent review and a more complete literature search are required before representing it as research novelty.
