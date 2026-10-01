# Handoff failure matrix

Use exact errors and live state as evidence. Do not normalize an error into a
generic diagnosis before recording the complete tool response.

| Signal | Likely meaning | Safe response | Stop condition |
| --- | --- | --- | --- |
| `No matching saved project was found on <host>.` | The destination matcher did not find an eligible saved project. This can be a saved-project, host-connectivity, repository-identity, subdirectory, or stale-discovery problem. In observed pilots, no asynchronous operation was created. | List destination projects, live host IDs, roots, origins, and repository-relative saved subdirectories. Compare identity on both hosts. | Different/ambiguous identity, multiple plausible matches, unavailable host, or repeated failure. Never edit origins merely to satisfy matching. Restart is separate, explicitly authorized troubleshooting—not a default migration step. |
| `Failed to continue on another host: Destination checkout is already using the handoff branch, and Codex could not switch it to a default branch` | A direct cross-host transfer collided with branch occupancy in the saved checkout. | Re-inventory because the failed operation may have done some work. If safe, toggle the source task from its direct checkout to a source managed worktree, then hand off that newest task ID cross-host. | Dirty/conflicted state, an occupied branch that cannot be moved safely, or uncertainty about which task/branch now owns the worktree. |
| `Stash or commit your local changes to hand off.` | The current-host toggle needs a clean direct checkout. | Stop. With explicit authorization, preserve tracked and untracked changes using the procedure below. Otherwise ask the user to clean or commit them. | No authorization, any conflict/in-progress Git operation, or changes whose ownership is unclear. |
| Cross-host success but task appears only in Recents or a generated worktree path | Transfer succeeded physically, but the task is still isolated in a destination managed worktree. | If the user wants direct saved-project grouping, toggle the newest destination task on the destination host with `destinationHostId` omitted, then verify exact cwd. | Dirty destination checkout or uncertainty about whether shared-checkout placement is desired. |
| Step rows appear complete, or a destination task ID exists, but top-level status is `running` | Step progress, successor allocation, and operation finalization are distinct. | Keep polling the same operation with the latest revision and a bounded wait. Do not consume the successor ID yet. | Connectivity loss that prevents status retrieval; report and do not redispatch. |
| Error after one or more steps say `done`, possibly with a successor ID | The operation may have partially changed task, branch, worktree, or task-record state. | Re-list every involved task ID, worktree, branch, cwd, backing kind, status, operation field, and representative history. Adopt an error-born successor only when this evidence proves it is canonical. | More than one plausible current task, missing history, or state that cannot be mapped unambiguously. |
| Returned `destinationThreadId` differs from source ID | Normal identity transition for a successful stage. | Update the ledger and use the returned ID exclusively. Re-list and verify history. | The returned task cannot be found or history is not the intended conversation. |
| Duplicate title, `(2)` suffix, or title/summary reverts to an old topic | Display metadata may be regenerated from old history. | Match by ID, host, cwd, timestamps, and representative history. Rename only after identity is proven. | History belongs to a different conversation. |
| Stash apply reports conflicts | Preserved user changes do not restore cleanly onto the current checkout state. | Stop, retain the stash, report exact conflicts and current branch/status. | Always. Do not drop the stash, reset, or auto-resolve without explicit authority. |
| Task is active | Handoff may interrupt it. | Confirm interruption is acceptable; otherwise wait for idle. | Work would be lost or the user has not authorized interruption. |
| Destination host is absent from the live enum | The destination is not currently available to the handoff tool. | Report the current candidates and diagnose host connectivity separately. | Do not substitute a similarly named host ID. |
| Calling task selected | The tool cannot move its own task. | Use a separate coordinator task on the appropriate host. | Always for the current task. |
| Cloud-backed source or destination | Cross-host cloud handoff is unsupported by the observed/live tool contract. | Explain the constraint and stop. | Always for this workflow. |
| `fatal: '<branch>' is already used by worktree at '<path>'` | Git's one-branch-per-worktree constraint is active. | Inventory branch ownership and use supported Handoff or coordinate a safe release under separate authorization. | Never force-switch, detach/delete another worktree, or prune to clear it. |
| Required ignored, nested-repository, or submodule files are absent | Ordinary stash/worktree transfer does not cover every machine-local file category. | Inventory separately and choose an explicit supported transfer/configuration strategy. | Secrets, unclear ownership, dirty nested repositories, or dirty submodule worktrees. |

## Authorized preservation of a dirty checkout

This is an exceptional recovery path, not the default preflight.

1. Record exact branch, HEAD, porcelain status, stash list, and in-progress Git
   markers. Stop if a merge, rebase, cherry-pick, revert, bisect, sequencer, or
   conflict is active.
2. Obtain explicit permission to preserve and restore the changes.
3. Serialize other repository activity. Create a uniquely labeled stash
   including untracked files. Immediately record its commit OID and message; do
   not rely only on its ordinal position.
4. Verify the checkout is clean and the stash exists before handoff.
5. Serialize the required toggle or toggles. After every terminal result,
   re-inventory the checkout.
6. Restore the checkout's original branch before restoring user changes.
7. Apply the recorded stash by OID without dropping it, preserving the index
   when the original staged state must be restored.
8. Compare restored branch, HEAD, staged/unstaged/untracked inventory, files,
   and pre-existing stash list to the preflight record.
9. Locate the temporary stash's current list entry by OID. Drop only that entry
   after successful verification and only if this
   cleanup is within the user's authorization.

If ignored files matter, inspect ignore rules and any worktree include mechanism
before promising portability. Never expose secrets or infer that ignored files
travel with task history.

## Retry rule

A retry is allowed only when all of the following are true:

- the exact cause was identified and removed;
- the previous operation is terminal;
- task IDs, host/cwd placement, and Git state were re-inventoried;
- the retry cannot duplicate or move an unintended task;
- the operation is still within the user's original scope.

A full desktop restart changed matcher behavior in one pilot, but a remote
runtime restart did not. Causality was not established. Treat restart as
version-sensitive, separately authorized connectivity/cache troubleshooting,
never as a default handoff step or retry loop.
