# Research Contract and Sharp-Conjecture Design

Use this reference when beginning or materially changing a conjecture. The
contract prevents a formally correct statement from evading the intended
question.

## 1. Canonical target

Record the fields needed to make this particular question unambiguous:

| Field | Specification |
|---|---|
| Question | The exact unknown or decision the research should resolve |
| Objects | The systems, structures, processes, data, or mathematical entities involved |
| Definitions | Meanings and conventions that determine the statement |
| Admissible domain | Inputs, parameters, regularity, boundary cases, and exclusions |
| Assumptions | Hypotheses granted rather than proved in the current program |
| Quantifiers | Their exact order and the allowed dependencies between choices |
| Conclusion | The property, relation, mechanism, prediction, or classification asserted |
| Scope | Regime, population, domain, time range, or level of generality claimed |
| Evidence standard | What would count as proof, support, refutation, or inconclusive evidence |
| Permitted inputs | Sources, data, prior results, observations, and information available to a construction or test |
| Forbidden substitutions | Changes of object, definition, assumption, target, method, or evidentiary standard that would answer a different question |
| Authorization | Read-only, theory, design, computation, delegation, and resource constraints |

Include specialized fields only when the conjecture needs them. For example,
state a norm when the claim is quantitative, a limit order when several limits
occur, a causal intervention when causality is asserted, or a complexity measure
when efficiency is part of the target. Do not force every research question
into those forms.

## 2. Non-vacuity filters

Reject or explicitly repair a candidate statement if it relies on any of the
following:

1. **Target substitution:** Replace the named object, property, or decision by
   an easier one.
2. **Definition drift:** Change a central term between the conjecture, argument,
   and evaluation.
3. **Quantifier weakening:** Alter the order or scope of “for every” and “there
   exists,” or hide a forbidden dependency.
4. **Circularity:** Assume the conclusion, an equivalent statement, or the
   decisive missing lemma.
5. **Privileged information:** Use future, held-out, unavailable, or
   conclusion-dependent information that the contract excludes.
6. **Post hoc success:** Choose the metric, instances, threshold, or
   interpretation after seeing the outcome.
7. **Proxy escape:** Succeed on a measurement that does not control or identify
   the stated target.
8. **Hidden violation:** Satisfy the displayed form while violating an intended
   resource, regularity, invariance, independence, or computability requirement.
9. **Instance substitution:** Establish a selected example when the claim
   concerns a class, or infer a class-wide conclusion from an unrepresentative
   case.
10. **Unfalsifiable reformulation:** Weaken or reinterpret the claim so that no
    admissible outcome can count against it.

Apply only the filters relevant to the contract, but never omit a known loophole
merely because it is inconvenient.

## 3. Claim map

Decompose the program according to its actual logical structure. Possible roles
include:

| Role | Question |
|---|---|
| Definition | Are the central objects and properties well defined? |
| Assumption | What is granted, and where is it used? |
| Lemma | Which intermediate implication has independent content? |
| Central conjecture | What exact statement would resolve the research question? |
| Construction or example | Does a proposed object establish an existence or possibility claim? |
| Mechanism | Does the proposed explanation entail distinguishable consequences? |
| Empirical prediction | What observable result follows within the tested scope? |
| Extension | Which stronger, broader, global, uniform, or optimal claim goes beyond the center? |

Record the directed relations between claims: requires, implies, supports,
contradicts, or leaves unchanged. Omit roles that do not apply. A construction
can prove existence without uniqueness; an experiment can support a prediction
without proving a theorem; failure of one route need not refute the central
conjecture.

## 4. Sharp-conjecture template

Write the conjecture as a complete declarative statement, not as a topic. A
flexible pattern is:

> For every object in the stated admissible domain satisfying the named
> assumptions, the stated conclusion holds, with the declared dependencies and
> exceptions.

Replace that pattern when the intended statement is existential, probabilistic,
causal, algorithmic, classificatory, or otherwise different. Then verify:

- every symbol and central term is defined;
- quantifiers appear in the intended order;
- constants, choices, data, or constructions depend only on permitted
  information;
- the conclusion has the intended strength and scope;
- edge and degenerate cases are included or explicitly excluded;
- at least one concrete outcome could refute or materially narrow the statement.

## 5. Falsifiers and route failures

Name outcomes with their exact logical force. Depending on the program,
distinguish:

- a counterexample to the central conjecture;
- evidence against a proposed mechanism or empirical prediction;
- failure of an assumption or required definition;
- failure of one construction, method, or proof route;
- failure of a stronger extension while the central claim remains open or true.

For each outcome, identify the precise claim and downstream dependencies it
changes. Do not let failure of one witness or route masquerade as a general
impossibility result.

## 6. Contract-change rule

When evidence suggests changing the problem:

1. Preserve the original contract.
2. State the proposed change and scientific reason.
3. Explain whether it weakens, strengthens, or replaces the conjecture.
4. Obtain user direction when the change is material.
5. Never present results for the revised contract as answers to the original
   one.
