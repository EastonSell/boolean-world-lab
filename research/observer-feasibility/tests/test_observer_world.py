import unittest
from itertools import product
import observer_world as ow
from boolean_world import World, ImpossibleEvent

class ObserverTests(unittest.TestCase):
    def test_forward_feedback(self):
        self.assertEqual(ow.forward((True,False,True)), ((True,True),(False,True),(False,True)))
    def test_compiler_agrees_independent_execution(self):
        for steps in (1,2,4):
            for event in ow.EVENTS:
                c=ow.compile_world(steps,event)
                for tape in product((False,True),repeat=steps+1):
                    self.assertEqual(c.evaluate(tape),ow.accepts(ow.forward(tape[:steps]),event))
    def test_unused_bit_preserves_multiplicity(self):
        w=World(ow.compile_world(2,'all_observations_true'))
        self.assertEqual(w.count(),2)
        self.assertEqual(ow.forward(w.unrank(0)[:2]),ow.forward(w.unrank(1)[:2]))
    def test_impossible(self):
        w=World(ow.compile_world(2,'impossible'))
        self.assertEqual(w.count(),0)
        with self.assertRaises(ImpossibleEvent): w.unrank(0)
    def test_invalid_parameters(self):
        for steps in (0,-1,True):
            with self.assertRaises(ValueError): ow.compile_world(steps,'none')
        with self.assertRaises(ValueError): ow.compile_world(2,'bogus')
    def test_full_rank_transcript_distribution(self):
        from collections import Counter
        for event in ow.EVENTS:
            steps=3; w=World(ow.compile_world(steps,event))
            baseline=Counter(ow.forward(t[:steps]) for t in product((False,True),repeat=steps+1) if ow.accepts(ow.forward(t[:steps]),event))
            ranked=Counter(ow.forward(w.unrank(r)[:steps]) for r in range(w.count()))
            self.assertEqual(baseline,ranked)


class RegressionTests(unittest.TestCase):
    def test_exact_denominators_and_counts(self):
        from fractions import Fraction
        for steps in (2,4):
            n=steps+1
            for event,numerator in [('none',1<<n),('terminal_memory_true',1<<steps),('all_observations_true',2),('impossible',0)]:
                w=World(ow.compile_world(steps,event))
                self.assertEqual(w.count(),numerator)
                self.assertEqual(w.probability(),Fraction(numerator,1<<n))
    def test_bad_tape_type(self):
        with self.assertRaises(ValueError): ow.forward((1,))
    def test_bad_event_type(self):
        with self.assertRaises(ValueError): ow.accepts((), 'bad')

if __name__=='__main__': unittest.main()
