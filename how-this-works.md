# System Architecture

This document covers the technical architecture of the BiP session archive: how recordings become published summaries, what each tool does, and how the pieces connect. For the weekly workflow, skill usage guide, and repo structure, see the [README](README.md).

## The Big Picture

```
Teams recording (.mp4)
    |
    ├──────────────────────────────────┐
    v                                  v
Transcription pipeline          documenting-video skill
(scripts/transcribe.py          (downloads video, plays it locally
 calls Deepgram Nova-3 API,     in Chrome via a custom HTML player,
 then analyze-speakers.py       uses Chrome DevTools MCP to seek
 resolves names + flags         to key moments, captures screenshots)
 low-confidence attributions)          |
    |                                  v
    v                           screenshots/ directory
deepgram-transcript.md          (board state, demos, screen shares,
+ speaker-confidence-report.md  participant grid)
    |                                  |
    v                                  |
bip-summary skill                      |
(reads transcript + report,            |
 verifies flagged attributions)        |
    └──────────┬───────────────────────┘
               v
    Session summary markdown
    (prose + inline screenshot references,
     with verified speaker attributions)
               |
               v
    Two output paths:
        ├── Eleventy --> GitHub Pages (web archive)
        └── Pandoc + WeasyPrint --> standalone HTML & PDF (for sharing offline)
```

The video recording is the single raw input. The transcription pipeline extracts audio, sends it to Deepgram, analyzes speaker confidence, and cross-references with the Teams VTT to resolve names. A separate skill automates screenshot capture by driving a real browser. Claude synthesizes both into prose, with flagged attributions verified by a human before publishing. Everything downstream is formatting and publishing.

For a deep dive on the transcription and speaker analysis pipeline, see [transcription-pipeline.md](transcription-pipeline.md).

## The Toolchain

| Tool | What it does |
|------|-------------|
| **Claude Code** | Anthropic's CLI agent. Reads files, runs commands, edits code. Orchestrates the entire workflow. |
| **Claude Skills** (`.claude/skills/`) | Reusable prompt templates that live in the repo. Slash commands like `/bip-prep` or `/bip-summary` expand into detailed instructions Claude follows. |
| **Eleventy** (v3.1) | Static site generator. Turns session summary markdown into HTML pages. ESM config, Nunjucks templates, markdown-it with implicit figures plugin. |
| **Pandoc** | Universal document converter. Produces standalone HTML (with embedded images) or feeds to WeasyPrint for PDF. |
| **WeasyPrint** | CSS-based PDF renderer. Takes HTML + a print stylesheet and produces paginated PDFs with running headers/footers. |
| **Chrome DevTools MCP** | MCP server that lets Claude control a real Chrome browser -- navigate pages, seek video, take screenshots. Powers automated screenshot capture. |
| **GitHub Actions** | On push to `main`, runs `npx eleventy` and deploys `_site/` to GitHub Pages. |
| **yt-dlp** | Video downloader. Grabs the Teams recording (or any video URL) as a local `.mp4` for the screenshot pipeline. |
| **Deepgram Nova-3** | Primary transcription path. `scripts/transcribe.py` sends session audio to Deepgram's API via the Python SDK and gets back word-level data with `speaker_confidence` scores. `scripts/analyze-speakers.py` then cross-references with the Teams VTT to resolve speaker names and flags uncertain attributions. See [transcription-pipeline.md](transcription-pipeline.md) for the full breakdown. |

## The Skills

Skills are the heart of the automation. Each is a `SKILL.md` file in `.claude/skills/` -- a detailed prompt with templates and guidelines that tells Claude exactly what to do.

### bip-prep

**What:** Prepares a run sheet for the upcoming session.

**Invocation:** `/bip-prep 2026-02-20`

**What it does:**
1. Reads last week's session summary to pull out a recap
2. Creates a new session folder (e.g., `2-20-26/`)
3. Generates a run sheet with the welcome preamble, recap section, voting instructions, guardrail prompts, and outro template

The run sheet is the facilitator's script -- it has everything needed during the meeting to handle transitions without winging it.

### bip-summary

**What:** Creates a session summary from a meeting transcript.

