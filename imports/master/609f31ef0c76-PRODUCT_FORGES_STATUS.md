# Product Forges — status audit (2026-08-10)

Checked every tool's actual entry point (not just that a `start.command` file
exists) by running it and reading what happens. Full picture below.

| Tool | Port | Status | Launch |
|---|---|---|---|
| **SavvyAppForge** | 4427 | 🔴 Broken | `start.command` |
| **SavvySiteForge** | 4428 | 🔴 Broken | `start.command` |
| **SavvyTubeForge** | 4429 | 🟢 Working | `start.command` |
| **SavvyMarketForge** | 4430 | 🔴 Broken | `start.command` |
| **SavvyHomeForge** | 4431 | 🔴 Broken | `start.command` |
| **Track Forge** | 4432 | 🟢 Working | `start.command` |

## The broken four — same root cause

`start.command` and the `.app` wrapper both run `node src/server.js` in each
tool's folder. In all four, `src/`, `public/`, and `scripts/` are **completely
empty** — no server was ever actually written. Running the `.app` directly
confirms it: `Error: Cannot find module '.../src/server.js'`.

This traces back to the original ChatGPT/Codex build session (2026-07-17) that
built all 6 "Forge" tools — see `integration_log.md` 2026-08-07 entry.
SavvyTubeForge is the only one that got a real rebuild after that session was
found to be broken; the other four were never revisited.

Despite the empty `src/`, three of the four have real content sitting in
`generated/` — meaning something *did* produce real output at some point,
just not through this `src/server.js` path (most likely written directly by
a ChatGPT/Codex session, not by running a local tool):

- **SavvyAppForge** (`generated/`): a full-stack scaffold — auth, billing,
  database schema, deployment config (Dockerfile, render.yaml) — for what
  looks like a commercial AI-app-generator product, plus a separate
  "luxury AI automation" website scaffold.
- **SavvySiteForge** (`generated/`): a campsite-rental website scaffold, plus
  a duplicate of the same "commercial AI app generator" scaffold AppForge has.
- **SavvyMarketForge** (`generated/bidflow`): despite the name, the actual
  output is a rendered .mp4 + narration .aiff + several .svg assets — a
  promotional/marketing video, not a GovCon bid document. "bidflow" looks
  like it was the name of a demo product it made a commercial for, not
  what the tool itself does. So MarketForge appears to be a marketing-video
  generator, closer in concept to SavvyTubeForge/Track Forge than to the
  GovCon pipeline — worth confirming with Joe before assuming scope.
- **SavvyHomeForge**: `generated/` is empty — this one has never produced
  anything, not even once.

## What it would take to fix them

Rebuilding these to actually work is a real project per tool, comparable in
size to the SavvyTubeForge rebuild (real Node server + real generation logic
+ a working UI) — not a quick patch. Before starting any of them I'd want
from Joe:

1. **What each tool is actually supposed to do**, in his words — the
   `generated/` folders are a clue but not a spec. In particular:
   HomeForge's purpose isn't clear from anything on disk (home automation?
   home-services business generator?).
2. **Whether MarketForge should even be separate from the GovCon pipeline**,
   given the `bidflow` naming overlap.
3. **Priority order** — which one(s) Joe actually wants working first, since
   doing all four is a multi-session effort.

Not started without that direction — didn't want to guess at requirements
and build the wrong thing four times over.
