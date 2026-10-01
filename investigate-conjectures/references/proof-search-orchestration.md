# Bounded Multi-Route Proof Search

Use this mode to search for a complete proof of a mathematical conjecture across several genuinely different approaches. Do not treat the mode, the user's optimism, or the conjecture's fame as evidence that a proof exists.

## Fix the proof contract

Before choosing approaches, record:

- the exact theorem, quantifiers, hypotheses, definitions, and edge cases;
- which classical or supplied results may be used;
- what counts as a complete proof;
- which special cases, reductions, computations, or conditional results do not resolve the target;
- the time, compute, token, and concurrency budget;
- the terminal outcomes: a proof that survives audit, or budget exhaustion with exact proved results and gaps.

Do not prohibit literature search unless the user requests an independent-discovery or benchmark-integrity mode. Do not assume an affirmative proof exists unless the user explicitly poses a hypothetical; even then, accept only a complete audited argument.

## Choose the execution mode

Use delegated or parallel workers only when the user explicitly authorizes delegation or parallel work and the environment supports it. Otherwise explore the routes sequentially with the same records and stopping rules. Never hard-code an agent count, runtime, or product-specific orchestration feature.

Allocate available effort dynamically. Match the portfolio size to the budget, keep synthesis capacity in reserve, and reduce breadth when routes cannot be audited adequately.

## Seed a diverse portfolio

Define approach families by mathematical mechanism, not wording. Choose only families appropriate to the theorem, such as structural induction, extremal arguments, algebraic or analytic reformulation, probabilistic construction, duality, invariants, decomposition, topology, optimization, or computation-assisted discovery.

During the first round, preserve independence:

- give each route the same proof contract without presenting a favored strategy as established;
- avoid duplicating superficially different versions of one mechanism;
- keep incompatible approaches alive long enough to expose their real strengths and obstructions;
- reserve cross-pollination until routes have produced concrete mathematics.

## Maintain an approach registry

Keep one row per route:

| Field | Record |
|---|---|
| Route | Stable identifier and approach family |
| Mechanism | Proposed reason the route could prove the theorem |
| Deliverable | Lemma, construction, equation, reduction, or counterexample sought |
| Dependencies | External theorems and unproved internal claims |
| Strongest result | Exact statement currently established |
| Obstacle | Smallest unresolved step and its logical strength |
| Distinctiveness | How the route differs from active alternatives |
| Status | Active, promising, blocked, refuted, merged, or complete |
| Reopen condition | New mechanism, lemma, or evidence required |

Update the registry after every round. Cluster routes that use the same mathematical idea even when their notation differs.

## Enforce a concrete route contract

Require every route to return:

1. a precise claim or construction;
2. a derivation or proof of everything asserted;
3. every external dependency and its checked hypotheses;
4. a counterexample search or sanity check when applicable;
5. the exact unresolved implication, if any;
6. a registry-status recommendation and reason.

Reject vague progress reports, unsupported optimism, and claims that a global compatibility step is routine. A reduction is meaningful progress only when its target is already proved, strictly better understood, or accompanied by a new mechanism that attacks it.

## Run adaptive rounds

After each round:

1. verify concrete outputs before treating them as progress;
2. merge duplicate routes by mechanism;
3. identify reductions whose missing lemma is equivalent in strength to the original theorem;
4. redirect effort toward underexplored families or newly enabled bottlenecks;
5. mark a route blocked when it stalls at a theorem-strength lemma;
6. reopen a blocked route only after a materially new invariant, construction, theorem, or counterexample appears;
7. cross-pollinate mature routes when one route supplies another's missing ingredient;
8. preserve valid lemmas and counterexamples from failed routes.

Do not let elegance, early popularity, or the amount of work already invested determine allocation.

## Audit candidate proofs independently

When a complete route appears, stop expanding it and begin reconstruction. Assign separate checks, sequentially or through authorized workers, to:

- reconstruct every implication from the proof contract;
- verify all cited theorem statements and hypotheses;
- test definitions, degenerate cases, boundary cases, and well-definedness;
- search for circular dependence or an equivalent-strength hidden lemma;
- generate the theorem-specific failure checklist;
- seek a minimal counterexample to every vulnerable intermediate claim;
- distinguish a complete proof from a plausible proof sketch.

Integrate the final mathematical argument using the rigorous proof workflow. Label it `candidate proof` until the full chain survives independent audit, and state whether any formal or machine verification was actually performed.

## Stop and report honestly

Stop when a complete proof survives the authorized audit, or when the hard budget is exhausted. At exhaustion, report the registry, all proved lemmas, refuted and blocked routes, exact remaining gaps, and each route's reopen condition. Never convert persistence instructions into permission to fabricate a proof or conceal an unresolved implication.
