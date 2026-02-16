# The Transcription Pipeline

This document covers how BiP session recordings get transcribed, how speakers get identified, and how the system flags uncertain attributions before they make it into a published summary.

## Why This Exists

BiP is a hybrid meeting. Remote participants dial in via Teams. In-room participants sit around a conference table and share a single room microphone. This setup creates a specific problem for transcription: the remote participants are individually identifiable (Teams knows who they are), but the in-room participants all sound like they're coming from the same source.

When you run audio through a speech-to-text service with speaker diarization (speaker identification), the service assigns speaker numbers -- Speaker 0, Speaker 1, Speaker 2, etc. For remote participants with clear, isolated audio channels, this works well. For a conference room mic picking up five people in the same room, it's a guess. And the guesses are frequently wrong.

We discovered this the hard way with the February 6 session. The transcript attributed a passage at 4:44 to the wrong speaker. When we looked at the raw data, Deepgram had assigned a `speaker_confidence` score of 0.274 to those words -- well below the 0.50 threshold that would indicate reasonable certainty. The attribution was wrong, and the data was telling us it probably was, but we weren't looking at the data.

That's what this pipeline solves. It doesn't fix diarization -- that's fundamentally hard with a shared mic. But it does two things:

1. **Automates the transcription** so it's not a manual upload-and-copy process.
2. **Flags uncertain attributions** so a human can verify them against the video before publishing.

The old process was: record the meeting, download the Teams recording, upload the audio to Deepgram's web UI, wait, copy the output, paste it into the repo. Now it's one command.

## The Pipeline

```
Teams recording (.mp4)
    |
    v  scripts/transcribe.py
Extract audio (ffmpeg)
    |
    v
*.mp3 ──> Deepgram Nova-3 API (via Python SDK)
                |
                v
          deepgram.json
          (word-level data with speaker_confidence per word)
                |
                v  scripts/analyze-speakers.py
          ┌─────┴──────┐
          |             |
          v             v
deepgram-transcript.md  speaker-confidence-report.md
(readable transcript    (speaker map, flagged passages,
 with resolved names    confidence scores for
 and [LOW CONFIDENCE]   human review)
 markers)               |
          |             |
          └──────┬──────┘
                 v
          /bip-summary skill
          (reads both files, uses confidence
           report to verify attributions
           before publishing)
```

The two scripts can run independently. `transcribe.py` calls the Deepgram API and then automatically chains `analyze-speakers.py`. But you can also run `analyze-speakers.py` on its own against any existing `deepgram.json` -- useful for re-running analysis with a different confidence threshold.

## Setup

### One-time setup

**1. Deepgram API key**

Create a `.env.local` file at the project root:

```
DEEPGRAM_API_KEY=your-key-here
```

