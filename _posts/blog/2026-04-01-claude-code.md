---
layout: post
title: claude code
date: 2026-04-01
categories: ai
---

Accounts of the Claude Code leak typically summarize code findings or retell the story from memory. This post reconstructs the chronology using public artifacts: the [npm registry time ledger for `@anthropic-ai/claude-code`](https://registry.npmjs.org/@anthropic-ai/claude-code), GitHub repository metadata, GitHub issues and pull requests, the [GitHub DMCA notice](https://github.com/github/dmca/blob/master/2026/03/2026-03-31-anthropic.md), and Hacker News item JSON. For X links, I decoded the Snowflake ID to recover the exact creation timestamp. 

## Summary

- The leaky npm build was **`2.1.88`**, published at **2026-03-30 22:36:48 UTC**.
- `2.1.88` vanished from npm's live version endpoints. The registry ledger retained the timestamp, but the per-version manifest returned `version not found`. The expected tarball URL returned **HTTP 404**.
- Chaofan Shou published the first discovery post at **2026-03-31 08:23:33 UTC**.
- The mirror and rewrite wave started immediately: `instructkr/claw-code` appeared at **08:58:08 UTC**, `paoloanzn/free-code` at **11:11:49 UTC**, and `alex000kim/claude-code` at **12:47:09 UTC**.
- Anthropic published **`2.1.89`** at **2026-03-31 23:32:40 UTC**. Its live tarball contained **no `.map` files**.
- Anthropic engineer Boris Cherny explained the leak **after** it spread across GitHub and Hacker News.

## Method

- **npm timestamps** come from the package's `time` object in the registry JSON.
- **GitHub repo creation times** come from the GitHub API, capturing original creation rather than branch history.
- **X post times** are decoded directly from the Snowflake IDs.

## The timeline

All times below are exact UTC and Pacific times derived directly from the sources.

| UTC | Pacific | Event | Source |
|---|---|---|---|
| 2026-03-11 08:21:38 | 2026-03-11 01:21:38 | Bun issue `#28001` is opened: "Source map incorrectly served when in production." | [GitHub issue API](https://api.github.com/repos/oven-sh/bun/issues/28001), [issue page](https://github.com/oven-sh/bun/issues/28001) |
| 2026-03-19 04:26:48 | 2026-03-18 21:26:48 | OpenCode opens PR `#18186`, titled `anthropic legal requests`. | [GitHub PR API](https://api.github.com/repos/anomalyco/opencode/pulls/18186), [PR page](https://github.com/anomalyco/opencode/pull/18186) |
| 2026-03-19 04:45:24 | 2026-03-18 21:45:24 | OpenCode merges PR `#18186`, removing Anthropic-specific auth and references. | [GitHub PR API](https://api.github.com/repos/anomalyco/opencode/pulls/18186) |
| 2026-03-30 22:36:48.424 | 2026-03-30 15:36:48 | npm records publication of Claude Code version `2.1.88`. | [npm registry ledger](https://registry.npmjs.org/@anthropic-ai/claude-code) |
| 2026-03-31 08:23:33.113 | 2026-03-31 01:23:33 | Chaofan Shou (`@Fried_rice`) posts the first public leak notice. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code) and [Alex Kim](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/): `https://x.com/Fried_rice/status/2038894956459290963` |
| 2026-03-31 08:58:08 | 2026-03-31 01:58:08 | `instructkr/claw-code` is created on GitHub. | [GitHub repo API](https://api.github.com/repos/instructkr/claw-code), [repo page](https://github.com/instructkr/claw-code) |
| 2026-03-31 09:00:40 | 2026-03-31 02:00:40 | The main Hacker News thread goes live. | [HN item `47584540`](https://hacker-news.firebaseio.com/v0/item/47584540.json), [HN thread](https://news.ycombinator.com/item?id=47584540) |
| 2026-03-31 11:11:49 | 2026-03-31 04:11:49 | `paoloanzn/free-code` is created. | [GitHub repo API](https://api.github.com/repos/paoloanzn/free-code), [repo page](https://github.com/paoloanzn/free-code) |
| 2026-03-31 12:37:02.011 | 2026-03-31 05:37:02 | Wes Bos posts about the spinner verb list. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code): `https://x.com/wesbos/status/2038958747200962952` |
| 2026-03-31 12:47:09 | 2026-03-31 05:47:09 | `alex000kim/claude-code` is created as a source mirror. | [GitHub repo API](https://api.github.com/repos/alex000kim/claude-code), [repo page](https://github.com/alex000kim/claude-code) |
| 2026-03-31 13:04:30 | 2026-03-31 06:04:30 | Alex Kim's breakdown hits Hacker News. | [HN item `47586778`](https://hacker-news.firebaseio.com/v0/item/47586778.json), [HN thread](https://news.ycombinator.com/item?id=47586778) |
| 2026-03-31 14:24:22.406 | 2026-03-31 07:24:22 | Gergely Orosz outlines PR and legal risks of suing rewrites. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code): `https://x.com/GergelyOrosz/status/2038985760175505491` |
| 2026-03-31 16:50:02.479 | 2026-03-31 09:50:02 | Paolo Anzani posts `free-code`, a stripped fork without telemetry. | X URL from [free-code](https://github.com/paoloanzn/free-code): `https://x.com/paoloanzn/status/2039022418698907949` |
| 2026-03-31 23:32:40.530 | 2026-03-31 16:32:40 | npm records publication of Claude Code version `2.1.89`. | [npm registry ledger](https://registry.npmjs.org/@anthropic-ai/claude-code), [2.1.89 manifest](https://registry.npmjs.org/%40anthropic-ai%2Fclaude-code/2.1.89) |
| 2026-04-01 02:32:13.053 | 2026-03-31 19:32:13 | Boris Cherny attributes the leak to developer error. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code): `https://x.com/bcherny/status/2039168928145109343` |
| 2026-04-01 05:18:12.396 | 2026-03-31 22:18:12 | Cherny follows up with a blameless-postmortem framing. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code): `https://x.com/bcherny/status/2039210700657307889` |
| 2026-04-01 23:31:39.018 | 2026-04-01 16:31:39 | npm records publication of Claude Code version `2.1.90`. | [npm registry ledger](https://registry.npmjs.org/@anthropic-ai/claude-code) |

## Key timeline revelations

### 1. The leaked build was `2.1.88`

- The npm registry ledger records **`2.1.88` at 2026-03-30 22:36:48.424 UTC**.
- The live per-version manifest for `2.1.88` returns **`version not found`**.
- The tarball URL for `2.1.88` at **2026-04-02 00:36:23 UTC** returned **HTTP 404**.
- The `2.1.89` tarball at **2026-04-02 00:36:25 UTC** lacked **`.map` files**.

Anthropic published a leaky `2.1.88` on **March 30**, and replaced it with a cleaned `2.1.89` after public discovery on **March 31**. The registry preserved the initial publication timestamp despite the metadata deletion.

### 2. The public leak window lasted nearly ten hours

`2.1.88` published at **2026-03-30 22:36:48 UTC**. Chaofan Shou posted the discovery at **2026-03-31 08:23:33 UTC**. The package sat exposed for almost ten hours before drawing public attention.

### 3. The mirror wave preempted Anthropic's response

Boris Cherny posted the first public explanation at **2026-04-01 02:32:13 UTC**. By then, the leak had:

- circulated for **18 hours** following Chaofan's post.
- generated three prominent GitHub mirrors (`claw-code`, `free-code`, `alex000kim/claude-code`).
- dominated Hacker News.

Anthropic executed containment. The mirrors transformed a packaging error into an uncontainable distribution event.

### 4. OpenCode primed the audience

On **March 18**, OpenCode removed Anthropic-specific authentication files due to legal pressure. The developer community already focused on platform control and closed clients. When the source exposed anti-distillation hooks, fake-tool injection, and Bun-level client attestation, developers interpreted them as strategic maneuvers.

### 5. Bun previewed the failure mode

Bun issue `#28001` opened on **2026-03-11 08:21:38 UTC**, titled **"Source map incorrectly served when in production."** The underlying toolchain publicly documented the exact failure mode twenty days before the Claude Code leak. 

## Date-only events

Certain major events lack exact public timestamps:

- The GitHub DMCA notice exists as [2026-03-31-anthropic.md](https://github.com/github/dmca/blob/master/2026/03/2026-03-31-anthropic.md). GitHub processed the takedown against **8.1K repositories**.
- [Engineer's Codex published its roundup on April 1, 2026](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code).
- [Alex Kim published his breakdown on March 31, 2026](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/). He created his repo mirror at **12:47:09 UTC**.

## Critical disclosures

The source code exposed Anthropic's strategic direction:

- **Roadmap leakage**: The `KAIROS` and `PROACTIVE` paths detailed Anthropic's background-agent trajectory.
- **Moat design**: Anti-distillation flags, fake-tool injection, connector-text summarization, and native-client attestation revealed product protection strategies.
- **Internal naming and launch hints**: Codenames and launch comments signaled future features.
- **Harness architecture**: Prompt-cache boundaries, compaction strategies, LSP tooling, and coordinator-mode prompting provided a blueprint for production coding agents.

## Remaining uncertainties

Public sources leave minor gaps:

- The precise minute Anthropic invalidated `2.1.88` remains hidden.
- The exact submission time for the DMCA notice is absent from GitHub's record.
- The leak's root cause—a Bun behavior versus an independent packaging mistake—remains unproven.

## Bottom line

Anthropic published a leaky Claude Code build, `2.1.88`, on **March 30, 2026 at 22:36:48 UTC**. Chaofan Shou surfaced it publicly at **08:23:33 UTC** on March 31. The code rapidly populated GitHub mirrors and Hacker News. Anthropic published a cleaned `2.1.89` at **23:32:40 UTC**, followed hours later by the first engineer explanation. 

A ten-hour packaging exposure became a massive ecosystem event. The audience, primed by the OpenCode conflict and a documented Bun source-map bug, mirrored and analyzed the product before the company could respond. A packaging mistake is fixable; a distribution event is permanent.

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
