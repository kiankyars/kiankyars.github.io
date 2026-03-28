#!/usr/bin/env python3
"""Fetch tallest-building height and SC population for Wikidata top cities. Prints JSON to stdout."""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

WIKIDATA_QUERY = """
SELECT ?cityLabel (MAX(?pop) AS ?p) WHERE {
  ?city wdt:P31 wd:Q515 .
  ?city wdt:P1082 ?pop .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
GROUP BY ?city ?cityLabel
ORDER BY DESC(?p)
LIMIT 110
"""

SLUG_OVERRIDES: dict[str, str] = {
    "São Paulo": "sao-paulo",
    "Mexico City": "mexico-city",
    "New York City": "new-york-city",
    "Ho Chi Minh City": "ho-chi-minh-city",
    "Dar es Salaam": "dar-es-salaam",
    "Xi'an": "xian",
    "Xian": "xian",
    "Washington, D.C.": "washington-dc",
    "Hong Kong": "hong-kong",
    "Saint Petersburg": "saint-petersburg",
    "St. Petersburg": "saint-petersburg",
    "Belo Horizonte": "belo-horizonte",
    "Bogotá": "bogota",
    "Bogota": "bogota",
    "Santiago": "santiago",
    "Jeddah": "jeddah",
    "Riyadh": "riyadh",
    "Busan": "busan",
    "Yokohama": "yokohama",
    "İstanbul": "istanbul",
    "Istanbul": "istanbul",
    "Stuttgart": "stuttgart",
}


def slugify(label: str) -> str:
    s = label.lower()
    for a, b in (
        ("ā", "a"),
        ("á", "a"),
        ("à", "a"),
        ("ä", "a"),
        ("ã", "a"),
        ("â", "a"),
        ("ē", "e"),
        ("é", "e"),
        ("è", "e"),
        ("ī", "i"),
        ("í", "i"),
        ("ï", "i"),
        ("ó", "o"),
        ("ō", "o"),
        ("ö", "o"),
        ("ú", "u"),
        ("ū", "u"),
        ("ü", "u"),
        ("ç", "c"),
        ("ć", "c"),
        ("ş", "s"),
        ("ğ", "g"),
        ("ñ", "n"),
        ("ł", "l"),
        ("đ", "d"),
        ("ı", "i"),
        ("ô", "o"),
        ("ș", "s"),
    ):
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def wikidata_cities() -> list[tuple[str, int]]:
    url = "https://query.wikidata.org/sparql"
    data = urllib.parse.urlencode(
        {"query": WIKIDATA_QUERY, "format": "json"}
    ).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "User-Agent": "kiankyars.github.io skyline study/1.0",
            "Accept": "application/sparql-results+json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.load(r)
    rows: list[tuple[str, int]] = []
    for b in out["results"]["bindings"]:
        name = b["cityLabel"]["value"]
        p = int(b["p"]["value"].split(".")[0])
        rows.append((name, p))
    return rows


def scrape_city(slug: str) -> tuple[int | None, float | None, str | None]:
    url = f"https://www.skyscrapercenter.com/city/{slug}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research)"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            html = r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, None, "404"
        return None, None, str(e.code)
    except Exception as e:
        return None, None, repr(e)

    pm = re.search(
        r"Population</p>[\s\S]{0,600}?<p class=\"pb-0\">\s*([0-9,]+)",
        html,
    )
    pop = int(pm.group(1).replace(",", "")) if pm else None
    tm = re.search(
        r"Tallest Building</p>[\s\S]{0,400}?\(([\d.]+)\s*m\)",
        html,
    )
    tallest = float(tm.group(1)) if tm else None
    return pop, tallest, None


def main() -> None:
    cities = wikidata_cities()
    seen: set[str] = set()
    unique: list[tuple[str, int]] = []
    for name, p in cities:
        if name in seen:
            continue
        seen.add(name)
        unique.append((name, p))
        if len(unique) >= 100:
            break

    results: list[dict] = []
    for name, wd_pop in unique:
        slug = SLUG_OVERRIDES.get(name, slugify(name))
        pop, tallest, err = scrape_city(slug)
        time.sleep(0.35)
        row = {
            "city": name,
            "slug": slug,
            "wikidata_pop": wd_pop,
            "sc_pop": pop,
            "tallest_m": tallest,
            "error": err,
        }
        if pop and tallest:
            row["m_per_capita"] = tallest / pop
            row["mm_per_1000"] = 1000 * tallest / pop
        results.append(row)

    cache = Path(__file__).resolve().parent / "skyline_per_capita_cache.json"
    text = json.dumps(results, indent=2)
    cache.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
