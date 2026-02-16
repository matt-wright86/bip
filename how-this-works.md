# How the BiP Session Archive Works

Hey Daniel -- you asked how the session summaries get made, so here's the full breakdown. It's a mix of Claude Code, custom skills, and a small static site pipeline. The whole thing runs on my laptop and deploys to GitHub Pages.

## The Big Picture

The flow each week looks like this:

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

The key idea: the video recording is the single raw input. The transcription pipeline extracts audio, sends it to Deepgram, analyzes speaker confidence, and cross-references with the Teams VTT to resolve names. A separate skill automates screenshot capture by driving a real browser. Claude synthesizes both into prose, with flagged attributions verified by a human before publishing. Everything downstream is formatting and publishing.

For a deep dive on the transcription and speaker analysis pipeline, see [transcription-pipeline.md](transcription-pipeline.md).

## The Toolchain

Here's what's involved:

| Tool | What it does |
|------|-------------|
| **Claude Code** | Anthropic's CLI agent. It reads files, runs commands, edits code. It's the orchestrator for everything. |
| **Claude Skills** (`.claude/skills/`) | Reusable prompt templates that live in the repo. Think of them like slash commands -- `/bip-prep` or `/bip-summary` -- that expand into detailed instructions Claude follows. |
| **Eleventy** (v3.1) | Static site generator. Turns the session summary markdown into HTML pages. ESM config, Nunjucks templates, markdown-it with implicit figures plugin. |
| **Pandoc** | Universal document converter. Takes the same markdown and produces standalone HTML (with embedded images) or feeds it to WeasyPrint for PDF. |
| **WeasyPrint** | CSS-based PDF renderer. Pandoc hands it HTML + a print stylesheet, it produces a paginated PDF with running headers/footers. |
| **Chrome DevTools MCP** | MCP server that lets Claude control a real Chrome browser -- navigate pages, seek video, take screenshots. This is what makes automated screenshot capture possible. |
| **GitHub Actions** | On push to `main`, runs `npx eleventy` and deploys the `_site/` directory to GitHub Pages. |
| **yt-dlp** | Video downloader. Grabs the Teams recording (or any video URL) as a local `.mp4` file for the screenshot pipeline. |
| **Deepgram Nova-3** | Primary transcription path. `scripts/transcribe.py` sends the session audio to Deepgram's API via the Python SDK and gets back word-level data with `speaker_confidence` scores. `scripts/analyze-speakers.py` then cross-references with the Teams VTT to resolve speaker names and flags uncertain attributions for human review. See [transcription-pipeline.md](transcription-pipeline.md) for the full breakdown. |

## The Skills

Skills are the heart of the automation. They live in `.claude/skills/` and each one is a `SKILL.md` file -- basically a detailed prompt that tells Claude exactly what to do, with templates and guidelines.

### bip-prep

**What:** Prepares a run sheet for the upcoming session.

**Invocation:** `/bip-prep 2026-02-20`

**What it does:**
1. Reads last week's session summary to pull out a recap
2. Creates a new session folder (e.g., `2-20-26/`)
3. Generates a run sheet with the welcome preamble, recap section, voting instructions, guardrail prompts, and outro template

The run sheet is my facilitator script. It has everything I need during the meeting so I'm not winging the transitions.

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

The guidelines tell Claude to attribute contributions to specific people, capture the "why" not just the "what," note any frameworks or models that emerged, and keep things scannable. It's not a transcript -- it's a synthesis.

Before publishing, the skill presents all uncertain attributions (flagged by the confidence pipeline) in a verification table with timestamps. A human confirms or corrects each one against the video. This is a hard requirement -- no unverified attributions make it into the published summary.

### documenting-video

**What:** Turns any video recording into comprehensive markdown documentation with inline screenshots. This is probably the most technically interesting part of the pipeline -- it's an AI agent driving a real browser to extract frames from video.

This one's a general-purpose skill (not BiP-specific). I built it for knowledge transfers, demos, and recorded meetings. It lives in my global skills at `~/.claude/skills/documenting-video/`. But it's become central to BiP -- it's how I get the screenshots that make the session summaries visual instead of a wall of text.

**Invocation:** `/documenting-video`

**How it actually works under the hood:**

1. **Video acquisition** -- Downloads the video via `yt-dlp` or uses a local `.mp4`. For BiP, the input is the Teams meeting recording.

2. **Transcript analysis** -- Claude reads the transcript and identifies "screenshot-worthy moments." The skill defines detection patterns for this:
   - *Critical*: Visual references ("as you can see"), demonstrations ("let me show you"), diagrams/architecture
   - *High*: Topic changes, code being shown, UI navigation, errors
   - *Medium*: Key concepts, important takeaways

   It produces a `moments.json` with timestamps, categories, and suggested captions. Density control keeps it to roughly 1 screenshot per 2-3 minutes (more for screen shares, fewer for talking-head content).

