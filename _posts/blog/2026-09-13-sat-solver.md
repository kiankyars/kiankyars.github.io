---
layout: post
title: make a SAT solver faster
date: 2026-09-13
categories: machine_learning
---

I wanted to test the latest generation models on well-defined optimization tasks, to see whether they could get incremental improvements. My initial though was to improve compression techniques, but the problem there is that compression techniques are based on the data type, so you can have a compression technique that is really good at compressing a specific type of video, and so on. Therefore, I said to myself, "Compression is task-specific, and it would be hard to demonstrate a general improvement." I subsquently asked Astra 6 to make an existing SAT solver faster, which Astra proposed as a promising task.

Only the solver source could change, and I used a SAT solving compeition which already has an LLM track for ease-of-integration; answers also needed independently checked certificates (whatever that means, I don't know how SAT solvers work). The exact score was PAR-2, which is apparently average runtime, with failures charged twice the timeout.

The agent initially reported a 0.054% improvement and declared success. That difference was smaller than the variation between runs. After that, I switched to goal mode, and one preprocessing change shrank a formula from 140 MiB to 49 MiB. The algo timed out, though, and overall performance got worse. Another change solved a previously failing problem but lost a solve elsewhere (classic ground-hogger).

A later candidate scored 1.1% better in one run, with both versions still solving 10/30 problems. These were 30-second trials in Docker Desktop. I haven't repeated that result or tested unseen families, so I don't yet have a confirmed improvement, and not really interested in digging deeper into this, since I am already at the pareto-optimal 80% of intuition from 20% effort threshold imo.

The most useful part of this experiment was catching how easily a small positive number became a claim of success, and I conclude that there is not that much free alpha in single-task hill-climbing on verifiable tasks, even with frontier models. Notwithstanding, if you put a domain expert behind Codex instead, then I think that's an easy way to get substantial gains. Also, if you choose some domain that is only semi-verifiable or some intersection of a verifiable and non-verifiable domain, and really go deep into it, that's another case where I think there's a lot of potential.

If you guys want to check out the [repo](https://github.com/kiankyars/sat-solver-eval), go ahead.
