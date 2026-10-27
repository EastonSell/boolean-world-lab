import random
import unittest
from itertools import product
from comparison import (Work, MeasuredCounter, CachedSampler, family_circuit,
                        enumerate_sample, rejection_sample)
from boolean_world import CNF, Circuit, World, ImpossibleEvent

class ComparisonTests(unittest.TestCase):
    def test_instrumentation_hand_count(self):
        work = Work()
        self.assertEqual(MeasuredCounter(CNF(1, ((1,),)), work).count(), 1)
        self.assertEqual(work.count_calls, 1)
        self.assertEqual(work.recursive_visits, 3)
        self.assertEqual(work.restriction_calls, 2)
        self.assertEqual(work.clauses_scanned, 2)
        self.assertEqual(work.literal_inspections, 3)
        self.assertEqual(work.empty_clause_checks, 2)

    def test_counter_matches_reference_all_prefixes(self):
        for n in range(1, 5):
            for family in ('certain', 'impossible', 'first_bit', 'all_true', 'parity'):
                cnf = family_circuit(n, family).compile()
                for length in range(n+1):
                    for prefix in product((False, True), repeat=length):
                        expected = cnf.count(dict(enumerate(prefix, 1)))
                        self.assertEqual(MeasuredCounter(cnf, Work()).count(prefix), expected)

    def test_exhaustive_unranking_and_cache(self):
        for n in range(1, 6):
            for family in ('certain', 'impossible', 'first_bit', 'all_true', 'parity'):
                circuit = family_circuit(n, family)
                expected = World(circuit).exhaustive_inputs()
                sampler = CachedSampler(circuit)
                self.assertEqual(sampler.total, len(expected))
                self.assertEqual([sampler.unrank(r) for r in range(len(expected))], expected)
                self.assertLessEqual(len(sampler.cache), min(len(expected)*n, 2**n-1))
                old = sampler.work.count_calls
                self.assertEqual([sampler.unrank(r) for r in range(len(expected))], expected)
                self.assertEqual(sampler.work.count_calls, old)
                self.assertEqual(old, 1+len(sampler.cache))
                if not expected:
                    with self.assertRaises(ImpossibleEvent): sampler.sample(random.Random(0))

    def test_zero_input_and_invalid(self):
        for value in (True, False):
            sampler = CachedSampler(Circuit(0, ((('TRUE' if value else 'FALSE'), ()),), 1))
            if value:
                self.assertEqual(sampler.unrank(0), ())
                for rank in (-1, 1, True):
                    with self.assertRaises(ValueError): sampler.unrank(rank)
            else:
                with self.assertRaises(ImpossibleEvent): sampler.unrank(0)

    def test_method_status_accounting(self):
        for family in ('certain', 'impossible', 'first_bit', 'all_true', 'parity'):
            c = family_circuit(4, family)
            samples, work, size = enumerate_sample(c, 16, 2)
            self.assertEqual(work.evaluated_inputs, 16)
            self.assertEqual(work.evaluated_gates, 16*len(c.gates))
            sampler = CachedSampler(c)
            rng = random.Random(2)
            self.assertEqual(samples, [sampler.sample(rng) for _ in range(16)] if size else [])
            rejected, work = rejection_sample(c, 16, 2, cap=7)
            self.assertEqual(work.evaluated_inputs, 7)
            self.assertEqual(work.generated_input_bits, 28)
            self.assertTrue(all(c.evaluate(x) for x in rejected))
            if family == 'impossible': self.assertEqual(rejected, [])
