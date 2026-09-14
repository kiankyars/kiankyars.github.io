---
layout: post
title: trying to make a SAT solver faster
date: 2026-09-13
categories: machine_learning
---

I wanted to test the latest generation of models on well-defined optimization tasks, to see whether they could get incremental improvements. I started by asking an agent to make an existing SAT solver faster.

Only solver source could change. The benchmark, checker, build and resource limits stayed fixed. Answers needed independently checked certificates. The score was PAR-2: average runtime, with failures charged twice the timeout.

The agent initially reported a 0.054% improvement and declared success. That difference was smaller than the variation between runs. I had to ask whether it was actually meaningful.

One preprocessing change shrank a formula from 140 MiB to 49 MiB. It still timed out, and overall performance got worse. Another change solved a previously failing problem but lost a solve elsewhere. Proof-file limits and checker timeouts also counted as failures; getting an answer was only useful if it could be verified within the limits.

A later candidate scored about 1.1% better in one run, with both versions still solving 10/30 problems. These were 30-second trials in Docker Desktop. I haven't repeated that result or tested unseen families, so I don't yet have a confirmed improvement.

The most useful part of this experiment was catching how easily a small positive number became a claim of success, even with a precise objective and automatic feedback.
