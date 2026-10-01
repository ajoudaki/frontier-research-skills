# Evidence Ledger and Supersession

Use this reference when resuming research, incorporating new evidence, reconciling artifacts, or producing an authoritative report.

## 1. Source hierarchy

Treat conversation recollection as a locator, not as the technical authority. Prefer:

1. checked derivations, proofs, and raw experimental outputs;
2. source code, frozen configurations, and provenance manifests;
3. audited final reports tied to those artifacts;
4. provisional notes and intermediate reports;
5. conversational summaries.

Recency alone does not establish correctness. A later statement supersedes an earlier one only when it uses corrected assumptions, better evidence, or a valid argument that changes the conclusion.

## 2. Claim record

Maintain one record per central claim:

```markdown
### C-<number>: <short name>

- Statement:
- Claim-ladder rung:
- Status:
- Scope and assumptions:
- Supporting evidence:
- Contrary evidence:
- Dependencies:
- Cheapest decisive resolver:
- Concrete falsifier:
- Supersedes:
- Superseded by:
- Authoritative sources:
```

Keep the statement narrow enough that one status applies.

## 3. Status vocabulary

Use one primary status:

| Status | Meaning |
|---|---|
| Proved | Established by a complete argument under stated hypotheses |
| Exact-under-assumptions | Algebraically or logically exact once named assumptions are granted |
| Empirically-supported | Supported over a specified tested scope |
| Strongly-disfavored | Conflicts with replicated valid evidence but is not logically impossible |
| Disfavored | Has meaningful contrary evidence with caveats |
| Falsified | Contradicted over the exact stated scope |
| Open | A necessary bridge or discriminator is missing |
| Inconclusive | The attempted test failed a validity gate or decision threshold |
| Superseded | Replaced by a more valid formulation or result |

Add a confidence qualifier only when it clarifies evidence quality; do not substitute confidence for status.

## 4. Supersession protocol

When a result changes:

1. Identify the exact old claim.
2. Identify what changed: statement, assumption, method, data, numerical validity, or interpretation.
3. Decide whether the old claim is falsified, narrowed, or merely superseded.
4. Point the old record to the new one.
5. Use only the new valid conclusion in the main narrative.
6. Preserve the old record for provenance, not as a competing conclusion.

Examples of legitimate supersession:

- a parity or indexing correction invalidates an old comparison;
- a well-conditioned replication overturns a numerically confounded trend;
- a stronger matched control defeats the earlier baseline inference;
- a proof audit finds a missing hypothesis;
- a later theorem establishes a previously assumed bridge.

A newer report that merely restates a claim does not supersede its source evidence.

## 5. Contradiction audit

For apparently conflicting artifacts, compare:

| Dimension | Questions |
|---|---|
| Target | Are they answering the same conjecture and observables? |
| Scope | Are data class, horizon, and limit order identical? |
| Approximation axis | Are they varying the same cutoff or resolution? |
| Reference | Do they compare against the same ground truth? |
| Numerics | Did either fail conditioning or replication gates? |
| Method | Did one repair a known flaw in the other? |
| Claim level | Is one empirical while the other asserts convergence? |

Often the correct resolution is two scoped claims, not one winner.

## 6. Causal update

After each meaningful result, add:

```markdown
### Update U-<number>

- New evidence:
- Validity scope:
- Mechanism affected:
- Claims upgraded:
- Claims downgraded:
- Claims unchanged and why:
- Superseded conclusion:
- Newly exposed dependency:
- Authorized next branch, if any:
```

State why unchanged claims do not follow from the result. This prevents a successful experiment from silently upgrading unrelated theorem obligations.

## 7. Research-state summary

Maintain a compact table:

| Category | Contents |
|---|---|
| Established | Proofs, exact constructions, and verified identities |
| Supported | Empirical or conditional claims with stated scope |
| Disfavored | Alternative explanations with contrary evidence |
| Falsified | Claims rejected over an exact scope |
| Open | Necessary unresolved assumptions and proof obligations |
| Superseded | Old conclusions replaced by corrected ones |

Rank open items by logical leverage rather than by ease.

## 8. Master-report protocol

Write an authoritative report in this order:

1. current bottom line;
2. canonical contract and sharp conjecture;
3. exact causal or mathematical skeleton;
4. strongest theoretical support;
5. empirical evidence and validity scope;
6. adversarial alternatives and matched controls;
7. established, supported, disfavored, falsified, and open claims;
8. supersession note for materially changed conclusions;
9. highest-leverage unresolved obligation.

Do not narrate every historical iteration. Include history only when it explains why a conclusion changed or why a tempting argument is invalid.

## 9. Failed-program salvage

When an approach fails, inventory separately:

- exact identities that remain valid;
- useful representations or algorithms;
- counterexamples and no-go results;
- causal mechanisms exposed;
- assumptions shown necessary;
- conclusions that must be discarded.

Failure of the theorem does not erase valid algebra. Valid algebra does not rescue the failed theorem.
