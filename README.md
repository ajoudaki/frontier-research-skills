# Personal Codex skills

This repository versions eight skills:

- `explain-with-canonical-notation`: canonical notation and self-contained mathematical presentation.
- `teach-technical-math`: source-grounded mathematical teaching.
- `solve-math-rigorously`: rigorous standalone mathematics and proofs.
- `investigate-conjectures`: mathematical and computational research workflows.
- `organize-research-project`: modular project organization, study isolation, promotion, and reproducible artifacts.
- `review-ai-paper`: evidence-backed reviews of AI research papers.
- `handoff-codex-project-tasks`: Codex project and task handoffs.
- `formalize-lean-theory`: DLTLean-dependent routing for source-faithful Lean formalization.

Each skill folder includes its `SKILL.md` and supporting resources. All skills
except the Lean snapshot are maintained here. Their installed personal folders at
`/home/amir/.codex/skills/<skill-name>` link directly to the matching folders in
this repository, so edits through either path affect the same files. The Lean
skill is a separate versioned import, described below.

## Validation

Validate any changed skill using the locally installed creator's validator:

```sh
python3 /home/amir/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./<skill-name>
```

Also inspect any changed references and UI metadata. Structural validation does
not establish that the instructions produce the intended behavior.

## Installation scope

The seven linked personal installations are available across projects. Activation
depends on the task, explicit invocation, and project instructions such as PDE's
`AGENTS.md`. Existing activation settings are preserved. Keep machine
configuration and credentials outside this repository.

The separate admin installations under `/etc/codex/skills/` are not maintained
here. Codex may list those alongside the personal versions; creating this
repository does not disable them.

Built-in `.system` skills and plugin-managed skills are outside this repo.

## Project organization skill

Use `$organize-research-project` to set up, adapt, or audit a large research
project. Its [entry point](organize-research-project/SKILL.md) selects focused
[references](organize-research-project/references/) and provides reusable
[project templates](organize-research-project/assets/templates/). Scientific
investigation, proof, teaching, and review remain separate skill responsibilities.
Adopted project workflows are versioned locally; updating this skill does not
automatically rewrite another project's policies.

## Lean skill import

`formalize-lean-theory/` is an unchanged copy of
`DLTLean/.agents/skills/formalize-lean-theory/` from DLTLean commit
`ad075b834c3e61f8237dd23b96d8c9f9fcb519e1`. DLTLean continues to maintain
and use its tracked project installation. This import is a versioned snapshot,
not an automatically synchronized installation. It has not been installed as a
global personal skill.

The router depends on the target project's `AGENTS.md`,
`FORMALIZATION_PLAYBOOK.md`, `README.md`,
`.agents/evals/formalize-lean-theory.yaml`, and local contract, status, and
corrections records. Copying its package does not make that workflow standalone.

From this repository, compare the imported package with DLTLean and run its
read-only integration check with the project root specified explicitly:

```sh
diff -r ./formalize-lean-theory /home/amir/Codes/DLTLean/.agents/skills/formalize-lean-theory
bash ./formalize-lean-theory/scripts/check-routes.sh --root /home/amir/Codes/DLTLean
```

The route checker validates DLTLean's project records and local skill package;
the comparison verifies that this imported package matches that installation.
To refresh the snapshot later, review changes in DLTLean, copy the package,
repeat these checks, and update the source commit recorded here.
