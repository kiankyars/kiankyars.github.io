---
name: weekly-victories
description: Populate a Weekly Victories post on kiankyars.github.io from the week's daily time-lapse posts on X (@neuralkian). Use this whenever the user mentions weekly victories, filling in or drafting this week's or last week's victories, pulling their time-lapses from X or Twitter, or asks what they posted each day this week, even if they don't name the post. Also use it to run, debug or reschedule the Sunday-morning automation that does this.
license: MIT
compatibility: Python 3.9+ (stdlib only). Network access to api.x.ai with XAI_API_KEY, or to api.x.com with X_BEARER_TOKEN.
metadata:
  author: kiankyars
  schedule: Sunday morning, America/Los_Angeles (see .github/workflows/weekly-victories.yml)
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

Then read the resulting file. Captions are copied verbatim, minus the trailing
media link, with a `([time-lapse](url))` pointer after each. If a day says
`- ` the script found no post for it. Tell the user which days are missing
rather than inventing content. Never paraphrase or "improve" the captions
unless the user asks, since the post is meant to be their words.

## Backends

| `--backend` | Needs | When |
| --- | --- | --- |
| `xai` (default) | `XAI_API_KEY` | Grok's `x_search` tool reads the posts and returns them as JSON. No X developer account needed. Read the output before publishing; the model transcribes rather than copies. |
| `x` | `X_BEARER_TOKEN` | Deterministic timeline fetch via X API v2, if an X developer token is available. |
| `json` | `--from-json file` | Local fixture for tests and dry runs. |

Both paid backends cost a few cents a week for seven posts. See
`references/x-access.md` for the trade-offs and how to get either credential.

## Automation

`.github/workflows/weekly-victories.yml` runs the script every Sunday morning
Pacific and commits the new post. The workflow reads `XAI_API_KEY` (or
`X_BEARER_TOKEN` with the repository variable `TIMELAPSE_BACKEND=x`) from
repository secrets. To run it by hand, trigger the workflow from the Actions
tab or run the script locally and commit.

If the workflow fails, the usual causes are an expired token (HTTP 401), the
pay-per-use cap or rate limit (HTTP 429), or a week with no video posts. The
script exits non-zero with the HTTP body, so read the job log first.
