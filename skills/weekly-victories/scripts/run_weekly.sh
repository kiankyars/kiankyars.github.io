#!/usr/bin/env bash
# Unattended Sunday run: build last week's post with the Grok CLI, commit, push.
# Installed by install_schedule.sh; safe to run by hand too.
#
# Works in a throwaway worktree of origin/main, so uncommitted edits or a
# different branch in the main checkout never block the run.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/weekly-victories.XXXXXX")"
cleanup() { git -C "$REPO" worktree remove --force "$WORK" 2>/dev/null || rm -rf "$WORK"; }
trap cleanup EXIT

echo "== $(date) weekly-victories start"
git -C "$REPO" fetch origin main
git -C "$REPO" worktree add --detach "$WORK" origin/main
cd "$WORK"

python3 skills/weekly-victories/scripts/build_weekly_victories.py "$@"

if git status --porcelain -- _posts/weekly-victories | grep -q .; then
  git add -- _posts/weekly-victories
  git commit -m "Add weekly victories from time-lapses"
  git push origin HEAD:main
else
  echo "Nothing to commit."
fi
echo "== $(date) weekly-victories done"