3. **Local playback setup** -- This is where it gets interesting. The skill builds a minimal HTML page:
   ```html
   <video id="v" src="video.mp4" preload="auto"></video>
   ```
   Then serves it locally with a custom Python server (`serve.py`) that supports HTTP range requests -- Python's built-in `http.server` doesn't handle range requests, which means the browser can't seek in the video at all. The custom server handles `Range` headers and returns `206 Partial Content`. Claude navigates Chrome to `http://localhost:8765/player.html`.

4. **Chrome DevTools MCP screenshot loop** -- This is the core. For each moment in `moments.json`, Claude:
   - Seeks the video to the timestamp via `evaluate_script` (sets `video.currentTime`)
   - Runs a player health check -- is `readyState >= 2`? Any error overlays? `video.error` set?
   - Checks for blank/black frames by sampling a 3x3 pixel grid via canvas
   - Captures the screenshot with `take_screenshot`, targeting the `<video>` element UID directly (so you get the clean video frame, not browser chrome)
   - Waits 1-2 seconds between captures to avoid crashing the player

   The filenames encode the metadata: `03-09m20s-daniel-research-workflow.png` means screenshot #3, taken at 9 minutes 20 seconds, showing Daniel's research workflow.

5. **Assembly** -- The screenshots land in the session's `screenshots/` directory, and the summary references them with standard markdown image syntax: `![caption](screenshots/filename.png)`.

**What it produced for the 2-13-26 session:**

That session had 7 screenshots captured from the Teams recording:
- `05-00m30s-session-opening.png` -- the fresh agile.coffee board before voting
- `03-09m20s-daniel-research-workflow.png` -- Daniel's research workflow demo
- `01-24m45s-screenshare-claudio-tlc-app.png` -- Claudio's TLC app screen share
- `06-26m10s-claudio-tlc-app-detail.png` -- detail view of that same app
- `04-37m35s-event-sourcing-discussion.png` -- during the event sourcing topic
- `07-53m20s-session-close.png` -- the wrap-up

Those screenshots are placed inline in the summary at the relevant discussion points. When Eleventy builds the site, the `markdown-it-implicit-figures` plugin wraps them in `<figure><figcaption>` tags, so the alt text becomes a visible caption.

**Hard-won lessons baked into the skill:**

The `SKILL.md` is ~600 lines because video automation is full of edge cases:
- **YouTube crashes after rapid seeks.** The player silently enters an error state after ~5 quick seeks. Error overlays look normal to canvas-based blank detection (they have text and icons that produce pixel variance). Fix: download the video and play it locally instead.
- **`seeked` event never fires.** Even with local playback, the HTML5 `seeked` event is unreliable. Fix: use a 3-second timeout as the primary seek mechanism. The event listener is just a bonus if it happens to work.
- **Canvas can't catch error screens.** The 3x3 pixel sampling detects black/blank frames but not "Something went wrong" overlays. Fix: a separate health check that inspects `video.error`, `readyState`, `networkState`, and scans `document.body.innerText` for error strings.
- **Python's `http.server` breaks seeking.** No range request support means `video.seekable` is empty. Fix: custom `serve.py` with proper `Range` header handling and `206 Partial Content` responses.

## The Publishing Pipeline

There are two parallel output paths from the same markdown source.

### Path 1: Eleventy --> GitHub Pages (the web archive)

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

A few Eleventy details that matter:
- **Computed permalinks** -- session pages output to `/<session-dir>/index.html` (not nested under the markdown filename) so relative image paths in the markdown just work. A `![screenshot](screenshots/foo.png)` resolves correctly.
- **Passthrough copy** -- screenshots directories and board images get copied as-is to `_site/`.
- **markdown-it-implicit-figures** -- any image with alt text automatically gets wrapped in `<figure><figcaption>`, which is how the captions appear.
- **Lightbox** -- there's a tiny inline JS snippet in `base.njk` that makes every image click-to-expand. No library, just a fixed overlay with the image.

### Path 2: Pandoc + WeasyPrint --> HTML & PDF (for offline sharing)

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

The CSS is aligned to Improving's brand colors. I extracted them from improving.com:

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

There are two stylesheets:
- **`bip-web.css`** -- screen-optimized. Max-width container, responsive breakpoints, hover effects on links, styled table of contents with "In This Issue" header.
- **`bip-print.css`** -- print-optimized for WeasyPrint. `@page` rules with running headers (document title top-right) and footers ("Page X of Y" center, "Build in Public @ Improving" bottom-right). Links get their URLs printed inline. Orphan/widow control. `page-break-inside: avoid` on figures and tables.

