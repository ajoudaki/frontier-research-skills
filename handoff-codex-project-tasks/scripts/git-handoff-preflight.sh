#!/usr/bin/env bash
set -euo pipefail

repo_path="${1:-.}"

git_read() {
  git --no-optional-locks -C "$repo_path" "$@"
}

if ! git_read rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf 'error\tnot a Git working tree: %s\n' "$repo_path" >&2
  exit 2
fi

process_cwd="$(pwd -P)"
requested_physical_path="$(cd -- "$repo_path" && pwd -P)"
git_top_level="$(git_read rev-parse --show-toplevel)"
git_top_level_physical="$(cd -- "$git_top_level" && pwd -P)"
git_dir="$(git_read rev-parse --path-format=absolute --git-dir 2>/dev/null || git_read rev-parse --git-dir)"
git_common_dir="$(git_read rev-parse --path-format=absolute --git-common-dir 2>/dev/null || git_read rev-parse --git-common-dir)"
head_oid="$(git_read rev-parse --verify HEAD 2>/dev/null || printf 'MISSING_OR_UNBORN')"
branch_name="$(git_read symbolic-ref --quiet --short HEAD 2>/dev/null || printf 'DETACHED')"
origin_url="$(git_read remote get-url origin 2>/dev/null || printf 'MISSING')"
upstream_name="$(git_read rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || printf 'MISSING')"
host_name="$(hostname 2>/dev/null || uname -n)"

printf 'host\t%s\n' "$host_name"
printf 'process_cwd\t%s\n' "$process_cwd"
printf 'requested_path\t%s\n' "$repo_path"
printf 'requested_physical_path\t%s\n' "$requested_physical_path"
printf 'git_top_level\t%s\n' "$git_top_level"
printf 'git_top_level_physical\t%s\n' "$git_top_level_physical"
printf 'git_dir\t%s\n' "$git_dir"
printf 'git_common_dir\t%s\n' "$git_common_dir"
printf 'origin\t%s\n' "$origin_url"
printf 'head\t%s\n' "$head_oid"
printf 'branch\t%s\n' "$branch_name"
printf 'upstream\t%s\n' "$upstream_name"

printf '\n[status_porcelain_v2]\n'
git_read status --porcelain=v2 --branch --untracked-files=all

printf '\n[unstaged_name_status]\n'
git_read diff --name-status

printf '\n[staged_name_status]\n'
git_read diff --cached --name-status

printf '\n[untracked_paths]\n'
git_read ls-files --others --exclude-standard

printf '\n[unresolved_index_entries]\n'
git_read ls-files --unmerged

printf '\n[stashes]\n'
git_read stash list --format='%gd%x09%H%x09%s'

printf '\n[worktrees]\n'
git_read worktree list --porcelain

printf '\n[submodules]\n'
if ! submodule_output="$(git_read submodule status --recursive 2>&1)"; then
  printf 'ERROR\tgit submodule status --recursive failed\n'
  printf '%s\n' "$submodule_output"
elif [[ -n "$submodule_output" ]]; then
  printf '%s\n' "$submodule_output"
else
  printf 'none\n'
fi

printf '\n[in_progress_operations]\n'
operation_count=0
index_lock_path="$(git_read rev-parse --git-path index.lock)"
case "$index_lock_path" in
  /*) ;;
  *) index_lock_path="$git_top_level/$index_lock_path" ;;
esac
if [[ -e "$index_lock_path" ]]; then
  printf 'index.lock\t%s\n' "$index_lock_path"
  operation_count=$((operation_count + 1))
fi
for operation_marker in MERGE_HEAD rebase-merge rebase-apply CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG sequencer; do
  marker_path="$(git_read rev-parse --git-path "$operation_marker")"
  case "$marker_path" in
    /*) ;;
    *) marker_path="$git_top_level/$marker_path" ;;
  esac
  if [[ -e "$marker_path" ]]; then
    printf '%s\t%s\n' "$operation_marker" "$marker_path"
    operation_count=$((operation_count + 1))
  fi
done

if [[ "$operation_count" -eq 0 ]]; then
  printf 'none\n'
fi
