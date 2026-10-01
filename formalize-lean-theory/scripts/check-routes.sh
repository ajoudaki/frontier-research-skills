#!/usr/bin/env bash

set -eu

EXPECTED_SCHEMA=4
EXPECTED_ROUTES=(
  FLT-00 FLT-10 FLT-20 FLT-25 FLT-30 FLT-40
  FLT-45 FLT-50 FLT-60 FLT-70 FLT-80 FLT-90
)
EXPECTED_GATES=(preflight semantic-revision public-acceptance flagship-posthoc)

fail() {
  local code="$1"
  shift
  printf 'formalization-route-check: FAIL code=%s reason="%s"\n' "$code" "$*" >&2
  exit "$code"
}

count_exact_line() {
  local file="$1"
  local line="$2"
  awk -v wanted="$line" '$0 == wanted { count++ } END { print count + 0 }' "$file"
}

require_exact_line_once() {
  local file="$1"
  local line="$2"
  local code="$3"
  local label="$4"
  local count
  count="$(count_exact_line "$file" "$line")"
  [ "$count" -eq 1 ] || fail "$code" "$label occurs $count times"
}

marker_values() {
  local file="$1"
  local kind="$2"
  sed -n "s/^<!-- ${kind}: \([^ ]*\) -->$/\1/p" "$file" | LC_ALL=C sort
}

expected_values() {
  printf '%s\n' "$@" | LC_ALL=C sort
}

if [ "$#" -eq 0 ]; then
  script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
  repo_root="$(git -C "$script_dir" rev-parse --show-toplevel 2>/dev/null)" ||
    fail 3 "cannot resolve Git top-level from skill directory"
elif [ "$#" -eq 2 ] && [ "$1" = "--root" ]; then
  repo_root="$(CDPATH= cd -- "$2" 2>/dev/null && pwd -P)" ||
    fail 3 "explicit repository root is unreadable"
else
  fail 2 "usage: check-routes.sh [--root REPOSITORY_ROOT]"
fi

agents="$repo_root/AGENTS.md"
playbook="$repo_root/FORMALIZATION_PLAYBOOK.md"
readme="$repo_root/README.md"
skill_dir="$repo_root/.agents/skills/formalize-lean-theory"
skill="$skill_dir/SKILL.md"
metadata="$skill_dir/agents/openai.yaml"
fixtures="$repo_root/.agents/evals/formalize-lean-theory.yaml"

for required in "$agents" "$playbook" "$readme" "$skill" "$metadata" "$fixtures"; do
  [ -f "$required" ] && [ -r "$required" ] ||
    fail 3 "required input missing or unreadable: ${required#"$repo_root"/}"
done

require_exact_line_once "$playbook" \
  "<!-- formalization-routing-schema: $EXPECTED_SCHEMA -->" 4 \
  "playbook routing schema"
require_exact_line_once "$skill" \
  "<!-- formalization-router-schema: $EXPECTED_SCHEMA -->" 4 \
  "skill routing schema"

[ "$(marker_values "$playbook" formalization-routing-schema | wc -l)" -eq 1 ] ||
  fail 4 "playbook has a contradictory routing schema marker"
[ "$(marker_values "$skill" formalization-router-schema | wc -l)" -eq 1 ] ||
  fail 4 "skill has a contradictory routing schema marker"

require_exact_line_once "$agents" \
  "<!-- formalization-authority: operational -->" 6 \
  "operational authority marker"
require_exact_line_once "$playbook" \
  "<!-- formalization-authority: methodology -->" 6 \
  "methodology authority marker"
require_exact_line_once "$skill" \
  "<!-- formalization-authority: router-only -->" 6 \
  "router authority marker"

[ "$(marker_values "$agents" formalization-authority)" = "operational" ] ||
  fail 6 "AGENTS authority marker is contradictory"
[ "$(marker_values "$playbook" formalization-authority)" = "methodology" ] ||
  fail 6 "playbook authority marker is contradictory"
[ "$(marker_values "$skill" formalization-authority)" = "router-only" ] ||
  fail 6 "skill authority marker is contradictory"

for route in "${EXPECTED_ROUTES[@]}"; do
  require_exact_line_once "$playbook" \
    "<!-- formalization-route: $route -->" 5 "playbook route $route"
  require_exact_line_once "$skill" \
    "<!-- formalization-skill-route: $route -->" 5 "skill route $route"
done

actual_playbook_routes="$(marker_values "$playbook" formalization-route)"
actual_skill_routes="$(marker_values "$skill" formalization-skill-route)"
expected_routes="$(expected_values "${EXPECTED_ROUTES[@]}")"
[ "$actual_playbook_routes" = "$expected_routes" ] ||
  fail 5 "playbook route set differs from schema"
[ "$actual_skill_routes" = "$expected_routes" ] ||
  fail 5 "skill route set differs from schema"

