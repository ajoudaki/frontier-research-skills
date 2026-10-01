# Neural-network and response-memory conventions

Read this reference when explaining, deriving, writing, or reviewing mathematics
involving neural networks, training flows, or response-memory closures. These are
presentation defaults for the relevant model, not a replacement for its actual
equations. Explicit user choices and previously agreed conventions take precedence.

## Canonical layer notation

Prefer:

- \(W^{(\ell)}\): layer weights.
- \(z_a^{(\ell)}\): preactivations.
- \(h_a^{(\ell)}\): activations.
- \(\phi\): activation function.
- \(L\): number of hidden layers; \(\mathcal L\): loss.
- \(W^{(L+1)}\): readout when adopting this layer convention.
- \(m\): number of training examples; \(n\): width; \(d\): input dimension.
- \(a,b,c\): sample indices; \(\ell\): layer index.
- \(q\): closure order; \(j=0,\ldots,q-1\): Legendre mode index.

Specify matrix and vector shapes when first needed. Use layer-dependent widths
if the model has them. Distinguish mode, neuron, input-coordinate, and sample
indices where they appear together.

Keep the model's actual normalizations and mobilities. Factors such as \(1/n\),
\(1/\sqrt d\), and \(2\) are not universal conventions. Map a source's readout
vector or other notation explicitly before using the layer convention above.

## Stored memories

For the corresponding response-memory construction, preserve the moment names

\[
\bar h_{a,j}^{(\ell-1)}, \qquad \bar\delta_{a,j}^{(\ell)}.
\]

Do not replace them with keys, values, \(k\), \(v\), or another alias merely for
brevity. Keep these meanings distinct:

- \(h_a^{(\ell)}\): a current activation.
- \(\bar h_{a,j}^{(\ell)}\): a stored history moment.
- \(\dot{\bar h}_{a,j}^{(\ell)}\): that moment's time derivative.

A stored moment is not automatically a normalized average or a projection
coefficient. State the required clock normalization and Legendre weights.
Define the clock, initialization, and initial-history prefix when they affect
the memory. Do not replace a historical pairing by a current-current or
history-history pairing without deriving the change.

## Physical flows and sample contributions

Use dots for derivatives with respect to physical training time. If a different
clock is chosen, explicitly change the derivative convention.

Use a sample index for a sample's contribution to the shared weight velocity:

\[
\dot W^{(\ell)} = \sum_a \dot W_a^{(\ell)}.
\]

By default, \(\dot W_a^{(\ell)}\) includes its residual factor. It is not the
derivative of a separately stored sample-specific weight. The total velocity
has no sample subscript.

Memory objects already identify their sample. Use

\[
\dot{\bar h}_{a,j}^{(\ell)}, \qquad
\dot{\bar\delta}_{a,j}^{(\ell)}.
\]

Do not add redundant flow labels such as [b], arrows between samples, or
fictitious sample clocks. When an evaluated sample and a driving sample truly
require separate indices, define both roles.

Never silently reinterpret an actual velocity as a unit-residual direction,
gradient, or response coefficient. A sample's full physical contribution and
its contribution per unit residual have different normalizations.

## Compact flow expressions

Use inner products of weight or memory velocities when they simplify a
chain-rule expression. Define the Frobenius inner product when needed:

\[
\langle U,V\rangle_F = \operatorname{tr}(U^\top V).
\]

If two velocities contain \(r_a\) and \(r_b\), their inner product contains
\(r_a r_b\). Preserve these factors. At zero residual, compute an underlying
response coefficient from its regular state-based formula or by first
cancelling explicit factors in the known update expressions. Do not numerically
divide zero velocities by zero residuals. A product identity with prefactor
\(r_a r_b\) does not itself define the coefficient when that prefactor vanishes.

Check which memory velocities represent current error-driven writes. In
Legendre closures, higher-mode velocities can also contain clock-driven mode
mixing. Do not substitute them for current backward responses without checking
the exact equations.

Prefer a valid recursion involving already defined quantities over introducing
a new backward-signal symbol merely to abbreviate a chain-rule expression.
State the computation order, and distinguish a recursion for moment velocities
from a recursion for the stored moments themselves.

## Formula typography

Attach transpose directly:

\[
W^{(\ell)\top}, \qquad h_a^{(\ell)\top}, \qquad
\bar h_{a,j}^{(\ell)\top}.
\]

Avoid wrapping these objects in extra parentheses just to transpose them.
Use \(\odot\) for componentwise multiplication, aligned equations for related
updates, and standard inner products instead of long component sums when the
meaning remains explicit.

## Response coefficients and reduced models

Define a coefficient such as \(C_{ab}\) by its actual formula in the established
variables, not only by calling it a response. Identify the evaluated sample,
driving sample, contributing update paths, and any separately accounted clock
or memory-motion terms. Explain what state supplies its value.

When comparing with a tangent kernel, check the precise parameter derivatives,
learning-rate and loss factors, and whether the result is a symmetric Gram
matrix. Current-versus-history pairings need not have that structure.
Nonsymmetry alone does not imply a negative quadratic form: the symmetric part
determines that form.

Distinguish dense-network variables, order-q closure variables, and a further
scalar approximation. If model labels are suppressed for readability, state
which model all displayed weights and features belong to.

For a complete neural construction, present the setup and state, reconstruction,
forward pass and loss, autonomous equations and initialization, exact aggregate
equations, and then the proposed scalar approximation. Explain precisely where
the approximation begins.

A residual identity with coefficients depending on the evolving network is not
already a finite autonomous aggregate closure. If coefficients are frozen,
specify the switching state, saved coefficients, evolving reduced variables,
and their initialization. Count fixed storage separately from evolving state,
and disclose how the switching data were produced.

Residual-zero stopping, fitting, stable continuation, observable accuracy, and
approximation to dense training are separate claims. State each claim's actual
conditions and reference system.
