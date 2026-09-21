#!/usr/bin/env bash
# Unattended Sunday run: build last week's post with the Grok CLI, commit, push.
# Installed by install_schedule.sh; safe to run by hand too.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$REPO"
echo "== $(date) weekly-victories start"

git fetch origin main
git checkout main
git pull --ff-only origin main

python3 skills/weekly-victories/scripts/build_weekly_victories.py "$@"

if git status --porcelain -- _posts/weekly-victories | grep -q .; then
  git add -- _posts/weekly-victories
  git commit -m "Add weekly victories from time-lapses"
  git push origin main
else
  echo "Nothing to commit."
fi
echo "== $(date) weekly-victories done"
