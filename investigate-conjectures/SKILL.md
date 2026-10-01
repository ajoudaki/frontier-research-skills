---
name: investigate-conjectures
description: Develop, refine, and adversarially test open mathematical, computational, or mechanistic conjectures through bounded theory–experiment and multi-route proof-search programs. Use when Codex must formulate a non-vacuous research conjecture, recover or update a long-running research program, orchestrate an explicitly authorized search across independent proof approaches, separate proof obligations and claim levels, audit loopholes or competing explanations, design a mechanism-preserving discriminating experiment, interpret new evidence, or synthesize a supersession-aware research state. Do not use for teaching a technical source, solving an isolated mathematical problem, reviewing an external paper, or summarizing material that needs no research-state reconciliation.
---

# Investigate Conjectures

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

Specify the canonical object, admissible inputs, observables, error criterion, topology or norm, horizon, limit order, approximation family, coefficient provenance, complexity dependence, and forbidden substitutions. State what information the proposed surrogate may retain and whether it must be autonomous and restartable.

Apply the non-vacuity checks in [research-contract.md](references/research-contract.md). Reject oracle playback, hidden encodings of the target trajectory, replacement by an easier model, or quantifiers that avoid the intended compression problem.

### 3. Build the claim ladder

Separate at least:

1. exact identities or finite constructions;
2. well-posedness or internal correctness of the proposed approximation;
3. empirical accuracy on tested instances;
4. convergence of the approximation hierarchy;
5. identification with the intended limit or real system;
6. compact-horizon validity;
7. all-time or uniform validity;
8. existence of some admissible witness versus success of the current witness.

Do not promote evidence from one rung to another without an explicit bridge.

### 4. State the sharp conjecture

Write explicit quantifiers and dependencies. State:

- the admissible problem class;
- what may depend on accuracy, horizon, and regularity;
- what must remain independent of ambient scale or inaccessible trajectory information;
- the approximation guarantee and norm;
- coefficient provenance and initialization;
- autonomy, restartability, or finite-memory requirements;
- concrete falsifiers.

If several statements are needed, identify one central conjecture and label the rest as lemmas, assumptions, or stronger extensions.

### 5. Derive the exact causal skeleton

Derive before truncating. Mark each step as exact, conditional on named assumptions, heuristic, empirical, or open. Track causal dependencies, information flow, history dependence, and the source of every residual.

Keep distinct approximation axes distinct. Convergence in time step, basis degree, perturbation order, response depth, width, spatial resolution, or another coordinate does not imply convergence in any other axis.

In particular, separate:

- correctness of every fixed-order coefficient from convergence of the full expansion;
- production of omitted error from propagation or stability of that error;
- observable accuracy from state-space convergence;
- failure of a proof route from falsity of the conjecture.

### 6. Build a typed evidence ledger

For each central claim, record its exact statement, claim-ladder rung, status, assumptions, supporting and contrary evidence, dependencies, cheapest resolver, falsifier, and supersession relation.

Use calibrated labels. Distinguish proved, exact under assumptions, empirically supported, disfavored, falsified, open, and superseded. Never translate “not observed” into “ruled out.”

### 7. Run a hostile audit

Attack the strongest plausible version of each alternative, not a straw man. Check for:

- hidden memory or inaccessible information;
- tail escape and high-to-low feedback;
- topology or observable mismatch;
- nonnormal amplification and unstable error propagation;
- unjustified interchange of limits;
- easier-model substitution;
- nuisance explanations matched only by weak controls;
- numerical conditioning, discretization, leakage, or selection effects;
- a result that validates one witness but not the intended existence claim.

Use [adversarial-audit.md](references/adversarial-audit.md) and state what each surviving objection would change.

### 8. Select one bottleneck

Rank candidate next steps by logical leverage, expected uncertainty reduction, mechanism relevance, and cost. Prefer the smallest step whose possible outcomes would change the research state.

Do not optimize for volume of algebra, number of experiments, or apparent completeness. Avoid polishing downstream machinery while an upstream identification or compactness gap remains decisive.

Normally pursue one bottleneck at a time. In an authorized multi-route proof search, retain a small structurally diverse portfolio and select one explicit bottleneck per active route using [proof-search-orchestration.md](references/proof-search-orchestration.md).

### 9. Precommit any authorized experiment

Before implementation or execution, read [decisive-experiments.md](references/decisive-experiments.md) and freeze:

- competing hypotheses;
- the disputed mechanism and why the testbed preserves it;
- primary metric and matched controls;
- pass, fail, and inconclusive thresholds;
- numerical validity gates;
- replication rule and conditional branches;
- exact budget and terminal stopping condition.

Use the smallest nondegenerate testbed, not automatically the smallest instance. Do not launch exploratory grids when one theory-selected stress or ablation can discriminate the hypotheses.

### 10. Update causally

After a derivation or experiment, ask:

1. What mechanism was supported, rejected, or left unresolved?
2. Which exact ledger claims change status?
3. Does a failure kill the broad conjecture, the current witness, one assumption, or only one proof route?
4. Which earlier conclusion is superseded?
5. Does the result authorize a precommitted branch? If not, stop.

Salvage valid identities, tools, counterexamples, and mechanisms from failed programs. Do not preserve their invalid conclusion.

### 11. Synthesize the current state

Lead with the strongest defensible conclusion. Report separately:

- established results;
- supported but unproved claims;
- disfavored or falsified explanations;
- unresolved decisive gaps;
- superseded conclusions;
- the single highest-leverage next action, if requested and authorized.

When later work corrects earlier work, use the corrected result in the main narrative and record the supersession once. Do not accumulate mutually inconsistent report layers.

## Decision rules

- **Strong surrogate performance:** Treat it as evidence of utility, not hierarchy convergence or arbitrary-accuracy existence.
- **A successful matched nonlinear or causal control:** Downgrade that particular mundane explanation; do not infer a theorem.
- **A failed high-order trend:** Check parity, conditioning, common-reference comparability, and replication before inferring divergence.
- **A correct local expansion with growing coefficients:** Preserve the local algebra while rejecting unsupported positive-horizon convergence.
- **A stability theorem without a source estimate:** Record propagation control; leave error production open.
- **Failure of one representation:** Distinguish failure of the explicit witness from failure of the broader admissible class.
- **Confounded evidence:** Mark inconclusive and stop unless a resolution run was preauthorized.
- **Budget exhausted:** Stop even when the scientific question remains open.

## Output standards

Match the requested artifact. For a concise assessment, provide the current conclusion, decisive evidence, and leading gap. For a full research state, provide:

1. canonical target and research contract;
2. sharp conjecture;
3. exact causal skeleton;
4. claim and evidence ledger;
5. adversarial alternatives;
6. experimental evidence and validity limits;
7. what is established, disfavored, falsified, open, and superseded;
8. ranked proof obligations or next decision.

Keep notation stable and minimal. Attach claims to evidence close to where they appear. State assumptions at the claim they support. Never hide a decisive gap in a generic limitations section.
