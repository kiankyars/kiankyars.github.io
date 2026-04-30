---
layout: post
title: Skyline per capita
date: 2026-03-28
categories: data
---

I calculated the vertical metres of supertall architecture per resident for the world's largest cities. This metric divides the **architectural height of the tallest completed high-rise** by the municipal **headcount**.

A hundred people sharing a 100 m tower get **1 metre of pinnacle per person**. Doubling the population halves the ratio. At municipal scales, geology, flight paths, and CTBUH definitions complicate the calculation.

## The metric

For each city *i*, *H<sub>i</sub>* represents the tallest completed building tracked by the [CTBUH Skyscraper Center](https://www.skyscrapercenter.com/). *P<sub>i</sub>* represents the residential population from [Wikidata](https://www.wikidata.org/) property [P1082](https://www.wikidata.org/wiki/Property:P1082) using the **March 2026** snapshot. The ratio is *R<sub>i</sub> = H<sub>i</sub> / P<sub>i</sub>*.

When the Skyscraper Center lacked a city page, I used the tallest figure from curated national Wikipedia tables (India, Bangladesh, Pakistan) or hand-checked municipal sources. Where both existed, I used the **maximum** of the Center height and the national-table height to correct under-reported figures in South Asian extracts.

*R<sub>i</sub>* produces tiny values. The tables below multiply the result by 10<sup>6</sup> to report **micrometres of pinnacle per resident** (µm / person). Dubai allocates each inhabitant about **0.21 millimetres** of the Burj Khalifa. The scaling facilitates comparison. Dhaka and Lagos sit in the low tens of micrometres because their massive populations absorb the height of their tallest towers.

## Who made the cut

I selected the **hundred most populous** distinct English labels among Wikidata entities typed exactly as [`Q515`](https://www.wikidata.org/wiki/Q515) (`city`). This captures Beijing but omits Shanghai, Delhi, and Guangzhou, which use more specific regional classifications. The ranking represents a stratified sample of the hundred largest entities Wikidata confidently classifies as a `city`.

## What the numbers do

The distribution skews right. The mean sits at **54 µm**, the median near **48 µm**, and the 90th percentile lands just under **100 µm**. City-states, affluent second cities, and petro-capitals dominate the upper percentiles. Ultra-dense South Asian and West African basins occupy the bottom, where tall towers leave almost no per-capita trace.

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

Dubai and Taipei share similar ratios resulting from small denominator populations and very tall buildings. American coastal hubs like Los Angeles land mid-pack because their consolidated Wikidata populations dilute the impact of their skyscrapers.

Chinese megacity prefectures occupy the lower third despite building skyscrapers exceeding 400 m. Their population figures (*P<sub>i</sub>*) include millions of exurban residents outside the central business district. The algebra mathematically penalizes these inclusive municipal boundaries.

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

Dhaka finishes last with **10.2 µm**, despite a 171 m tower. The denominator dwarfs the numerator. Tall buildings fail to impact per-capita metrics when housing demand scales exponentially.

## Caveats

The ranking depends entirely on boundary definitions. Swapping city-proper boundaries for metropolitan areas shifts Taipei, Toronto, and Los Angeles significantly. The metric ignores slums, informal housing, and buildings below high-rise thresholds. It uses a single spire to represent an entire skyline and ignores architectural intent like flood safety or aesthetic prestige.

Extensive growth (population) and intensive growth (building height) scale independently. The ratio makes this trade-off legible. A city can build the world's tallest tower, but rapid population growth will erase its per-capita impact.

Full machine-readable rankings (all 100 rows) live alongside the Jekyll tree in [`misc/skyline_per_capita_ranked.json`](https://github.com/kiankyars/kiankyars.github.io/blob/main/misc/skyline_per_capita_ranked.json). The reproducible merge logic is `misc/build_skyline_rankings.py`, with raw Skyscraper Center passes cached by `misc/skyline_per_capita_data.py`.

Future scrapes should check whether Dubai retains the top rank. A systematic decline across emerging markets would indicate populations outrunning vertical construction.
