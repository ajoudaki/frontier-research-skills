---
name: solve-math-rigorously
description: Produce compact but complete solutions to standalone mathematical questions and proof requests. Use when the user asks to solve, prove, derive, analyze, verify, or correct a mathematical problem that is not primarily an incremental lesson about supplied technical documents. Infer the strongest reasonable interpretation without inventing assumptions, establish a minimal setup, use minimal notation, expose every nontrivial step, state and verify external theorem hypotheses, give proof architecture when useful, and silently audit the draft before answering.
---

# Solve Mathematics Rigorously

Produce a complete mathematical answer rather than a staged document lesson, unless the user explicitly requests incremental pacing. Optimize simultaneously for correctness, rigor, clarity, and economy.

## Determine the intended problem

Interpret the strongest reasonable version supported by the wording and mathematical context. Do not exploit an omission to answer a trivial or uninteresting straw-man version.

Handle ambiguity according to its effect:

- If it does not change the substance, adopt the conventional interpretation and state it briefly.
- If one reasonable assumption makes the intended problem precise, state that assumption before solving.
- If several reasonable interpretations lead to materially different answers, ask for clarification or give a compact case split when that fully resolves the ambiguity.
- If a missing assumption is necessary for the claimed conclusion, do not invent it silently.

If the stated claim is false, say so and give a decisive counterexample or contradiction. Present a corrected nearby statement only when it helps, and label it as a correction rather than the original result.

Answer the problem actually asked. Do not weaken a universal claim to a convenient special case, replace an exact question with a numerical approximation, or prove a converse instead of the stated direction.

## Establish a minimal setup

Begin with a compact setup or preliminaries passage when it reduces ambiguity or supports later reasoning. State only the necessary:

- domain and assumptions;
- definitions used in the solution;
- boundary, regularity, integrability, independence, or nondegeneracy conditions that matter;
- notation that must persist through the answer.

Reuse the problem's notation whenever possible. Introduce a new symbol only when the unabbreviated expression is genuinely cumbersome and recurs often. Define every new symbol before use and state its mathematical type when that is not immediately evident.

Do not force a visible setup heading for a short elementary problem. Do not hide substantive assumptions in prose later in the solution.

## Give the architecture before a substantial proof

Before a long or conceptually difficult proof, explain the plan in a short paragraph or compact list. Identify the main steps, cases, claims, or lemmas and how they combine to yield the conclusion.

Keep the architecture at the level needed to orient the reader. Do not duplicate the detailed proof, and do not substitute a plan for the proof itself. For a routine calculation or one-step argument, omit the architecture.

## Execute every nontrivial step

Derive each nontrivial algebraic, analytic, probabilistic, geometric, combinatorial, or logical transition. Give enough detail for the user to verify the step without reconstructing missing reasoning.

In particular:

- identify the definition, identity, inequality, or prior claim being used;
- show substitutions, rearrangements, case transitions, and changes of variables that carry real mathematical content;
- track domains, signs, quantifiers, equality conditions, exceptional cases, and possible zero denominators;
- justify limit exchanges, differentiation or integration under a sign, convergence claims, and optimization steps;
- distinguish exact arguments from heuristics, approximations, and numerical evidence;
- show that intermediate claims actually imply the requested conclusion.

Avoid words such as “clearly,” “obviously,” “standard,” and “it follows” when they replace reasoning. They are acceptable only after the supporting reason has been supplied.

Do not over-explain elementary arithmetic or definitions already established. Compress routine steps while preserving the chain of verification.

## Invoke external results completely

Whenever the solution relies on a nontrivial theorem or external fact:

1. state the exact form needed, including its assumptions and conclusion;
2. verify each assumption in the present problem;
3. identify the current objects substituted into the theorem;
4. state exactly what conclusion the theorem yields here.

Do not merely name a theorem or call a fact standard. Prefer the relevant specialization over an unnecessarily general statement.

Verify a recent, specialized, source-specific, or uncertain result against a primary or authoritative source before relying on it. Cite the source near the claim. Paraphrase the relevant result unless its exact wording matters; quote only a short compliant excerpt when useful.

If the required theorem is unavailable, uncertain, or does not apply, expose the gap instead of proceeding as though it were valid.

## Use examples and checks proportionately

Include an example, boundary case, counterexample, or remark only when it clarifies an abstraction, tests a hypothesis, explains a consequence, or exposes why an assumption is needed.

Use low-cost sanity checks when they add confidence, such as:

- substituting the result back into the defining relation;
- checking dimensions, signs, or units;
- testing a boundary or small case;
- comparing with a known special case;
- deriving the same conclusion by a second short route.

Do not add examples mechanically or let them replace the general argument.

## Keep the presentation compact

Use headings only when they make a substantial solution easier to navigate. Keep notation sparse and stable. Prefer explicit expressions to disposable shorthand.

Use equations to carry mathematical content, not decoration. Avoid formula dumps, decorative summaries, and boxed equations. State the conclusion plainly.

Let the problem's complexity determine the answer length. Preserve every necessary assumption, theorem check, and logical transition, but remove repetition and exposition that does not improve understanding or verification.

## Audit and revise silently

Draft the solution, then review it before sending. Check:

1. Did the solution address the strongest reasonable interpretation rather than a straw man?
2. Were all adopted assumptions stated, and were none invented merely to force the result?
3. Was the setup sufficient but minimal?
4. Was every persistent symbol necessary and defined?
5. Did a substantial proof receive a useful architecture?
6. Can the reader verify every nontrivial transition?
7. Was every external theorem stated in the needed form, with its hypotheses checked and its conclusion applied explicitly?
8. Were recent, specialized, or uncertain results verified from an authoritative source?
9. Were edge cases, equality conditions, domains, and quantifiers handled?
10. Does the final conclusion answer the exact question?
11. Do examples or remarks earn their space?
12. Is the answer as compact as rigor allows, with no boxed equations?

Revise any failing part and repeat the audit until the answer satisfies the checklist as well as possible. Do not mention the drafting or audit process in the final answer.
