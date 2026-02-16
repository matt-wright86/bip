# Build in Public (BiP) Project

## Overview
Build in Public is a weekly lightly moderated open forum at Improving (a consulting company). The purpose is to create space for narrating real work, sharing unfinished thinking, and learning through explanation rather than performance.

**Facilitator**: Matthew Wright
**Schedule**: Fridays, 2:00–3:00 PM Central
**Format**: ~1 hour hybrid meeting (in-office + remote participants)

## File Naming Convention
All files should use the format:
```
YYYY-MM-DD-<descriptor>.md
```
Examples:
- `2026-01-30-session-summary.md`
- `2026-01-30-run-sheet.md`

Session folders are named by date: `M-DD-YY` (e.g., `1-30-26`)

## Session Workflow

### Before the Meeting
1. Review last week's transcript and summary
2. Create a **run sheet** with:
   - Recording consent reminder
   - Welcome preamble
   - Board link (agile.coffee)
   - Recap of previous session
   - Voting instructions
   - Outro template

### During the Meeting
- Drop board link in chat: `http://agile.coffee/#<board-id>`
- Participants get 6 votes to distribute across discussion items
- Facilitate top-voted items
- Use guardrails if discussion drifts to abstraction:
  - "Can you give a specific example?"
  - "What did that look like in practice?"
  - "What signal did you miss in hindsight?"

### After the Meeting
1. Save transcript (VTT file from Teams)
2. Screenshot the board state
3. Create **session summary** capturing:
   - Topics discussed with key points
   - Participant contributions
   - Insights and themes
   - Follow-up items

## Key Documents

| File | Purpose |
|------|---------|
| `build-in-public.md` | Core context document - spirit, intent, operating principles |
| `historical-convo.md` | ChatGPT conversation history showing BiP evolution |
| `YYYY-MM-DD-run-sheet.md` | Facilitator's guide for a specific session |
| `YYYY-MM-DD-session-summary.md` | Post-meeting synthesis |

## Publishing Infrastructure

### Website (Eleventy + GitHub Pages)
- **Live site**: https://matt-wright86.github.io/bip/
- **Repo**: github.com/matt-wright86/bip (public, personal account)
- **GitHub account**: matt-wright86 (switch with `gh auth switch --user matt-wright86`)
- **Static site generator**: Eleventy v3.1.2 (ESM config)
- **Deployment**: GitHub Actions → GitHub Pages (automatic on push to main)
- **Path prefix**: `/bip/` in production, `/` locally (via `ELEVENTY_PATH_PREFIX` env var)
- **Local dev**: `npm start` (runs on port 9091)
- **Build**: `npm run build`

### Site Architecture
```
eleventy.config.js          — Eleventy config (markdown-it, collections, filters, passthrough copy)
_includes/base.njk          — Base HTML layout (CSS link, lightbox script)
_includes/session.njk       — Session page layout (extends base, adds nav)
index.njk                   — Archive index listing all sessions
.eleventyignore             — Excludes non-content files from processing
.github/workflows/deploy.yml — GitHub Actions deployment workflow
templates/bip-web.css       — Web stylesheet (copied to /css/bip-web.css at build)
templates/bip-print.css     — Print/PDF stylesheet for WeasyPrint
scripts/build.sh            — Pandoc + WeasyPrint pipeline for standalone HTML/PDF
```

### CSS / Branding
Stylesheets use Improving brand colors extracted from improving.com:
- Primary Blue (headings): `#005596`
- Green Accent: `#5bc2a7`
- Link Color: `#2f9f7c`
- Body Text: `#212121`
- Gray (captions): `#646466`
- Background: `#f0f4f7`
- Border: `#daeaf6`

### Session Markdown Requirements
Session summaries need YAML frontmatter for Eleventy to process them:
```yaml
---
layout: session.njk
title: "BiP Session Summary — YYYY-MM-DD"
date: YYYY-MM-DD
description: "Brief summary for the index page."
---
```

