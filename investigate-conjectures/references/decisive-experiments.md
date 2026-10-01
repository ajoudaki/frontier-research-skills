# Decisive, Bounded Experiments

Read this reference only when computation is authorized or the user requests an experimental design. If execution is not authorized, stop after producing the preregistered design.

## 1. Convert the bottleneck into competing hypotheses

State:

- \(H_1\): the mechanism or conjecture-supported prediction;
- \(H_0\): the strongest viable mundane or structural alternative;
- the observation on which they disagree;
- the claim-ladder rung affected by each outcome.

Prefer hypotheses with different predictions, not merely different narratives after the fact.

## 2. Choose the smallest mechanism-preserving testbed

Use the smallest setting that retains every disputed ingredient. Create a mechanism map:

| Ingredient | Why required | How preserved | What simplification removes |
|---|---|---|---|
| Disputed interaction | Creates the predicted effect | Exact testbed component | Irrelevant ambient complexity |
| Alternative mechanism | Gives the control a fair chance | Matched nuisance parameter | Straw-man behavior |
| Observable | Separates predictions | Primary metric | Insensitive diagnostics |

Do not use a toy problem merely because it is cheap. Explain why removing scale, dimension, samples, layers, or geometry does not remove the mechanism at issue.

## 3. Rank by decision value

Compare candidate tests using:

\[
\text{decision value}
\;\propto\;
\frac{\text{logical leverage}\times
\text{expected uncertainty reduction}\times
\text{mechanism fidelity}}
{\text{cost}\times\text{confounding risk}}.
\]

Use the score qualitatively. Select one bottleneck and one primary experiment. Add another run only through an explicit branch rule.

## 4. Preregister the test

Before implementation or execution, freeze:

### Scientific design

- canonical model and exact simplifications;
- \(H_0\), \(H_1\), and any third outcome;
- primary observable and error normalization;
- strongest matched baseline;
- causal ablation or stress, if needed;
- pass, fail, and inconclusive thresholds;
- what each outcome changes in the evidence ledger.

### Numerical validity

- discretization or solver tolerance;
- conditioning threshold;
- common-reference construction;
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
3. a mechanism-removing ablation;
4. the proposed causal or nonlinear model;
5. the real or high-fidelity reference.

Fit nuisance parameters using only information the alternative is legitimately allowed to know. Do not tune a control on the future target trajectory.

## 6. Stress from theory

Choose a stress that amplifies the predicted disagreement based on prior algebra, symmetry, scaling, or qualitative dynamics. Avoid searching a large grid for a favorable case and presenting the winner as confirmatory evidence.

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

Then update only the claims named in the preregistration. A pass can reject a nuisance explanation without proving hierarchy convergence. A fail can kill one witness without disproving broad finite-representation existence.

## Compact preregistration template

```markdown
### Decision question

### H1 / H0

### Mechanism preserved by the testbed

### Primary metric and matched control

### Pass / fail / inconclusive thresholds

### Numerical validity gates

### Replication and branch rule

### Hard budget and terminal stop

### Ledger consequence of each outcome
```
