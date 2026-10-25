# Adversarial Audit

Use this reference before calling a result decisive, closing a loophole,
declaring a route impossible, or claiming that only technical work remains.

## Audit protocol

For every central claim or proposed next step, record:

| Item | Question |
|---|---|
| Target claim | What exact statement is under attack? |
| Strongest alternative | What is the most plausible competing explanation, counterexample, or obstruction? |
| Failure signature | What observation or derivation would distinguish it? |
| Cheapest discriminator | What is the smallest valid theoretical, empirical, or computational check? |
| Validity gates | What would make the check logically, empirically, or numerically uninterpretable? |
| Consequence | Which claims and dependencies change under each outcome? |

Attack the strongest viable alternative. Do not use a weak baseline merely
because it is easy to defeat.

## Structural attacks

### Target and definition integrity

- Compare the exact objects, definitions, and conclusion in the conjecture with
  those used by the argument or experiment.
- Check whether a reformulation preserves the original problem or silently
  answers an easier one.
- Look for a proxy, metric, or observable that can succeed while the named target
  remains wrong or unidentified.
- Verify that special conventions, normalizations, and exclusions are stated and
  used consistently.

### Assumptions and dependencies

- List every explicit and hidden assumption, including regularity, independence,
  genericity, access to information, and boundary conditions when relevant.
- Check whether an intermediate result assumes the conclusion or an
  equivalent-strength missing lemma.
- Verify that constants, choices, constructions, and data depend only on what the
  contract permits.
- Test whether the argument survives plausible edge, degenerate, and adversarial
  cases within the stated domain.

### Logic, quantifiers, and scope

- Write the quantifiers in their exact order and check every dependency between
  them.
- Check converses, contrapositives, necessity, sufficiency, uniqueness, and
  optimality separately.
- Distinguish local, selected-instance, average, generic, and asymptotic results
  from uniform, global, or class-wide claims.
- Do not infer a stronger statement merely because it would make the narrative
  cleaner.

### Operations requiring extra justification

Apply only the checks required by the actual argument:

- When limits or analytic operations are exchanged, verify the hypotheses that
  justify each interchange.
- When a causal mechanism is claimed, identify the intervention or variation that
  distinguishes it from association and confounding.
- When an algorithmic or computational claim is made, separate correctness,
  termination, resource use, and numerical validity.
- When omitted effects or perturbations are present, distinguish their production
  from the argument controlling their influence.

### One route versus the central claim

- Determine whether a failure concerns the conjecture, an assumption, a proposed
  construction, a mechanism, an experiment, or one proof route.
- Ask whether another admissible route could avoid the obstruction.
- Do not promote failure of one candidate into a general impossibility result
  without an argument covering the full stated class.

## Competing-explanation attacks

Construct the strongest scientifically plausible alternative, such as:

- an uncontrolled nuisance variable or confounder;
- an artifact of selection, preprocessing, measurement, or implementation;
- a special symmetry, boundary case, or degeneracy;
- a simpler mechanism that produces the same observation;
- a metric that is insensitive to the disputed distinction;
- a favorable example that is not representative of the claimed domain.

Use a matched control that gives the alternative its strongest legitimate
parameters without granting information forbidden by the contract. Add a
mechanism-specific ablation or stress when it would distinguish the explanations.

Closing a loophole requires evidence against the strongest relevant version,
not against a straw man.

## Numerical and empirical attacks

- Check conditioning, discretization, measurement, sampling, optimization, and
  implementation errors relevant to the result.
- Use comparable references, metrics, and evaluation conditions.
- Replicate any conclusion whose effect is comparable to numerical or sampling
  variability.
- Freeze primary metrics and thresholds before inspecting the decisive result.
- Track negative, failed, and excluded runs with their reasons.
- Distinguish a theory-selected stress test from a searched favorable example.
- Check source identities, configurations, seeds, and raw-result provenance.
- Treat failure of a validity gate as inconclusive, not as evidence for either
  hypothesis.

## Logical severity

Classify each surviving issue:

- **Fatal:** contradicts the central conjecture under its stated contract.
- **Route-specific:** defeats the current construction, explanation, experiment,
  or proof route but does not settle the central conjecture.
- **Major:** blocks a necessary implication or evidentiary bridge.
- **Conditional:** matters only if a named assumption fails.
- **Minor:** affects constants, presentation, or a noncentral extension.

Do not call a gap “technical” unless a known theorem or fully specified argument
appears to close it under already verified hypotheses.

## Evidence language

Use these distinctions:

- **Ruled out:** logically contradicted or rejected by a valid, sufficiently
  powered discriminator over the stated scope.
- **Strongly disfavored:** survives logically but conflicts with replicated
  evidence.
- **Disfavored:** has contrary evidence with meaningful caveats.
- **Unsupported:** lacks positive evidence.
- **Open:** viable possibilities remain or the decisive check is missing.
- **Inconclusive:** the attempted check failed a logical, empirical, or numerical
  validity gate.

“No failure observed” is not “ruled out.” Agreement on selected measurements is
not identification of the claimed mechanism.

## Final hostile questions

Before upgrading the research claim, answer:

1. What is the strongest surviving alternative explanation or counterexample?
2. What is the strongest structural or logical obstruction?
3. What artifact could mimic the result?
4. Which necessary implication or evidentiary bridge remains assumed?
5. Would the opposite result have changed the conclusion?
6. Was that decision rule fixed before observing the result?
7. Does the evidence support the full stated scope?
8. What would still make the central claim false?
