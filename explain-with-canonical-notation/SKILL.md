---
name: explain-with-canonical-notation
description: Use when explaining, deriving, writing, or reviewing mathematics, including proofs, research notes, and scientific interpretations of experiments. Govern symbol introduction, explicit definitions, self-contained presentation, and compact canonical notation. Applies beyond teaching; skip purely operational work with no mathematical content.
---

# Explain with canonical notation

Minimize the reader's translation work between the explanation and the thing
being explained. Make the mechanism visible through familiar objects and a
coherent representation. Optimize for understanding, not merely fewer symbols.

Apply this guidance whenever producing mathematical content in conversation or
written artifacts, including derivations, proofs, research notes, reviews, and
scientific interpretations of experiments. Do not wait for a request to teach
or explain. Purely operational work with no mathematical content does not need
the full skill.

This skill governs notation and presentation alongside the task's research,
proof, review, or teaching workflow. It does not impose a new research program,
a comprehensive source audit, extra tool use, or a fixed lesson pace, and does
not cancel source-reading requirements of an applicable workflow. Preserve the
user's requested scope and existing authorization.

Use each subject's own established objects and conventions; do not impose one
field's notation on another.

## Explanatory principles

- **Start with the natural objects.** Anchor the account in the quantities,
  states, operations, and relationships the subject actually uses. Prefer its
  recognizable representation over a private alphabet of aliases.
- **Make every abstraction earn its place.** Introduce a name when it reveals
  structure or materially simplifies reasoning. Avoid naming a compound
  expression only to make a displayed equation look short.
- **Define through construction.** Give a central object's formula, rule, or
  procedure in already defined quantities. Calling it a response, correction,
  or interaction is an interpretation, not a definition.
- **Keep the requested passage self-contained.** Include the setup, definitions,
  assumptions, and intermediate relations needed to follow it. Do not make the
  reader recover a central definition from an earlier message or guess an
  omitted dependency. Recall only what this passage needs.
- **Compactify through structure.** Use shared patterns, recursions, inner
  products, and decompositions to shorten explanations while preserving their
  meaning. Neither sprawling component expansions nor opaque shorthand is
  automatically clearer.
- **Maintain one coherent representation.** Connect an original system to its
  aggregate, transformed, or approximate description explicitly. Preserve
  notation wherever its meaning is unchanged.
- **Treat corrections as guidance for the whole passage.** When a reader
  objects to the representation, rewrite the relevant block consistently.
  Do not add another notation patch while leaving the confusing structure.

## Define objects and dependencies

Define a symbol before using it in an argument or formula, or alongside its
first defining formula. For a central object, state its mathematical type, index
roles, and whether it is fixed, evolving, or computed from something else. Use
its actual definition, not a new name standing in for an unexplained formula.

Keep the state, its numerical representation, and quantities evaluated from it
distinct. Identify which system a variable belongs to when multiple models or
approximations coexist. If labels or time arguments are suppressed, state that
convention once.

Follow the user's explicitly requested or previously agreed conventions.
Otherwise preserve the applicable project notation contract and source notation;
use established domain notation for new objects. When translating, give the exact
correspondence, including signs, normalization, scales, and constant factors.
Do not silently modify the model or rename unrelated existing material to fit a
preferred notation.

Distinguish quantities with similar names but different roles: a current value,
a stored history, an average, a derivative, and a directional response are not
interchangeable. A label or index may identify a contribution to a shared
object rather than a separate object.

## Organize the requested explanation

For a complete construction, adapt this order to the subject:

1. Setup, objects, and conventions.
2. State and fixed data.
3. Algebraic evaluation or reconstruction.
4. Evolution or algorithmic updates, with initialization.
5. Observables and exact derived relationships.
6. Any approximation and its guarantees or limitations.

Adapt these steps to the domain's natural operations instead of forcing this
vocabulary.

Show the origin of each important term by the necessary substitution,
differentiation, or logical step. Explain how recursively computed quantities
are evaluated and why the dependencies are well defined. A recursion for
velocities does not automatically give a recursion for stored states.

For a focused follow-up, answer that question with only the necessary recall.
For a requested full rewrite, deliver the whole relevant construction rather
than restarting a staged lesson or offering only a plan.

## Keep notation compact and honest

Use aligned equations and standard operations where they make structure
visible. Attach transpose directly, as in \(A^\top\), without unnecessary
parentheses around the object. Define non-obvious products and conventions.

Do not silently turn an actual derivative into a gradient, an independently
normalized direction, or a different-time derivative. Track factors when
rewriting expressions using flows or other derived quantities.

Handle vanishing denominators. Algebraic cancellation from known formulas can
define a regular coefficient where a displayed quotient cannot be evaluated.
An identity with a vanishing prefactor does not, on its own, determine that
coefficient there.

Preserve asymmetric pairings when they come from distinct roles. Do not
symmetrize an expression for appearance or identify it with a standard kernel
or operator without checking the definition, scaling, and relevant properties.

## Separate mathematical claims

Mark the first approximation. An exact observable identity is not a closed
reduced model if evaluating its coefficients still requires the full state.

When explaining a reduction, identify what is retained, frozen, and evolved;
how its initial data are obtained; and what information evaluates its updates.
Count moving coordinates and fixed coefficient storage separately, including
the provenance or cost of producing the coefficients when relevant.

Distinguish internal consistency, autonomy, equilibrium, convergence, fitting,
and approximation accuracy. Attach guarantees to their actual assumptions,
reference system, observable, horizon, norm, and parameter dependence.

## Write for understanding

Use connected prose around the equations. Explain why a term appears, not only
what it is called. Keep the notation economical without leaving the central
object undefined or concealing a necessary dependency.

Treat these instructions as guidance for producing a clear explanation, not
a checklist to recite to the user. Preserve conventions agreed during the
conversation, and incorporate later corrections throughout subsequent work.
