# Decisive, Bounded Experiments

Read this reference only when computation is authorized or the user requests an experimental design. If execution is not authorized, stop after producing the preregistered design.

## 1. Convert the bottleneck into competing hypotheses

State:

- \(H_1\): the prediction supported by the conjecture or proposed explanation;
- \(H_0\): the strongest viable competing explanation or alternative;
- the observation on which they disagree;
- the exact claims affected by each outcome.

Prefer hypotheses with different predictions, not merely different narratives after the fact.

## 2. Choose the smallest discriminating testbed

Use the smallest setting that preserves the distinction between the competing
hypotheses. Create a testbed map:

| Element | Why required | How preserved | What may be simplified |
|---|---|---|---|
| Disputed factor | Makes the predictions differ | Explicit testbed component | Irrelevant surrounding complexity |
| Strongest alternative | Gives the competing account a fair chance | Matched control or condition | Weaker straw-man alternatives |
| Observation | Distinguishes the outcomes | Primary metric or decision rule | Insensitive diagnostics |

Do not use a toy problem merely because it is cheap. Explain why every
simplification leaves the disputed distinction and required validity conditions
intact.

## 3. Rank by decision value

Compare candidate tests using:

\[
\text{decision value}
\;\propto\;
\frac{\text{logical leverage}\times
\text{expected uncertainty reduction}\times
\text{test fidelity}}
{\text{cost}\times\text{confounding risk}}.
\]

Use the score qualitatively. Select one bottleneck and one primary experiment. Add another run only through an explicit branch rule.

## 4. Preregister the test

Before implementation or execution, freeze:

### Scientific design

- canonical question, tested system, and exact simplifications;
- \(H_0\), \(H_1\), and any third outcome;
- primary measurement or metric and any normalization;
- strongest matched baseline;
- causal ablation or stress, if needed;
- pass, fail, and inconclusive thresholds;
- what each outcome changes in the evidence ledger.

### Numerical validity

- resolution, discretization, solver, or measurement tolerance as applicable;
- conditioning or numerical-stability threshold when relevant;
- reference or ground-truth definition;
- seed or scramble policy;
- replication trigger;
- diagnostic quantities that invalidate interpretation;
- maximum permitted runtime, memory, and run count.

### Branches and stopping

- branch condition stated in observable terms;
- exact authorized follow-up;
- total cumulative budget;
- terminal condition after which computation stops regardless of outcome.

Do not invent a new branch after seeing the result.

## 5. Use a strong control ladder

When applicable, compare:

1. a naive control only as a sanity check;
2. the strongest nuisance-matched alternative;
3. an ablation or stress targeted at the disputed distinction;
4. the proposed explanation, intervention, method, or model;
5. a direct measurement, accepted benchmark, or higher-fidelity reference when
   one exists.

Fit nuisance parameters using only information the alternative is legitimately
allowed to know. Do not tune a control on observations reserved for evaluation
or on conclusion-dependent information.

## 6. Stress from theory

Choose a stress that amplifies the predicted disagreement based on prior
reasoning, structure, symmetry, invariance, scaling, or qualitative predictions.
Avoid searching a large grid for a favorable case and presenting the winner as
confirmatory evidence.

If a pilot is needed only for numerical validity:

1. use it to choose resolution or conditioning;
2. freeze the scientific configuration afterward;
3. do not count the pilot as independent confirmation.

## 7. Preserve reproducibility

Record:

- exact command and environment;
- immutable source or archive hash;
- configuration and seed;
- raw outputs and logs;
- derived metrics with formulas;
- failures, excluded runs, and exclusion reasons.

Do not silently rewrite code between compared runs. Distinguish newly generated artifacts from pre-existing ones.

## 8. Interpret without moving the goalposts

Classify the result:

- **Pass:** satisfies the preregistered discriminator and every validity gate.
- **Fail:** contradicts the prediction while satisfying every validity gate.
- **Inconclusive:** falls in the indifference region or violates a validity gate.

Then update only the claims named in the preregistration. A pass supports the
specified prediction and may reject the tested alternative; it does not establish
logically stronger claims. A fail rejects the named prediction within the valid
test scope and refutes the broad conjecture only when that prediction was a
necessary consequence of it.

## Compact preregistration template

```markdown
### Decision question

### H1 / H0

### Distinction preserved by the testbed

### Primary metric and matched control

### Pass / fail / inconclusive thresholds

### Numerical validity gates

### Replication and branch rule

### Hard budget and terminal stop

### Ledger consequence of each outcome
```
