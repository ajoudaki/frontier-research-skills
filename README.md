# Frontier research skills

Agent skills for doing open-ended research with today's most capable models
without losing control.

Capable models can now do real research, but on an open question they produce
far more than you can check, and their mistakes are silent: the prose, the
figures, even the math look right while one hidden assumption sinks the result.
The result is a haystack that may hold a gem, and finding it costs more time
than the agents saved. These skills are the habits I developed to keep the
signal-to-noise ratio high. They are not a principled framework, just what
worked for me, mostly in theoretical research.

## The strategy

1. **Start from one open-ended question.**
2. **Organize it into research thrusts.** Each is an isolated study with its own
   question, inputs and folder, pushed forward by its own agents. Most advance
   step by step; some split, and some stop.
3. **Promote only what passes a gate into an established core.** A result enters
   the core when an independent review finds it correct, it fits the
   maintained notation, interfaces and tests, and you judge it relevant.
   Everything else stays outside, with its evidence kept. You read the core,
   not the haystack, and new studies build on it.
4. **Carve out a paper and audit it again**, this time for novelty and
   significance as well as correctness.

Inside each thrust, many agents do the work instead of one long thread: one
thread anchors on its early mistakes, while fresh agents with separate inputs
can catch what the others missed, and an author and a critic can argue a claim
round after round until the objections are resolved.

## The skills

| Skill | What it does |
|---|---|
| [`organize-research-project`](organize-research-project/SKILL.md) | The architecture: isolated studies, a promotion gate into maintained theory and code, reproducible runs and figures, and templates for a project's own workflow. |
| [`formulate-problem`](formulate-problem/SKILL.md) | Pins a thrust's question down as a research contract (question, definitions, quantifier order, evidence standard, scope) and freezes it, then pursues it adversarially: claim map, evidence ledger, hostile audit, decisive experiments, and a bounded multi-route proof search with a route registry. |
| [`solve-problem`](solve-problem/SKILL.md) | Writes the solution: the strongest reasonable reading of the question, the plan before a long proof, every nontrivial step derived, each external theorem stated with its hypotheses checked, and an answer to exactly the question asked. |
| [`teach-material`](teach-material/SKILL.md) | Teaches a result or source in layers: canonical notation, the idea, a toy example, then every step, with cited theorems checked; a confusing block is rebuilt, not patched. |
| [`review-paper`](review-paper/SKILL.md) | Audits a paper and its code: a ledger of the central claims, re-derived proofs, retrieved citations, code treated as untrusted, calibrated severity that cascades to dependent claims, and confidence limited to what was checked. |
| [`explain-canonically`](explain-canonically/SKILL.md) | A companion to the others: canonical notation, typed symbols defined before use, and self-contained presentation. |

`organize-research-project` runs the whole project. Inside each thrust,
`formulate-problem`, `solve-problem` and `teach-material` take a question from
vague to precise, to proved, to understood. `review-paper` audits what becomes
a paper, and its findings can start the next round.

## Install

The skills are plain folders with a `SKILL.md`, so they work with any agent
that reads skills, including Claude Code and Codex.

```sh
git clone https://github.com/ajoudaki/frontier-research-skills
cd frontier-research-skills
for s in organize-research-project formulate-problem solve-problem \
         teach-material review-paper explain-canonically; do
  ln -s "$PWD/$s" ~/.claude/skills/$s   # or ~/.codex/skills/$s for Codex
done
```

A skill loads when you name it or when a task matches its description. To make
one a project's default, name it in the project's `AGENTS.md` or `CLAUDE.md`.
`organize-research-project` can set up that file and the project's workflow
for you; the adopted workflow is versioned in the project, so later changes to
the skill do not silently rewrite it.

**Renamed in 0.2.0:** `investigate-conjectures` is now `formulate-problem`,
`solve-math-rigorously` is `solve-problem`, `teach-technical-math` is
`teach-material`, `review-ai-paper` is `review-paper`, and
`explain-with-canonical-notation` is `explain-canonically`. Update existing
links and any project instructions that use the old names.

## In practice

I have used these skills on a deep-learning theory project: about 235 studies
in eleven weeks, of which only a small fraction made it into the core.

## The talk

[`talk/`](talk/) holds the talk "Open-ended research with AI agents":

- `deck.html`, the slides. Arrow keys step through the builds, `N` shows the
  speaker notes, `P` opens a presenter window with the next build, the notes
  and a timer, and `F` toggles fullscreen.
- `Research_with_AI_Agents_static.pdf` (one page per state that matters) and
  `Research_with_AI_Agents_steps.pdf` (every build step).
- `speaker-notes.md`, the full script.
- `Research_with_AI_Agents.pdf`, the slides of the talk as first given.

The slides are generated by the scripts in `talk/slides/`; see
`talk/build_deck.py` for the build.

## What's next

- **Beyond theory.** The skills are theory-first; adapting them to other
  domains should be straightforward.
- **Evaluations.** There is no way yet to tell whether a change to a skill
  really improves it.
- **Live skills.** A process that watches your sessions, adapts the skills and
  writes new ones, checked by those evaluations.

## Validation

Validate a changed skill with the validator supplied by `skill-creator`:

```sh
python3 "<skill-creator-directory>/scripts/quick_validate.py" "./<skill-name>"
```

Structural validation does not establish that the instructions produce the
intended behavior; inspect changed references and metadata too.
