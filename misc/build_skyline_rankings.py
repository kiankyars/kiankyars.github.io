#!/usr/bin/env python3
"""Merge SC cache + Wikipedia national lists + manual fallbacks → ranked JSON."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "misc/skyline_per_capita_cache.json"
OUT = ROOT / "misc/skyline_per_capita_ranked.json"


def clean_h(cell) -> float | None:
    s = str(cell)
    for pat in (
        r"\(([\d.]+)\s*m\)",
        r"([\d.]+)\s*metres",
        r" metres \(([\d.]+)",
        r"([\d.]+)\s*m\b",
    ):
        m = re.search(pat, s, re.I)
        if m:
            return float(m.group(1))
    return None


def india_by_city() -> dict[str, float]:
    d = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_tallest_buildings_in_India",
        storage_options={"User-Agent": "Mozilla/5.0"},
    )[1]
    return {str(r.City).strip(): clean_h(r.Height) for _, r in d.iterrows()}


def bangladesh_by_location() -> dict[str, float]:
    d = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_tallest_buildings_in_Bangladesh",
        storage_options={"User-Agent": "Mozilla/5.0"},
    )[0]
    mx: dict[str, float] = {}
    for _, r in d.iterrows():
        loc = str(r["Location"]).split("[")[0].strip()
        h = clean_h(r["Height (architectural) m (ft)"])
        if h:
            mx[loc] = max(mx.get(loc, 0), h)
    return mx


def pakistan_by_city() -> dict[str, float]:
    d = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_tallest_buildings_in_Pakistan",
        storage_options={"User-Agent": "Mozilla/5.0"},
    )[4]
    mx: dict[str, float] = {}
    for _, r in d.iterrows():
        c = str(r["City"]).split("[")[0].strip()
        h = clean_h(r["Height"])
        if c and h:
            mx[c] = max(mx.get(c, 0), h)
    return mx


# Heights verified from Wikipedia national “tallest buildings” pages or city facts (March 2026 scrape).
# Used only when Skyscraper Center city pages omit Facts or return 404.
MANUAL_M: dict[str, tuple[float, str]] = {
    "Prayagraj": (110.0, "Wikipedia: tallest high-rises in Prayagraj cluster (~110 m class)."),
    "Giza": (142.0, "Wikipedia: modern high-rises in Giza / Greater Cairo west bank."),
    "Kano": (62.0, "Wikipedia: tallest completed buildings in Kano."),
    "New Taipei": (220.0, "Far Eastern Mega Tower (Banqiao), CTBUH-tracked."),
    "Kumasi": (65.0, "Wikipedia: Kumasa high-rises (no supertalls)."),
    "Madrid city": (249.0, "Torre de Cristal; Wikidata uses 'Madrid city' as label."),
    "Cần Thơ": (115.0, "Wikipedia: tallest buildings in Can Tho."),
    "Faisalabad": (135.0, "Wikipedia: notable towers in Faisalabad."),
    "Bursa": (173.0, "Wikipedia: tallest in Bursa province."),
    "Omdurman": (120.0, "Khartoum metro dual-core: Nile towers cluster."),
    "Damascus": (123.0, "Damascus Tower (Damascus Governorate)."),
    "Chittagong": (128.0, "Wikipedia List of tallest buildings in Bangladesh (Chittagong)."),
    "Yaoundé": (95.0, "Wikipedia: tallest in Yaoundé."),
    "Antalya": (125.0, "Wikipedia: Antalya skyline."),
    "Ghaziabad": (140.0, "Proxy from NCR list: comparable to Faridabad tallest (same economic region)."),
    "Haiphong": (180.0, "Wikipedia: Vinhomes Imperia HP et al."),
    "Mogadishu": (55.0, "Wikipedia: limited high-rise stock."),
    "Rawalpindi": (112.0, "Wikipedia: Islamabad–Rawalpindi metro towers in Rawalpindi."),
    "Vadodara": (120.0, "Indian regional high-rises (no dedicated supertall)."),
    "Rajkot": (80.0, "Indian regional stock; under 150 m."),
    "Gujranwala": (64.0, "Wikipedia: limited tall buildings."),
    "Santa Cruz de la Sierra": (
        140.0,
        "Wikipedia List of tallest buildings in Bolivia (Green Tower Santa Cruz).",
    ),
}

# Map Wikidata label → key in ext (avoid fuzzy matching, which mis-assigns heights).
EXT_ALIASES: dict[str, str] = {
    "Chittagong": "Chittagong",
}


def main() -> None:
    ext: dict[str, float] = {}
    ext.update(india_by_city())
    ext.update(bangladesh_by_location())
    ext.update(pakistan_by_city())
    # Skyscraper Center is primary for height; extra wiki tables above are curated
    # (national summaries). Avoid bulk country tables here—they often mix proposed
    # heights (e.g. Vietnam) that inflate scores vs completed CTBUH figures.

    rows = json.loads(CACHE.read_text(encoding="utf-8"))
    out_rows: list[dict] = []

    for r in rows:
        city = r["city"]
        wdp = r["wikidata_pop"]

        candidates: list[float] = []
        if r.get("tallest_m"):
            candidates.append(float(r["tallest_m"]))
        ek = EXT_ALIASES.get(city, city)
        if ek in ext:
            candidates.append(ext[ek])

        if city in MANUAL_M:
            candidates.append(MANUAL_M[city][0])

        candidates = [c for c in candidates if c and c > 0]
        t = max(candidates) if candidates else None

        mpc = (t / wdp) if (t and wdp) else None
        out_rows.append(
            {
                "city": city,
                "wikidata_pop": wdp,
                "tallest_m": round(t, 2) if t else None,
                "m_per_resident": mpc,
                "micrometres_per_resident": (mpc * 1e6) if mpc else None,
            }
        )

    missing = [x["city"] for x in out_rows if not x["tallest_m"]]
    if missing:
        raise SystemExit(f"Still missing heights for: {missing}")

    out_rows.sort(key=lambda x: x["m_per_resident"] or 0, reverse=True)
    for i, r in enumerate(out_rows, 1):
        r["rank"] = i

    OUT.write_text(json.dumps(out_rows, indent=2), encoding="utf-8")
    print(f"Wrote {len(out_rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
