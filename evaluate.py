"""Complete frozen evaluation; write deterministic results to stdout."""
import json
from boolean_world import Circuit,World,all_true

def run():
    cases=[(f'all_true_{n}',all_true(n)) for n in range(1,9)]
    cases += [('impossible',Circuit(8,(('FALSE',()),),9)),('certain',Circuit(8,(('TRUE',()),),9)),('unused_bits',Circuit(8,(),1))]
    rows=[]
    for name,c in cases:
        w=World(c); count=w.count(); oracle=len(w.exhaustive_inputs())
        row=dict(case=name,input_bits=c.n_inputs,gates=len(c.gates),cnf_variables=w.cnf.n_variables,clauses=len(w.cnf.clauses),count=count,denominator=2**c.n_inputs,oracle_count=oracle,agrees=count==oracle,probability=str(w.probability()))
        rows.append(row)
    assert all(r['agrees'] for r in rows)
    return {'purpose':'correctness only; no asymptotic or speedup evidence','rows':rows,'all_agree':True}

if __name__ == '__main__': print(json.dumps(run(),indent=2)+'\n',end='')
