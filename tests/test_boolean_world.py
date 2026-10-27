import unittest
import random
from itertools import product
from fractions import Fraction
from boolean_world import Circuit,CNF,World,ImpossibleEvent,all_true,ARITY

class Tests(unittest.TestCase):
    def check_world(self,c):
        w = World(c); expected = w.exhaustive_inputs()
        self.assertEqual(w.count(),len(expected))
        self.assertEqual(w.probability(),Fraction(len(expected),2**c.n_inputs))
        self.assertEqual([w.unrank(r) for r in range(len(expected))],expected)
        cnf = c.compile(False)
        # Truly enumerate auxiliary bit assignments, independently of count().
        for bits in product((False,True),repeat=c.n_inputs):
            extension_count = 0
            for aux in product((False,True),repeat=len(c.gates)):
                vals = (False,)+bits+aux
                extension_count += all(any(vals[abs(x)] == (x>0) for x in clause) for clause in cnf.clauses)
            self.assertEqual(extension_count,1)
        self.assertTrue(all(len(clause)<=3 for clause in w.cnf.clauses))
        self.assertLessEqual(len(w.cnf.clauses),4*len(c.gates)+1)
        if not expected:
            with self.assertRaises(ImpossibleEvent): w.sample()
        else:
            self.assertIn(w.sample(random.Random(7)),expected)

    def test_primitives(self):
        for op,arity in ARITY.items():
            for args in product((1,2),repeat=arity):
                self.check_world(Circuit(2,((op,args),),3))

    def test_random_circuits(self):
        rng = random.Random(20261027)
        for _ in range(100):
            n = rng.randint(1,3); gates=[]
            for i in range(rng.randint(1,4)):
                op=rng.choice(list(ARITY)); args=tuple(rng.randint(1,n+i) for _ in range(ARITY[op]))
                gates.append((op,args))
            self.check_world(Circuit(n,tuple(gates),n+len(gates)))

    def test_edges(self):
        self.check_world(Circuit(0,(('TRUE',()),),1))
        self.check_world(Circuit(0,(('FALSE',()),),1))
        self.check_world(Circuit(3,(),1))
        self.check_world(Circuit(2,(('NOT',(1,)),('AND',(1,3))),4))
        self.assertEqual(CNF(7,()).count(),128)
        self.assertEqual(CNF(7,((),)).count(),0)
        self.assertEqual(CNF(3,((1,-1),)).count(),8)
        self.assertEqual(CNF(3,((1,1),)).count(),4)
        self.assertEqual(CNF(3,()).count({1:True}),4)
        for n in range(1,9): self.assertEqual(World(all_true(n)).count(),1)

    def test_invalid(self):
        for args in [(-1,(),1),(1,(('AND',(1,2)),),2),(1,(('WHAT',()),),2),(1,(),0)]:
            with self.assertRaises(ValueError): Circuit(*args)
        with self.assertRaises(ValueError): CNF(1,((0,),))
        with self.assertRaises(ValueError): CNF(1,()).count({2:True})
        with self.assertRaises(ValueError): Circuit(1,(),1).evaluate([1])
        with self.assertRaises(ValueError): World(all_true(1)).unrank(1)

if __name__ == '__main__': unittest.main()