**Invocation:** `/bip-summary <session-dir>`

**What it does:**
1. Checks for transcript sources (prefers `deepgram.json` + `speaker-confidence-report.md`, falls back to VTT)
2. Reads the speaker confidence report to know which attributions need verification
3. Reads the transcript and checks for board screenshots
4. Generates a structured summary with:
   - Session overview (duration, participants)
   - Topics discussed with vote counts and attribution
   - Key points and notable quotes
   - Themes and insights
   - Follow-up items and undiscussed board items

The guidelines emphasize attributing contributions to specific people, capturing the "why" not just the "what," noting any frameworks or models that emerged, and keeping things scannable. The output is a synthesis, not a transcript.

Before publishing, the skill presents all uncertain attributions (flagged by the confidence pipeline) in a verification table with timestamps. A human confirms or corrects each one against the video. No unverified attributions make it into the published summary.

### documenting-video

**What:** Turns any video recording into comprehensive markdown documentation with inline screenshots. This is an AI agent driving a real browser to extract frames from video.

This is a general-purpose skill (not BiP-specific). It lives in global skills at `~/.claude/skills/documenting-video/` but has become central to BiP -- it's how screenshots make the session summaries visual instead of a wall of text.

**Invocation:** `/documenting-video`

**How it works under the hood:**

1. **Video acquisition** -- Downloads the video via `yt-dlp` or uses a local `.mp4`. For BiP, the input is the Teams meeting recording.

2. **Transcript analysis** -- Claude reads the transcript and identifies "screenshot-worthy moments." The skill defines detection patterns:
   - *Critical*: Visual references ("as you can see"), demonstrations ("let me show you"), diagrams/architecture
   - *High*: Topic changes, code being shown, UI navigation, errors
   - *Medium*: Key concepts, important takeaways

   This produces a `moments.json` with timestamps, categories, and suggested captions. Density control keeps it to roughly 1 screenshot per 2-3 minutes (more for screen shares, fewer for talking-head content).

3. **Local playback setup** -- The skill builds a minimal HTML page:
   ```html
   <video id="v" src="video.mp4" preload="auto"></video>
   ```
   Then serves it locally with a custom Python server (`serve.py`) that supports HTTP range requests -- Python's built-in `http.server` doesn't handle range requests, which means the browser can't seek at all. The custom server handles `Range` headers and returns `206 Partial Content`. Claude navigates Chrome to `http://localhost:8765/player.html`.

4. **Chrome DevTools MCP screenshot loop** -- For each moment in `moments.json`, Claude:
   - Seeks the video to the timestamp via `evaluate_script` (sets `video.currentTime`)
   - Runs a player health check -- `readyState >= 2`? Any error overlays? `video.error` set?
   - Checks for blank/black frames by sampling a 3x3 pixel grid via canvas
   - Captures the screenshot with `take_screenshot`, targeting the `<video>` element UID directly (clean video frame, no browser chrome)
   - Waits 1-2 seconds between captures to avoid crashing the player

   Filenames encode metadata: `03-09m20s-daniel-research-workflow.png` means screenshot #3, taken at 9 minutes 20 seconds, showing Daniel's research workflow.

5. **Assembly** -- Screenshots land in the session's `screenshots/` directory. The summary references them with standard markdown image syntax: `![caption](screenshots/filename.png)`.

**Hard-won lessons baked into the skill:**

The `SKILL.md` is ~600 lines because video automation is full of edge cases:
- **YouTube crashes after rapid seeks.** The player silently enters an error state after ~5 quick seeks. Error overlays look normal to canvas-based blank detection (they have text and icons that produce pixel variance). Fix: download the video and play it locally instead.
- **`seeked` event never fires.** Even with local playback, the HTML5 `seeked` event is unreliable. Fix: use a 3-second timeout as the primary seek mechanism. The event listener is just a bonus if it happens to work.
- **Canvas can't catch error screens.** The 3x3 pixel sampling detects black/blank frames but not "Something went wrong" overlays. Fix: a separate health check that inspects `video.error`, `readyState`, `networkState`, and scans `document.body.innerText` for error strings.
- **Python's `http.server` breaks seeking.** No range request support means `video.seekable` is empty. Fix: custom `serve.py` with proper `Range` header handling and `206 Partial Content` responses.

