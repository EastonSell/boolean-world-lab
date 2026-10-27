"""Deterministic exact checks under PROTOCOL.md; no performance benchmark."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib, json, sys, traceback
from comparison_baseline import CachedSampler, Work


def words(n):
    return list(product((False, True), repeat=n))


def occupancy(S, n, K):
    M = len(S)
    if not M:
        raise ValueError('empty event')
    if K == 0:
        return Fraction(0)
    return sum((1 - Fraction(M-c, M)**K for d in range(n)
                for c in Counter(w[:d] for w in S).values()), Fraction(0))


def envelope(n, M, K):
    def f(t):
        return 1-Fraction(M-t, M)**K if K else Fraction(0)
    lo = hi = Fraction(0)
    for d in range(n):
        b, L = 2**d, 2**(n-d)
        q,r = divmod(M,L)
        a,s = divmod(M,b)
        lo += (q*f(L) if q else 0) + f(r)
        hi += (b-s)*f(a) + (s*f(a+1) if s else 0)
    return lo,hi


class TableCounter:
    def __init__(self, S, work):
        self.S, self.work = S, work
    def count(self, prefix=()):
        self.work.count_calls += 1
        return sum(w[:len(prefix)] == prefix for w in self.S)


def make_sampler(n,S):
    obj = CachedSampler.__new__(CachedSampler)
    obj.n, obj.work, obj.cache = n, Work(), {}
    obj.counter = TableCounter(S, obj.work)
    obj.total = obj.counter.count()
    return obj


STATE = {"failures": [], "counts": Counter(), "block_illustrations": []}

def run(inject=None):
    failures=STATE["failures"]
    counts=STATE["counts"]
    def check(ok, kind, witness):
        counts[kind] += 1
        if not ok:
            failures.append({'kind':kind, 'witness':witness})
    if inject == "failure":
        check(False, "injected_failure", ["reporting fault test, not scientific result"])
        return
    if inject == "exception":
        raise RuntimeError("injected reporting exception")
    for n in range(5):
        W=words(n)
        for mask in range(1,2**len(W)):
            S=[w for i,w in enumerate(W) if mask>>i&1]
            for K in [0,1,2,3,8]:
                E=occupancy(S,n,K)
                lo,hi=envelope(n,len(S),K)
                check(lo<=E<=hi,'all_subset_envelope', [n,mask,K,str(lo),str(E),str(hi)])
    for n in range(4):
        W=words(n)
        for mask in range(1,2**len(W)):
            S=[w for i,w in enumerate(W) if mask>>i&1]
            for K in range(4):
                cache_sum=call_sum=trace_count=0
                for ranks in product(range(len(S)),repeat=K):
                    obj=make_sampler(n,S)
                    out=[obj.unrank(r) for r in ranks]
                    check(out == [S[r] for r in ranks], 'trace_outputs', [n,mask,K,ranks])
                    cache_sum += len(obj.cache)
                    call_sum += obj.work.count_calls
                    trace_count += 1
                E=occupancy(S,n,K)
                check(Fraction(cache_sum,trace_count)==E and Fraction(call_sum,trace_count)==1+E,
                      'trace_expectation',[n,mask,K,trace_count,str(E),cache_sum,call_sum])
    for n in range(9):
        W=words(n)
        for M in range(1,len(W)+1):
            S=W[:M]
            R=[w[::-1] for w in S]
            for K in [0,1,2,3,8]:
                lo,hi=envelope(n,M,K)
                check(occupancy(S,n,K)==lo and occupancy(R,n,K)==hi,
                      'extremizer_attainment',[n,M,K])
    illustrations=STATE["block_illustrations"]
    for m in range(1,11):
        M=2**m
        lo,hi=envelope(2*m,M,M)
        illustrations.append({'m':m,'n':2*m,'M':M,'K':M,
            'lower_exact':str(lo),'upper_exact':str(hi),'ratio_float_illustrative':float(hi/lo)})
    obj=make_sampler(0,[])
    try:
        obj.unrank(0)
        empty_rejected=False
    except Exception as exc:
        empty_rejected=type(exc).__name__=='ImpossibleEvent'
    check(empty_rejected and obj.work.count_calls==1,'empty_boundary',[])


def main():
    output = Path(sys.argv[1] if len(sys.argv)>1 else 'results-v2.json')
    # Refuse overwrite before any evaluation, not only when writing at the end.
    if output.exists():
        raise FileExistsError(str(output))
    try:
        run(sys.argv[2] if len(sys.argv)>2 else None)
    except BaseException as exc:
        STATE['error']={'type':type(exc).__name__, 'message':str(exc), 'traceback':traceback.format_exc()}
    result={**STATE,
            'protocol_sha256':hashlib.sha256(Path('PROTOCOL.md').read_bytes()).hexdigest(),
            'amendment_sha256':hashlib.sha256(Path('AMENDMENT-v2.md').read_bytes()).hexdigest(),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'baseline_comparison_sha256':hashlib.sha256(Path('comparison_baseline.py').read_bytes()).hexdigest(),
            'failure_count':len(STATE['failures'])}
    with output.open('x') as stream:
        json.dump(result,stream,indent=2)
        stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='block_illustrations'},indent=2))
    return int(bool(result['failure_count'] or result.get('error')))

if __name__=='__main__':
    sys.exit(main())
