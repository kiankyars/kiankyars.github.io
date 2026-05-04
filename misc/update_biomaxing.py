#!/usr/bin/env python3
"""Auto-fill the L-theanine trial table in _posts/blog/2026-02-04-biomaxing.md
from Polar AccessLink. Idempotent — only writes empty cells.

Date conventions (verified against existing rows):
  Sleep score/charge for log row X  ←  Polar /users/sleep night where date == X+1
    (Polar's `date` is the wake-up date; Kian logs sleep under the night's start date.)
  Cardio load status for log row X  ←  Polar /users/cardio-load/X

Auth: reads POLAR_ACCESS_TOKEN from ~/.env (or environment).
If the token is expired, refresh it with:
  python3 ~/obsidian/scripts/polar_accesslink.py local-auth
"""

import json
import os
import re
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

API = "https://www.polaraccesslink.com/v3"
ENV = Path.home() / ".env"
POST = Path(__file__).resolve().parent.parent / "_posts/blog/2026-02-04-biomaxing.md"

STATUS = {
    "MAINTAINING": "maintaining",
    "PRODUCTIVE": "productive",
    "DETRAINING": "detraining",
    "OVERREACHING": "overreaching",
    "STRAINED": "strained",
}


def parse_env(path):
    out = {}
    for line in path.read_text().splitlines() if path.exists() else []:
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        out[k.strip()] = v
    return out


def fetch(token, path):
    req = urllib.request.Request(
        f"{API}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"WARN {path}: {e}", file=sys.stderr)
        return None


def main():
    token = parse_env(ENV).get("POLAR_ACCESS_TOKEN") or os.environ.get("POLAR_ACCESS_TOKEN")
    if not token:
        sys.exit("POLAR_ACCESS_TOKEN not found in ~/.env or environment")

    sleep = {n["date"]: n for n in (fetch(token, "/users/sleep") or {}).get("nights", [])}
    today = date.today()
    changes = []
    out_lines = []

    for line in POST.read_text().splitlines():
        if not line.startswith("| "):
            out_lines.append(line)
            continue

        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) not in (7, 8):
            out_lines.append(line)
            continue

        m = re.match(r"^(\d{4}-\d{2}-\d{2})(\s*\[\^[^\]]+\])?$", cells[0])
        if not m:
            out_lines.append(line)
            continue

        cells[0] = m.group(1)
        if len(cells) == 7:
            cells.append("")

        log_date = date.fromisoformat(cells[0])
        if log_date > today:
            out_lines.append(line)
            continue

        sleep_key = (log_date + timedelta(days=1)).isoformat()
        n = sleep.get(sleep_key)
        if n and n.get("sleep_score"):  # skip score=0 (watch didn't record)
            if not cells[4]:
                cells[4] = str(n["sleep_score"])
                changes.append(f"{log_date}: sleep_score={n['sleep_score']}")
            if not cells[5] and n.get("sleep_charge") is not None:
                cells[5] = str(n["sleep_charge"])
                changes.append(f"{log_date}: sleep_charge={n['sleep_charge']}")

        if not cells[6]:
            cl = fetch(token, f"/users/cardio-load/{log_date}")
            if isinstance(cl, list) and cl:
                friendly = STATUS.get(cl[0].get("cardio_load_status"))
                if friendly:
                    cells[6] = friendly
                    changes.append(f"{log_date}: cardio={friendly}")

        out_lines.append("| " + cells[0] + " | " + " | ".join(cells[1:]) + " |")

    if changes:
        POST.write_text("\n".join(out_lines) + "\n")
        print("Updated:")
        for c in changes:
            print(" -", c)
    else:
        print("No changes — table is up to date.")


if __name__ == "__main__":
    main()
