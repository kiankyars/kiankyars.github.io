---
layout: post
title: Skyline per capita
date: 2026-03-28
categories: data
---

I divided each city's tallest completed building by its population.

## The metric

For each city _i_, _H<sub>i</sub>_ is the tallest completed building tracked by the [CTBUH Skyscraper Center](https://www.skyscrapercenter.com/). _P<sub>i</sub>_ is the residential population from [Wikidata](https://www.wikidata.org/) property [P1082](https://www.wikidata.org/wiki/Property:P1082) using the March 2026 snapshot. The ratio is _R<sub>i</sub> = H<sub>i</sub> / P<sub>i</sub>_.

When the Skyscraper Center lacked a city page, I used the tallest figure from national Wikipedia tables (India, Bangladesh, Pakistan) or hand-checked municipal sources.

_R<sub>i</sub>_ is tiny, so the tables multiply by 10<sup>6</sup> and report micrometres per resident (µm / person). In Dubai that's about 0.21 millimetres of the Burj Khalifa per person.

### Top 15

| Rank | City        | Tallest (m) | Pop (Wikidata) | µm / resident |
| ---: | ----------- | ----------: | -------------: | ------------: |
|    1 | Dubai       |         828 |      3,944,751 |         209.9 |
|    2 | Taipei      |         508 |      2,442,991 |         207.9 |
|    3 | Kuwait City |         413 |      2,989,000 |         138.2 |
|    4 | Kaohsiung   |         348 |      2,733,964 |         127.3 |
|    5 | Busan       |         412 |      3,453,198 |         119.3 |
|    6 | Perth       |         253 |      2,141,834 |         118.1 |
|    7 | Algiers     |         264 |      2,364,230 |         111.7 |
|    8 | Phnom Penh  |         228 |      2,129,371 |         107.1 |
|    9 | Toronto     |         298 |      2,794,356 |         106.6 |
|   10 | Caracas     |         225 |      2,245,744 |         100.2 |
|   11 | Brisbane    |         270 |      2,706,966 |          99.7 |
|   12 | Pyongyang   |         274 |      2,863,000 |          95.7 |
|   13 | Tashkent    |         267 |      2,956,384 |          90.3 |
|   14 | Xining      |         219 |      2,467,965 |          88.7 |
|   15 | Los Angeles |         335 |      3,898,747 |          85.9 |

### Basement

| Rank | City      | Tallest (m) | Pop (Wikidata) | µm / resident |
| ---: | --------- | ----------: | -------------: | ------------: |
|   89 | Bamako    |          80 |      4,227,569 |          18.9 |
|   90 | Prayagraj |         110 |      5,954,391 |          18.5 |
|   91 | Yangon    |         122 |      6,874,000 |          17.7 |
|   92 | Kumasi    |          65 |      3,903,480 |          16.7 |
|   93 | Surat     |          93 |      5,935,000 |          15.6 |
|   94 | São Paulo |         172 |     11,451,999 |          15.0 |
|   95 | Kano      |          62 |      4,348,000 |          14.3 |
|   96 | Lima      |         140 |      9,943,800 |          14.1 |
|   97 | Chengdu   |         284 |     20,937,757 |          13.6 |
|   98 | Lahore    |         150 |     11,126,285 |          13.5 |
|   99 | Lagos     |         160 |     15,070,000 |          10.6 |
|  100 | Dhaka     |         171 |     16,800,000 |          10.2 |
