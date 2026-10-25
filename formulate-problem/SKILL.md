---
name: formulate-problem
description: Turn an open-ended research question into a precise, non-vacuous, frozen research contract, then pursue it adversarially through claim maps, evidence ledgers, hostile audits, decisive experiments, and bounded multi-route proof search. Use when the agent must formulate a non-vacuous research conjecture, recover or update a long-running research program, orchestrate an explicitly authorized search across independent proof approaches, separate proof obligations and evidence levels, audit loopholes or competing explanations, design a discriminating experiment, interpret new evidence, or synthesize a supersession-aware research state. Do not use for teaching a technical source, solving an isolated mathematical problem, reviewing an external paper, or summarizing material that needs no research-state reconciliation.
metadata:
  version: "0.2.0"
---

# Formulate Problem

## Purpose

Turn a broad research question into a precise, falsifiable conjecture and an efficient program for resolving its weakest links. Integrate theory, adversarial reasoning, and only authorized computation. Preserve uncertainty: an honest open or inconclusive result is preferable to a stronger unsupported claim.

Treat the skill as the research-program controller. Use a specialized proof, teaching, paper-review, data, or coding skill for bounded subtasks when appropriate, while retaining the claim structure and evidence updates here.

## Load references selectively

- Read [research-contract.md](references/research-contract.md) when starting, materially reformulating, or checking the non-vacuity of a conjecture.
- Read [evidence-ledger.md](references/evidence-ledger.md) when resuming prior work, reconciling contradictory artifacts, updating conclusions, or writing a master report.
- Read [adversarial-audit.md](references/adversarial-audit.md) before declaring a loophole closed, a route impossible, a result decisive, or a theorem nearly established.
- Read [decisive-experiments.md](references/decisive-experiments.md) only when computation is explicitly authorized or when the user asks for an experimental design. Do not run an experiment merely because it would be informative.
- Read [proof-search-orchestration.md](references/proof-search-orchestration.md) when the user requests a bounded multi-route search for a complete mathematical proof. Use parallel agents only when the user explicitly authorizes delegation or parallel work; otherwise apply the same registry and round discipline sequentially.

## Establish scope and authority

1. Restate the research target in one sentence.
2. Determine whether the user authorized:
   - read-only synthesis or assessment;
   - new theoretical analysis;
   - experiment design only;
   - implementation or computation;
   - delegated or parallel proof search;
   - a bounded continuation under conditional branches.
3. Record any time, compute, token, data, model, or run budget as a hard constraint.
4. Ask only for a missing choice that would materially change the result. Otherwise make the narrowest reasonable assumption and label it.
5. Never expand a diagnostic or reporting request into implementation, computation, external actions, or a new research branch.

## Core workflow

### 1. Restore the authoritative state

Read the current primary artifacts before reasoning from memory. Identify the canonical statement, latest valid methods, raw evidence, unresolved objections, and superseded conclusions. Prefer derivations and raw results over summaries; prefer audited later results only when they actually repair or invalidate earlier work.

When resuming or synthesizing, maintain the ledger in [evidence-ledger.md](references/evidence-ledger.md).

### 2. Freeze the research contract

Specify the canonical question, objects, definitions, admissible domain, assumptions, quantifiers, conclusion, scope, permitted evidence or methods, and forbidden substitutions. Record parameter dependencies, regimes, success criteria, and failure criteria when they matter to the claim.

Apply the non-vacuity checks in [research-contract.md](references/research-contract.md). Reject circular formulations, definition drift, weakened quantifiers, privileged information, post hoc success criteria, or replacement of the intended question by an easier one.

### 3. Build the claim map

Identify the central conjecture and only the supporting claim types that actually apply, such as:

- definitions and well-posedness requirements;
- necessary and sufficient conditions;
- exact identities, lemmas, and reductions;
- existence, uniqueness, construction, or classification claims;
- mechanism or explanatory claims;
- empirical predictions and observations;
- local, global, uniform, asymptotic, or stronger extensions.

Record which claims imply, require, support, contradict, or merely motivate others. Do not transfer evidence between logically different claims without an explicit bridge. In particular, distinguish a central existence claim from one proposed construction, a mathematical statement from empirical support, and a claim from a stronger extension.

### 4. State the sharp conjecture

Write explicit quantifiers and dependencies. State:

- the objects and admissible domain;
- definitions and hypotheses;
- universal and existential quantifiers in their intended order;
- the exact conclusion;
- allowed dependencies of constants, parameters, choices, or constructions;
- the intended scope, including edge or degenerate cases;
- concrete outcomes that would refute or materially narrow the statement.

If several statements are needed, identify one central conjecture and label the rest as lemmas, assumptions, or stronger extensions.

### 5. Derive the exact mathematical or causal skeleton

Derive before simplifying. Mark each step as exact, conditional on named assumptions, heuristic, empirical, or open. Track logical dependencies and, when relevant, causal direction, information flow, interventions, and omitted effects.

