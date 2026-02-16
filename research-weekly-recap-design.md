# Research: Weekly Meeting Recap Document Design & Automation

**Project**: Build in Public (BiP) Weekly Recap
**Date**: 2026-02-16
**Purpose**: Design a beautiful, repeatable workflow for weekly meeting summaries

---

## 1. Document Design Patterns for Meeting Recaps

### Recommended Pattern: **Newsletter-Report Hybrid**

The most effective meeting recaps combine the scannable structure of newsletters with the depth of technical reports. This approach works because:

- **Newsletter elements**: Visual hierarchy, section breaks, pull quotes
- **Report elements**: Detailed narratives, appendices, structured metadata
- **Magazine elements**: Generous whitespace, striking imagery, editorial flow

### Information Architecture

```
┌─────────────────────────────────────┐
│ Header Banner                       │
│ - Session date, number, attendance  │
└─────────────────────────────────────┘
│ Executive Summary (1-2 paragraphs)  │
│ - Key themes, notable moments       │
└─────────────────────────────────────┘
│ Topic Sections (2-4)                │
│ ┌─────────────────────────────────┐ │
│ │ Topic Title                     │ │
│ │ - Lead: Who raised it, why      │ │
│ │ - Discussion highlights         │ │
│ │ - Key insights                  │ │
│ │ - [Screenshot/visual evidence]  │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
│ Reflections & Meta-Insights         │
│ - Patterns across topics            │
│ - Facilitator observations          │
└─────────────────────────────────────┘
│ Participation & Next Steps          │
│ - Contributors acknowledged         │
│ - Follow-up items                   │
│ - Next session date                 │
└─────────────────────────────────────┘
│ Appendix (collapsible/secondary)    │
│ - Full voting results               │
│ - Additional screenshots            │
│ - Transcript excerpts               │
└─────────────────────────────────────┘
```

### Layout Patterns Ranked by Effectiveness

1. **Single Column with Breakout Elements** (Recommended)
   - Main prose in readable column (65-75 characters wide)
   - Images, quotes, and asides break full-width or offset
   - Easy to scan, works on all devices
   - Example: Stripe's engineering updates, GitHub's blog

2. **Magazine Two-Column**
   - Left column: Prose and discussion
   - Right column: Screenshots, quotes, metadata
   - Professional appearance, harder to implement responsively
   - Example: Traditional print publications, some Medium layouts

3. **Card-Based Sections**
   - Each topic is a distinct card with consistent structure
   - Works well for diverse content types
   - Risk: feels disconnected without strong narrative flow
   - Example: Linear's changelogs, Notion databases

4. **Timeline/Chronological**
   - Follows meeting progression linearly
   - Good for live notes, less good for synthesis
   - BiP use case: Not recommended (we synthesize, not transcribe)

### Screenshot Integration Strategies

**Option A: Full-Width Hero Images** (Recommended for BiP)
```markdown
# Topic: Voice Journaling Workflow

*Claudio shares his approach to processing thoughts before writing*

![Agile.coffee board showing voice journaling discussion](./images/voice-journaling-board.png)
*The board after voting: voice journaling received 8 votes*

Key points from the discussion...
```

**Why this works:**
- Screenshots provide visual evidence of the actual discussion
- Full-width creates "moments" that break up prose
- Captions give context without disrupting reading flow

**Option B: Side-by-Side Comparison**
```markdown
| Before | After |
|--------|-------|
| ![Initial board](./img1.png) | ![After voting](./img2.png) |
```

**Use when:** Showing process or transformation

**Option C: Thumbnail Gallery**
- Use in appendix for "other highlights"
- Not recommended for main content (too busy)

### Content Structure Best Practices

**Executive Summary Formula:**
```
[Session metadata] + [Attendance note] + [1-2 sentence theme]
+ [Notable contribution or moment] + [Forward-looking statement]
```

Example:
> **Session #47 - January 30, 2025**
> 8 participants (5 in-office, 3 remote)
>
> This week's BiP centered on the tension between structure and
> emergence in creative work. Claudio's voice journaling workflow
> sparked a broader conversation about how we externalize thinking
> before it's ready for polish. The session demonstrated BiP at its
> best: starting with a concrete practice, discovering the principles
> underneath.

**Topic Section Structure:**
1. **Lead paragraph**: Who, what, why (context)
2. **Discussion narrative**: Key exchanges, build-up of ideas
3. **Insight extraction**: What was learned, what matters
4. **Visual evidence**: Screenshot showing the actual board/moment
5. **Connection to BiP values**: How this exemplifies the forum's purpose

**Pull Quote Strategy:**
Use blockquotes to highlight participant voice:

```markdown
> "I realized I was waiting for the perfect framework before starting.
> Voice journaling let me capture the mess first."
> — Claudio, on creative process
```

**Effect:** Humanizes the document, breaks up prose, elevates contributor voices

---

## 2. Visual Design Considerations

### Typography System

**Primary Text (Body Copy):**
- Font: System fonts for reliability
  - Web: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
  - PDF: Georgia (serif for warmth) or Inter (sans-serif for modernity)
