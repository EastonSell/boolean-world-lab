"""Instrumented elementary baselines; not the external subexponential algorithm."""
from dataclasses import dataclass, asdict
from itertools import product
import random
from boolean_world import Circuit, World, ImpossibleEvent, all_true

@dataclass
class Work:
    count_calls: int = 0
    recursive_visits: int = 0
    restriction_calls: int = 0
    clauses_scanned: int = 0
    literal_inspections: int = 0
    empty_clause_checks: int = 0
    evaluated_inputs: int = 0
    evaluated_gates: int = 0
    generated_input_bits: int = 0
    rank_requests: int = 0
    compiled_literals: int = 0

class MeasuredCounter:
    def __init__(self, cnf, work):
        self.cnf, self.work = cnf, work

    def count(self, prefix=()):
        if len(prefix) > self.cnf.n_variables or any(type(x) is not bool for x in prefix):
            raise ValueError('invalid prefix')
        w = self.work
        w.count_calls += 1
        def restrict(cs, variable, value):
            w.restriction_calls += 1
            true_lit = variable if value else -variable
            out = []
            for clause in cs:
                w.clauses_scanned += 1
                satisfied = False
                for literal in clause:
                    w.literal_inspections += 1
                    if literal == true_lit:
                        satisfied = True
                        break
                if not satisfied:
                    remaining = []
                    for literal in clause:
                        w.literal_inspections += 1
                        if literal != -true_lit:
                            remaining.append(literal)
                    out.append(tuple(remaining))
            return tuple(out)
        def visit(cs, remaining):
            w.recursive_visits += 1
            for clause in cs:
                w.empty_clause_checks += 1
                if not clause:
                    return 0
            if not cs:
                return 1 << remaining
            variable = abs(cs[0][0])
            return (visit(restrict(cs, variable, False), remaining-1) +
                    visit(restrict(cs, variable, True), remaining-1))
        cs = self.cnf.clauses
        for variable, value in enumerate(prefix, 1):
            cs = restrict(cs, variable, value)
        return visit(cs, self.cnf.n_variables-len(prefix))

class CachedSampler:
    """Cache one zero-child count per visited parent prefix; include setup work."""
    def __init__(self, circuit):
        self.n = circuit.n_inputs
        self.work = Work()
        cnf = circuit.compile()
        self.work.compiled_literals = sum(map(len, cnf.clauses))
        self.counter = MeasuredCounter(cnf, self.work)
        self.total = self.counter.count()
        self.cache = {}

    def unrank(self, rank):
        if not self.total:
            raise ImpossibleEvent('zero accepted worlds')
        if type(rank) is not int or not 0 <= rank < self.total:
            raise ValueError('invalid rank')
        prefix = ()
        for _ in range(self.n):
            if prefix not in self.cache:
                self.cache[prefix] = self.counter.count(prefix+(False,))
            zero = self.cache[prefix]
            bit = rank >= zero
            if bit:
                rank -= zero
            prefix += (bit,)
        return prefix

    def sample(self, rng):
        if not self.total:
            raise ImpossibleEvent('zero accepted worlds')
        self.work.rank_requests += 1
        return self.unrank(rng.randrange(self.total))

def interpret(circuit, bits, work):
    work.evaluated_inputs += 1
    work.evaluated_gates += len(circuit.gates)
    return circuit.evaluate(bits)

def enumerate_sample(circuit, k, seed):
    work = Work()
    accepted = [bits for bits in product((False, True), repeat=circuit.n_inputs)
                if interpret(circuit, bits, work)]
    rng = random.Random(seed)
    samples = []
    if accepted:
        for _ in range(k):
            work.rank_requests += 1
            samples.append(accepted[rng.randrange(len(accepted))])
    return samples, work, len(accepted)

def rejection_sample(circuit, k, seed, cap=4096):
    work = Work()
    rng = random.Random(seed)
    samples = []
    while len(samples) < k and work.evaluated_inputs < cap:
        bits = tuple(bool(rng.getrandbits(1)) for _ in range(circuit.n_inputs))
        work.generated_input_bits += circuit.n_inputs
        if interpret(circuit, bits, work):
            samples.append(bits)
    return samples, work

def family_circuit(n, family):
    if family in ('certain', 'impossible'):
        return Circuit(n, ((('TRUE' if family == 'certain' else 'FALSE'), ()),), n+1)
    if family == 'first_bit':
        return Circuit(n, (), 1)
    if family == 'all_true':
        return all_true(n)
    if family == 'parity':
        gates, wire = [], 1
        for i in range(2, n+1):
            gates.append(('XOR', (wire, i)))
            wire = n+len(gates)
        return Circuit(n, tuple(gates), wire)
    raise ValueError('unknown family')