Get a key from [console.deepgram.com](https://console.deepgram.com). The free tier includes enough credits to transcribe several hours of audio. The key is loaded by `transcribe.py` at runtime -- it never touches git (`.env.local` is in `.gitignore`).

**2. Python dependency**

```bash
/usr/bin/python3 -m pip install deepgram-sdk
```

The dependency is documented in `requirements.txt` at the project root (`deepgram-sdk>=5.0.0`). The analyze script uses only Python standard library -- no additional installs needed.

**3. ffmpeg**

If you only have `.mp4` files (no pre-extracted `.mp3`), you need ffmpeg:

```bash
brew install ffmpeg
```

If an `.mp3` already exists in the session directory, ffmpeg is not needed -- the script skips extraction.

## Running It

### Full pipeline (most common)

```bash
/usr/bin/python3 scripts/transcribe.py 2-06-26
```

This:
1. Looks for `*.mp3` in `2-06-26/` (uses it if found, otherwise extracts from `*.mp4` via ffmpeg)
2. Sends the audio to Deepgram Nova-3 with diarization enabled
3. Saves the raw API response as `deepgram.json` in the session directory
4. Prints a summary (duration, word count, speakers detected)
5. Auto-runs `analyze-speakers.py` on the result

For a ~50 minute recording (~24 MB mp3), the Deepgram API call takes about 2-5 minutes. The analysis step takes under a second.

**What you'll see:**

```
Found audio: MicrosoftTeams-video.mp3

Sending MicrosoftTeams-video.mp3 (24.1 MB) to Deepgram Nova-3...
This may take 2-5 minutes for a 50-minute recording.
Transcription complete in 147s.

Saved: /path/to/2-06-26/deepgram.json (2.9 MB)

--- Summary ---
  Duration:  51m 30s
  Words:     8,753
  Speakers:  7

Running analyze script...
VTT: transcript (1).vtt (91 named entries)

Session:    2026-02-06
Duration:   51 minutes
Words:      8,753
Segments:   199
Speakers:   7 detected, 2 identified via VTT
            Speaker 1 → Josh Fryer
            Speaker 6 → Joanna Szymczyk
Flagged:    121 segments below 0.5 threshold

Written: /path/to/2-06-26/deepgram-transcript.md
Written: /path/to/2-06-26/speaker-confidence-report.md

Done.
```

### Analysis only (re-run on existing data)

```bash
/usr/bin/python3 scripts/analyze-speakers.py 2-06-26
```

Useful when:
- You already have `deepgram.json` and want to regenerate the transcript/report
- You want to try a different confidence threshold: `--threshold 0.4`
- You've added a VTT file after the initial transcription and want to pick up the speaker names

### If deepgram.json already exists

`transcribe.py` will ask before overwriting:

```
deepgram.json already exists. Overwrite? [y/N]
```

This prevents accidentally re-running the API call (and spending credits) on a session that's already been transcribed.

## What Gets Produced

### deepgram.json

The raw Deepgram API response. This is a large JSON file (~3 MB for a 50-minute session) containing everything Deepgram returns. The key structure:

```json
{
  "metadata": {
    "duration": 3090.5,
    "models": ["nova-3"],
    "model_info": { ... }
  },
  "results": {
    "channels": [{
      "alternatives": [{
        "words": [
          {
            "word": "right",
            "start": 4.24,
            "end": 4.48,
            "confidence": 0.99,
            "speaker": 0,
            "speaker_confidence": 0.27,
            "punctuated_word": "Right."
          },
          ...
        ],
        "paragraphs": { ... }
      }]
    }],
    "utterances": [ ... ]
  }
}
```

The critical fields in each word object:
- **`speaker`** -- Deepgram's assigned speaker number (0-indexed)
- **`speaker_confidence`** -- How confident Deepgram is about the speaker assignment (0.0 to 1.0)
- **`confidence`** -- How confident Deepgram is about the word itself (speech-to-text accuracy)
- **`start` / `end`** -- Timestamps in seconds
- **`punctuated_word`** -- The word with smart formatting (capitalization, punctuation)

The distinction between `confidence` (word accuracy) and `speaker_confidence` (speaker assignment) is important. A word can have high speech confidence (Deepgram is sure it heard "right") but low speaker confidence (Deepgram isn't sure *who* said it).

### deepgram-transcript.md

A readable, speaker-labeled transcript. This is what you'd read to follow the conversation:

```markdown
# Transcript — 2026-02-06

**Duration:** 51 minutes | **Speakers:** 7 detected (2 identified via VTT)

---

**Josh Fryer** [0:05]:

Right. But So I'm I'm just kinda looking for those of you who are publishing.
How did you make the space to get started? How do you guard that space now
that you are already doing that?

---

**Speaker 2 (in-room)** [0:26] [LOW CONFIDENCE]:

Let me ask you a question. What do you mean by secure the the material?
Like, what do you what do you mean by that?

---
```

Key features:
- **Resolved names** for speakers identified via VTT cross-reference (e.g., "Josh Fryer" instead of "Speaker 1")
- **`(in-room)`** label for unresolved speakers -- these are the conference room participants that can't be individually identified
- **`[LOW CONFIDENCE]`** markers on segments where Deepgram's speaker assignment is uncertain
- **Timestamps** in `[M:SS]` format for easy video cross-reference

### speaker-confidence-report.md

The human review document. This is what you check before publishing a summary:

```markdown
# Speaker Confidence Report

## Speaker Map

| Deepgram # | Resolved Name | Match % | Evidence |
|---|---|---|---|
| Speaker 0 | (in-room) | — | 1,176 words |
| Speaker 1 | Josh Fryer | 82% | 1,343 words |
| Speaker 2 | (in-room) | — | 1,759 words |
| Speaker 3 | (in-room) | — | 3,449 words |
| Speaker 4 | (in-room) | — | 488 words |
| Speaker 5 | (in-room) | — | 232 words |
| Speaker 6 | Joanna Szymczyk | 81% | 306 words |

## Overall Statistics

- Total words: 8,753
- Total segments: 199
- Low-confidence segments (< 0.50): 121 (61%)
- Speakers identified via VTT: 2 of 7

## Flagged Passages

Review these against the video before publishing.

| # | Time | Speaker | Avg Conf | Text (first 80 chars) |
|---|---|---|---|---|
| 1 | 0:04 | Speaker 0 (in-room) | 0.00 | Right. |
| 2 | 0:26 | Speaker 2 (in-room) | 0.41 | Let me ask you a question... |
| 6 | 4:32 | Josh Fryer | 0.25 | Usually, listen to an audiobook. |
| 7 | 4:35 | Speaker 2 (in-room) | 0.13 | Audiobook? Either |
| ... | ... | ... | ... | ... |
```

The speaker map tells you at a glance who was identified and how confident the mapping is. The flagged passages table is the review checklist -- every entry there needs a human to check the video and confirm or correct the attribution.

## How the Algorithms Work

### Speaker segmentation

The Deepgram response contains individual words, each tagged with a speaker number. The analysis script groups these into segments -- contiguous runs of words from the same speaker.

```
Word: "Right."       speaker=0  start=4.24
Word: "But"          speaker=1  start=5.12    ← speaker changed, new segment
Word: "so"           speaker=1  start=5.28
Word: "I'm"          speaker=1  start=5.44
...
```

After initial grouping, consecutive segments from the same speaker are merged if the gap between them is 2 seconds or less. This handles the common case where Deepgram briefly assigns a filler word ("yeah", "mhmm") to a different speaker in the middle of someone's sentence.

Each segment gets an average `speaker_confidence` across all its words, plus a flag for whether any individual word had a confidence of 0.0 (which Deepgram uses to signal "I really have no idea").

### VTT cross-reference

Teams VTT transcripts identify remote participants by name using `<v Name>text</v>` tags. In-room participants appear as unnamed or `@`-prefixed tags. The analysis script exploits this asymmetry to map Deepgram speaker numbers to real names.

The algorithm:

1. **Parse the VTT** for entries with real speaker names (skip unnamed and `@`-prefixed entries).

2. **Time-overlap matching**: For each named VTT entry, find all Deepgram words that fall within the same time window (with 1-second tolerance on each side). Count which Deepgram speaker number appears most often.

3. **Build a tally**: For each VTT name, accumulate how many Deepgram words from each speaker number overlap.
   ```
   "Josh Fryer" → { Speaker 1: 847, Speaker 3: 42, Speaker 0: 15 }
   "Joanna Szymczyk" → { Speaker 6: 198, Speaker 3: 8 }
   ```

4. **Accept the mapping** only if:
   - The dominant speaker accounts for >70% of overlapping words
   - There are at least 20 words of evidence
   - No other name has already claimed that speaker number (highest match % wins conflicts)

For the February 6 session, this resolved Speaker 1 → Josh Fryer (82% match) and Speaker 6 → Joanna Szymczyk (81% match). The remaining 5 speakers were in-room participants that Teams couldn't individually name, so they stay as "Speaker N (in-room)."

### Why remote speakers resolve but in-room speakers don't

This is a direct consequence of the hybrid meeting setup:

- **Remote participants** (Josh, Joanna) each have their own microphone and their own Teams audio channel. Teams knows exactly who is talking and labels the VTT entries with their name. Deepgram also gets a cleaner signal for these speakers.
- **In-room participants** (Matthew, Daniel, Claudio, Terrence, Jonathan, etc.) all talk into the same conference room mic. Teams sees them as one audio source and can't distinguish between them. The VTT entries for in-room speech are either unnamed or attributed to the room's Teams account. Deepgram tries to distinguish them by voice characteristics, but with a shared mic and natural conversation dynamics (interruptions, laughter, people talking over each other), the confidence drops.

The VTT cross-reference can only resolve names that appear *in* the VTT. If Teams doesn't label a speaker, we can't map them.

### Confidence flagging

A segment is flagged for review if either:
- Its **average speaker_confidence** is below 0.50, or
- **Any word** in the segment has a speaker_confidence of 0.0

The 0.50 threshold was chosen empirically from the February 6 session data. The known-wrong attribution at 4:44 had a confidence of 0.274. The passages around it (where speakers were changing rapidly near the shared mic) ranged from 0.07 to 0.48. Meanwhile, clearly-attributed passages from remote speakers consistently scored above 0.70.

In practice, this threshold flags about 60% of segments in a typical BiP session. That's a lot -- but most of those are in-room speakers where attribution genuinely is uncertain. The flagging is conservative by design: it's better to flag something that turns out to be correct than to miss something that's wrong.

**What the numbers mean in practice:**
- **0.80+**: Deepgram is confident. Usually a remote speaker with clean audio.
- **0.50-0.80**: Reasonable confidence. Worth a quick check if the speaker is in-room.
- **0.25-0.50**: Low confidence. Likely a speaker change near the shared mic, or crosstalk.
- **0.00-0.25**: Very low or no confidence. Deepgram is essentially guessing. Short utterances ("yeah", "mhmm") near speaker transitions often land here.
- **0.00 exactly**: Deepgram's signal for "I have no idea who said this." Always flagged.

### The `--threshold` flag

The default threshold is 0.50, but you can adjust it:

```bash
/usr/bin/python3 scripts/analyze-speakers.py 2-06-26 --threshold 0.4
```

Lower thresholds flag fewer segments (less conservative, more risk of missed misattributions). Higher thresholds flag more (more conservative, more review work). For BiP's shared-mic setup, 0.50 is a good balance.

## Integration with /bip-summary

The `/bip-summary` skill is aware of the transcription pipeline. When invoked, it checks for available data in this priority order:

1. **`deepgram.json` + `speaker-confidence-report.md`** → Best case. Proceeds directly with reading both files.
2. **`deepgram.json` only** → Runs `analyze-speakers.py` first to generate the report and transcript.
3. **`*.mp4` or `*.mp3` only** → Runs `transcribe.py` (which chains `analyze-speakers.py` automatically).
4. **`*.vtt` only** → Falls back to reading the VTT directly. No confidence data available in this mode.

When writing the summary, the skill uses the confidence report as its primary guide for attribution verification. Before publishing, it presents all uncertain attributions in a table:

| Timestamp | Current Attribution | Confidence | Quote/Content |
|---|---|---|---|
| 4:44 | Speaker 0 (in-room) | 0.27 | "I have a small child, she's four years old..." |
| 12:11 | Speaker 4 (in-room) | 0.23 | "You're talking about the recording tool?" |

The user verifies these against the video, confirms or corrects each one, and only then does the summary get published. This is the safety net that prevents misattributions from reaching the published archive.

## Limitations

**Diarization is still a guess.** This pipeline doesn't improve Deepgram's speaker identification -- it just tells you when Deepgram isn't confident. The underlying challenge (shared mic, in-room participants) remains.

**In-room speakers stay unresolved.** In a typical BiP session with 7 speakers, only 2 (the remote participants) get resolved via VTT. The other 5 remain "Speaker N (in-room)." A human still needs to identify them from context, voice recognition, or the video.

**The threshold is empirical.** The 0.50 cutoff works well for BiP's setup based on the February 6 data. Different rooms, different microphone configurations, or different numbers of speakers might need a different threshold. The `--threshold` flag exists for this reason.

**Quick transitions are the hardest.** When speakers change rapidly -- someone interjects, two people talk over each other, or there's a quick back-and-forth -- confidence drops sharply. These are also the moments where attribution matters most (who said what in a disagreement or rapid exchange).

**61% flagged is normal.** A typical BiP session will have more than half its segments flagged. This isn't a failure of the system -- it's an honest reflection of how hard speaker attribution is with a shared mic. The flag rate would drop significantly with individual microphones or a dedicated speaker tracking system.

## File Reference

| File | Committed | Purpose |
|------|-----------|---------|
| `scripts/transcribe.py` | Yes | Deepgram API call via Python SDK, audio extraction |
| `scripts/analyze-speakers.py` | Yes | Speaker analysis, VTT cross-reference, confidence flagging |
| `requirements.txt` | Yes | Documents `deepgram-sdk>=5.0.0` dependency |
| `.env.local` | No (gitignored) | Deepgram API key |
| `deepgram.json` | No (gitignored) | Raw Deepgram API response per session |
| `deepgram-transcript.md` | No (gitignored) | Readable transcript with resolved names |
| `speaker-confidence-report.md` | No (gitignored) | Flagged passages for human review |
