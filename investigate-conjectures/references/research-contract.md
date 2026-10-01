# Research Contract and Sharp-Conjecture Design

Use this reference when beginning or materially changing a conjecture. The contract prevents a formally true statement from evading the scientific question.

## 1. Canonical target

Record the following before choosing a proof strategy or surrogate:

| Field | Required specification |
|---|---|
| Object | Exact system, process, operator, distribution, or model |
| Admissible class | Inputs, parameters, regularity, data, and initial conditions |
| Dynamics or relation | Update rule, flow, equilibrium condition, or map |
| Observables | State components or derived quantities to approximate |
| Error | Norm, metric, probability mode, and reference object |
| Horizon | Fixed time, compact interval, asymptotic regime, or all time |
| Limits | Exact order of size, depth, step, sample, or continuum limits |
| Approximation family | Permitted state, equations, basis, memory, and operations |
| Provenance | Information from which coefficients and initial data may be computed |
| Complexity | What may scale with accuracy, horizon, or regularity |
| Invariance | What must not scale with ambient system size or a hidden oracle |
| Restartability | Whether the approximation must continue from its current state |
| Forbidden substitutions | Easier architectures, norms, limits, observables, or optimizers |
| Authorization | Read-only, theory, design, compute, and budget constraints |

If a field is immaterial, say why rather than silently omitting it.

## 2. Non-vacuity filters

Reject or explicitly exclude a candidate statement if it permits any of the following:

1. **Trajectory playback:** Encode the answer as a time-indexed forcing, interpolation table, or oracle coefficient.
2. **Hidden full state:** Call a representation “finite” while one coordinate contains an unbounded function, history, matrix, dataset, or arbitrary-precision code for the original system.
3. **Instance memorization:** Choose coefficients after observing the target trajectory unless system identification is explicitly the scientific problem.
4. **Quantifier inversion:** Prove existence separately for each realized trajectory when a uniform construction over a problem class is required.
5. **Ambient scaling:** Let state dimension or coefficient complexity grow with the system size that the approximation is meant to compress.
6. **Blind metric:** Measure an error that can be small while the named observables or mechanism are wrong.
7. **Easier-model substitution:** Change the architecture, dynamics, data geometry, optimizer, scaling, or limit order that defines the question.
8. **Noncausal initialization:** Initialize from future observations or unavailable latent variables.
9. **Nonrestartable closure:** Match a curve from time zero but fail to evolve from an intermediate state when autonomy is part of the claim.
10. **Unbounded precision loophole:** Store arbitrary information in finitely many real numbers without a regularity, computability, or provenance restriction.

## 3. Claim ladder

Write separate propositions when the following are logically different:

| Rung | Claim |
|---|---|
| A | An exact identity or finite truncation is well defined |
| B | The truncated or surrogate dynamics are internally well posed |
| C | The surrogate matches tested instances |
| D | Successive approximations converge in the stated topology |
| E | The hierarchy limit equals the intended mathematical limit |
| F | The approximation is valid on every compact horizon |
| G | The approximation is uniform or stable for all time |
| H | Some admissible finite witness exists |
| W | The particular proposed witness succeeds |

Do not use evidence for C to assert D, or failure of W to reject H.

## 4. Sharp-conjecture template

Adapt this template rather than copying it mechanically:

> Let \(\mathcal C\) be the stated admissible class and let \(O[S](t)\) be the named observable of the canonical system \(S\). For every accuracy \(\varepsilon>0\), horizon \(T<\infty\), and required regularity bound \(R\), there exists an admissible autonomous approximation \(A_{\varepsilon,T,R}\) of complexity \(N(\varepsilon,T,R)\), independent of the ambient scale and of the realized future trajectory, whose coefficients and initial state are computable from the permitted source data, such that
> \[
> \sup_{S\in\mathcal C_R} d_T\!\left(O[S],O[A_{\varepsilon,T,R}[S]]\right)\le \varepsilon.
> \]
> The approximation remains restartable from its finite state and obeys the stated limit order and provenance restrictions.

Then specify:

- whether the bound is deterministic, in probability, almost sure, or in expectation;
- whether \(N\) may depend on the data dimension, sample count, or other fixed structural quantities;
- whether one construction works uniformly over \(\mathcal C_R\);
- what computable or regular coefficient class excludes real-number oracle encodings;
- what observation map compares the approximation to the target.

## 5. Falsifiers and witnesses

Name concrete outcomes with distinct logical force:

- **Witness falsifier:** disproves the current representation or closure.
- **Mechanism falsifier:** rejects a proposed reason for convergence or success.
- **Uniformity falsifier:** exhibits a family on which required complexity or error escapes.
- **Existence falsifier:** proves no admissible approximation in the full stated class can work.
- **Proof-route falsifier:** invalidates one argument while leaving the conjecture intact.

For each, state the exact assumption or rung it affects.

## 6. Contract-change rule

When evidence suggests changing the problem:

1. Preserve the original contract.
2. State the proposed change and scientific reason.
3. Explain whether it weakens, strengthens, or replaces the conjecture.
4. Obtain user direction when the change is material.
5. Never present results for the revised contract as answers to the original one.
