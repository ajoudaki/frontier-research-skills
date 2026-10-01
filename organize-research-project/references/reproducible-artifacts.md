# Reproducible runs, data, and figures

Separate authored scientific material from generated products while preserving
their exact relationship. Synchronized storage means identifiable, retrievable
versions with consistent references; matching directory names alone do not
establish which source produced a figure.

## Keep authoritative source retrievable

Version proofs, source code, configurations, test definitions, and reproduction
recipes. Keep maintained APIs separate from experiment-specific drivers. No
unique argument or essential hand-written configuration should exist only in
an ignored output directory or a transient tool session.

Use a fresh run identifier and output namespace for each execution that becomes
evidence. Preserve consumed inputs and previous runs. A separate convenience
pointer may identify the latest run, but citations must identify the actual run.

Choose storage appropriate to the project: ordinary files, a separate data
repository, or a remote artifact store. Large outputs need not enter the source
Git repository. Small reference fixtures may be versioned there when useful.
Record retrieval, access requirements, retention, and integrity information for
external data. A checksum verifies available bytes; it does not preserve them.

## Plan an authorized experiment before executing it

Record its question, competing explanations, controls, primary metrics,
numerical validity checks, seed or replication rule, resource budget, stopping
condition, and what would count as success, failure, or inconclusive evidence.
Scale the record to the experiment. A routine deterministic regression test
does not need a new research campaign or extensive preregistration document.

A request to organize outputs or design an experiment does not authorize
running it. Record executed checks separately from planned ones.

## Record enough provenance to reproduce the claim

Use the run's existing metadata or current study record; a new file format is
not mandatory. Preserve the applicable fields:

- Study, run identity, purpose, and scientific scope.
- Exact input identity and durable location, including selection or splits.
- Source revision and relevant dirty source/configuration hashes or snapshot.
- Command, working directory, parameters, random seeds, and environment.
- Numerical precision, relevant software versions, hardware and thread settings
  when they can affect the result or its interpretation.
- Exit status, validity checks, metrics, uncertainty, and unresolved failures.
- Output locations and integrity checks; analysis and figure-generation source.

Repeatability may be statistical rather than bit-for-bit. State the appropriate
criterion and numerical tolerances. An old result array or a redrawn plot does
not constitute a fresh reproduction of the upstream experiment.

## Keep figures attached to their evidence

Trace each reported figure or table through analysis settings to its actual
runs and inputs. When copying a selected figure into a paper or documentation,
retain its run identity and generation recipe. A changed run or analysis must
update the figure's provenance and the interpretation that depends on it.

For a storage move, verify the destination contents and update references as
one controlled operation. Keep the source until the new location is verified;
the storage policy governs later deletion. Do not overwrite an old run to make
a report appear synchronized with newer code.

## Maintain accepted reproductions

At promotion, provide a reproduction route through maintained source and
retained inputs, independent of private study paths or conversation history.
Run it in a fresh namespace and record its result. Distinguish the scientific
claim, its numerical verification, and the portability of its reproduction.

Do not discard costly or unavailable raw inputs merely because most outputs
are generated. Document what can actually be regenerated and retain the rest
under the project's storage policy. Failed and interrupted runs stay labelled
with their observed status and cannot silently become positive evidence.
