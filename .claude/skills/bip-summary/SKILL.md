---
name: bip-summary
description: Create a session summary from a Build in Public transcript. Use after a BiP meeting to generate the summary document.
argument-hint: "[path to transcript file]"
---

# Build in Public Session Summary

You are creating a session summary from a BiP meeting transcript.

## Instructions

1. **Locate the transcript**: Use the path provided in `$ARGUMENTS`, or look for the most recent `.vtt` file
2. **Read the full transcript** - it may require multiple reads for long files
3. **Check for a board screenshot** in the same folder (usually `.png`)
4. **Generate the summary** following the template below

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

**Before publishing, you MUST present any uncertain attributions to the user for manual confirmation.** Format them as a table with timestamps so the user can easily verify against the video:

| Timestamp | Current Attribution | Quote/Content |
|---|---|---|
| 4:44 | Claudio? | "I have a small child, she's four years old..." |

Do NOT publish the summary with unverified attributions. Getting attribution wrong misrepresents what people said and undermines trust in the summary.

## After Creating

The summary serves as:
- Input for next week's run sheet recap
- Historical record of BiP discussions
- Reference for recurring themes and participant contributions

**Next steps**:
1. Run `/documenting-video` on the meeting video recording to extract screenshots at key moments (board state, demos, discussion points). Screenshots are saved to the session's `screenshots/` directory and can be referenced in the summary using standard markdown image syntax: `![Caption](screenshots/filename.png)`.
2. Run `/bip-publish <session-dir>` to build standalone HTML/PDF, preview the Eleventy site, and deploy to GitHub Pages.
