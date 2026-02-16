# How the BiP Session Archive Works

Hey Daniel -- you asked how the session summaries get made, so here's the full breakdown. It's a mix of Claude Code, custom skills, and a small static site pipeline. The whole thing runs on my laptop and deploys to GitHub Pages.

## The Big Picture

The flow each week looks like this:

```
Teams recording (.mp4)
    |
    v
Transcript (.vtt from Teams, or Deepgram for better diarization)
    |
    v
Claude Code + bip-summary skill --> session summary markdown + screenshots
    |
    v
Two output paths:
    ├── Eleventy --> GitHub Pages (web archive)
    └── Pandoc + WeasyPrint --> standalone HTML & PDF (for sharing offline)
```

The key idea: the transcript is the raw material, Claude does the synthesis, and everything downstream is just formatting and publishing.

## The Toolchain

Here's what's involved:

| Tool | What it does |
|------|-------------|
| **Claude Code** | Anthropic's CLI agent. It reads files, runs commands, edits code. It's the orchestrator for everything. |
| **Claude Skills** (`.claude/skills/`) | Reusable prompt templates that live in the repo. Think of them like slash commands -- `/bip-prep` or `/bip-summary` -- that expand into detailed instructions Claude follows. |
| **Eleventy** (v3.1) | Static site generator. Turns the session summary markdown into HTML pages. ESM config, Nunjucks templates, markdown-it with implicit figures plugin. |
| **Pandoc** | Universal document converter. Takes the same markdown and produces standalone HTML (with embedded images) or feeds it to WeasyPrint for PDF. |
| **WeasyPrint** | CSS-based PDF renderer. Pandoc hands it HTML + a print stylesheet, it produces a paginated PDF with running headers/footers. |
| **GitHub Actions** | On push to `main`, runs `npx eleventy` and deploys the `_site/` directory to GitHub Pages. |
| **Deepgram** (optional) | When I need better speaker diarization than Teams provides, I run the recording through Deepgram's API. The transcript comes back with speaker labels, which makes attribution in the summary much more accurate. |

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

**Invocation:** `/bip-summary path/to/transcript.vtt`

**What it does:**
1. Reads the full transcript (VTT or Deepgram format)
2. Checks for board screenshots in the session folder
3. Generates a structured summary with:
   - Session overview (duration, participants)
   - Topics discussed with vote counts and attribution
   - Key points and notable quotes
   - Themes and insights
   - Follow-up items and undiscussed board items

The guidelines tell Claude to attribute contributions to specific people, capture the "why" not just the "what," note any frameworks or models that emerged, and keep things scannable. It's not a transcript -- it's a synthesis.

### documenting-video

**What:** Turns any video recording into comprehensive markdown documentation with inline screenshots.

This one's more general-purpose (not BiP-specific). I built it for knowledge transfers, demos, and recorded meetings. It lives in my global skills at `~/.claude/skills/documenting-video/`.

**The workflow:**
1. Downloads the video (via `yt-dlp`) or uses a local file
2. Gets a transcript -- either from YouTube captions, or by running OpenAI Whisper locally
3. Analyzes the transcript for "screenshot-worthy moments" (visual references, demos, topic changes, code being shown)
4. Uses Chrome DevTools MCP to automate a browser: loads the video, seeks to each timestamp, captures screenshots
5. Assembles everything into a markdown document with screenshots placed at narrative points

It has a bunch of hard-won lessons baked in -- like the fact that YouTube's player crashes after ~5 rapid seeks (so it downloads the video and plays it locally instead), and that the `seeked` event almost never fires on HTML5 video (so it uses a 3-second timeout as the primary mechanism).

I use this for the BiP screenshots -- it captures the board state, the Teams participant view, and any screen shares during the session.

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

1. **Save the transcript** -- Teams generates a `.vtt` file. Sometimes I also run the recording through Deepgram for better speaker diarization.

2. **Generate the summary:**
   ```
   /bip-summary 2-20-26/transcript.vtt
   ```
   Claude reads the entire transcript, cross-references the board screenshot, and produces the session summary markdown.

3. **Capture screenshots** (if I recorded video):
   ```
   /documenting-video
   ```
   This pulls screenshots from the recording at key moments -- board state, participant grid, screen shares.

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
│   └── build.sh                    # Pandoc + WeasyPrint pipeline
├── index.njk                       # Archive index page
├── eleventy.config.js              # Eleventy config
├── CLAUDE.md                       # Project context for Claude
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