- Size: 16-18px (web), 11-12pt (PDF)
- Line height: 1.6-1.75 (generous for readability)
- Measure: 65-75 characters (roughly 600-700px max-width)
- Color: Dark gray (#1a1a1a or #2d3748), not pure black

**Headings:**
- H1 (Session title): 2.5-3em, bold, tracking tight
- H2 (Topic): 1.75-2em, semibold
- H3 (Subsection): 1.25-1.5em, medium weight
- Use color or subtle top border to create visual rhythm
- Example hierarchy:
  ```css
  h1: 48px, font-weight: 700, margin-top: 0, margin-bottom: 1.5rem
  h2: 32px, font-weight: 600, margin-top: 3rem, margin-bottom: 1rem,
      border-top: 3px solid accent-color, padding-top: 1.5rem
  h3: 24px, font-weight: 500, margin-top: 2rem, margin-bottom: 0.75rem
  ```

**Monospace (code/metadata):**
- Font: `"SF Mono", "Consolas", "Monaco", monospace`
- Use for: Session IDs, timestamps, technical references
- Size: 0.9em of body text

### Color Scheme: Professional but Approachable

**Option 1: Improving Brand Colors** (Corporate cohesion)
- Primary: Improving red/orange (if available in brand guide)
- Accents: Complementary blues or grays
- Neutral: Warm grays for text (#2d3748, #4a5568, #718096)

**Option 2: Understated Editorial** (Recommended)
- Text: Charcoal (#1a202c)
- Headings: Deep blue-gray (#2d3748)
- Accent: Muted teal or indigo (#2c7a7b or #5a67d8)
- Links: Slightly brighter than accent (#319795 or #667eea)
- Backgrounds: Off-white (#fafafa or #f7fafc)
- Code blocks: Light gray background (#edf2f7)

**Option 3: High Contrast Modern**
- Pure black text on pure white background
- Single accent color (e.g., electric blue #0066ff)
- Minimalist, bold, magazine-like
- Risk: Can feel sterile without careful execution

### Layout Rhythm & White Space

**Vertical Spacing Rules:**
```
Paragraph gap: 1.25em
Section gap (H2): 4-5em (create clear breaks)
Subsection gap (H3): 2.5-3em
Before images: 2em
After images: 1.5em (with caption)
Blockquote margins: 2em left indent, 1.5em top/bottom
```

**Image Treatment:**
- Full-width: Bleed to content edges
- Drop shadow: Subtle (0 2px 8px rgba(0,0,0,0.1)) for depth
- Rounded corners: 4-8px for friendliness
- Captions: Italic, smaller (0.9em), centered, gray (#718096)

**Section Dividers:**
Instead of horizontal rules, use:
1. White space alone (cleanest)
2. Subtle top border on H2 (creates rhythm without noise)
3. Decorative element (●●● or emoji) centered, sparingly

### Handling Mixed Content Types

**Prose:**
- Let it breathe with generous line height
- Break into 2-4 sentence paragraphs

**Bullet Points:**
- Use for lists, not full paragraphs
- Indent slightly from body text
- 1.5em spacing between items
- Consider custom bullets (colored circles, dashes)

**Blockquotes (Pull Quotes):**
```markdown
> Quote text in larger size (1.15-1.25em)
>
> — Attribution in smaller, regular weight
```
- Left border-accent (4px solid color)
- Background: Very light tint of accent color
- Padding: Generous (1.5em)

**Code/Technical Content:**
- Background: Light gray
- Border: 1px solid slightly darker gray
- Padding: 0.5em
- Border-radius: 3-4px

**Tables:**
- Rare in meeting recaps, but if needed:
- Header row: Bold, background tint
- Zebra striping: Very subtle
- Padding: Generous in cells

### Print/PDF Considerations

**Page Breaks:**
- Avoid breaking in the middle of a topic section
- Use CSS: `page-break-before: auto; page-break-inside: avoid;` on section containers

**Images:**
- 150-300 DPI for print quality
- Size images appropriately (full page width = ~1200-1500px @ 150dpi)

**Colors:**
- Test in grayscale (some people print in B&W)
- Ensure sufficient contrast for link text

**Headers/Footers:**
- Header: Session date & number (small, top right)
- Footer: Page number, "Build in Public @ Improving" (centered)

**Margins:**
- PDF: 1 inch all sides (standard)
- Web: Flexible, center content with max-width

---

## 3. Weekly Automation Workflow

### Ideal End-to-End Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: CAPTURE (During/Immediately After Meeting)            │
└─────────────────────────────────────────────────────────────────┘
  1. Meeting happens (Teams recording)
  2. Facilitator takes live notes (optional, lightweight)
  3. Download transcript (VTT from Teams)
  4. Screenshot key board states (3-5 images)

┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: EXTRACT & ORGANIZE (Same day or next morning)         │
└─────────────────────────────────────────────────────────────────┘
  5. Run transcript through extraction script:
     - Identify speakers
     - Extract topic boundaries
     - Pull out key quotes
     - Generate initial structure
  6. Manually review extracted content
  7. Place screenshots in session folder
  8. Optimize images (resize, compress)

┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: DRAFT & REFINE (Day after meeting)                    │
└─────────────────────────────────────────────────────────────────┘
  9. Fill in markdown template with:
     - Executive summary (manual, based on extraction)
     - Topic sections (extracted + facilitator synthesis)
     - Image references
     - Participant acknowledgments
  10. Light editing pass for narrative flow
  11. Add facilitator reflections

┌─────────────────────────────────────────────────────────────────┐
│ PHASE 4: PUBLISH (Within 48 hours of meeting)                  │
└─────────────────────────────────────────────────────────────────┘
  12. Run build script:
      - Generate HTML from markdown (with CSS)
      - Generate PDF from HTML
      - Create archive copy
  13. Share links (Slack, email, internal wiki)
  14. File in archive folder with naming convention
```

### Automation Opportunities

**High-Value Automation (Implement First):**

1. **Transcript Processing**
   - Tool: Python script using spaCy or GPT-4 API
   - Input: VTT file
   - Output: JSON with topics, speakers, key quotes
   - Time saved: 30-45 minutes

2. **Image Pipeline**
   - Tool: Shell script using ImageMagick or sharp (Node.js)
   - Input: Raw screenshots (PNG)
   - Output: Optimized, resized images (web + print versions)
   - Actions: Resize to standard width, compress, add metadata
   - Time saved: 10-15 minutes

3. **Document Generation**
   - Tool: Pandoc or custom Node.js script
   - Input: Markdown + CSS template
   - Output: HTML and PDF
   - Time saved: 5-10 minutes
   - Benefit: Consistency week over week

4. **Template Scaffolding**
   - Tool: CLI script or Makefile
   - Command: `./scripts/new-session.sh 2026-02-20`
   - Actions:
     - Create folder: `2-20-26/`
     - Generate markdown template with date pre-filled
     - Create `images/` subfolder
     - Copy transcript file to session folder
   - Time saved: 5 minutes

**Medium-Value Automation:**

5. **Participant Tracking**
   - Maintain a YAML file with regular participants
   - Auto-generate acknowledgments section
   - Track contribution frequency

6. **Archive Management**
   - Auto-update index page with new sessions
   - Generate "Past Sessions" listing
   - Create searchable archive

**Low-Priority (Manual is Fine):**

7. **Executive summary writing** - Requires facilitator judgment
8. **Insight synthesis** - Core value-add, keep manual
9. **Narrative editing** - Human touch essential

### Recommended Tech Stack

**Document Generation:**
- **Pandoc** (markdown → HTML → PDF)
  - Pro: Industry standard, highly customizable
  - Con: Requires learning template syntax
- Alternative: **mdbook** or **Hugo** (if web publishing is primary)

**Image Processing:**
- **ImageMagick** (CLI) or **sharp** (Node.js)
- Workflow:
  ```bash
  # Resize to web width, maintain aspect ratio
  magick input.png -resize 1200x -quality 85 output.png

  # Generate print version
  magick input.png -resize 2400x -quality 95 output-print.png
  ```

**Transcript Analysis:**
- **GPT-4 API** (OpenAI) for intelligent extraction
- Prompt engineering for:
  - Topic identification
  - Key quote extraction
  - Speaker attribution
  - Summary generation

**Version Control:**
- **Git** (already using) for all markdown sources and images
- Archive strategy: Keep everything, it's text and compressed images

**Build Automation:**
- **Makefile** or **package.json scripts**
- Example:
  ```makefile
  SESSION_DATE := $(shell date +%Y-%m-%d)
  SESSION_DIR := $(shell date +%-m-%-d-%y)

  .PHONY: new-session build publish

  new-session:
      mkdir -p $(SESSION_DIR)/images
      cp templates/session-template.md $(SESSION_DIR)/$(SESSION_DATE)-session-summary.md
      echo "Created $(SESSION_DIR)"

  build:
      ./scripts/process-images.sh $(SESSION_DIR)/images
      pandoc $(SESSION_DIR)/*.md -o $(SESSION_DIR)/recap.html --css=styles/main.css
      pandoc $(SESSION_DIR)/*.md -o $(SESSION_DIR)/recap.pdf --pdf-engine=weasyprint

  publish: build
      cp $(SESSION_DIR)/recap.* public/
      ./scripts/update-index.sh
  ```

### Weekly Time Budget (With Automation)

| Task | Time (Manual) | Time (Automated) | Savings |
|------|---------------|------------------|---------|
| Download transcript, screenshots | 5 min | 5 min | 0 |
| Process transcript | 45 min | 10 min | 35 min |
| Optimize images | 15 min | 1 min | 14 min |
| Draft executive summary | 15 min | 15 min | 0 |
| Fill topic sections | 30 min | 20 min | 10 min |
| Edit & refine | 20 min | 15 min | 5 min |
| Generate output files | 10 min | 1 min | 9 min |
| Publish & archive | 10 min | 2 min | 8 min |
| **Total** | **2h 30m** | **1h 9m** | **1h 21m** |

**Target:** Reduce from 2.5 hours to just over 1 hour per week.

### Version Management Strategy

**File Structure:**
```
Build In Public/
├── templates/
│   ├── session-template.md
│   ├── run-sheet-template.md
│   └── styles/
│       ├── main.css
│       └── print.css
├── scripts/
│   ├── new-session.sh
│   ├── process-transcript.py
│   ├── process-images.sh
│   └── build.sh
├── archive/
│   └── index.md (auto-generated)
├── 1-30-26/
│   ├── 2026-01-30-session-summary.md
│   ├── 2026-01-30-run-sheet.md
│   ├── recap.html
│   ├── recap.pdf
│   └── images/
│       ├── board-initial.png
│       └── board-after-voting.png
├── 2-6-26/
│   └── ...
└── 2-13-26/
    └── ...
```

**Naming Convention (Already Established):**
- Folders: `M-DD-YY` (e.g., `2-13-26`)
- Files: `YYYY-MM-DD-descriptor.md` (e.g., `2026-02-13-session-summary.md`)

**Git Workflow:**
```bash
# After generating session
git add 2-13-26/
git commit -m "Add session recap for Feb 13, 2026"
git tag session-2026-02-13
git push && git push --tags
```

---

## 4. Dual-Output Strategy (PDF + Web)

### Write Once, Publish Twice: Is It Feasible?

**Yes, with caveats.** Markdown is the right source format, but you need to:

1. Write with both outputs in mind
2. Use a build system that handles format-specific tweaks
3. Accept some compromises or use conditional content

### Single Source Approach

**Best Practice: Markdown + Pandoc + CSS**

```markdown
---
title: "Build in Public - Session #47"
date: 2026-01-30
author: Matthew Wright
---

# Build in Public - Session #47

![Hero image](./images/board-final.png)

Executive summary here...

## Topic 1: Voice Journaling

Discussion content...
```

**Build Commands:**
```bash
# Web output (HTML)
pandoc session-summary.md \
  -o recap.html \
  --standalone \
  --css=../templates/styles/main.css \
  --metadata title="BiP Recap - Jan 30, 2026"

# PDF output
pandoc session-summary.md \
  -o recap.pdf \
  --pdf-engine=weasyprint \
  --css=../templates/styles/print.css \
  -V geometry:margin=1in
```

**Alternative: Markdown → HTML → PDF**
```bash
# Step 1: Generate HTML
pandoc session-summary.md -o temp.html --css=main.css

# Step 2: HTML to PDF (better control)
weasyprint temp.html recap.pdf

# Or use headless Chrome for web→PDF
npx playwright pdf temp.html recap.pdf
```

### Key Differences to Handle

| Aspect | Web | PDF | Solution |
|--------|-----|-----|----------|
| **Images** | Responsive, can be large | Fixed size, must fit page | Use `max-width: 100%` in CSS, provide high-res source |
| **Links** | Clickable | Show URL or convert to footnote | Use Pandoc's footnote conversion for PDF |
| **Page breaks** | Infinite scroll | Fixed pages | Add `page-break-inside: avoid` on section containers for PDF CSS |
| **Typography** | Screen fonts (sans) | Print fonts (serif or sans) | Separate CSS files: `main.css` vs `print.css` |
| **Navigation** | Sidebar, TOC links | Page numbers, static TOC | Generate TOC for both, style differently |
| **Interactive elements** | Possible (toggles, etc.) | Static | Avoid or provide PDF-friendly alternative |

### Gotchas & Solutions

**Gotcha 1: Image Sizing**
- Problem: Same image size doesn't work for both
- Solution: Use CSS to handle sizing
  ```css
  /* main.css (web) */
  img { max-width: 100%; height: auto; }

  /* print.css (PDF) */
  img { max-width: 6.5in; height: auto; }
  ```

**Gotcha 2: Page Breaks**
- Problem: PDF cuts topic sections awkwardly
- Solution: Add page break control in print CSS
  ```css
  @media print {
    .topic-section {
      page-break-inside: avoid;
      page-break-after: auto;
    }
    h2 {
      page-break-after: avoid;
    }
  }
  ```

**Gotcha 3: Color in Print**
- Problem: Colors look different in PDF, expensive to print
- Solution: Test PDF in grayscale, ensure sufficient contrast

**Gotcha 4: Hyperlinks**
- Problem: Links don't work in PDF
- Solution: Pandoc can auto-convert to footnotes
  ```bash
  pandoc --reference-links input.md -o output.pdf
  ```

**Gotcha 5: Typography Rendering**
- Problem: Fonts render differently in browsers vs PDF engines
- Solution: Use web-safe fonts or embed custom fonts
  ```css
  @font-face {
    font-family: 'Inter';
    src: url('fonts/Inter-Regular.woff2') format('woff2');
  }
  ```

### Recommended Dual-Output Workflow

**Option 1: Pandoc + WeasyPrint** (Recommended)
```bash
# Single command, two outputs
pandoc session.md \
  -o recap.html \
  --standalone \
  --css=main.css \
  --metadata title="BiP Recap"

pandoc session.md \
  -o recap.pdf \
  --pdf-engine=weasyprint \
  --css=print.css \
  -V geometry:margin=1in
```

**Pros:**
- Simple, text-based workflow
- Full control via CSS
- No external dependencies (beyond Pandoc & WeasyPrint)

**Cons:**
- Learning curve for Pandoc templates
- CSS for print is less intuitive than web CSS

**Option 2: Static Site Generator + Print Stylesheet**
```bash
# Use Hugo, 11ty, or mdbook
hugo new sessions/2026-01-30.md
hugo server  # Preview web version
# Then use browser "Print to PDF" with print.css
```

**Pros:**
- Beautiful web output with minimal configuration
- Built-in navigation, search, etc.
- Can use browser's print engine (reliable)

**Cons:**
- PDF generation less automated
- More moving parts (Node.js, npm packages, etc.)

**Option 3: Typst (Modern Alternative)**
```typst
// session.typ
#set page(margin: 1in)
#set text(font: "Inter", size: 11pt)

= Build in Public - Session #47

Executive summary...
```

```bash
# Generate both
typst compile session.typ recap.pdf
typst compile --format png session.typ recap.png  # For web
```

**Pros:**
- Purpose-built for beautiful PDFs
- Markdown-like syntax with more power
- Modern tooling

**Cons:**
- Newer tool, smaller ecosystem
- No direct HTML output (workarounds exist)
- Requires learning new syntax

### Recommended Choice for BiP

**Pandoc + WeasyPrint** with separate CSS files

**Reasoning:**
1. You're already working in Markdown
2. Simple build process fits weekly cadence
3. Full control over both outputs
4. No complex dependencies
5. Easy to version control (everything is text)

**Setup:**
```bash
# Install dependencies (macOS)
brew install pandoc
pip3 install weasyprint

# Verify
pandoc --version
weasyprint --version
```

**Build Script (`scripts/build.sh`):**
```bash
#!/bin/bash
SESSION_DIR=$1
SESSION_MD="${SESSION_DIR}/*.md"

# Generate HTML
pandoc ${SESSION_MD} \
  -o ${SESSION_DIR}/recap.html \
  --standalone \
  --css=../templates/styles/main.css \
  --metadata title="Build in Public Recap" \
  --toc \
  --toc-depth=2

# Generate PDF
pandoc ${SESSION_MD} \
  -o ${SESSION_DIR}/recap.pdf \
  --pdf-engine=weasyprint \
  --css=../templates/styles/print.css \
  -V geometry:margin=1in \
  --toc \
  --toc-depth=2

echo "Built recap.html and recap.pdf in ${SESSION_DIR}/"
```

---

## 5. Inspiration & Examples

### Example 1: Basecamp's "Shape Up" Methodology Guide

**URL**: basecamp.com/shapeup (book format)

**What Makes It Effective:**
- **Single-column, generous margins**: Easy to read, no distractions
- **Inline images integrated into prose**: Not as separate "figures," but as part of the narrative flow
- **Consistent header hierarchy**: Clear visual rhythm, easy to scan
- **Casual but professional tone**: Accessible without being dumbed down
- **Web-first but PDF-ready**: Same content works in both formats

**Borrowable Elements for BiP:**
- Section numbers (1.1, 1.2) for easy reference
- Inline images with light borders and captions
- Side notes or callouts for meta-commentary
- Simple, clean typography (system fonts)

### Example 2: Linear's Changelog

**URL**: linear.app/changelog

**What Makes It Effective:**
- **Visual hierarchy through spacing**: Generous white space creates rhythm
- **Consistent structure**: Date → Title → Description → Image
- **High-quality screenshots**: Full-width, crisp, professional
- **Subtle animations (web)**: Delightful but not distracting
- **Clean, modern aesthetic**: Dark mode support, gorgeous typography

**Borrowable Elements for BiP:**
- Date-first organization
- Full-width hero images
- Subtle color accents (their purple)
- "What's new" vs "Improvements" categorization (we could do "Topics" vs "Meta-insights")

### Example 3: Stripe's Engineering Blog

**URL**: stripe.com/blog/engineering

**What Makes It Effective:**
- **Magazine-quality layout**: Feels premium, not corporate-boring
- **Hero images set the tone**: Large, full-bleed images
- **Readable measure**: Content width constrained to ~70 characters
- **Technical depth with accessibility**: Complex topics explained clearly
- **Code blocks integrated seamlessly**: Syntax highlighting, copy button

**Borrowable Elements for BiP:**
- Hero image + title + subtitle layout
- Pull quotes to highlight participant voices
- Emphasis on storytelling, not just facts
- Technical details in expandable sections or appendices

### Example 4: Notion's "What's New" Updates

**URL**: notion.so/releases

**What Makes It Effective:**
- **Card-based layout**: Each update is a self-contained card
- **Visual-first**: Every update has an image or illustration
- **Scannable**: You can understand the whole update from thumbnails
- **Consistent branding**: Notion's color palette and rounded corners throughout

**Borrowable Elements for BiP:**
- Visual consistency week over week
- Emoji or icons to categorize content (🎤 for voice journaling topic, 🤔 for philosophical discussions)
- Short, punchy headlines with longer description below

### Example 5: GitHub's "The ReadME Project"

**URL**: github.com/readme

**What Makes It Effective:**
- **Long-form storytelling**: Not afraid of depth
- **Human-centered**: Profiles and narratives, not just feature lists
- **Rich media**: Images, pull quotes, videos embedded
- **Accessible design**: High contrast, clear typography, works on all devices
- **Table of contents for longer pieces**: Easy navigation

**Borrowable Elements for BiP:**
- TOC at the top for long recaps
- Pull quotes to break up sections
- Participant profiles or recurring contributor highlights
- "Read time" estimate at the top

### Newspaper/Magazine Layout Lessons

**From Print Design:**

1. **Inverted Pyramid** (Journalism)
   - Most important info first
   - Details follow
   - Background last
   - BiP adaptation: Executive summary → Topics → Reflections → Appendix

2. **Visual Hierarchy** (Magazines)
   - Large, striking images
   - Big headlines
   - Subheads and decks
   - Body copy
   - Captions
   - BiP adaptation: Hero image of board → Topic title → Lead paragraph → Discussion → Screenshot → Caption

3. **Grid System** (Both)
   - Consistent margins and gutters
   - Elements align to invisible grid
   - Creates professional appearance
   - BiP adaptation: All images same width, headings align left, consistent spacing

4. **White Space as Design Element** (Modern magazines)
   - Don't fear empty space
   - Creates breathing room
   - Signals premium quality
   - BiP adaptation: Generous paragraph spacing, section breaks, margins

5. **Pull Quotes** (Magazines)
   - Break up gray text
   - Highlight key ideas
   - Give readers an entry point
   - BiP adaptation: Pull out participant insights as blockquotes

6. **Section Fronts** (Newspapers)
   - Clear visual break between sections
   - Sets tone for what follows
   - BiP adaptation: Each topic section starts with visual element (image or decorative break)

---

## Proposed Ideal Workflow

### Overview

**Goal:** From meeting to published recap in 24-48 hours with 60-90 minutes of effort.

**Phases:**
1. **Capture** (during meeting): 0 min extra work
2. **Process** (same day): 15 min automated + 15 min manual
3. **Draft** (next day): 30 min writing + 10 min editing
4. **Publish** (next day): 5 min automated

**Total time investment:** ~75 minutes per week (down from 150+ minutes)

### Detailed Workflow

#### Thursday 1:30-2:30 PM: Meeting Happens

**During meeting:**
- Teams recording active (automatic)
- Facilitator participates, notes mental highlights
- Screenshot board state 2-3 times:
  - Initial state (items before voting)
  - After voting
  - During key discussion moments

**Immediately after (2:30-2:35 PM):**
- Download transcript from Teams (VTT file)
- Save screenshots to Desktop
- (Optional) Voice note to self with top 2-3 highlights

#### Thursday Evening or Friday Morning: Process

**Step 1: Setup** (Automated - 2 min)
```bash
cd ~/Work/Build\ In\ Public
./scripts/new-session.sh 2026-02-20

# This creates:
# - 2-20-26/ folder
# - 2026-02-20-session-summary.md from template
# - images/ subfolder
```

**Step 2: Organize Raw Materials** (Manual - 5 min)
- Move transcript VTT file into session folder
- Move screenshots into `images/` subfolder
- Rename screenshots descriptively:
  - `board-initial.png`
  - `board-after-voting.png`
  - `voice-journaling-discussion.png`

**Step 3: Process Transcript** (Automated - 10 min runtime, 0 min hands-on)
```bash
./scripts/process-transcript.py 2-20-26/transcript.vtt
# Outputs: 2-20-26/transcript-processed.json
# Contains: topics, speakers, key quotes, timestamps
```

**Step 4: Optimize Images** (Automated - 1 min)
```bash
./scripts/process-images.sh 2-20-26/images
# Resizes, compresses, creates @2x versions
```

**Step 5: Review Processed Transcript** (Manual - 10 min)
- Open `transcript-processed.json`
- Verify topics identified correctly
- Note 2-3 key quotes per topic
- Identify any missed moments

**Total process time: 28 minutes** (18 min automated, 10 min manual)

#### Friday Afternoon: Draft

**Step 6: Write Executive Summary** (Manual - 15 min)

Using template + transcript insights, write 2 paragraphs covering:
- Session number, date, attendance
- 1-2 sentence theme statement
- Notable moment or contribution
- Forward-looking closer

**Step 7: Fill Topic Sections** (Manual - 20 min)

For each of 2-3 main topics:
- Lead paragraph: Who raised it, why it matters (3-4 sentences)
- Discussion narrative: Key exchanges, how conversation built (1-2 paragraphs)
- Insight extraction: What was learned (1 paragraph)
- Insert image reference: `![Caption](./images/filename.png)`

**Step 8: Add Reflections & Meta-Insights** (Manual - 10 min)
- Patterns across topics
- Facilitator observations
- How this session exemplified BiP values

**Step 9: Edit Pass** (Manual - 10 min)
- Read through for flow
- Tighten prose
- Check image references
- Verify formatting

**Total draft time: 55 minutes**

#### Friday Late Afternoon: Publish

**Step 10: Build** (Automated - 2 min)
```bash
./scripts/build.sh 2-20-26
# Generates:
# - 2-20-26/recap.html (web version)
# - 2-20-26/recap.pdf (PDF version)
```

**Step 11: Review Outputs** (Manual - 3 min)
- Open HTML in browser
- Open PDF
- Check images, formatting
- Verify links (if any)

**Step 12: Publish & Share** (Automated + Manual - 3 min)
```bash
# Copy to shared location (if applicable)
./scripts/publish.sh 2-20-26

# Or manually:
# - Upload PDF to SharePoint/Drive
# - Post link in Slack/Teams
# - Update archive index
```

**Step 13: Archive** (Automated - 1 min)
```bash
git add 2-20-26/
git commit -m "Add BiP recap for Feb 20, 2026"
git tag session-2026-02-20
git push && git push --tags
```

**Total publish time: 9 minutes**

### Weekly Time Budget Summary

| Phase | Time | When | Automation |
|-------|------|------|------------|
| Capture | 0 min | Thu meeting | ✅ Automatic recording |
| Process | 28 min | Thu evening | ✅ 64% automated |
| Draft | 55 min | Fri afternoon | ❌ Manual (core value) |
| Publish | 9 min | Fri late | ✅ 78% automated |
| **Total** | **92 min** | **24-48 hours** | **52% automated** |

### Future Optimizations

**Phase 2 Improvements (3-6 months out):**

1. **AI-Assisted Summary Generation**
   - Use GPT-4 to draft executive summary from transcript
   - Still requires facilitator review/editing
   - Could save 10 min

2. **Template Variations**
   - Light recap (1 page, bullet points only)
   - Full recap (current plan)
   - Deep dive (focus on one topic with extended analysis)
   - Choose template based on week's content

3. **Web Publishing**
   - Static site for all recaps
   - Searchable archive
   - RSS feed for subscribers
   - Automated deploy on git push

4. **Metrics Tracking**
   - Attendance over time
   - Topics covered
   - Contributor participation
   - Most-voted items

---

## Immediate Next Steps

### Phase 1: Design Foundation (Week 1-2)

**Tasks:**
1. Create `templates/session-template.md` with structure
2. Design `templates/styles/main.css` for web
3. Design `templates/styles/print.css` for PDF
4. Choose color scheme (recommend: Understated Editorial)
5. Test Pandoc + WeasyPrint installation
6. Generate sample output with mock content

**Deliverable:** Working template that produces beautiful HTML + PDF

### Phase 2: Automation Scripts (Week 3-4)

**Tasks:**
1. Write `scripts/new-session.sh` (scaffolding)
2. Write `scripts/process-images.sh` (ImageMagick)
3. Write `scripts/build.sh` (Pandoc commands)
4. Write `scripts/process-transcript.py` (GPT-4 API)
5. Test full workflow with past session
6. Document workflow in README

**Deliverable:** End-to-end automation for next session

### Phase 3: Refinement (Ongoing)

**Tasks:**
1. Run workflow for real session
2. Time each step, identify friction points
3. Refine CSS based on actual content
4. Adjust template based on what works
5. Iterate on transcript processing prompts
6. Build archive index page

**Deliverable:** Smooth, repeatable weekly workflow

---

## Appendix: Technical Specifications

### CSS Template Starter (main.css)

```css
/* BiP Recap Stylesheet - Web Version */

:root {
  --text-color: #1a202c;
  --heading-color: #2d3748;
  --accent-color: #2c7a7b;
  --link-color: #319795;
  --background: #fafafa;
  --code-bg: #edf2f7;
  --border-color: #e2e8f0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 18px;
  line-height: 1.7;
  color: var(--text-color);
  background: var(--background);
  max-width: 750px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

h1 {
  font-size: 3rem;
  font-weight: 700;
  color: var(--heading-color);
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

h2 {
  font-size: 2rem;
  font-weight: 600;
  color: var(--heading-color);
  margin: 4rem 0 1rem 0;
  padding-top: 1.5rem;
  border-top: 3px solid var(--accent-color);
}

h3 {
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--heading-color);
  margin: 2.5rem 0 0.75rem 0;
}

p {
  margin: 0 0 1.25rem 0;
}

a {
  color: var(--link-color);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s;
}

a:hover {
  border-bottom-color: var(--link-color);
}

img {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin: 2rem 0 1rem 0;
}

figure {
  margin: 2rem 0;
}

figcaption {
  text-align: center;
  font-style: italic;
  font-size: 0.9em;
  color: #718096;
  margin-top: 0.5rem;
}

blockquote {
  margin: 2rem 0;
  padding: 1.5rem;
  border-left: 4px solid var(--accent-color);
  background: rgba(44, 122, 123, 0.05);
  font-size: 1.15em;
  font-style: italic;
}

blockquote p:last-child {
  margin-bottom: 0;
}

code {
  font-family: "SF Mono", Consolas, Monaco, monospace;
  font-size: 0.9em;
  background: var(--code-bg);
  padding: 0.2em 0.4em;
  border-radius: 3px;
}

pre {
  background: var(--code-bg);
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  margin: 1.5rem 0;
}

pre code {
  background: none;
  padding: 0;
}

ul, ol {
  margin: 0 0 1.25rem 0;
  padding-left: 2rem;
}

li {
  margin: 0.5rem 0;
}

hr {
  border: none;
  border-top: 1px solid var(--border-color);
  margin: 3rem 0;
}

.session-meta {
  color: #718096;
  font-size: 0.95em;
  margin-bottom: 2rem;
}

.toc {
  background: var(--code-bg);
  padding: 1.5rem;
  border-radius: 6px;
  margin: 2rem 0;
}

.toc h2 {
  margin: 0 0 1rem 0;
  padding: 0;
  border: none;
  font-size: 1.25rem;
}

.toc ul {
  margin: 0;
  list-style: none;
  padding-left: 0;
}

.toc li {
  margin: 0.5rem 0;
}

@media (max-width: 768px) {
  body {
    font-size: 16px;
    padding: 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  h2 {
    font-size: 1.5rem;
  }
}
```

### Pandoc Build Command Reference

```bash
# Basic HTML generation
pandoc input.md -o output.html --standalone

# HTML with custom CSS
pandoc input.md -o output.html --standalone --css=main.css

# HTML with table of contents
pandoc input.md -o output.html --standalone --css=main.css --toc --toc-depth=2

# PDF via WeasyPrint
pandoc input.md -o output.pdf --pdf-engine=weasyprint --css=print.css

# PDF with geometry
pandoc input.md -o output.pdf --pdf-engine=weasyprint -V geometry:margin=1in

# Markdown to Markdown (normalize formatting)
pandoc input.md -o output.md --to=markdown --wrap=auto

# With metadata
pandoc input.md -o output.html --metadata title="My Title" --metadata author="Name"

# Using YAML frontmatter
# (Put this at top of markdown file)
---
title: "Build in Public - Session #47"
date: 2026-01-30
author: Matthew Wright
---
```

### ImageMagick Commands

```bash
# Resize to max width, maintain aspect ratio
magick input.png -resize 1200x output.png

# Resize and compress
magick input.png -resize 1200x -quality 85 output.png

# Create @2x version (retina)
magick input.png -resize 2400x -quality 95 output@2x.png

# Batch process all PNGs in directory
for f in *.png; do
  magick "$f" -resize 1200x -quality 85 "optimized-$f"
done

# Convert to WebP (modern format, smaller files)
magick input.png -quality 85 output.webp

# Add border
magick input.png -border 1 -bordercolor "#e2e8f0" output.png

# Compress without resize
magick input.png -quality 85 output.png
```

### Sample Transcript Processing Prompt (GPT-4)

```python
import openai
import json

def process_transcript(vtt_file_path):
    # Read VTT file
    with open(vtt_file_path, 'r') as f:
        transcript = f.read()

    # GPT-4 prompt
    prompt = f"""
Analyze this meeting transcript and extract:

1. Main topics discussed (2-5 topics)
2. For each topic:
   - Who introduced it
   - Key points made
   - 1-2 notable quotes (with speaker names)
3. Overall themes or insights

Transcript:
{transcript}

Return as JSON:
{{
  "topics": [
    {{
      "title": "Topic name",
      "introduced_by": "Speaker name",
      "key_points": ["point 1", "point 2"],
      "quotes": [
        {{"speaker": "Name", "quote": "Quote text"}}
      ]
    }}
  ],
  "themes": ["theme 1", "theme 2"]
}}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a meeting analyst extracting key information from transcripts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    result = json.loads(response.choices[0].message.content)
    return result

# Usage
result = process_transcript("transcript.vtt")
with open("transcript-processed.json", "w") as f:
    json.dump(result, f, indent=2)
```

---

## Conclusion

This research document provides:

1. **Clear design patterns** for meeting recaps (newsletter-report hybrid, single column with breakouts)
2. **Visual design guidance** (typography, color, spacing, image treatment)
3. **Practical automation workflow** reducing effort from 2.5h to ~1.5h per week
4. **Dual-output strategy** using Pandoc + WeasyPrint (single source, two formats)
5. **Real-world inspiration** from Basecamp, Stripe, Linear, and editorial design

**Recommended immediate action:**
1. Set up Pandoc + WeasyPrint
2. Create CSS templates (use provided starter)
3. Build first recap with new workflow
4. Iterate based on results

**The goal**: Beautiful, consistent, professional weekly recaps that honor the BiP spirit while reducing facilitator burden.

The workflow prioritizes:
- **Automation** where it saves time without sacrificing quality
- **Human judgment** for insight synthesis (the core value)
- **Consistency** in visual design week over week
- **Flexibility** to handle variable content length and types
- **Sustainability** for long-term weekly cadence

With this system, BiP recaps become an artifact participants look forward to—not just a record of what happened, but a polished narrative that reinforces the forum's value and builds institutional memory.
