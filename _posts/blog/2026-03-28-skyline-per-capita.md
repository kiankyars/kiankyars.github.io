---
layout: post
title: Skyline per capita
date: 2026-03-28
categories: data
---

Someone on the internet (me, today) asked which great cities allocate the most vertical metres of supertall to each resident. Not total floorspace, not skyline mass, not aesthetic charm: the blunt ratio of **architectural height of the tallest completed high-rise** divided by **headcount**, for a fixed list of mega-agglomerations.

The toy version is obvious. A hundred people sharing one 100 m tower get **1 metre of pinnacle per person**. Double the population without raising the spire and you halve the ratio. The question is what happens when you run the same arithmetic on real municipalities at nine-figure scale, where politics, geology, airport flight paths, and CTBUH definitions all interfere with the clean parable.

## The metric

For each city *i*, let *H<sub>i</sub>* be the tallest completed building in the urban jurisdiction tracked by the [CTBUH Skyscraper Center](https://www.skyscrapercenter.com/) (municipal population in their city facts panel when present), and *P<sub>i</sub>* residential population from [Wikidata](https://www.wikidata.org/) property [P1082](https://www.wikidata.org/wiki/Property:P1082) using the **March 2026** snapshot returned by their public SPARQL endpoint. The ratio is *R<sub>i</sub> = H<sub>i</sub> / P<sub>i</sub>*.

When Skyscraper Center had no city page, I took the tallest figure from curated national tables on Wikipedia (India, Bangladesh, Pakistan summaries) or a short list of hand-checked municipal sources documented in the build script. Where both existed, I used the **maximum** of the Center height and the national-table height (mainly to correct under-reported figures in some South Asian extracts), never a fuzzy cross-match across unrelated cities.

*R<sub>i</sub>* is tiny, so the tables below multiply by 10<sup>6</sup> and report **micrometres of pinnacle per resident** (µm / person). Dubai at roughly 210 µm is handing each inhabitant about **0.21 millimetres** of Burj Khalifa if you insist on visualising it that way. The point of the scaling is comparative: Dhaka and Lagos sit in the low tens of micrometres because a tower that looks heroic in silhouette still disappears inside a demographic ocean.

## Who made the cut

Wikidata typing is messier than it has any right to be. I took the **hundred most populous** distinct English labels among entities whose `instance of` is exactly [`Q515`](https://www.wikidata.org/wiki/Q515) (`city`). That captures Beijing and omits Shanghai, because Shanghai’s ontology uses more specific “city in China” classes instead. Delhi and Guangzhou fall out for similar reasons. The ranking is therefore **not** “the world population top hundred by any single census definition”; it is “the hundred largest things Wikidata confidently calls `city` in the narrow sense.” Treat the set as a large stratified sample of the urban human experiment, not as a claim to completeness.

## What the numbers do

The distribution is **right-skewed** but not lawless. After the micrometre conversion the mean is about **54 µm**, the median near **48 µm**, and the 90th percentile lands just under **100 µm**. Below that mass you find city-states, affluent second cities, and petro-capital skylines. Above it you find the ultra-dense South Asian and West African basins where even a respectable tower leaves almost no per-capita trace.

### Upper tiers (selected)

| Rank | City | Tallest (m) | Pop (Wikidata) | µm / resident |
|---:|---|---:|---:|---:|
| 1 | Dubai | 828 | 3,944,751 | 209.9 |
| 2 | Taipei | 508 | 2,442,991 | 207.9 |
| 3 | Kuwait City | 413 | 2,989,000 | 138.2 |
| 4 | Kaohsiung | 348 | 2,733,964 | 127.3 |
| 5 | Busan | 412 | 3,453,198 | 119.3 |
| 6 | Perth | 253 | 2,141,834 | 118.1 |
| 7 | Algiers | 264 | 2,364,230 | 111.7 |
| 8 | Phnom Penh | 228 | 2,129,371 | 107.1 |
| 9 | Toronto | 298 | 2,794,356 | 106.6 |
| 10 | Caracas | 225 | 2,245,744 | 100.2 |
| 11 | Brisbane | 270 | 2,706,966 | 99.7 |
| 12 | Pyongyang | 274 | 2,863,000 | 95.7 |
| 13 | Tashkent | 267 | 2,956,384 | 90.3 |
| 14 | Xining | 219 | 2,467,965 | 88.7 |
| 15 | Los Angeles | 335 | 3,898,747 | 85.9 |

Dubai and Taipei are effectively tied once you account for rounding: different politics, similar order-of-magnitude story about **small denominator populations carrying very tall symbolic needles**. American coastal hubs (Los Angeles, later New York in the full table) land mid-pack not because their towers are short (they are not) but because Wikidata populations for consolidated cities swallow a lot of people.

Chinese administrative cities split into surreal land-area units; several megacity prefectures occupy the **lower third** despite skyscrapers exceeding 400 m, because *P<sub>i</sub>* includes millions of exurban residents who will never set foot in the central business district tall zone. That is not a bug in the algebra; it is the algebra **punishing inclusive municipal boundaries**.

### Basement floor (selected)

| Rank | City | Tallest (m) | Pop (Wikidata) | µm / resident |
|---:|---|---:|---:|---:|
| 89 | Bamako | 80 | 4,227,569 | 18.9 |
| 90 | Prayagraj | 110 | 5,954,391 | 18.5 |
| 91 | Yangon | 122 | 6,874,000 | 17.7 |
| 92 | Kumasi | 65 | 3,903,480 | 16.7 |
| 93 | Surat | 93 | 5,935,000 | 15.6 |
| 94 | São Paulo | 172 | 11,451,999 | 15.0 |
| 95 | Kano | 62 | 4,348,000 | 14.3 |
| 96 | Lima | 140 | 9,943,800 | 14.1 |
| 97 | Chengdu | 284 | 20,937,757 | 13.6 |
| 98 | Lahore | 150 | 11,126,285 | 13.5 |
| 99 | Lagos | 160 | 15,070,000 | 10.6 |
| 100 | Dhaka | 171 | 16,800,000 | 10.2 |

Dhaka finishes last with **~10.2 µm** despite an earnest 171 m roof: the numerator is fine; the denominator is the demographic equivalent of a neutron star. If you wanted a policy reading, it is not “build tall”; it is “tall is a feeble lever when housing demand scales like compound interest.”

## How seriously to take this

Not very, and also quite a lot. The ranking is fragile to **boundary choice**: swap city-proper for metropolitan definitions and Taipei, Toronto, and Los Angeles dance several slots without changing a single steel beam. It ignores slums, informal floors, and anything below high-rise prestige thresholds. It treats one spire as the stand-in for an entire vertical program. It cannot know whether you *wanted* skyline ego or flood-safe mass timber.

What survives those caveats is the reminder that **extensive growth** (more bodies) and **intensive growth** (higher steel) are logged on different ledgers. Most public conversations fuse them into a single aesthetic judgement. Separating them with a brutish ratio does not solve urban planning. It does make the trade-off legible: you can always win the height arms race in the photograph; you cannot automatically win it in the denominator.

Full machine-readable rankings (all 100 rows) live alongside the Jekyll tree in [`misc/skyline_per_capita_ranked.json`](https://github.com/kiankyars/kiankyars.github.io/blob/main/misc/skyline_per_capita_ranked.json). The reproducible merge logic is `misc/build_skyline_rankings.py`, with raw Skyscraper Center passes cached by `misc/skyline_per_capita_data.py`.

If you redo the scrape in five years, check whether Dubai still anchors the top: the exciting scientific result would not be a reshuffle, but a **systematic decline** in the ratio across emerging markets as populations outrun even aggressive vertical construction. That would tell you something about asymptotics that photographs never will.
