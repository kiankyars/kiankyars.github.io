---
layout: post
title: The Claude Code leak saga
date: 2026-04-01
categories: ai
---

Most writeups about the Claude Code leak do one of two things: they either summarize the juicy code findings, or they retell the story from memory. Both leave out the most useful part: **what actually happened, in what order, and which claims still survive contact with primary-source timestamps**.

This post is a chronology built from public artifacts: the [npm registry time ledger for `@anthropic-ai/claude-code`](https://registry.npmjs.org/@anthropic-ai/claude-code), GitHub repository metadata, GitHub issues and pull requests, the [GitHub DMCA notice](https://github.com/github/dmca/blob/master/2026/03/2026-03-31-anthropic.md), and Hacker News item JSON. For X links, I use the public URL and decode the Snowflake ID to recover the creation timestamp. When I infer something rather than observe it directly, I say so.

## The short version

- The best public evidence says the leaky npm build was **`2.1.88`**, published at **2026-03-30 22:36:48 UTC**.
- By the time I checked, `2.1.88` had effectively been scrubbed from npm's live version endpoints: its timestamp still existed in the registry ledger, but its per-version manifest returned `version not found`, and the guessed tarball URL returned **HTTP 404**.
- The first public discovery post I could timestamp was Chaofan Shou's at **2026-03-31 08:23:33 UTC**.
- The mirror and rewrite wave started almost immediately after that: `instructkr/claw-code` was created at **08:58:08 UTC**, `paoloanzn/free-code` at **11:11:49 UTC**, and `alex000kim/claude-code` at **12:47:09 UTC**.
- Anthropic's visible npm cleanup appears to be **`2.1.89`**, published at **2026-03-31 23:32:40 UTC**. Its tarball is live, and when I listed its contents it contained **no `.map` files**.
- Anthropic engineer Boris Cherny's public explanation came **after** the leak had already spent the whole day spreading through GitHub and HN.

## Method

Three notes matter for reading the table below:

1. **npm timestamps** come from the package's `time` object in the registry JSON. That is the cleanest public record of when a version was published.
2. **GitHub repo creation times** come from the GitHub API, not from today's branch history. That distinction matters because the current branch history of a fast-moving mirror repo does not necessarily preserve its original public state.
3. **X post times** are decoded from the post IDs themselves. This is not guesswork. X Snowflake IDs embed the creation timestamp.

## The timeline

All times below are exact when the source exposes an exact time. I list both UTC and Pacific time because the story was discussed mostly in US developer circles, but the raw sources are a mix of UTC, local time, and date-only displays.

| UTC | Pacific | Event | Source |
|---|---|---|---|
| 2026-03-11 08:21:38 | 2026-03-11 01:21:38 | Bun issue `#28001` is opened: "Source map incorrectly served when in production." | [GitHub issue API](https://api.github.com/repos/oven-sh/bun/issues/28001), [issue page](https://github.com/oven-sh/bun/issues/28001) |
| 2026-03-19 04:26:48 | 2026-03-18 21:26:48 | OpenCode opens PR `#18186`, titled `anthropic legal requests`. | [GitHub PR API](https://api.github.com/repos/anomalyco/opencode/pulls/18186), [PR page](https://github.com/anomalyco/opencode/pull/18186) |
| 2026-03-19 04:45:24 | 2026-03-18 21:45:24 | That OpenCode PR is merged, removing Anthropic-specific auth and related references. | [GitHub PR API](https://api.github.com/repos/anomalyco/opencode/pulls/18186) |
| 2026-03-30 22:36:48.424 | 2026-03-30 15:36:48 | npm records publication of Claude Code version `2.1.88`. | [npm registry ledger](https://registry.npmjs.org/@anthropic-ai/claude-code) |
| 2026-03-31 08:23:33.113 | 2026-03-31 01:23:33 | Chaofan Shou (`@Fried_rice`) posts the first public leak notice I could timestamp. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code) and [Alex Kim](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/): `https://x.com/Fried_rice/status/2038894956459290963` |
| 2026-03-31 08:58:08 | 2026-03-31 01:58:08 | `instructkr/claw-code` is created on GitHub. | [GitHub repo API](https://api.github.com/repos/instructkr/claw-code), [repo page](https://github.com/instructkr/claw-code) |
| 2026-03-31 09:00:40 | 2026-03-31 02:00:40 | The main Hacker News thread about the leak goes live. | [HN item `47584540`](https://hacker-news.firebaseio.com/v0/item/47584540.json), [HN thread](https://news.ycombinator.com/item?id=47584540) |
| 2026-03-31 11:11:49 | 2026-03-31 04:11:49 | `paoloanzn/free-code` is created. | [GitHub repo API](https://api.github.com/repos/paoloanzn/free-code), [repo page](https://github.com/paoloanzn/free-code) |
| 2026-03-31 12:37:02.011 | 2026-03-31 05:37:02 | Wes Bos posts about the leak's smaller curiosities, such as the spinner verb list. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code): `https://x.com/wesbos/status/2038958747200962952` |
| 2026-03-31 12:47:09 | 2026-03-31 05:47:09 | `alex000kim/claude-code` is created as another source mirror. | [GitHub repo API](https://api.github.com/repos/alex000kim/claude-code), [repo page](https://github.com/alex000kim/claude-code) |
| 2026-03-31 13:04:30 | 2026-03-31 06:04:30 | Alex Kim's breakdown hits Hacker News. | [HN item `47586778`](https://hacker-news.firebaseio.com/v0/item/47586778.json), [HN thread](https://news.ycombinator.com/item?id=47586778) |
| 2026-03-31 14:24:22.406 | 2026-03-31 07:24:22 | Gergely Orosz publicly frames the likely PR and proof problems around suing rewrites. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code): `https://x.com/GergelyOrosz/status/2038985760175505491` |
| 2026-03-31 16:50:02.479 | 2026-03-31 09:50:02 | Paolo Anzani posts `free-code`, the stripped fork with telemetry removed and experimental features unlocked. | X URL from [free-code](https://github.com/paoloanzn/free-code): `https://x.com/paoloanzn/status/2039022418698907949` |
| 2026-03-31 23:32:40.530 | 2026-03-31 16:32:40 | npm records publication of Claude Code version `2.1.89`. | [npm registry ledger](https://registry.npmjs.org/@anthropic-ai/claude-code), [2.1.89 manifest](https://registry.npmjs.org/%40anthropic-ai%2Fclaude-code/2.1.89) |
| 2026-04-01 02:32:13.053 | 2026-03-31 19:32:13 | Boris Cherny publicly says the leak was plain developer error, not a toolchain bug. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code): `https://x.com/bcherny/status/2039168928145109343` |
| 2026-04-01 05:18:12.396 | 2026-03-31 22:18:12 | Cherny follows up with the blameless-postmortem framing. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code): `https://x.com/bcherny/status/2039210700657307889` |
| 2026-04-01 23:31:39.018 | 2026-04-01 16:31:39 | npm records publication of Claude Code version `2.1.90`. | [npm registry ledger](https://registry.npmjs.org/@anthropic-ai/claude-code) |

## What this timeline says that most posts miss

### 1. The leaked build was almost certainly `2.1.88`, not `2.1.89`

This is the most important factual cleanup.

Public evidence:

- The npm registry ledger still records **`2.1.88` at 2026-03-30 22:36:48.424 UTC**.
- The live per-version manifest for `2.1.88` now returns **`version not found`**.
- When I checked the guessed tarball URL for `2.1.88` at **2026-04-02 00:36:23 UTC**, `https://registry.npmjs.org/@anthropic-ai/claude-code/-/claude-code-2.1.88.tgz` returned **HTTP 404**.
- When I checked `2.1.89` at **2026-04-02 00:36:25 UTC**, the tarball was live and listing its contents showed **no `.map` files**.

Inference: Anthropic appears to have published a leaky `2.1.88`, then replaced it with a cleaned `2.1.89` after the leak went public. The registry preserves the publication timestamp even though the leaked version's live metadata and tarball are no longer normally retrievable.

That is a materially better account than the usual "Anthropic accidentally shipped a sourcemap on March 31" summary. The most likely package publication happened on **March 30**, and public discovery happened on **March 31**.

### 2. The public leak window was roughly 9 hours and 47 minutes, not "instantly"

`2.1.88` was published at **2026-03-30 22:36:48 UTC**. Chaofan Shou's public discovery post came at **2026-03-31 08:23:33 UTC**.

That gap matters. It means the package appears to have sat in the wild for nearly ten hours before the first public post I could timestamp. This was still extremely fast, but it was not zero-latency internet omniscience.

### 3. The mirror wave beat the public Anthropic response by most of a day

By the time Cherny's first public explanation landed at **2026-04-01 02:32:13 UTC**, the leak had already:

- spent almost **18 hours** in the open since Chaofan's discovery post,
- produced at least three high-visibility GitHub descendants (`claw-code`, `free-code`, `alex000kim/claude-code`),
- reached the main HN thread,
- and crossed from "leaked package" into "rewrite, strip, mirror, analyze, argue about copyright."

This is why the visible Anthropic response reads as containment rather than prevention. Once the mirrors existed, the problem stopped being a package bug and became an information-propagation problem.

### 4. The leak landed in a pre-heated fight over closed clients

The leak did not occur into neutral space. On **March 18 to 19 Pacific time**, OpenCode was already removing Anthropic-specific auth and prompt files in direct response to Anthropic legal pressure.

That means the leak hit a developer public already primed to care about three things:

- first-party versus third-party access,
- client attestation and platform control,
- and whether Anthropic was tightening the moat around Claude Code.

So when the source exposed things like anti-distillation hooks, hidden feature flags, and Bun-level client attestation, people did not read them as isolated technical curiosities. They read them as evidence in an ongoing strategic fight.

### 5. The Bun issue was not proof, but it was a real warning shot

The Bun bug report was opened on **2026-03-11 08:21:38 UTC**, twenty days before the first public leak post. The issue title is blunt: **"Source map incorrectly served when in production."**

This does **not** prove that Bun caused the Claude Code leak. Anthropic could still have made an independent packaging mistake. But it does prove that the exact failure mode had already been documented publicly in the underlying toolchain. That is enough to make the "sounds impossible" framing too generous.

## Important date-only events

Some major events are public but do not expose an exact time in the source I could verify:

- The GitHub DMCA notice is filed as [2026-03-31-anthropic.md](https://github.com/github/dmca/blob/master/2026/03/2026-03-31-anthropic.md), and GitHub notes that it processed the takedown against a network of **8.1K repositories**.
- [Engineer's Codex published its roundup on April 1, 2026](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code).
- [Alex Kim published his breakdown on March 31, 2026](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/), and his repo mirror itself was created at **12:47:09 UTC** the same day.

## What actually leaked that mattered

The code itself was not the only important thing. The more durable disclosures were:

- **Roadmap leakage**: the `KAIROS` and `PROACTIVE` paths exposed a much clearer picture of Anthropic's background-agent direction than any public product page.
- **Moat design**: anti-distillation flags, fake-tool injection, connector-text summarization, and native-client attestation revealed how Anthropic thinks about protecting Claude Code as a product, not just as a model frontend.
- **Internal naming and launch hints**: model codenames and launch comments told competitors and power users where Anthropic was likely headed.
- **Harness architecture**: prompt-cache boundaries, compaction strategies, LSP tooling, and coordinator-mode prompting gave researchers and rival tool builders a more concrete blueprint for what a production coding agent harness looks like.

In other words, the real damage was not just "people saw the source." It was that they saw **the strategy encoded in the source**.

## What remains uncertain

There are still a few things public sources do not settle cleanly:

- The exact minute Anthropic unpublished or invalidated `2.1.88` is not exposed in the npm data I could verify.
- The exact time the DMCA notice was submitted is not public on the GitHub DMCA page.
- The public tweet texts themselves are harder to retrieve than the URLs, so for X I use the URL plus the timestamp encoded in the ID.
- It is still not publicly proven whether the leak came from a Bun behavior, a packaging mistake on Anthropic's side, or both.

Those are real uncertainties. They do not change the core chronology.

## Bottom line

The cleanest public reconstruction is this:

Anthropic likely published a leaky Claude Code build, `2.1.88`, on **March 30, 2026 at 22:36:48 UTC**. Chaofan Shou surfaced it publicly at **08:23:33 UTC** on March 31. Within hours the code had crossed into GitHub mirrors, stripped forks, rewrite projects, and Hacker News. Anthropic's visible npm cleanup, `2.1.89`, did not land until **23:32:40 UTC** that same day, and the first public engineer explanation came **after that**.

So the real saga is not just "Anthropic leaked a sourcemap." It is that a ten-hour packaging exposure turned into a one-day ecosystem event because it hit an audience already primed by the OpenCode fight, a toolchain with a publicly documented source-map bug, and a developer culture now fast enough to mirror, strip, fork, litigate, and mythologize a product before the original company can finish explaining what happened.

If you want the single most useful sentence in this whole story, it is this: **the leak was a package event for a few hours, but it became a distribution event almost immediately, and distribution events are much harder to unwind than packaging mistakes.**

## Primary sources

- [npm registry document for `@anthropic-ai/claude-code`](https://registry.npmjs.org/@anthropic-ai/claude-code)
- [npm manifest for `2.1.89`](https://registry.npmjs.org/%40anthropic-ai%2Fclaude-code/2.1.89)
- [GitHub repo metadata for `instructkr/claw-code`](https://api.github.com/repos/instructkr/claw-code)
- [GitHub repo metadata for `paoloanzn/free-code`](https://api.github.com/repos/paoloanzn/free-code)
- [GitHub repo metadata for `alex000kim/claude-code`](https://api.github.com/repos/alex000kim/claude-code)
- [OpenCode PR `#18186` (`anthropic legal requests`)](https://github.com/anomalyco/opencode/pull/18186)
- [Bun issue `#28001`](https://github.com/oven-sh/bun/issues/28001)
- [GitHub DMCA notice `2026-03-31-anthropic.md`](https://github.com/github/dmca/blob/master/2026/03/2026-03-31-anthropic.md)
- [HN item `47584540`](https://news.ycombinator.com/item?id=47584540)
- [HN item `47586778`](https://news.ycombinator.com/item?id=47586778)
- [HN item `47444748`](https://news.ycombinator.com/item?id=47444748)
- [Engineer's Codex roundup](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code)
- [Alex Kim's breakdown](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/)
