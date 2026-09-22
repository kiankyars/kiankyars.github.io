---
name: weekly-victories
description: Populate a Weekly Victories post on kiankyars.github.io from the week's daily time-lapse posts on X (@neuralkian). Use this whenever the user mentions weekly victories, filling in or drafting this week's or last week's victories, pulling their time-lapses from X or Twitter, or asks what they posted each day this week, even if they don't name the post. Also use it to run, debug or reschedule the Sunday-morning automation that does this.
license: MIT
compatibility: Python 3.9+ (stdlib only). The Grok Build CLI signed in with `grok login` (default), or network access to api.x.ai with XAI_API_KEY, or to api.x.com with X_BEARER_TOKEN.
metadata:
  author: kiankyars
  schedule: Sunday 08:00 local on Kian's machine via launchd (see scripts/install_schedule.sh)
---

# Weekly Victories

Every day Kian posts a time-lapse of that day on X. Each time-lapse caption is
already a one-line summary of the day, so a Weekly Victories post is just those
seven captions, one under each weekday heading. This skill turns that into a
single command and explains the conventions so the result lands in the right
file with the right dates.

## Conventions that matter

- **Posts are dated on Fridays.** The file is
  `_posts/weekly-victories/YYYY-MM-DD-weekly-victories.md` where the date is the
  Friday the week ends on. Sections run `### Saturday` through `### Friday`.
- **A time-lapse is posted the next day.** The post published on Saturday shows
  Friday. So a post on day D describes day D-1, and the week ending Friday F is
  only complete on Saturday evening. That is why the automation runs on
  **Sunday** morning, not Saturday.
- **Days are Pacific time.** A post at 03:00 UTC Sunday is Saturday evening in
  San Francisco and therefore describes Friday.
- **Hand-written text wins.** If Kian already typed something under a day, keep
  it and only fill the days that are still empty (`- `). Pass `--force` only if
  asked to regenerate a day.

## Do it

From the repo root:

```bash
python3 skills/weekly-victories/scripts/build_weekly_victories.py             # last completed week
python3 skills/weekly-victories/scripts/build_weekly_victories.py --dry-run   # preview, no write
python3 skills/weekly-victories/scripts/build_weekly_victories.py --week 2026-09-18
```

The script picks the week itself: on a Sunday it takes the Friday two days ago.
On a Friday or Saturday the current week is not yet complete, so it goes back
one more week. Pass `--week <friday>` to override.

Then read the resulting file. Each `- ` line of the caption becomes its own bullet; the
`Timelapse #N | H Hours` header is folded into a `([time-lapse #N, H hours](url))`
pointer on the last bullet. If a day says
`- ` the script found no post for it. Tell the user which days are missing
rather than inventing content. Never paraphrase or "improve" the captions
unless the user asks, since the post is meant to be their words.

## Backends

| `--backend` | Needs | When |
| --- | --- | --- |
| `grok` (default) | `grok login` once | Runs the Grok Build CLI headlessly (`grok -p ... --always-approve --output-format json`) on this machine. It uses your Grok/X subscription session from `~/.grok/auth.json`, so no API key and no per-token bill. Read the output before publishing; the model transcribes rather than copies. Set `GROK_MODEL` to pick a model, `GROK_CLI` if the binary is not on PATH. |
| `xai` | `XAI_API_KEY` | Same search through the xAI Responses API `x_search` tool, for CI or machines without the CLI. |
| `x` | `X_BEARER_TOKEN` | Deterministic timeline fetch via X API v2, if an X developer token is available. |
| `json` | `--from-json file` | Local fixture for tests and dry runs. |

The two API backends cost a few cents a week for seven posts. See
`references/x-access.md` for the trade-offs and how to get either credential.

## Grok CLI setup (once)

```bash
curl -fsSL https://x.ai/cli/install.sh | bash   # installs `grok`
grok login                                       # browser sign-in, cached in ~/.grok/auth.json
python3 skills/weekly-victories/scripts/build_weekly_victories.py --dry-run
```

The script calls `grok --always-approve --output-format json -p ...`.
`--always-approve` auto-approves every tool call so an unattended run never waits on a
permission prompt; the prompt also tells Grok not to touch files or run
commands, and `Bash`, `Edit` and `Write` are passed to `--disallowed-tools`.
If a run says you are not signed in, run `grok login` again.

## Automation

Because the default backend uses the login on Kian's own computer, the
schedule lives there, not in GitHub Actions:

```bash
bash skills/weekly-victories/scripts/install_schedule.sh              # launchd on macOS, cron on Linux
bash skills/weekly-victories/scripts/install_schedule.sh --uninstall
```

That runs `scripts/run_weekly.sh` every Sunday at 08:00 local time: pull
`main`, build the post, commit and push. The log is
`~/Library/Logs/weekly-victories.log` (macOS) or `~/.weekly-victories.log`.
To run it now: `bash skills/weekly-victories/scripts/run_weekly.sh`. The
machine has to be awake at 08:00; launchd runs a missed job at next wake, cron
does not.

If a run fails, the usual causes are a lapsed `grok login`, an expired API
token (HTTP 401), a rate limit (HTTP 429), or a week with no video posts. The
script exits non-zero with the CLI or HTTP output, so read the log first.
