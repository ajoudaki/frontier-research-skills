# Checklists and evidence-backed lessons

## Scope record

Before mutation, write a compact manifest:

```text
source host:
source saved-project root:
destination host:
destination saved-project root:
desired final placement: managed worktree | direct saved checkout
selected task IDs and reviewed titles:
explicitly excluded task IDs and titles:
whether active tasks may be interrupted:
authorization for dirty-state preservation: yes | no
calling coordinator task ID (always excluded):
```

Never select by title alone. Titles can collide, receive a suffix, or be
regenerated from older history after handoff.

## Per-host Git preflight

Use the included script on the actual host for each involved root:

```sh
scripts/git-handoff-preflight.sh <project-root>
```

Review all output; the script diagnoses but does not decide safety. In addition,
verify any repository-specific worktree include/ignore behavior if nontracked
files are expected to matter.

Safe default preconditions:

- exact source and destination repository identity and repository-relative
  saved subdirectory are understood;
- both saved checkouts have known branch/HEAD/status;
- no merge, rebase, cherry-pick, revert, bisect, sequencer, or conflict exists;
- relevant branches are not unexpectedly occupied by another worktree;
- task source status is idle, or interruption is explicitly acceptable;
- destination host ID comes from the live schema;
- source and destination tasks/projects are distinguished by IDs and roots.

## Operation ledger template

Use one row per stage, not one row per original task:

| Original task ID | Working task ID | Stage | Source host/cwd | Destination host/cwd | Operation ID | Start/latest revision | Terminal status | Returned task ID | Error code/message |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Append the complete terminal step list beneath any error. A failed operation may
have changed state before failing.

## Batch discipline

Use the phase order in `Batch order` below. If the user explicitly requests a
controlled pilot, or the route has not yet been validated for the repository,
migrate one representative task through the complete route, fully restore and
verify the checkout, re-preflight, and only then expand. Otherwise do not
introduce a full pilot that would install a branch in the shared destination
checkout before the remaining cross-host stages.

In every batch, re-list source and destination inventories after each task and
never move the coordinator or an exclusion.

## Final verification checklist

- [ ] Every recorded operation is terminal, not merely step-complete.
- [ ] Every selected task has one known newest ID.
- [ ] Each final task has the intended host, exact cwd, status, and backing kind.
- [ ] Representative early and recent turns prove conversation continuity.
- [ ] Display titles were verified or restored only after identity checks.
- [ ] The source contains no selected task and still contains all exclusions.
- [ ] The destination contains all selected tasks and no unintended task.
- [ ] Original branch, HEAD, staged state, user changes, and pre-existing stashes
      are restored.
- [ ] No new conflict or in-progress Git operation exists.
- [ ] Any preservation stash was verified before being dropped.
- [ ] Residual managed worktrees were reported and left intact.
- [ ] Shared direct-checkout tasks received a concurrency warning.

## What two controlled migrations established

The following behaviors were directly observed across two repositories moved
from a local saved checkout to an SSH-hosted saved checkout:

- successful handoff stages can create new task IDs;
- current-host omission toggled a task between checkout and managed worktree;
- direct cross-host placement could fail because the destination checkout was
  using the handoff branch;
- checkout -> source worktree -> destination worktree succeeded reliably;
- cross-host success alone left tasks in destination managed worktrees/Recents;
- a final destination-host toggle placed tasks at the exact saved checkout;
- a dirty destination checkout blocked that final toggle;
- a failed operation could show earlier steps already completed;
- terminal status could remain `running` after all visible steps said `done`;
- titles/summaries could be duplicated or regenerated while history remained
  the intended conversation;
- project metadata could remain null even after correct direct-checkout grouping;
- detached managed worktrees could remain after success and did not need deletion.

## Evidence, inference, and version sensitivity

### Directly documented by the live tool schema

- `handoff_thread` moves another task, not the calling task.
- omitting `destinationHostId` performs the current-host checkout/worktree toggle.
- selecting another host targets a matching saved-project worktree.
- running tasks may be interrupted.
- cloud handoff is unsupported.
- status polling is revisioned and bounded.

Always inspect the live schema because host enums and behavior may change.

### Strong evidence-backed inference

- Git repository identity, especially observed origin identity, strongly affects
  destination project matching.
- exact final cwd matching the saved-project root strongly affects sidebar
  grouping, even when `projectId` is null.
- labels alone do not establish matching or grouping.

Do not present these as published app contracts.

### Version-sensitive observations

- one full local desktop-process restart changed stale matching behavior after
  repository identity had been corrected and verified, while a remote runtime
  restart did not; the causal repair remains unproven;
- exact matcher normalization and cache invalidation are unknown;
- exact operation step names and revision counts can change;
- worktree cleanup and display-title regeneration can change;
- whether the three-stage route remains necessary in all future versions is
  unknown.

## Concurrency and placement tradeoff

A managed worktree isolates a task's Git state. Multiple tasks placed at one
saved-project checkout share branch and working-tree state. Sidebar convenience
therefore trades away isolation. Serialize Git-changing work there, or toggle an
active task back into a managed worktree before parallel development.

## Anti-patterns

- choosing a task by title or a host by display name;
- treating equal project labels as repository identity;
- assuming cross-host success also means saved-project sidebar grouping;
- fabricating a project ID or editing origins to influence matching;
- polling without the latest revision, or redispatching while still running;
- continuing after failure without a fresh inventory;
- using a stale task ID after a successful stage;
- toggling multiple tasks into one checkout concurrently;
- creating an unlabeled stash, immediately popping it, or dropping before verify;
- forcing a branch, resetting changes, or deleting a managed worktree as repair;
- promising that ignored or machine-local files migrate;
- archiving apparent duplicates before history and identity are proven;
- moving the calling coordinator task.

## Batch order

For several tasks with a shared destination checkout, prefer phase batching:

1. Perform source checkout -> source worktree when needed, then cross-host
   placement, for each task.
2. Confirm every task is safely isolated in a destination managed worktree.
3. Preflight and, only if authorized, preserve the shared destination checkout
   once.
4. Perform each requested destination worktree -> saved-checkout toggle
   serially, waiting for terminal success and successor idle state each time.
5. Restore and verify the destination checkout once after the final toggle.

This avoids a later cross-host stage colliding with a branch installed in the
shared checkout by an earlier regrouping stage. If an untested route requires a
pilot, complete and restore one pilot, re-preflight, then use the phase order.
