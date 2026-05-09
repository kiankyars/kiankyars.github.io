---
layout: post
title: claude code
date: 2026-04-01
categories: ai
---

## Summary

- The leaky npm build was **`2.1.88`**, published at **2026-03-30 22:36:48 UTC**.
- `2.1.88` vanished from npm's live version endpoints. The registry ledger retained the timestamp, but the per-version manifest returned `version not found`. The expected tarball URL returned **HTTP 404**.
- Chaofan Shou published the first discovery post at **2026-03-31 08:23:33 UTC**.
- The mirror and rewrite wave started immediately: `instructkr/claw-code` appeared at **08:58:08 UTC**, `paoloanzn/free-code` at **11:11:49 UTC**, and `alex000kim/claude-code` at **12:47:09 UTC**.
- Anthropic published **`2.1.89`** at **2026-03-31 23:32:40 UTC**. Its live tarball contained **no `.map` files**.

## Timeline

| Pacific | Event | Source |
|---|---|---|
| 2026-03-11 01:21:38 | Bun issue `#28001` is opened: "Source map incorrectly served when in production." | [GitHub issue API](https://api.github.com/repos/oven-sh/bun/issues/28001), [issue page](https://github.com/oven-sh/bun/issues/28001) |
| 2026-03-18 21:26:48 | OpenCode opens PR `#18186`, titled `anthropic legal requests`. | [GitHub PR API](https://api.github.com/repos/anomalyco/opencode/pulls/18186), [PR page](https://github.com/anomalyco/opencode/pull/18186) |
| 2026-03-18 21:45:24 | OpenCode merges PR `#18186`, removing Anthropic-specific auth and references. | [GitHub PR API](https://api.github.com/repos/anomalyco/opencode/pulls/18186) |
| 2026-03-30 15:36:48 | npm records publication of Claude Code version `2.1.88`. | [npm registry ledger](https://registry.npmjs.org/@anthropic-ai/claude-code) |
| 2026-03-31 01:23:33 | Chaofan Shou (`@Fried_rice`) posts the first public leak notice. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code) and [Alex Kim](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/): `https://x.com/Fried_rice/status/2038894956459290963` |
| 2026-03-31 01:58:08 | `instructkr/claw-code` is created on GitHub. | [GitHub repo API](https://api.github.com/repos/instructkr/claw-code), [repo page](https://github.com/instructkr/claw-code) |
| 2026-03-31 02:00:40 | The main Hacker News thread goes live. | [HN item `47584540`](https://hacker-news.firebaseio.com/v0/item/47584540.json), [HN thread](https://news.ycombinator.com/item?id=47584540) |
| 2026-03-31 04:11:49 | `paoloanzn/free-code` is created. | [GitHub repo API](https://api.github.com/repos/paoloanzn/free-code), [repo page](https://github.com/paoloanzn/free-code) |
| 2026-03-31 05:37:02 | Wes Bos posts about the spinner verb list. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code): `https://x.com/wesbos/status/2038958747200962952` |
| 2026-03-31 05:47:09 | `alex000kim/claude-code` is created as a source mirror. | [GitHub repo API](https://api.github.com/repos/alex000kim/claude-code), [repo page](https://github.com/alex000kim/claude-code) |
| 2026-03-31 06:04:30 | Alex Kim's breakdown hits Hacker News. | [HN item `47586778`](https://hacker-news.firebaseio.com/v0/item/47586778.json), [HN thread](https://news.ycombinator.com/item?id=47586778) |
| 2026-03-31 07:24:22 | Gergely Orosz outlines PR and legal risks of suing rewrites. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code): `https://x.com/GergelyOrosz/status/2038985760175505491` |
| 2026-03-31 09:50:02 | Paolo Anzani posts `free-code`, a stripped fork without telemetry. | X URL from [free-code](https://github.com/paoloanzn/free-code): `https://x.com/paoloanzn/status/2039022418698907949` |
| 2026-03-31 16:32:40 | npm records publication of Claude Code version `2.1.89`. | [npm registry ledger](https://registry.npmjs.org/@anthropic-ai/claude-code), [2.1.89 manifest](https://registry.npmjs.org/%40anthropic-ai%2Fclaude-code/2.1.89) |
| 2026-03-31 19:32:13 | Boris Cherny attributes the leak to developer error. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code): `https://x.com/bcherny/status/2039168928145109343` |
| 2026-03-31 22:18:12 | Cherny follows up with a blameless-postmortem framing. | X URL cited in [Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code): `https://x.com/bcherny/status/2039210700657307889` |
| 2026-04-01 16:31:39 | npm records publication of Claude Code version `2.1.90`. | [npm registry ledger](https://registry.npmjs.org/@anthropic-ai/claude-code) |

## Critical disclosures

The source code exposed Anthropic's strategic direction:

- **Roadmap leakage**: The `KAIROS` and `PROACTIVE` paths detailed Anthropic's background-agent trajectory.
- **Moat design**: Anti-distillation flags, fake-tool injection, connector-text summarization, and native-client attestation revealed product protection strategies.
- **Internal naming and launch hints**: Codenames and launch comments signaled future features.
- **Harness architecture**: Prompt-cache boundaries, compaction strategies, LSP tooling, and coordinator-mode prompting provided a blueprint for production coding agents.

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
