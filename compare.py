"""Execute the frozen full-grid protocol; never discard failed cells."""
import hashlib
import json
from collections import Counter
from dataclasses import asdict
from fractions import Fraction
from itertools import product
from pathlib import Path
import platform
import random
import subprocess
from comparison import CachedSampler, enumerate_sample, rejection_sample, family_circuit

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

def run():
    rows, errors = [], []
    for n, family, k, seed in product((4,8,12), ('certain','impossible','first_bit','all_true','parity'), (1,16,64), (0,1,2)):
        base = dict(n=n, family=family, requested=k, seed=seed)
        try:
            circuit = family_circuit(n, family)
            # Enumeration baseline doubles as independent oracle. Its FULL cost is reported.
            enum_samples, enum_work, count = enumerate_sample(circuit, k, seed)
            cnf = circuit.compile()
            base.update(g=len(circuit.gates), N=cnf.n_variables, clauses=len(cnf.clauses),
                        accepted_worlds=count, denominator=2**n,
                        expected_uncapped_rejection_proposals=str(Fraction(k*2**n, count)) if count else None)
            sampler = CachedSampler(circuit)
            assert sampler.total == count, 'count/oracle disagreement'
            rng = random.Random(seed)
            conditional = [sampler.sample(rng) for _ in range(k)] if count else []
            assert conditional == enum_samples, 'seeded rank/index disagreement'
            assert len(sampler.cache) <= min(k*n, 2**n-1), 'cache bound violated'
            assert sampler.work.count_calls == 1+len(sampler.cache), 'count work omitted'
            rejected, rejection_work = rejection_sample(circuit, k, seed)
            methods = [('conditional', conditional, sampler.work, len(sampler.cache), 0),
                       ('enumeration', enum_samples, enum_work, 0, count),
                       ('rejection', rejected, rejection_work, 0, 0)]
            for name, samples, work, cache_size, accepted_storage in methods:
                assert all(circuit.evaluate(x) for x in samples), 'invalid sample'
                status = ('complete' if len(samples) == k else
                          'budget_exhausted' if name == 'rejection' else 'impossible')
                rows.append(dict(base, method=name, status=status, produced=len(samples),
                                 work=asdict(work), cache_entries=cache_size,
                                 accepted_tuples_stored=accepted_storage,
                                 sample_sha256=hashlib.sha256(json.dumps(samples).encode()).hexdigest()))
        except Exception as exc:
            errors.append(dict(base, exception=type(exc).__name__, message=str(exc)))
    summaries = {}
    for method in ('conditional', 'enumeration', 'rejection'):
        subset = [r for r in rows if r['method'] == method]
        summaries[method] = dict(rows=len(subset), statuses=dict(Counter(r['status'] for r in subset)),
            requested=sum(r['requested'] for r in subset), produced=sum(r['produced'] for r in subset),
            work_totals={key:sum(r['work'][key] for r in subset) for key in asdict(sampler.work)})
    output = dict(protocol_commit='995c9d8', protocol_sha256=sha('docs/COMPARISON_PROTOCOL.md'),
        source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        source_hashes={p:sha(p) for p in ('boolean_world.py','comparison.py','compare.py','tests/test_comparison.py')},
        python=platform.python_version(), planned_cells=135, planned_method_rows=405,
        completed_cells=135-len(errors), validation_errors=errors, summaries=summaries, rows=rows)
    (ROOT/'results/comparison.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('rows','source_hashes')},indent=2))
    if errors or len(rows) != 405:
        raise SystemExit('Comparison failed; full errors retained in results/comparison.json')

if __name__ == '__main__': run()