Keep distinct axes of variation distinct. A result under one parameter, regime, topology, dataset, model class, or limiting operation does not automatically transfer to another.

In particular, separate:

- local conclusions from global ones;
- necessary conditions from sufficient ones;
- association from causation or mechanism;
- a successful construction from a universal or uniqueness claim;
- empirical agreement from mathematical proof;
- failure of a proof route from falsity of the conjecture.

### 6. Build a typed evidence ledger

For each central claim, record its exact statement, role in the claim map, status, assumptions, supporting and contrary evidence, dependencies, cheapest resolver, falsifier, and supersession relation.

Use calibrated labels. Distinguish proved, exact under assumptions, empirically supported, disfavored, falsified, open, and superseded. Never translate “not observed” into “ruled out.”

### 7. Run a hostile audit

Attack the strongest plausible version of each alternative, not a straw man. Check for:

- hidden assumptions, circularity, or inaccessible information;
- definition, quantifier, implication, or scope mismatch;
- unchecked edge cases and illicit strengthening;
- unjustified changes of regime or interchange of operations;
- target or model substitution;
- nuisance explanations matched only by weak controls;
- numerical conditioning, discretization, leakage, or selection effects;
- evidence for one construction or instance being treated as a broader theorem.

Use [adversarial-audit.md](references/adversarial-audit.md) and state what each surviving objection would change.

### 8. Select one bottleneck

Rank candidate next steps by logical leverage, expected uncertainty reduction, relevance to the central claim, and cost. Prefer the smallest step whose possible outcomes would change the research state.

Do not optimize for volume of algebra, number of experiments, or apparent completeness. Avoid polishing downstream machinery while an upstream definition, identification, missing implication, or validity gap remains decisive.

Normally pursue one bottleneck at a time. In an authorized multi-route proof search, retain a small structurally diverse portfolio and select one explicit bottleneck per active route using [proof-search-orchestration.md](references/proof-search-orchestration.md).

### 9. Precommit any authorized experiment

Before implementation or execution, read [decisive-experiments.md](references/decisive-experiments.md) and freeze:

- competing hypotheses;
- the exact prediction on which they disagree and why the test isolates it;
- primary metric and matched controls;
- pass, fail, and inconclusive thresholds;
- numerical validity gates;
- replication rule and conditional branches;
- exact budget and terminal stopping condition.

Use the smallest nondegenerate testbed, not automatically the smallest instance. Do not launch exploratory grids when one reasoned stress or ablation can discriminate the hypotheses.

### 10. Update by logical consequence

After a derivation or experiment, ask:

1. What claim, assumption, prediction, or mechanism was supported, rejected, or left unresolved?
2. Which exact ledger claims change status?
3. Does a failure refute the central conjecture, one assumption, the current construction, or only one proof route?
4. Which earlier conclusion is superseded?
5. Does the result authorize a precommitted branch? If not, stop.

Salvage valid identities, tools, counterexamples, and mechanisms from failed programs. Do not preserve their invalid conclusion.

### 11. Synthesize the current state

Lead with the strongest defensible conclusion. Report separately:

- established results;
- supported but unproved claims;
- disfavored or falsified claims and explanations;
- unresolved decisive gaps;
- superseded conclusions;
- the single highest-leverage next action, if requested and authorized.

When later work corrects earlier work, use the corrected result in the main narrative and record the supersession once. Do not accumulate mutually inconsistent report layers.

## Decision rules

- **Success of one construction or method:** Treat it as evidence for that construction or method within the tested or proved scope, not as a universal, unique, or optimal result.
- **A successful matched control or discriminator:** Downgrade the tested alternative within the valid scope; do not infer a theorem or unrelated mechanism.
- **A numerical trend:** Check conditioning, comparability, selection, and replication before inferring a general law.
- **A correct local result:** Preserve its exact scope; require an additional argument for global, uniform, or asymptotic conclusions.
- **A theorem proving one implication:** Record that implication; do not silently use its converse or a stronger statement.
- **Failure of one route or construction:** Distinguish it from failure of the central conjecture or the full admissible class.
- **Confounded evidence:** Mark inconclusive and stop unless a resolution run was preauthorized.
- **Budget exhausted:** Stop even when the scientific question remains open.

## Output standards

Match the requested artifact. For a concise assessment, provide the current conclusion, decisive evidence, and leading gap. For a full research state, provide:

1. canonical target and research contract;
2. sharp conjecture;
3. exact mathematical or causal skeleton;
4. claim map and evidence ledger;
5. adversarial alternatives;
6. empirical or computational evidence and validity limits, when present;
7. what is established, disfavored, falsified, open, and superseded;
8. ranked proof obligations or next decision.

Keep notation stable and minimal. Attach claims to evidence close to where they appear. State assumptions at the claim they support. Never hide a decisive gap in a generic limitations section.
