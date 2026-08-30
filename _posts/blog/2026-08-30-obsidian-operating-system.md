---
layout: post
title: my obsidian operating system
date: 2026-08-30
categories: productivity
---

My [Obsidian](https://obsidian.md/) vault is the filesystem for my life.

## architecture

```text
Obsidian vault in iCloud Drive
├── iCloud: live sync between my Macs
└── Git: one snapshot to private GitHub every midnight
```

My Mac mini is the only Git writer; every midnight, a LaunchAgent commits and pushes the complete vault; large voice recordings go through Git LFS.

## workflow

I make one dated note every day in `notes/YYYY-MM-DD.md`; there are 617 of them at the moment. The template has three prompts, **must win today**, **proof of day**, and **gratefullness**, and I add a plan based on my calendar. If I learn something, meet someone, have an idea, or simply want to remember what happened, I write it there without first deciding where it belongs permanently. I also have a shortcut on my iPhone, which I speak to, and then the audio is uploaded to my Mac via iCloud, which uses Gemini Flash 3.7 to transcribe into the Daily Note. I actually don't have the Obsidian app on my phone, and I believe that that's an anti-pattern because, instead of having to type and open up the app, I just literally press the shortcut button on my iPhone and can register any thought quickly. This feature is useful because I record many thoughts while walking and would otherwise never write them down.

A dashboard shows the bullets I marked as important for the current week, month, and year. People notes are in a folder called people; every person has a file with their name.md, e.g. people/kian.md. They contain facts and context about someone, but follow-ups stay in daily notes because otherwise every person page eventually becomes a graveyard of stale tasks (I learned this by creating the graveyard first).

## systems

My AI running-coach uses the polar api as the source of truth, a script generates the training report, `plan.md` contains the current block, `playbook.md` contains the rules which should survive any one block, and completed plans go into an archive.

My job-search system has an application pipeline, a separate outreach tracker, and one note for every important conversation.

Research which I actually need to remember becomes spaced-repetition flashcards with the obsidian-spaced-repitition extension.
