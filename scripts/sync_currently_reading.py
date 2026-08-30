#!/usr/bin/env python3
"""Sync the Goodreads currently-reading shelf into Jekyll data."""

import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree


PUBLIC_FEED_URL = (
    "https://www.goodreads.com/review/list_rss/108079212?shelf=currently-reading"
)
OUTPUT = Path(__file__).resolve().parents[1] / "_data" / "currently_reading.json"


def feed_url() -> str:
    return os.environ.get("GOODREADS_RSS_URL", "").strip() or PUBLIC_FEED_URL


def text(item: ElementTree.Element, tag: str) -> str:
    return (item.findtext(tag) or "").strip()


def main() -> None:
    request = Request(feed_url(), headers={"User-Agent": "kiankyars.github.io RSS sync"})
    with urlopen(request, timeout=30) as response:
        root = ElementTree.fromstring(response.read())
    channel = root.find("channel")
    if root.tag != "rss" or channel is None:
        raise ValueError("Goodreads returned an unexpected document")

    books = []
    seen = set()
    for item in channel.findall("item"):
        book_id = text(item, "book_id")
        title = text(item, "title")
        author = text(item, "author_name")
        if not (book_id.isdigit() and title and author) or book_id in seen:
            continue
        seen.add(book_id)
        books.append(
            {
                "author": author,
                "title": title,
                "url": f"https://www.goodreads.com/book/show/{book_id}",
            }
        )

    rendered = json.dumps(books, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if OUTPUT.exists() and OUTPUT.read_text(encoding="utf-8") == rendered:
        print("Currently-reading data is already current.")
        return

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"Updated {OUTPUT.relative_to(OUTPUT.parents[1])} with {len(books)} book(s).")


if __name__ == "__main__":
    main()
