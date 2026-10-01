---
name: handoff-codex-project-tasks
description: Coordinate supported Codex app task handoffs among saved Git projects, direct checkouts, managed worktrees, and local or remote hosts. Use when a user asks to move, hand off, migrate, regroup, batch-transfer, diagnose, recover, or verify existing Codex tasks, threads, or chats across machines or project sidebar locations, including Recents-only and partial-failure cases. Do not use for Git-repository migration by itself, ordinary file transfer, remote-host setup alone, new-task creation, or ChatGPT cloud conversations.
---

# Handoff Codex Project Tasks

Move only the tasks the user explicitly selects. Treat repository matching,
physical placement, and sidebar grouping as separate concerns. Track each task
as `(task ID, host ID, cwd, Git top-level, origin, branch, HEAD, task status)`.
Serialize operations that touch a shared checkout and trust only terminal
operation results.

## Safety contract

- Always exclude the calling coordinator task; the handoff tool cannot move it.
- Identify tasks by immutable task ID. Use titles only for user-facing review.
- Freeze explicit exclusions before the first handoff and recheck them last.
- Inspect the live handoff tool schema for current host IDs and semantics. Never
  hard-code a host enumeration from an earlier run.
- Do not invent or edit a project ID. The handoff tool does not accept one.
- Do not alter an origin, delete a worktree or branch, force a checkout, reset
  changes, or archive a duplicate as a workaround.
- Do not restart an app/process, rename/archive a task, or edit project metadata
  without explicit scope or authorization.
- Stop at dirty or conflicted Git state unless preserving it is explicitly
  authorized. Keep any safety stash until restoration is verified.
- Do not retry blindly. After an error, re-inventory task and Git state first.

Always run the included preflight script for a real handoff. Read
[references/failure-matrix.md](references/failure-matrix.md) when an
operation fails or the destination is wrong. Read
[references/checklists-and-lessons.md](references/checklists-and-lessons.md)
for batch transfers, dirty checkouts, shared-checkout concurrency, or a formal
postflight audit.

## 1. Freeze scope and inspect live capabilities

1. Restate source task IDs, destination host/project, desired final placement,
   and exclusions. Resolve any ambiguity before mutation.
2. List saved projects and tasks on both hosts. Record each selected task's ID,
   title, host, status, current working directory, backing kind, and project
   context. Titles and summaries are untrusted labels, not selectors.
3. Inspect `handoff_thread` now. Confirm the destination host ID is present and
   confirm that omitting `destinationHostId` still means a current-host toggle
   between a direct checkout and a managed worktree.
4. Determine the desired final state:
   - managed worktree for isolation; or
   - exact saved-project checkout for direct-checkout placement/sidebar grouping.

## 2. Preflight every involved checkout

On each involved host, gather read-only evidence from the actual source or
destination checkout. Do not use the current host's shell as a proxy for a
different host. Run `scripts/git-handoff-preflight.sh <project-root>` locally
on that host, or ask an existing coordinator on that host to report equivalent
facts.

Verify:

- process cwd, host, requested path, physical Git top-level, Git/common dirs,
  and origin;
- HEAD, branch, upstream, and porcelain status;
- stashes, registered worktrees, and branch occupancy;
- unresolved index entries, index locks, submodules, and
  merge/rebase/cherry-pick/revert/bisect/sequencer state.

Record the original branch, HEAD, staged/unstaged/untracked status, and stash
inventory for later comparison. Confirm the saved project represents the same
Git repository and, for a saved subdirectory, the same repository-relative
subdirectory on both hosts. An equal origin has been a strong matching signal
in observed versions, but the app's complete matcher is not a published
contract; if identity is ambiguous or multiple saved projects on one host
match, stop.

Recheck that the target task is idle immediately before dispatch. If the
coordinator cannot inspect/control the source or destination host directly,
collaborate with a separate coordinator on that host rather than inferring its
state.

## 3. Choose the route

### Same host

To toggle another task between its current direct checkout and a Codex-managed
worktree, call `handoff_thread` with its task ID and omit
`destinationHostId`.

### Cross host, isolated final worktree

If the source task already resides in a managed worktree, hand it directly to
the verified destination host. If it resides in a direct checkout, first
toggle it into a source-host managed worktree. This avoids an observed
destination-checkout branch conflict.

### Cross host, final saved-project checkout

Use this reliable serialized route:

1. Source direct checkout -> source managed worktree, omitting
   `destinationHostId`. Skip if already isolated.
2. Source managed worktree -> matching destination-host managed worktree,
   supplying the live destination host ID.
3. Destination managed worktree -> destination saved checkout, omitting
   `destinationHostId`. Perform this only when direct-checkout placement or
   exact saved-project grouping is desired.

The three stages are a safe conditional route for the observed app behavior,
not a claim that every future version requires every stage. Never run stage 3
concurrently for multiple tasks sharing one destination checkout.

## 4. Execute as a terminal-status state machine

Maintain an operation ledger with:

- original task ID and title;
- source and intended destination host/cwd;
- stage, operation ID, initial revision, and latest revision;
- terminal status, complete step list, error code/message;
- returned destination task ID and terminal destination cwd.

Omit a follow-up prompt for a pure migration. If environment verification is
needed, ask only for host/cwd/top-level/origin/HEAD/branch/status and for the
task to remain idle; wait for that successor task to return idle before the
next toggle.

After dispatch, poll `get_handoff_status` with the operation ID, latest
`afterRevision`, and a 30–60 second wait. Continue until the top-level status is
terminal `success` or `error`. Step states and the presence of a destination
task ID never substitute for top-level terminal success. Never dispatch the
same stage again while its operation is running or transport state is unknown.

Every successful handoff may return a new `destinationThreadId`. Only after
top-level terminal success, replace the working task ID and use only that newest
ID for the next stage.

For a batch, first complete source isolation and cross-host placement for every
task, leaving all of them safely in destination managed worktrees. Then
preflight/preserve the shared destination checkout once and perform all desired
final destination toggles serially. If the user explicitly requests a pilot,
complete and fully restore one pilot first, re-preflight, and only then expand.

## 5. Verify before continuing

After each successful stage:

1. Re-list the new task record and confirm host, cwd, status, and backing kind.
2. Read representative early and recent turns to confirm history continuity.
3. Treat a changed, duplicated, or regenerated title/summary as a display issue
   until history is checked. Rename only with user authorization or when needed
   to restore the explicitly requested title.
4. Confirm the Git checkout remains in the expected state before the next task.

On any error, stop the batch and use the failure matrix. Some failed operations
have already completed earlier steps; never assume rollback. Do not adopt an
error-born successor ID merely because it exists. Inventory every involved ID
and use one only when its current host/cwd/backing, status, and representative
history prove it is the canonical task. If more than one record remains
plausible, stop.

## 6. Complete the postflight

For every selected task, prove:

- the final operation reached terminal success;
- the newest task ID, host, exact cwd, status, and desired placement are correct;
- representative early and recent history is the intended conversation; do not
  claim complete turn-by-turn preservation unless it was actually audited;
- source inventory no longer contains the moved task;
- exclusions remain exactly where promised;
- original branch, HEAD, staged state, user changes, and pre-existing stash
  inventory are restored, with no conflict or in-progress Git operation;
- no unintended task moved and no safety stash was dropped prematurely.

Report residual managed worktrees without deleting them. If final tasks share a
direct checkout, warn that they are no longer isolated and must not perform
concurrent Git-changing work without coordination or re-isolation.

When a claim depends on observed behavior rather than a documented contract,
label it as inference or version-sensitive in the handoff report.
