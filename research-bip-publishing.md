# Research: Publishing Beautiful BiP Session Recaps

**Date**: 2026-02-16
**Goal**: Turn weekly session summaries into polished, shareable documents (PDF + web) with a streamlined, repeatable workflow.

---

## The Problem

We produce a markdown session summary each week with embedded PNG screenshots. Currently it lives as a `.md` file in a folder. We want it to be:
- Beautiful to read and consume
- Available as a PDF (for Teams threads, email, offline reading)
- Available in a browser (for link sharing, archiving)
- Streamlined to produce weekly without excessive effort

---

## Consensus Recommendation: Pandoc + WeasyPrint

All three research tracks converged on the same core pipeline:

```
Markdown (source) --> Pandoc --> HTML + CSS --> WeasyPrint --> PDF
                            \--> Standalone HTML (web version)
```

**Why this wins:**
- **Full design control via CSS** — not locked into LaTeX's academic look or a platform's aesthetic
- **Lightweight dependencies** — `brew install pandoc weasyprint` (no 4GB MacTeX)
- **Single source, dual output** — one markdown file produces both HTML and PDF
- **Images just work** — CSS handles sizing naturally; no LaTeX float surprises
- **Weekly automation** — two commands wrapped in a shell script
- **CSS is a known skill** — easier to iterate on than LaTeX or Typst templates

### The Build Commands

```bash
# Web version (self-contained HTML with embedded images)
pandoc session-summary.md \
  --standalone --embed-resources \
  --css=../../templates/bip-web.css \
  --metadata title="BiP Session Summary — 2026-02-13" \
  --toc --toc-depth=2 \
  -o session-summary.html

# PDF version
pandoc session-summary.md \
  --standalone \
  --css=../../templates/bip-print.css \
  --pdf-engine=weasyprint \
  -o session-summary.pdf
```

### What We Build Once

Two CSS files (~150-200 lines each):
- `bip-web.css` — screen-optimized, responsive, dark mode support
- `bip-print.css` — print-optimized, page breaks, running headers/footers, margins

These become reusable design assets. The markdown source doesn't change.

---

## Design Direction: Newsletter-Report Hybrid

