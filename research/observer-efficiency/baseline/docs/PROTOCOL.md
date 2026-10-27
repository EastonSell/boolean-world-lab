# Frozen validation protocol (2026-10-27)

This is a correctness/reference artifact, not an implementation or benchmark of
OpenAI's subexponential counting algorithm. No theorem novelty is claimed.

## Hypotheses and scope
H1: Each input assignment of a finite deterministic AND/OR/XOR/NOT/constant
circuit has exactly one extension satisfying its gate constraints. Asserting its
event output gives a bijection between accepted inputs and CNF models.
H2: Exact CNF counting agrees with independent input enumeration, including
zero events and unused input bits. Probability denominator is always 2**n_inputs,
never 2**n_cnf_variables.
H3: Count-guided integer-rank unranking maps ranks 0..count-1 bijectively onto
accepted inputs; uniform integer ranks therefore give exact uniform conditional
samples under the fair, independent input-bit model.

## Fixed analysis before evaluation
Python standard library only; unittest. Exhaust all assignments for primitive
gates (including repeated operands); 100 random circuits with seed 20261027,
1..3 inputs, 1..4 gates; enumerate auxiliary extensions on this tiny set.
Exhaust ranks rather than infer distribution correctness from noisy histograms.
Evaluate event families all-inputs-true for n=1..8, impossible, certain,
and an event depending only on bit 1 of 8. Report all rows, counts,
denominators, CNF sizes and agreement. Any discrepancy fails validation.
No performance threshold, selected favorable subset, p-value, speedup,
practical constants, or quantum-classical superiority claim is permitted.
Small examples cannot empirically validate an asymptotic theorem.

## Limitations
The circuit is an explicit finite Boolean world, not unrestricted physics.
Arbitrary biased/continuous inputs are unsupported. A dyadic random process can
be modeled by additional fair bits, but that costs explicit circuit size.
Rejecting impossible evidence is required. Large counts/inputs are exponential
reference work; this artifact provides no scalable solver.
