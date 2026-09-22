#!/usr/bin/env bash
# Schedule the Sunday-morning weekly-victories run on this machine.
#
# The default backend is the Grok Build CLI, which uses the account you signed
# into with `grok login` (no API key). That login only exists on your computer,
# so the schedule has to live here too rather than in GitHub Actions.
#
#   bash skills/weekly-victories/scripts/install_schedule.sh            # install (macOS launchd or Linux cron)
#   bash skills/weekly-victories/scripts/install_schedule.sh --uninstall
#
# It runs skills/weekly-victories/scripts/run_weekly.sh every Sunday at 08:00
# local time, which builds the post, commits it and pushes.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RUNNER="$REPO/skills/weekly-victories/scripts/run_weekly.sh"
LABEL="io.github.kiankyars.weekly-victories"
LOG_DIR="$HOME/Library/Logs"

if [[ "$(uname)" == "Darwin" ]]; then
  PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
  if [[ "${1:-}" == "--uninstall" ]]; then
    launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
    rm -f "$PLIST"
    echo "Removed $PLIST"
    exit 0
  fi
  mkdir -p "$(dirname "$PLIST")" "$LOG_DIR"
  cat >"$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>$RUNNER</string></array>
  <key>StartCalendarInterval</key>
  <dict><key>Weekday</key><integer>0</integer><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
  <key>EnvironmentVariables</key>
  <dict><key>PATH</key><string>$HOME/.grok/bin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string></dict>
  <key>StandardOutPath</key><string>$LOG_DIR/weekly-victories.log</string>
  <key>StandardErrorPath</key><string>$LOG_DIR/weekly-victories.log</string>
</dict>
</plist>
EOF
  launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$PLIST"
  echo "Installed $PLIST (Sundays 08:00, log: $LOG_DIR/weekly-victories.log)"
  echo "Run it now with: launchctl kickstart gui/$(id -u)/$LABEL"
else
  LINE="0 8 * * 0 /bin/bash $RUNNER >> \$HOME/.weekly-victories.log 2>&1"
  if [[ "${1:-}" == "--uninstall" ]]; then
    crontab -l 2>/dev/null | grep -vF "$RUNNER" | crontab - || true
    echo "Removed cron entry"
    exit 0
  fi
  { crontab -l 2>/dev/null | grep -vF "$RUNNER"; echo "$LINE"; } | crontab -
  echo "Installed cron entry: $LINE"
fi
