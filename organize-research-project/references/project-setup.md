# Set up or adapt a research project

## Separate the method from project choices

The reusable method defines evidence boundaries, ownership, reproducibility,
and how results become maintained dependencies. The project chooses scientific
objectives, documentation tools, paths, storage, collaboration mechanisms, and
the required review depth. Do not import a source project's model assumptions,
machine paths, archive names, or shared-checkout restrictions.

Before writing, identify existing instructions and accepted material. Preserve
them during migration. Inspect only the records authorized for the task; a
layout audit does not authorize reading all provisional research.

## Resolve the project contract

Record the following in the local workflow rather than a second registry:

| Decision | What must be explicit |
|---|---|
| Scientific authority | Maintained theory entry point, shared definitions or notation, reusable-code entry point |
| Studies | Location, ownership, scope, continuation rule, and permitted sources |
| Outputs | Run namespaces, retained inputs, storage locations, and retrieval method |
| Acceptance | Relevance, scientific review, integration checks, decision owner, and authorization |
| Collaboration | Allowed checkouts or worktrees, ownership of shared files, and Git coordination |
| Workflow version | Adopted skill revision, local modifications, and local policy revision |

Use the existing answers. For a new project, recommend simple defaults and
resolve consequential choices before a dependent operation. Review counts and
approval arrangements should be chosen before evaluating a candidate, not
relaxed because a particular candidate is hard to validate.

## Start with a small layout

One possible mapping is:

```text
AGENTS.md                    project entry instructions
RESEARCH_WORKFLOW.md          adopted policy and paths
docs/                        maintained theory and definitions
code/                        reusable implementation and reproduction recipes
studies/<study>/              study source and one current README
data/generated/<study>/<run>/ generated artifacts
data/established/<run>/       reproduction artifacts for maintained results
```

These names are examples. Preserve a project's existing `src/`, paper format,
data repository, or remote store. Map logical run identifiers to physical
locations when artifacts live elsewhere. Avoid a single mutable output file
shared by several studies or runs.

Create only the files and entry points needed now. Mark an empty maintained
corpus as empty; do not populate it with invented accepted results. A project
index may list neutral study questions, locations, owners, and lifecycle state
without exposing provisional findings to unrelated investigations.

## Adopt versioned project rules

Use these assets:

- [Project instructions](../assets/templates/AGENTS.md.template).
- [Local research workflow](../assets/templates/RESEARCH_WORKFLOW.md.template).
- [Study current record](../assets/templates/study-README.md.template).

Treat them as editable starting points, not files to copy over existing work.
Merge the necessary clauses into an established project. In a new project,
replace every `{{PLACEHOLDER}}` with an actual decision or an explicit
not-applicable entry. Resolve any decision required for the requested next
action; an unresolved acceptance policy blocks promotion, not ordinary reading.

The generated workflow must stand on its own. Include the applicable operating
rules from the modules; do not make the project depend on changing instructions
in a personal skill installation. The template supplies a compact baseline;
extend a section only when the selected policy needs additional detail.

Record the adopted skill tag or commit and local deviations. If copying a dirty
skill tree, identify the actual content snapshot as well; a base commit alone
does not identify those instructions. Updating this skill later is an invitation
to review a policy update, not automatic authorization to change active studies.

If a workflow changes during an investigation, record its effective scope and
which open checks need repeating. Do not silently invalidate earlier evidence
or retrospectively declare it reviewed under the new procedure.

## Verify the adoption

Check that paths and links resolve, placeholders are gone, adopted rules agree,
and each proposed action has a responsible role. Verify the handling of a new
study, an unchanged continuation, an unavailable review, and a routine repair.
For a claimed independent review, check the actual input boundary, not only its
folder name. Do not run a scientific experiment to validate these instructions.

Use ordinary file ownership and Git precautions. A shared index needs one
coordinated writer for each staging/commit transaction; separate worktrees need
an explicit merge owner. Neither arrangement is mandatory for every project.