awk '
  /^<!-- formalization-route: FLT-[0-9][0-9] -->$/ {
    if (active && (!heading || !content)) exit 1
    active = 1
    waiting = 1
    heading = 0
    content = 0
    next
  }
  active && waiting && /^[[:space:]]*$/ { next }
  active && waiting {
    if ($0 ~ /^#{2,4} /) {
      heading = 1
      waiting = 0
      next
    }
    exit 1
  }
  active && !waiting &&
      $0 !~ /^[[:space:]]*$/ &&
      $0 !~ /^<!--/ &&
      $0 !~ /^#{1,6} / { content = 1 }
  END {
    if (active && (!heading || !content)) exit 1
  }
' "$playbook" || fail 5 "a routed playbook section lacks a heading or content"

for gate in "${EXPECTED_GATES[@]}"; do
  require_exact_line_once "$agents" \
    "<!-- formalization-gate: $gate -->" 6 "constitutional gate $gate"
done
actual_gates="$(marker_values "$agents" formalization-gate)"
expected_gates="$(expected_values "${EXPECTED_GATES[@]}")"
[ "$actual_gates" = "$expected_gates" ] ||
  fail 6 "constitutional gate set differs from schema"

require_exact_line_once "$skill" \
  "<!-- formalization-router-requires: persisted-gates -->" 7 \
  "persisted-gates safeguard"
require_exact_line_once "$skill" \
  '| New large paper, paper family, corpus, high-fan-out source endpoint, or unclear flagship | `FLT-00`, `FLT-10`, then `FLT-40` and `FLT-20` |' 7 \
  "large-source FLT-10 route"
require_exact_line_once "$skill" \
  'When `FLT-10` applies, do not enter `FLT-50` until exactly one source-derived' 7 \
  "theory-map persistence guard"
require_exact_line_once "$skill" \
  'Never infer central curation.  A closeout, lesson candidate, or request to' 7 \
  "explicit central-curation guard"
require_exact_line_once "$playbook" \
  'For a new large paper, paper family, high-fan-out source endpoint, or unclear' 7 \
  "large-source methodology guard"
require_exact_line_once "$playbook" \
  'Central curation **MUST** be explicitly requested by the user or supervisor;' 7 \
  "central-curation methodology guard"
require_exact_line_once "$agents" \
  'entries, which remain `open` until central curation.  Promote a lesson into the' 7 \
  "local-open operational safeguard"
require_exact_line_once "$skill" "name: formalize-lean-theory" 7 \
  "skill identity"
require_exact_line_once "$metadata" "  allow_implicit_invocation: true" 7 \
  "implicit-invocation policy"
require_exact_line_once "$fixtures" "schema: $EXPECTED_SCHEMA" 7 \
  "fixture schema"
require_exact_line_once "$fixtures" "skill: formalize-lean-theory" 7 \
  "fixture skill identity"
require_exact_line_once "$fixtures" \
  "  - id: named-large-endpoint-enters-theory-retrieval" 7 \
  "named-large-source regression"
require_exact_line_once "$fixtures" \
  "  - id: lesson-closeout-harvests-open-only" 7 \
  "local-lesson-harvesting regression"
require_exact_line_once "$fixtures" \
  "  - id: explicit-central-lesson-curation" 7 \
  "explicit-central-curation regression"
require_exact_line_once "$fixtures" \
  "  - id: lesson-producer-cannot-self-promote" 7 \
  "producer-self-promotion regression"
require_exact_line_once "$fixtures" \
  "      referee_involved_in_candidate_production: false" 7 \
  "independent-referee regression coordinate"
require_exact_line_once "$fixtures" \
  "      accountable_approval_state: granted_after_review" 7 \
  "accountable-approval regression coordinate"
[ "$(count_exact_line "$fixtures" \
    '        - no-opportunistic-central-curation')" -eq 2 ] ||
  fail 7 "routine/resume central-curation guards are incomplete"
require_exact_line_once "$fixtures" "      endpoint_named: true" 7 \
  "named-endpoint regression coordinate"
for regression in \
  new-endpoint-enters-preflight \
  routine-repair-does-not-expand \
  resume-preserves-current-phase \
  semantic-normalization-change-stops; do
  require_exact_line_once "$fixtures" "  - id: $regression" 7 \
    "routing regression $regression"
done

old_macos="/""Users""/"
linux_home="/""home""/"
if grep -R -n -F -e "$old_macos" -e "$linux_home" "$skill_dir" >/dev/null; then
  fail 7 "skill package contains a machine-specific absolute path"
fi

printf 'formalization-route-check: PASS schema=%s routes=%s gates=%s\n' \
  "$EXPECTED_SCHEMA" "${#EXPECTED_ROUTES[@]}" "${#EXPECTED_GATES[@]}"