The `h2` elements get a green (`#5bc2a7`) top border as a section divider -- that's probably the most visually distinctive element.

## The Weekly Workflow

Here's what a typical week looks like:

### Before the meeting (Wednesday or Thursday morning)

```
/bip-prep 2026-02-20
```

Claude reads last week's summary, creates the new session folder, and generates the run sheet. I review it, paste in the agile.coffee board link, and tweak the recap if needed.

### During the meeting (Thursday 1:30 PM)

- Hit record in Teams
- Follow the run sheet
- Drop the board link in chat: `http://agile.coffee/#<board-id>`
- Screenshot the board at the end

### After the meeting (Thursday afternoon or Friday)

1. **Save the transcript and run transcription:**
   - Teams generates a `.vtt` file -- save it to the session folder
   - Run the transcription pipeline:
     ```bash
     /usr/bin/python3 scripts/transcribe.py 2-20-26
     ```
     This extracts audio from the `.mp4`, sends it to Deepgram, and produces `deepgram.json`, `deepgram-transcript.md`, and `speaker-confidence-report.md`. See [transcription-pipeline.md](transcription-pipeline.md) for details.

2. **Generate the summary:**
   ```
   /bip-summary 2-20-26
   ```
   Claude reads the Deepgram transcript and confidence report, cross-references the board screenshot, and produces the session summary markdown. It presents uncertain attributions for verification before finalizing.

3. **Capture screenshots** (if I recorded video):
   ```
   /documenting-video
   ```
   Claude downloads the recording, analyzes the transcript for screenshot-worthy moments, spins up a local video player in Chrome, and drives the browser through each timestamp -- seeking, health-checking, and capturing. The screenshots land in `screenshots/` with descriptive filenames like `03-09m20s-daniel-research-workflow.png`. I reference them in the summary markdown, and they flow through to both the web and PDF outputs.

4. **Review and edit** -- I read through the summary, fix any attribution errors, adjust emphasis, and make sure it captures the spirit of the conversation.

5. **Build local outputs** (optional, for sharing):
   ```bash
   ./scripts/build.sh 2-20-26
   ```

6. **Publish to the web:**
   ```bash
   git checkout -b session/2-20-26
   git add 2-20-26/
   git commit -m "Add 2026-02-20 session summary"
   git push -u origin session/2-20-26
   gh pr create --title "Add 2026-02-20 session summary" --body "..."
   gh pr merge --squash --delete-branch
   ```
   The merge to `main` triggers GitHub Actions, which builds and deploys to Pages.

### The repo structure

```
Build In Public/
├── .claude/skills/
│   ├── bip-prep/SKILL.md          # Run sheet generation skill
│   └── bip-summary/SKILL.md       # Session summary skill
├── .github/workflows/deploy.yml    # GitHub Actions -> Pages
├── _includes/
│   ├── base.njk                    # Base HTML layout
│   └── session.njk                 # Session page layout
├── templates/
│   ├── bip-web.css                 # Screen stylesheet
│   └── bip-print.css               # Print/PDF stylesheet
├── scripts/
│   ├── build.sh                    # Pandoc + WeasyPrint pipeline
│   ├── transcribe.py               # Deepgram API transcription
│   └── analyze-speakers.py         # Speaker confidence analysis
├── index.njk                       # Archive index page
├── eleventy.config.js              # Eleventy config
├── requirements.txt                # Python dependencies (deepgram-sdk)
├── CLAUDE.md                       # Project context for Claude
├── transcription-pipeline.md       # Transcription pipeline documentation
├── 1-30-26/                        # Session folder
│   ├── 2026-01-30-session-summary.md
│   ├── 2026-01-30-run-sheet.md
│   └── screenshots/
├── 2-06-26/
│   └── ...
└── 2-13-26/
    └── ...
```

## What Makes It Work

The thing that ties it all together is `CLAUDE.md`. It's a project-level context file that Claude reads automatically. It contains the BiP philosophy, session workflow, participant list, recurring themes, publishing infrastructure details, and file naming conventions. When Claude generates a summary or run sheet, it has all of that context -- it knows who the regular participants are, what the recurring themes are, what the welcome preamble sounds like, and how the files should be named.

The skills are essentially parameterized prompts that reference this shared context. They're reusable across sessions and they encode the patterns I've developed over weeks of iteration. The first few summaries I did manually in ChatGPT. Then I moved to Claude Code and started refining the prompt. Eventually I extracted the stable parts into skills so I could just invoke them with a path.

The whole thing is the kind of workflow that's worth narrating at BiP, honestly. It started as "I should probably take notes" and turned into a publishing pipeline. Classic scope creep, but the useful kind.