## The Publishing Pipeline

Two parallel output paths from the same markdown source.

### Path 1: Eleventy --> GitHub Pages

The session summary markdown needs YAML frontmatter:

```yaml
---
layout: session.njk
title: "BiP Session Summary -- 2026-02-13"
date: 2026-02-13
description: "Brief summary for the index page."
---
```

Eleventy picks up any file matching `*-*-26/*-session-summary.md`, builds it into HTML using Nunjucks templates, and outputs it to `_site/`. The GitHub Actions workflow runs on every push to `main`:

```yaml
- run: npx eleventy
  env:
    ELEVENTY_PATH_PREFIX: /bip/
```

The site lives at [matt-wright86.github.io/bip/](https://matt-wright86.github.io/bip/).

**Eleventy details that matter:**
- **Computed permalinks** -- session pages output to `/<session-dir>/index.html` (not nested under the markdown filename) so relative image paths just work. A `![screenshot](screenshots/foo.png)` resolves correctly.
- **Passthrough copy** -- screenshots directories and board images get copied as-is to `_site/`.
- **markdown-it-implicit-figures** -- any image with alt text automatically gets wrapped in `<figure><figcaption>`, producing visible captions.
- **Lightbox** -- a tiny inline JS snippet in `base.njk` makes every image click-to-expand. No library, just a fixed overlay with the image.

### Path 2: Pandoc + WeasyPrint --> HTML & PDF

```bash
./scripts/build.sh 2-13-26
```

This script:
1. Finds the `*-session-summary.md` in the session directory
2. Strips the YAML frontmatter (Pandoc doesn't need it and would render it as a title block)
3. Runs Pandoc twice:
   - **HTML**: `pandoc --standalone --embed-resources --css=bip-web.css --toc` -- produces a single self-contained HTML file with all images base64-encoded inline
   - **PDF**: `pandoc --standalone --css=bip-print.css --pdf-engine=weasyprint` -- produces a paginated PDF

The HTML and PDF are gitignored -- they're local artifacts for sharing via Teams or email, not deployed to the site.

## Branding

The CSS uses Improving's brand colors, extracted from improving.com:

```css
:root {
  --heading-color: #005596;   /* Improving primary blue */
  --accent-color: #5bc2a7;    /* Green accent */
  --link-color: #2f9f7c;      /* Link color */
  --text-color: #212121;      /* Body text */
  --caption-color: #646466;   /* Gray for captions */
  --background: #f0f4f7;      /* Light blue-gray background */
  --border-color: #daeaf6;    /* Subtle borders */
}
```

Two stylesheets:
- **`bip-web.css`** -- screen-optimized. Max-width container, responsive breakpoints, hover effects on links, styled table of contents with "In This Issue" header.
- **`bip-print.css`** -- print-optimized for WeasyPrint. `@page` rules with running headers (document title top-right) and footers ("Page X of Y" center, "Build in Public @ Improving" bottom-right). Links get their URLs printed inline. Orphan/widow control. `page-break-inside: avoid` on figures and tables.

The `h2` elements get a green (`#5bc2a7`) top border as a section divider -- the most visually distinctive element.

## What Makes It Work

The thing that ties it all together is `CLAUDE.md`. It's a project-level context file that Claude reads automatically. It contains the BiP philosophy, session workflow, participant list, recurring themes, publishing infrastructure details, and file naming conventions. When Claude generates a summary or run sheet, it has all of that context -- it knows who the regular participants are, what the recurring themes are, what the welcome preamble sounds like, and how the files should be named.

The skills are parameterized prompts that reference this shared context. They're reusable across sessions and encode patterns developed over weeks of iteration. The first few summaries were done manually in ChatGPT, then moved to Claude Code with a refined prompt. Eventually the stable parts were extracted into skills for one-command invocation.

The `CLAUDE.md` + skills pattern means the system is self-documenting in a sense: Claude reads the project context, the skill tells it what to do, and the output follows established conventions automatically. Adding a new session is running three or four commands, not rebuilding context from scratch each time.