### Eleventy Key Details
- **Collections**: `sessions` collection globs `*-*-26/*-session-summary.md`, sorted newest-first
- **Computed permalinks**: Session pages output to `/<session-dir>/index.html` (not nested under the markdown filename) so relative image paths resolve correctly
- **Passthrough copy**: Screenshots directories (`*-*-26/screenshots`), board PNGs, and CSS
- **Markdown**: markdown-it with `markdown-it-implicit-figures` plugin (images with caption text get `<figure><figcaption>` wrapping)
- **Lightbox**: All images are click-to-expand via a simple JS lightbox in base.njk
- **Templates use `| url` filter** for all paths to handle pathPrefix correctly

### Pandoc + WeasyPrint Pipeline
For standalone HTML and PDF output (offline sharing, not deployed to site):
```bash
./scripts/build.sh <session-dir>
# Example: ./scripts/build.sh 2-13-26
```
- Produces `session-summary.html` (self-contained with embedded images) and `session-summary.pdf`
- These files are gitignored — they're local artifacts only

### Git / Deployment Notes
- Videos (`.mp4`, `.mov`, `.avi`, `.mkv`) are gitignored — do not commit
- VTT transcripts and Deepgram transcripts are gitignored
- `session-summary.html` and `session-summary.pdf` (Pandoc output) are gitignored
- Always use feature branches for changes (hook blocks edits on main)
- Merge via `gh pr merge <num> --squash --delete-branch`

## BiP Philosophy

### What BiP Is
- Open, collaborative, voluntary
- Grounded in lived experience ("I tried...", "I noticed...", "I realized...")
- Low-pressure, high-trust
- An on-ramp to thought leadership, not a gate

### What BiP Is Not
- Polished demos or debates
- A place to arrive at consensus
- A backlog or voting mechanism for truth

### Board Item Qualities
Good board items are:
- Experiential, not abstract
- Imply a story already happened
- Reflect unfinished thinking
- Grounded in real work

Items move to "Done Discussing" when insight has been harvested—not because the topic is resolved.

## Session Shape

### Intro
- Welcome, restate intent
- Remind of "law of two feet" (leave when you need to)
- Everyone declares a goal (curiosity counts)

### Middle
- 1-2 discussion items based on votes
- Emphasis on narration, not expertise

### Outro
- Reconnect discussion to BiP intent
- Acknowledge contributors
- Invite participants back

## Welcome Preamble
> "Welcome to Build in Public, or BiP.
>
> This is an open space for building—blog posts, workflows, hobby projects, or anything still forming. The point isn't polish, it's progress.
>
> We're here to share, encourage one another, and offer accountability. We all lift together. Come when you can, be an Improver, and build with us.
>
> Remember the law of two feet—bounce when you need to.
>
> Everyone comes to BiP with a goal. That goal might be curiosity, but everyone has one. Let's start by sharing our goals for this session."

## Regular Participants
- **Matthew Wright** - Facilitator
- **Daniel** - Previous lead, frequent contributor on frameworks and writing, prompt/workflow libraries
- **Claudio** - Voice journaling, pomodoro method, AI workflows, daily blogging, TLC coordinator
- **Terrence** - Marketing background, AI adoption for non-technical roles
- **Josh Fryer** - Remote (San Antonio), brave space vs safe space framing, conference speaking
- **Jonathan** - Philosophy, epistemology, genuine connection
- **Devlin** - Training structure, developer productivity
- **Alexander Reeves** - Remote, deep AI expertise
- **Joanna Szymczyk** - Remote, event sourcing, TLC speaker
- **Alexis** - Talk creation, AI-assisted development

## Recurring Themes
- Intentionality in work and time use
- AI-assisted workflows (writing, journaling, presentations)
- Narration as a tool for clarity
- Meeting people where they are (vocabulary, context)
- Achievement vs. accolade (intrinsic vs. extrinsic motivation)
- Task decomposition for complex problems