### Layout
- **Single column** with full-width image breakouts (like Stripe's engineering blog)
- 65-75 character line measure (~750px max-width)
- Generous vertical spacing between sections
- Images at full content width with subtle shadow and rounded corners
- Pull quotes (blockquotes) styled with left accent border and tinted background

### Typography
- **Body**: System fonts (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto`), 18px, line-height 1.7
- **Headings**: Semibold, teal accent border on H2 to create visual rhythm
- **Captions**: Italic, 0.9em, centered, gray
- **Blockquotes**: 1.15em, italic, with left border accent

### Color Palette (Understated Editorial)
| Element | Color | Hex |
|---------|-------|-----|
| Body text | Charcoal | `#1a202c` |
| Headings | Deep blue-gray | `#2d3748` |
| Accent | Muted teal | `#2c7a7b` |
| Links | Brighter teal | `#319795` |
| Background | Off-white | `#fafafa` |
| Code blocks | Light gray | `#edf2f7` |
| Captions | Medium gray | `#718096` |

### Image Treatment
- `max-width: 100%` with `border-radius: 6px`
- Subtle drop shadow: `0 4px 12px rgba(0,0,0,0.1)`
- Captions styled as `figcaption` elements
- For PDF: `max-width: 6.5in` to fit page margins

### Information Hierarchy
```
Header (title, date, participants, duration)
  --> Executive Summary (2-3 sentences, session theme)
    --> Topic Sections (with screenshots inline)
      --> Key Themes & Insights
        --> Board State (final board screenshot)
          --> Session Notes (appendix-style)
```

---

## Alternative Approaches Considered

### For PDF Generation

| Option | Quality | Automation | Trade-off |
|--------|---------|------------|-----------|
| **Pandoc + WeasyPrint** | Excellent | Excellent | Need to write CSS (one-time) |
| **Pandoc + Eisvogel** | Very Good | Excellent | Report-style, not newsletter; 4GB LaTeX dep |
| **Typst** | Excellent | Excellent | Not markdown-native; conversion step needed |
| **Puppeteer** | Good | Good | No running headers/footers; 200MB+ Chromium |
| **Prince XML** | Best | Excellent | $3,800 commercial license |

**Eisvogel** is the fastest "good enough" option — one command, zero CSS, polished report look. Good fallback if we want results immediately before investing in custom CSS.

**Typst** is the future-forward option — blazing fast, beautiful output, tiny install. But requires learning new markup or maintaining a Pandoc conversion pipeline.

### For Web Publishing

| Option | Quality | Setup | Best For |
|--------|---------|-------|----------|
| **Pandoc + Pico CSS** (single HTML) | 8/10 | 30 min | Immediate sharing, zero infrastructure |
| **Eleventy + GitHub Pages** | 9/10 | 2-3 hours | Persistent archive with URLs |
| **Ghost** | 9/10 | 1-2 hours | Newsletter distribution + email subscribers |
| **Hugo** | 8/10 | 1-2 hours | Theme ecosystem, fast builds |

**Pandoc single-file HTML** is the starting point — self-contained file with base64-embedded images, shareable as an attachment or hosted anywhere.

**Eleventy** is the upgrade path — when you want `bip.improving.com/sessions/2026-02-13/` with an index, archive, and RSS feed.

**Ghost** becomes relevant if BiP recaps should reach people beyond the Teams thread (subscribers, email distribution). $9/month.

---

## Proposed Weekly Workflow

### Time Budget: ~90 minutes/week (down from 150+)

| Phase | Time | Automation |
|-------|------|------------|
| **Capture** (during meeting) | 0 min | Teams recording automatic |
| **Process** (same day) | ~28 min | 64% automated (transcript, images) |
| **Draft** (next day) | ~55 min | Manual — the core value |
| **Publish** (next day) | ~9 min | 78% automated (build, share) |

### What Gets Automated

1. **Session scaffolding**: `./scripts/new-session.sh 2026-02-20` creates folder, copies template
2. **Image optimization**: Resize, compress PNGs for web and print
3. **Document generation**: Pandoc + WeasyPrint produces HTML + PDF
4. **Archive management**: Git commit + push, update index

### What Stays Manual

- Executive summary writing (facilitator judgment)
- Topic section synthesis (the core value-add)
- Narrative editing and flow
- Facilitator reflections

---

## Implementation Phases

### Phase 1: Prove the Concept (This Week)

**Goal**: Take the existing Feb 13 summary and produce a beautiful HTML + PDF.

1. Install dependencies: `brew install pandoc && pip3 install weasyprint`
2. Create `templates/bip-web.css` (starter CSS provided by research agent)
3. Create `templates/bip-print.css` (adapted from web CSS with print rules)
4. Run Pandoc on the Feb 13 summary
5. Evaluate output, iterate on CSS

**Time**: 2-3 hours (one-time setup + first iteration)

### Phase 2: Build the Automation (Weeks 2-3)

1. Create `scripts/build.sh` wrapping the Pandoc commands
2. Create `scripts/new-session.sh` for folder scaffolding
3. Create `scripts/process-images.sh` for image optimization
4. Test full workflow with a real session
5. Refine CSS based on actual content variations

**Time**: 3-4 hours (one-time)

### Phase 3: Archive & Distribution (Month 2+)

1. Set up Eleventy or GitHub Pages for a persistent web archive
2. Automate deploy on git push
3. Add index page, navigation between sessions
4. Consider Ghost or email distribution if audience grows

---

## Inspiration Sources

The best recurring publications share these qualities:

- **Basecamp's Shape Up**: Single-column, inline images, casual-professional tone
- **Linear's Changelog**: Visual hierarchy through spacing, high-quality screenshots
- **Stripe's Engineering Blog**: Magazine-quality layout, readable measure, storytelling focus
- **Simon Willison's Weeknotes**: Prolific, well-structured, great use of links and inline code
- **GitHub's ReadME Project**: Long-form storytelling, pull quotes, rich media, TOC navigation

**Common pattern**: Generous whitespace, full-width images with captions, pull quotes to break up prose, consistent visual identity week over week.

---

## Files Referenced

- Full PDF generation research: agent output (Pandoc, WeasyPrint, Typst, Eisvogel, etc.)
- Full web publishing research: agent output (single-file HTML, Eleventy, Ghost, etc.)
- Full design & automation research: `research-weekly-recap-design.md`
  - Includes complete CSS starter template (~175 lines)
  - Includes Makefile and build script examples
  - Includes ImageMagick command reference
  - Includes proposed file structure
