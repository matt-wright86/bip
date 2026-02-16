---
name: bip-prep
description: Prepare a run sheet for an upcoming Build in Public session. Use when preparing for this week's BiP meeting.
argument-hint: "[date as YYYY-MM-DD]"
---

# Build in Public Session Preparation

You are preparing a run sheet for the upcoming Build in Public (BiP) session.

## Instructions

1. **Get the date**: Use the argument provided (e.g., `$ARGUMENTS`) or today's date if none given
2. **Read last week's session summary** from the most recent dated folder
3. **Create a new folder** for this session using format `M-DD-YY`
4. **Generate the run sheet** following the template below

## Run Sheet Template

Create a file named `YYYY-MM-DD-run-sheet.md` with this structure:

```markdown
# BiP Run Sheet — YYYY-MM-DD

## 1. Start Recording
- Confirm everyone consents to recording

---

## 2. Welcome & Preamble

> "Welcome to Build in Public, or BiP.
>
> This is an open space for building—blog posts, workflows, hobby projects, or anything still forming. The point isn't polish, it's progress.
>
> We're here to share, encourage one another, and offer accountability. We all lift together. Come when you can, be an Improver, and build with us.
>
> Remember the law of two feet—bounce when you need to.
>
> Everyone comes to BiP with a goal. That goal might be curiosity, but everyone has one. Let's start by sharing our goals for this session."

---

## 3. Drop Board Link in Chat

```
[INSERT BOARD LINK HERE]
```

---

## 4. Recap Last Week ([PREVIOUS DATE])

> "Quick recap from last week.
>
> [SUMMARIZE 2-3 KEY DISCUSSION POINTS FROM LAST SESSION]
>
> That's where we left off."

---

## 5. Check the Board / Vote

> "Let's see what's on the board. Take a moment to vote on what you'd like to discuss."

*(Wait for votes)*

---

## 6. Discussion

- Facilitate the top-voted item(s)
- Use guardrails if needed:
  - "Can you give a specific example?"
  - "What did that look like in practice?"
  - "What signal did you miss in hindsight?"

**Potential carryover topics from last week:**
[LIST ANY BOARD ITEMS THAT WEREN'T DISCUSSED FROM LAST SESSION]

**Suggested board items (if participation is low):**
- "Something I started but haven't shipped yet"
- "A workflow I changed this week because of AI"
- "Feedback I got that surprised me"
- "A side project I'm not sure is worth continuing"
- "Something I learned by explaining it to someone else"
- "A habit I'm trying to build (or break)"
- "A tool or technique I want to try but haven't yet"
- "Something I'm overthinking"

---

## 7. Outro

> "Thanks everyone for joining this Build in Public. Today we [reference what was discussed]. We'll have another session next week—bring your goals and your works-in-progress. Until then, safe travels."

---

## 8. Stop Recording
```

## After Creating

Remind the user to:
- Get the board link from agile.coffee and update the run sheet
- Review the recap section before the meeting
