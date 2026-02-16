# Build in Public (BiP)

Build in Public is a weekly lightly moderated open forum at [Improving](https://improving.com). The purpose is to create space for narrating real work, sharing unfinished thinking, and learning through explanation rather than performance.

**Schedule**: Fridays, 2:00-3:00 PM Central
**Format**: ~1 hour hybrid meeting (in-office + remote via Teams)
**Facilitator**: Matthew Wright
**Live site**: [matt-wright86.github.io/bip/](https://matt-wright86.github.io/bip/)

## Prerequisites

| Tool | Required for | Install |
|------|-------------|---------|
| **Node.js** | Eleventy site builds | `brew install node` |
| **Python 3** | Transcription scripts | Pre-installed on macOS (`/usr/bin/python3`) |
| **deepgram-sdk** | Deepgram API calls | `/usr/bin/python3 -m pip install deepgram-sdk` |
| **ffmpeg** | Audio extraction from .mp4 | `brew install ffmpeg` |
| **Pandoc** | Standalone HTML generation | `brew install pandoc` |
| **WeasyPrint** | PDF generation (optional) | `brew install weasyprint` |
| **Chrome DevTools MCP** | Screenshot capture (optional) | Claude Code MCP server |

**Environment setup:**

```bash
npm install                                          # Eleventy dependencies
/usr/bin/python3 -m pip install deepgram-sdk          # Python dependencies
cp .env.local.example .env.local                      # Then add your Deepgram API key
```

The `.env.local` file should contain:
```
DEEPGRAM_API_KEY=your-key-here
```

Get a key from [console.deepgram.com](https://console.deepgram.com).

## Skills

Skills are Claude Code slash commands that automate the BiP workflow. They live in `.claude/skills/` and are invoked in Claude Code.

| Skill | Invocation | Purpose |
|-------|-----------|---------|
| **bip-prep** | `/bip-prep 2026-02-20` | Generate a run sheet for the upcoming session |
| **bip-summary** | `/bip-summary <session-dir>` | Create a session summary from transcript data |
| **bip-publish** | `/bip-publish <session-dir>` | Build, preview, and deploy a session to the site |
| **documenting-video** | `/documenting-video` | Capture screenshots from video via Chrome DevTools |

### bip-prep

Generates a facilitator run sheet for the upcoming session. Reads last week's session summary to build a recap, creates a new session folder, and produces a markdown run sheet with the welcome preamble, recap, voting instructions, guardrails, and outro.

**When to use**: Wednesday or Thursday before the meeting.
**Produces**: `<session-dir>/YYYY-MM-DD-run-sheet.md`

### bip-summary

Creates a session summary from a meeting transcript. Checks for Deepgram data first (with speaker confidence analysis), falls back to VTT. Synthesizes discussion into structured prose with topic summaries, key points, themes, and follow-ups. Presents uncertain speaker attributions for human verification before finalizing.

**When to use**: After the meeting, once the transcript and/or Deepgram data is ready.
**Produces**: `<session-dir>/YYYY-MM-DD-session-summary.md`

### bip-publish

End-to-end publishing workflow. Verifies frontmatter, builds standalone HTML/PDF via Pandoc, builds the Eleventy site, launches a local preview server for review, then commits, pushes, creates a PR, merges, and verifies the GitHub Pages deployment.

**When to use**: After the session summary is reviewed and finalized.
**Produces**: Deployed session page at `https://matt-wright86.github.io/bip/<session-dir>/`

### documenting-video

General-purpose skill (not BiP-specific, lives in global skills at `~/.claude/skills/documenting-video/`). Downloads a video, analyzes the transcript for screenshot-worthy moments, spins up a local HTML5 video player, and uses Chrome DevTools MCP to seek to each moment and capture screenshots.

**When to use**: After generating the summary, to add visual context.
**Produces**: `<session-dir>/screenshots/*.png`

## Scripts

| Script | Usage | Purpose |
|--------|-------|---------|
| `transcribe.py` | `/usr/bin/python3 scripts/transcribe.py <session-dir>` | Send audio to Deepgram Nova-3, save word-level JSON |
| `analyze-speakers.py` | `/usr/bin/python3 scripts/analyze-speakers.py <session-dir>` | Cross-reference VTT, flag low-confidence attributions |
| `build.sh` | `./scripts/build.sh <session-dir>` | Generate standalone HTML + PDF via Pandoc/WeasyPrint |

`transcribe.py` automatically chains `analyze-speakers.py` after transcription completes. Run `analyze-speakers.py` separately to re-analyze with a different confidence threshold (`--threshold 0.4`).

See [transcription-pipeline.md](transcription-pipeline.md) for detailed documentation of the transcription and speaker analysis pipeline.

## Weekly Workflow

### Before the meeting

```
/bip-prep 2026-02-20
```

Review the generated run sheet. Add the agile.coffee board link. Tweak the recap if needed.

### During the meeting

- Hit record in Teams
- Follow the run sheet
- Drop the board link in chat: `http://agile.coffee/#<board-id>`
- Screenshot the board at the end

### After the meeting

```bash
# 1. Save the Teams .vtt transcript to the session folder

# 2. Transcribe and analyze speakers
/usr/bin/python3 scripts/transcribe.py 2-20-26

# 3. Generate the session summary (in Claude Code)
/bip-summary 2-20-26

# 4. Capture screenshots from the video (in Claude Code)
/documenting-video

# 5. Review the summary, verify flagged attributions against the video

# 6. Publish (in Claude Code)
/bip-publish 2-20-26
```

## Repo Structure

```
Build In Public/
├── .claude/skills/
│   ├── bip-prep/SKILL.md              # Run sheet generation
│   ├── bip-summary/SKILL.md           # Session summary synthesis
│   └── bip-publish/SKILL.md           # Publishing workflow
├── .github/workflows/deploy.yml        # GitHub Actions → Pages
├── _includes/
│   ├── base.njk                        # Base HTML layout (lightbox)
│   └── session.njk                     # Session page layout
├── templates/
│   ├── bip-web.css                     # Screen stylesheet
│   └── bip-print.css                   # Print/PDF stylesheet
├── scripts/
│   ├── build.sh                        # Pandoc + WeasyPrint pipeline
│   ├── transcribe.py                   # Deepgram API transcription
│   └── analyze-speakers.py             # Speaker confidence analysis
├── index.njk                           # Archive index page
├── eleventy.config.js                  # Eleventy config (ESM)
├── requirements.txt                    # Python dependencies
├── CLAUDE.md                           # Project context for Claude
├── how-this-works.md                   # System architecture deep dive
├── transcription-pipeline.md           # Transcription pipeline docs
├── build-in-public.md                  # BiP philosophy & principles
├── <M-DD-YY>/                          # Session folders
│   ├── YYYY-MM-DD-run-sheet.md
│   ├── YYYY-MM-DD-session-summary.md
│   ├── agile-board.png
│   └── screenshots/
└── ...
```

## Further Reading

- **[how-this-works.md](how-this-works.md)** — System architecture: the toolchain, how each skill works under the hood, the publishing pipeline, Eleventy configuration, and branding
- **[transcription-pipeline.md](transcription-pipeline.md)** — Deepgram transcription, speaker analysis algorithms, VTT cross-reference, confidence flagging
- **[build-in-public.md](build-in-public.md)** — BiP philosophy, session structure, facilitation guardrails, board item qualities
