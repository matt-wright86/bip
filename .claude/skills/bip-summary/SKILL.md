---
name: bip-summary
description: Create a session summary from a Build in Public transcript. Use after a BiP meeting to generate the summary document.
argument-hint: "[path to transcript file]"
---

# Build in Public Session Summary

You are creating a session summary from a BiP meeting transcript.

## Instructions

1. **Check for transcript sources** in the session directory (priority order):
   - `deepgram.json` + `speaker-confidence-report.md` → proceed to step 2
   - `deepgram.json` only → run `/usr/bin/python3 scripts/analyze-speakers.py <session-dir>` first
   - `*.mp4` or `*.mp3` only → run `/usr/bin/python3 scripts/transcribe.py <session-dir>` (this chains `analyze-speakers.py` automatically)
   - `*.vtt` only → fallback to reading VTT directly (no confidence data available)
2. **Read the speaker confidence report** (`speaker-confidence-report.md`) — note the speaker map (which speaker numbers map to which names) and all flagged passages
3. **Read the transcript** (`deepgram-transcript.md` for Deepgram-based, or `*.vtt` for fallback) — it may require multiple reads for long files
4. **Check for a board screenshot** in the same folder (usually `.png`)
5. **Generate the summary** following the template below

## Summary Template

Create a file named `YYYY-MM-DD-session-summary.md` with this structure.

**Important**: The file must start with YAML frontmatter so Eleventy can render it as a page on the BiP site. Place this block at the very top of the file, before the markdown heading:

```yaml
---
layout: session.njk
title: "BiP Session Summary — YYYY-MM-DD"
date: YYYY-MM-DD
description: "Brief one-line summary of the session topics."
---
```

Then continue with the markdown content:

```markdown
# BiP Session Summary — YYYY-MM-DD

## Session Overview
- **Duration**: ~XX minutes
- **Facilitator**: Matthew Wright
- **Participants**: [List names mentioned in transcript]

---

## Topics Discussed

### 1. [Topic Title] (X votes)
**Raised by**: [Name]

[2-3 paragraph summary of the discussion]

**Key points:**
- [Bullet point insights]

**Quotes/moments worth noting:**
- [Notable quotes if any]

---

### 2. [Next Topic]...

---

## Key Themes & Insights

1. **[Theme]** — [Brief explanation]
2. **[Theme]** — [Brief explanation]

---

## Next Week's Potential Follow-ups
- [Items mentioned for future discussion]

---

## Board Items Not Discussed
- [List items that were on the board but didn't get covered]
```

## Guidelines

- **Attribute contributions** to specific people when clear from transcript
- **Capture the "why"** not just the "what" of discussions
- **Note frameworks or models** that emerged (e.g., "Have/Do/Be framework")
- **Identify recurring themes** that connect to previous sessions
- **Keep summaries scannable** with clear headers and bullet points
- **Include humor or memorable moments** that captured the session's spirit

## Speaker Attribution — Important

BiP is a hybrid meeting with in-room participants sharing a single conference room microphone. This makes automated speaker identification unreliable:

- **Teams VTT transcripts** only identify remote participants by name. In-room speakers appear as unnamed `<v >` tags.
- **Deepgram diarization** assigns speaker numbers (Speaker 0, Speaker 1, etc.) but frequently misattributes when people talk over each other, speak in quick succession, or sit near each other by the shared mic.
- **Cross-referencing** VTT with Deepgram helps but is not sufficient — diarization errors can silently assign the wrong speaker to entire passages.

### Automated Confidence Flagging

The `scripts/analyze-speakers.py` script automatically:
- **Resolves speaker names** by cross-referencing Deepgram speaker numbers with VTT named entries (remote participants like Josh Fryer, Joanna Szymczyk)
- **Flags low-confidence passages** where `speaker_confidence` < 0.50 or any word has confidence of 0.0
- **Marks `[LOW CONFIDENCE]`** in `deepgram-transcript.md` on flagged segments
- **Generates `speaker-confidence-report.md`** with a table of all flagged passages including timestamps, attributed speaker, confidence score, and text preview

When writing the summary, **use the confidence report as your primary guide** for which attributions need verification. In-room speakers (not resolved via VTT) and any flagged passages should all be treated as uncertain.

**Before publishing, you MUST present ALL uncertain attributions to the user for manual confirmation.** Format them as a table with timestamps so the user can easily verify against the video:

| Timestamp | Current Attribution | Confidence | Quote/Content |
|---|---|---|---|
| 4:44 | Speaker 0 (in-room) | 0.27 | "I have a small child, she's four years old..." |

Do NOT publish the summary with unverified attributions. Getting attribution wrong misrepresents what people said and undermines trust in the summary.

## After Creating

The summary serves as:
- Input for next week's run sheet recap
- Historical record of BiP discussions
- Reference for recurring themes and participant contributions

**Next steps**:
1. Run `/documenting-video` on the meeting video recording to extract screenshots at key moments (board state, demos, discussion points). Screenshots are saved to the session's `screenshots/` directory and can be referenced in the summary using standard markdown image syntax: `![Caption](screenshots/filename.png)`.
2. Run `/bip-publish <session-dir>` to build standalone HTML/PDF, preview the Eleventy site, and deploy to GitHub Pages.
