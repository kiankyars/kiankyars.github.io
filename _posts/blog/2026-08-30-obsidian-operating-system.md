---
layout: post
title: my obsidian operating system
date: 2026-08-30
categories: productivity
---

My [Obsidian](https://obsidian.md/) vault is no longer a notes app. It is the filesystem for my life.

## architecture

```text
Obsidian vault in iCloud Drive
├── iCloud: live sync between my Macs
└── Git: one guarded snapshot to private GitHub every midnight
```

This separation is the entire trick: iCloud moves files; Git remembers them.

One Mac is the only Git writer. Every midnight, a LaunchAgent checks that every iCloud file is downloaded, waits until the vault is stable, and refuses to continue if GitHub has diverged. It then commits and pushes the complete vault; large voice recordings go through Git LFS. Bruh, a backup which silently snapshots half a vault is worse than no backup because it gives fake confidence.

If you already have enough iCloud storage, the marginal cost is zero. This does not reproduce literally every Obsidian Sync feature, but it gives me the two I actually care about: automatic replication and inspectable version history which I own.

## workflow

`capture → act → distill → review`

Everything first lands in a dated daily note. Each day has only three fixed prompts: **must win today**, **proof of day**, and **reconnaissant**. My calendar becomes a short plan for the day, while a dashboard rolls selected weekly, monthly, and yearly notes upward.

If something should still matter in a month, I promote it into a durable note. Which is to say, the daily note can be messy; the knowledge base cannot. Voice memos are transcribed and integrated, and coding agents work directly against the same Markdown instead of living in some disconnected chat universe.

## systems

- **notes:** 600+ dated notes are the capture layer, journal, and execution log.
- **research:** date-bound findings begin in the daily note; durable ideas graduate into source-grounded research notes.
- **running:** Polar is the source of truth; scripts generate the training record, while the plan, evergreen playbook, and old blocks stay separate.
- **job search:** one pipeline for applications, one tracker for outreach, and one durable note per important conversation.
- **relationships:** people notes hold stable context; tasks stay in daily notes so the relationship files do not rot into stale to-do lists.
- **learning:** the best research becomes spaced-repetition flashcards, so useful ideas eventually become recallable knowledge.

## why this works

The folders are not the point. Every system shares one substrate: ordinary local Markdown. I can think in Obsidian, automate with scripts, delegate to agents, search with Unix tools, and recover any previous state with Git. There is no export step and no platform-shaped data prison.

For an Apple-only workflow, this is the best setup I have found: fast enough to disappear, strict enough not to rot, and open enough that I can leave whenever I want.
