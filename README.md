# Personal Codex skills

The authoritative source for six personal skills, versioned together:

- `explain-with-canonical-notation`: canonical notation and self-contained mathematical presentation.
- `teach-technical-math`: source-grounded mathematical teaching.
- `solve-math-rigorously`: rigorous standalone mathematics and proofs.
- `investigate-conjectures`: mathematical and computational research workflows.
- `review-ai-paper`: evidence-backed reviews of AI research papers.
- `handoff-codex-project-tasks`: Codex project and task handoffs.

Each skill folder includes its `SKILL.md` and supporting resources. Edit those
files here and commit the relevant paths. Installed personal skill folders at
`/home/amir/.codex/skills/<skill-name>` link directly to the matching folders in
this repository, so edits through either path affect the same files.

## Validation

Validate any changed skill using the locally installed creator's validator:

```sh
python3 /home/amir/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./<skill-name>
```

Also inspect any changed references and UI metadata. Structural validation does
not establish that the instructions produce the intended behavior.

## Installation scope

These are personal installations, available across projects. Activation depends
on the task, explicit invocation, and project instructions such as PDE's
`AGENTS.md`. Existing activation settings are preserved. Keep machine
configuration and credentials outside this repository.

The separate admin installations under `/etc/codex/skills/` are not maintained
here. Codex may list those alongside the personal versions; creating this
repository does not disable them.

`formalize-lean-theory` remains maintained separately in the DLTLean repository.
Built-in `.system` skills and plugin-managed skills are also outside this repo.
