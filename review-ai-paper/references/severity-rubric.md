# Claim and Severity Rubric

Use this rubric mechanically. Judge a flaw within the affected claim first, then analyze whether that claim is central to the paper. Do not increase severity merely because a claim is prominent, and do not reduce severity because its conclusion seems plausible.

## Contents

1. Plausibility of a claim
2. Novelty of theoretical or conceptual work
3. Soundness of theoretical arguments
4. Unverified dependencies
5. External citation invocation audit
6. Empirical and code findings
7. Cascading impact
8. Concern identifiers

## Plausibility of a claim

- **Highly Plausible:** Strongly supported by verified argument, evidence, and context.
- **Plausible:** Consistent with the evidence, with no major warning sign.
- **Questionable:** Material evidence or assumptions remain doubtful or incomplete.
- **Unlikely:** Available evidence substantially cuts against the claim.
- **Clearly False:** A verified contradiction, counterexample, or invalidating result establishes falsity.

Plausibility concerns the conclusion. Soundness concerns the argument supplied for it. Report them separately.

## Novelty of theoretical or conceptual work

- **Trivial:** A classical or well-known fact, vacuous reformulation, routine reframing, or immediate application whose statement and technique are expected.
- **Simple:** A meaningful but straightforward synthesis, specialization, or predictable combination of known facts. The work is not trivial, but contains no surprising conceptual step.
- **Non-trivial:** A complex or innovative sequence of ideas, a genuinely new technique, or a known tool applied in a new context to produce a surprising and useful insight.

Judge novelty of both the statement and the argument. Cite relevant prior work rather than relying on impressions.

## Soundness of theoretical arguments

### Sound

The checked logical chain is valid, required assumptions are stated and satisfied, cited results are correctly invoked, and no material gap was found. Use `Sound` only to the extent actually checked.

### Minor Flaw

Classify a flaw as minor only when all of these hold:

1. it is localized;
2. the correction is straightforward;
3. the correction leaves the core logical structure and most proof steps intact;
4. the theoretical statement remains qualitatively unchanged.

### Major Flaw

Classify a flaw as major when either condition holds:

1. repair requires substantial new reasoning or restructuring, but significant non-trivial parts of the original argument remain reusable and repair appears materially easier than proving the result from scratch; or
2. a conceptually simple repair materially weakens the theorem's scope or strength while leaving a result that still supports the paper's overall direction.

### Fatal Flaw

Classify a flaw as fatal when either condition holds:

1. a foundational assumption, indispensable citation, or critical step fails so that the presented proof structure must be abandoned and an essentially new proof is required; or
2. every plausible correction makes the result trivial, vacuous, already known, or no longer supportive of the paper's core argument.

When categories overlap, use the more severe category. Explain which defining conditions are satisfied.

## Unverified dependencies

Use `Unverifiable — source unavailable` when a critical external source cannot be retrieved or its relevant statement cannot be located. This is a coverage status, not proof that the claim is false.

- Do not call the invocation `Sound`.
- State what source and statement were sought, what retrieval attempts failed, and which claim depends on it.
- Lower confidence to reflect the gap.
- If the paper itself fails to provide support for a critical, surprisingly strong dependency, classify that lack of substantiation as a review concern; distinguish it from a demonstrated logical flaw.

## External citation invocation audit

For each critical invocation:

1. identify the exact source version and statement location;
2. reconstruct the full relevant proposition in your own words;
3. record short verbatim excerpts only for wording that must be checked;
4. list every prerequisite from the source;
5. mark each prerequisite `Satisfied`, `Violated`, or `Modified/Incomparable`, with evidence;
6. state the source conclusion;
7. state the submission's use of that conclusion;
8. classify the use as `Correct`, `Logical Gap`, `Misinterpretation`, `Critical Omission`, `Changed Dependency`, or `Unjustified Extrapolation`;
9. give `Valid Invocation`, `Flawed Invocation`, or `Unverifiable — source unavailable`;
10. assign severity and trace cascading effects.

Do not let empirical support for the conclusion influence this mechanical invocation check.

## Empirical and code findings

Use these calibrated labels:

- **Minor Point:** A localized reporting, presentation, implementation, or statistical issue whose correction does not materially alter the relevant result.
- **Major Concern:** A problem that invalidates or substantially weakens an important experiment or headline result, such as unfair baselines, leakage, incorrect metrics, material paper–code mismatch, unsupported aggregation, or missing evidence requiring substantial new work.
- **Fatal Concern:** Use rarely, when the paper's central empirical evidence is invalidated and no substantial independent support for the core contribution survives.

Record whether each finding comes from static inspection, executed code, retrieved source evidence, or inference. A failure to reproduce under different resources is not automatically evidence of author error.

## Cascading impact

For every non-sound finding, state:

1. the affected theorem, experiment, or claim;
2. each dependent claim;
3. whether the dependency invalidates, weakens, or merely limits the dependent claim;
4. what contribution survives independently.

Do not let a flaw in an ancillary statement control the paper-level verdict unless the dependency analysis shows that it reaches a core contribution.

## Concern identifiers

- Use `F1`, `F2`, and so on for fatal flaws or concerns.
- Use `M1`, `M2`, and so on for major flaws or concerns.
- Use `L1`, `L2`, and so on for minor flaws or points.

Keep identifiers stable across `code_audit.md`, `claim_ledger.md`, and `review.md`.
