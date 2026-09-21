#!/usr/bin/env python3
"""Populate a Weekly Victories post from the week's daily time-lapse posts on X.

Conventions this script encodes (see SKILL.md for the reasoning):

* A Weekly Victories post is dated on a Friday and has one section per day,
  Saturday through Friday, in that order.
* Each day's time-lapse is posted on X the *next* day, so a post published on
  day D describes day D-1 (`--offset-days`, default 1).
* Days are reckoned in America/Los_Angeles (`--tz`).

Backends (`--backend`):

* `x`   - X API v2 `GET /2/users/:id/tweets` with `X_BEARER_TOKEN`.
* `xai` - xAI Responses API with the `x_search` tool, using `XAI_API_KEY`.
* `json`- a local file of `{"text", "created_at", "url"}` objects (`--from-json`),
          useful for dry runs and tests.

Usage:
    python3 skills/weekly-victories/scripts/build_weekly_victories.py           # last completed week
    python3 skills/weekly-victories/scripts/build_weekly_victories.py --week 2026-09-18
    python3 skills/weekly-victories/scripts/build_weekly_victories.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[3]
POSTS_DIR = REPO_ROOT / "_posts" / "weekly-victories"
DAYS = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
DEFAULT_HANDLE = "neuralkian"
DEFAULT_TZ = "America/Los_Angeles"
TRAILING_LINK = re.compile(r"\s*https?://t\.co/\S+\s*$")


@dataclass
class Post:
    text: str
    created_at: datetime  # timezone-aware
    url: str = ""
    has_video: bool = False


# --------------------------------------------------------------------------- dates


def last_completed_friday(today: date) -> date:
    """The most recent Friday whose time-lapse can already be on X.

    The Friday time-lapse is posted on Saturday, so from Sunday onward the week
    ending on the previous Friday is complete. On Saturday it isn't yet, so we
    fall back one more week.
    """
    days_since_friday = (today.weekday() - 4) % 7
    friday = today - timedelta(days=days_since_friday)
    if days_since_friday < 2:  # Friday or Saturday: this week's Friday post isn't up yet
        friday -= timedelta(days=7)
    return friday


def week_days(friday: date) -> list[date]:
    return [friday - timedelta(days=6 - i) for i in range(7)]


# ------------------------------------------------------------------------ backends


def http_json(url: str, headers: dict, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    request = Request(url, data=data, headers={"User-Agent": "kiankyars.github.io weekly-victories", **headers})
    try:
        with urlopen(request, timeout=60) as response:
            return json.load(response)
    except HTTPError as error:
        detail = error.read().decode(errors="replace")
        raise SystemExit(f"{url} -> HTTP {error.code}: {detail}") from error


def fetch_x_api(handle: str, start: datetime, end: datetime) -> list[Post]:
    token = os.environ.get("X_BEARER_TOKEN", "").strip()
    if not token:
        raise SystemExit("X_BEARER_TOKEN is not set (X developer portal -> project -> Bearer Token).")
    headers = {"Authorization": f"Bearer {token}"}

    user = http_json(f"https://api.x.com/2/users/by/username/{handle}", headers)
    user_id = user["data"]["id"]

    params = {
        "start_time": start.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_time": end.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "max_results": 100,
        "exclude": "retweets,replies",
        "tweet.fields": "created_at,text,attachments,note_tweet",
        "expansions": "attachments.media_keys",
        "media.fields": "type",
    }
    posts: list[Post] = []
    next_token = None
    while True:
        if next_token:
            params["pagination_token"] = next_token
        page = http_json(f"https://api.x.com/2/users/{user_id}/tweets?{urlencode(params)}", headers)
        media = {m["media_key"]: m.get("type") for m in page.get("includes", {}).get("media", [])}
        for item in page.get("data", []):
            keys = item.get("attachments", {}).get("media_keys", [])
            text = item.get("note_tweet", {}).get("text") or item["text"]
            posts.append(
                Post(
                    text=text,
                    created_at=datetime.fromisoformat(item["created_at"].replace("Z", "+00:00")),
                    url=f"https://x.com/{handle}/status/{item['id']}",
                    has_video=any(media.get(k) == "video" for k in keys),
                )
            )
        next_token = page.get("meta", {}).get("next_token")
        if not next_token:
            return posts


def fetch_xai(handle: str, start: datetime, end: datetime) -> list[Post]:
    """Ask Grok to pull the posts via its x_search tool and return them as JSON.

    Grok's x_search is a model tool, not a raw timeline endpoint, so the model
    is asked to transcribe posts verbatim into a strict JSON array. Results are
    validated but are inherently less deterministic than the X API backend.
    """
    key = os.environ.get("XAI_API_KEY", "").strip()
    if not key:
        raise SystemExit("XAI_API_KEY is not set (console.x.ai -> API keys).")
    model = os.environ.get("XAI_MODEL", "grok-4-fast")
    prompt = (
        f"List every original post (not replies or reposts) by @{handle} published between "
        f"{start.isoformat()} and {end.isoformat()}. Return ONLY a JSON array, no prose, where each "
        'element is {"text": <full post text verbatim>, "created_at": <ISO 8601 UTC timestamp>, '
        '"url": <post URL>, "has_video": <true if the post has a video attached>}.'
    )
    body = {
        "model": model,
        "input": [{"role": "user", "content": prompt}],
        "tools": [
            {
                "type": "x_search",
                "allowed_x_handles": [handle],
                "from_date": start.date().isoformat(),
                "to_date": end.date().isoformat(),
            }
        ],
    }
    response = http_json(
        "https://api.x.ai/v1/responses",
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        body,
    )
    text = ""
    for item in response.get("output", []):
        for part in item.get("content", []) or []:
            if part.get("type") == "output_text":
                text += part.get("text", "")
    match = re.search(r"\[.*\]", text, re.S)
    if not match:
        raise SystemExit(f"Grok did not return a JSON array. Raw output:\n{text}")
    return load_posts(json.loads(match.group(0)))


def load_posts(items: list[dict]) -> list[Post]:
    posts = []
    for item in items:
        created = datetime.fromisoformat(str(item["created_at"]).replace("Z", "+00:00"))
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        posts.append(Post(item["text"], created, item.get("url", ""), bool(item.get("has_video"))))
    return posts


# ------------------------------------------------------------------------ mapping


def clean_text(text: str) -> str:
    text = TRAILING_LINK.sub("", text.strip())
    return " ".join(text.split())


def posts_by_day(posts: list[Post], days: list[date], tz: ZoneInfo, offset_days: int) -> dict[date, list[Post]]:
    """Assign each post to the day it describes.

    Time-lapses are preferred (a video attachment); if a day has none, any
    original post from that day is used so a missing flag doesn't lose a day.
    """
    wanted = set(days)
    by_day: dict[date, list[Post]] = {d: [] for d in days}
    for post in sorted(posts, key=lambda p: p.created_at):
        covered = post.created_at.astimezone(tz).date() - timedelta(days=offset_days)
        if covered in wanted:
            by_day[covered].append(post)
    for day, items in by_day.items():
        videos = [p for p in items if p.has_video]
        by_day[day] = videos or items
    return by_day


def bullets_for(posts: list[Post], link: bool) -> list[str]:
    lines = []
    for post in posts:
        text = clean_text(post.text)
        if not text:
            continue
        lines.append(f"- {text} ([time-lapse]({post.url}))" if link and post.url else f"- {text}")
    return lines


# ----------------------------------------------------------------------- markdown

SECTION = re.compile(r"^### (\w+)\s*$", re.M)


def parse_existing(markdown: str) -> tuple[str, dict[str, str]]:
    """Split a post into (front matter, {day: body}) so hand-written days survive."""
    parts = markdown.split("---", 2)
    front = "---" + parts[1] + "---" if len(parts) == 3 else ""
    body = parts[2] if len(parts) == 3 else markdown
    sections: dict[str, str] = {}
    matches = list(SECTION.finditer(body))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sections[match.group(1)] = body[match.end():end].strip()
    return front, sections


def is_blank(section: str) -> bool:
    return not section.replace("-", "").strip()


def render(friday: date, sections: dict[str, str]) -> str:
    front = f"---\nlayout: post\ntitle: Weekly Victories\ndate: {friday.isoformat()}\ncategories: reflection\n---\n"
    chunks = [f"### {day}\n\n{sections.get(day) or '- '}\n" for day in DAYS]
    return front + "\n" + "\n".join(chunks)


# --------------------------------------------------------------------------- main


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--week", type=date.fromisoformat, help="Friday the post is dated (default: last completed week)")
    parser.add_argument("--handle", default=os.environ.get("X_HANDLE", DEFAULT_HANDLE))
    parser.add_argument("--backend", choices=["x", "xai", "json"], default=os.environ.get("TIMELAPSE_BACKEND", "x"))
    parser.add_argument("--from-json", type=Path, help="posts fixture for --backend json")
    parser.add_argument("--tz", default=DEFAULT_TZ)
    parser.add_argument("--offset-days", type=int, default=1, help="a post on day D describes day D-offset")
    parser.add_argument("--no-links", action="store_true", help="omit the link back to each post")
    parser.add_argument("--force", action="store_true", help="overwrite days that already have content")
    parser.add_argument("--dry-run", action="store_true", help="print the post instead of writing it")
    args = parser.parse_args()

    tz = ZoneInfo(args.tz)
    friday = args.week or last_completed_friday(datetime.now(tz).date())
    if friday.weekday() != 4:
        raise SystemExit(f"{friday} is not a Friday; weekly victories are dated on Fridays.")
    days = week_days(friday)

    # Posts describing Sat..Fri are published Sun..Sat; fetch that whole window.
    start = datetime.combine(days[0] + timedelta(days=args.offset_days), datetime.min.time(), tz)
    end = datetime.combine(days[-1] + timedelta(days=args.offset_days + 1), datetime.min.time(), tz)

    if args.backend == "json":
        if not args.from_json:
            raise SystemExit("--from-json is required with --backend json")
        posts = load_posts(json.loads(args.from_json.read_text()))
    elif args.backend == "xai":
        posts = fetch_xai(args.handle, start, end)
    else:
        posts = fetch_x_api(args.handle, start, end)

    grouped = posts_by_day(posts, days, tz, args.offset_days)

    target = POSTS_DIR / f"{friday.isoformat()}-weekly-victories.md"
    existing: dict[str, str] = {}
    if target.exists():
        _, existing = parse_existing(target.read_text(encoding="utf-8"))

    sections: dict[str, str] = {}
    filled, kept, missing = [], [], []
    for day, name in zip(days, DAYS):
        current = existing.get(name, "")
        if current and not is_blank(current) and not args.force:
            sections[name] = current
            kept.append(name)
            continue
        lines = bullets_for(grouped[day], link=not args.no_links)
        if lines:
            sections[name] = "\n".join(lines)
            filled.append(name)
        else:
            sections[name] = "- "
            missing.append(name)

    output = render(friday, sections)
    summary = f"{target.relative_to(REPO_ROOT)}: filled {filled or 'nothing'}"
    if kept:
        summary += f"; kept hand-written {kept}"
    if missing:
        summary += f"; no time-lapse found for {missing}"

    if args.dry_run:
        print(output)
        print(f"\n[dry run] {summary}", file=sys.stderr)
        return
    if target.exists() and target.read_text(encoding="utf-8") == output:
        print(f"{target.relative_to(REPO_ROOT)} is already current.")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(output, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
