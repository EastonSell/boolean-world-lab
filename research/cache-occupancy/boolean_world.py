"""Dependency-free exact reference: explicit fair-bit worlds, not a fast #SAT solver."""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import random

ARITY = {'AND': 2, 'OR': 2, 'XOR': 2, 'NOT': 1, 'TRUE': 0, 'FALSE': 0}

@dataclass(frozen=True)
class Circuit:
    n_inputs: int
    gates: tuple
    output: int

    def __post_init__(self):
        if type(self.n_inputs) is not int or self.n_inputs < 0:
            raise ValueError('n_inputs must be a nonnegative integer')
        object.__setattr__(self, 'gates', tuple((op, tuple(args)) for op, args in self.gates))
        for i, (op, args) in enumerate(self.gates):
            if op not in ARITY or len(args) != ARITY[op]:
                raise ValueError('unknown gate or incorrect arity')
            if any(type(a) is not int or not 1 <= a <= self.n_inputs+i for a in args):
                raise ValueError('references must point to inputs or earlier gates')
        if type(self.output) is not int or not 1 <= self.output <= self.n_inputs+len(self.gates):
            raise ValueError('invalid output wire')

    def evaluate(self, bits):
        bits = tuple(bits)
        if len(bits) != self.n_inputs or any(type(b) is not bool for b in bits):
            raise ValueError('provide exactly n_inputs Boolean values')
        values = [False, *bits]
        for op, args in self.gates:
            a = [values[i] for i in args]
            if op == 'AND': v = a[0] and a[1]
            elif op == 'OR': v = a[0] or a[1]
            elif op == 'XOR': v = a[0] != a[1]
            elif op == 'NOT': v = not a[0]
            else: v = op == 'TRUE'
            values.append(v)
        return values[self.output]

    def compile(self, assert_event=True):
        clauses = []
        for i, (op, args) in enumerate(self.gates):
            z = self.n_inputs+i+1
            if op == 'AND':
                a,b = args; clauses.extend([(-z,a),(-z,b),(z,-a,-b)])
            elif op == 'OR':
                a,b = args; clauses.extend([(z,-a),(z,-b),(-z,a,b)])
            elif op == 'XOR':
                a,b = args; clauses.extend([(a,b,-z),(-a,-b,-z),(a,-b,z),(-a,b,z)])
            elif op == 'NOT':
                a, = args; clauses.extend([(z,a),(-z,-a)])
            else: clauses.append((z if op == 'TRUE' else -z,))
        if assert_event: clauses.append((self.output,))
        return CNF(self.n_inputs+len(self.gates), tuple(clauses))

@dataclass(frozen=True)
class CNF:
    n_variables: int
    clauses: tuple

    def __post_init__(self):
        if type(self.n_variables) is not int or self.n_variables < 0:
            raise ValueError('invalid variable count')
        object.__setattr__(self, 'clauses', tuple(tuple(c) for c in self.clauses))
        if any(type(x) is not int or not 1 <= abs(x) <= self.n_variables for c in self.clauses for x in c):
            raise ValueError('invalid literal')

    def count(self, fixed=None):
        """Exact recursive enumeration with pruning; counts unused declared variables."""
        fixed = dict(fixed or {})
        if any(type(k) is not int or not 1 <= k <= self.n_variables or type(v) is not bool for k,v in fixed.items()):
            raise ValueError('invalid fixed assignment')
        clauses = self.clauses
        def restrict(cs, variable, value):
            true_lit = variable if value else -variable
            return tuple(tuple(x for x in c if x != -true_lit) for c in cs if true_lit not in c)
        for k,v in fixed.items(): clauses = restrict(clauses,k,v)
        def visit(cs, remaining):
            if any(not c for c in cs): return 0
            if not cs: return 1 << remaining
            variable = abs(cs[0][0])
            return visit(restrict(cs,variable,False),remaining-1) + visit(restrict(cs,variable,True),remaining-1)
        return visit(clauses, self.n_variables-len(fixed))

    def dimacs(self):
        return f'p cnf {self.n_variables} {len(self.clauses)}\n' + ''.join(' '.join(map(str,c))+' 0\n' for c in self.clauses)

class ImpossibleEvent(ValueError):
    pass

class World:
    def __init__(self, circuit):
        self.circuit = circuit
        self.cnf = circuit.compile()

    def count(self): return self.cnf.count()

    def probability(self): return Fraction(self.count(), 1 << self.circuit.n_inputs)

    def unrank(self, rank):
        total = self.count()
        if not total: raise ImpossibleEvent('cannot condition on probability-zero event')
        if type(rank) is not int or not 0 <= rank < total: raise ValueError('rank out of range')
        prefix = {}
        for variable in range(1,self.circuit.n_inputs+1):
            c0 = self.cnf.count({**prefix, variable: False})
            if rank < c0: prefix[variable] = False
            else: prefix[variable] = True; rank -= c0
        return tuple(prefix.values())

    def sample(self, rng=None):
        total = self.count()
        if not total: raise ImpossibleEvent('cannot condition on probability-zero event')
        return self.unrank((rng or random.SystemRandom()).randrange(total))

    def exhaustive_inputs(self):
        """Independent interpreter oracle, deliberately not using the CNF."""
        return [x for x in product((False,True),repeat=self.circuit.n_inputs) if self.circuit.evaluate(x)]


def all_true(n):
    if n < 1: raise ValueError('n must be positive')
    gates = []
    wire = 1
    for i in range(2,n+1):
        gates.append(('AND',(wire,i))); wire = n+len(gates)
    return Circuit(n,tuple(gates),wire)
