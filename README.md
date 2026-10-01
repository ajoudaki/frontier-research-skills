# Reusable Codex skills

This repository versions seven independently packaged skills:

- `explain-with-canonical-notation`: canonical notation and self-contained mathematical presentation.
- `teach-technical-math`: source-grounded mathematical teaching.
- `solve-math-rigorously`: rigorous standalone mathematics and proofs.
- `investigate-conjectures`: mathematical and computational research workflows.
- `organize-research-project`: modular project organization, study isolation, promotion, and reproducible artifacts.
- `review-ai-paper`: evidence-backed reviews of AI research papers.
- `handoff-codex-project-tasks`: Codex project and task handoffs.

Each top-level skill directory contains its `SKILL.md` and any supporting
resources needed by that skill. The packages do not assume a particular user,
machine, checkout location, research project, or installation scope.

Install a package using the method supported by the target Codex environment,
such as a skill installer, a copy, or a symbolic link. Activation is governed by
the package description and metadata together with explicit invocation and any
applicable project instructions. Keep machine configuration and credentials
outside this repository.

## Validation

Validate a changed package with the validator supplied by `skill-creator`:

```sh
python3 "<skill-creator-directory>/scripts/quick_validate.py" "./<skill-name>"
```

Also inspect any changed references and UI metadata. Structural validation does
not establish that the instructions produce the intended behavior.

## Project organization skill

Use `$organize-research-project` to set up, adapt, or audit a large research
project. Its [entry point](organize-research-project/SKILL.md) selects focused
[references](organize-research-project/references/) and provides reusable
[project templates](organize-research-project/assets/templates/). Scientific
investigation, proof, teaching, and review remain separate skill responsibilities.
Adopted project workflows are versioned locally; updating this skill does not
automatically rewrite another project's policies.
