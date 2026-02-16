---
name: bip-publish
description: End-to-end publishing workflow for a Build in Public session. Builds standalone HTML/PDF, builds the Eleventy site, tests locally, and deploys via PR.
argument-hint: "<session-dir> (e.g., 2-13-26)"
---

# Build in Public — Publish Session

You are publishing a BiP session summary to the project website.

## Instructions

Use the session directory provided in `$ARGUMENTS` (e.g., `2-13-26`). If no argument is given, look for the most recent session folder.

Work through each step below in order. Stop and report if any step fails.

---

### Step 1: Verify Session Summary Exists

Look for a `*-session-summary.md` file in the session directory.

```
<session-dir>/*-session-summary.md
```

If the file does not exist, stop and tell the user to run `/bip-summary` first.

---

### Step 2: Verify YAML Frontmatter

The session summary **must** have YAML frontmatter at the top for Eleventy to render it. Check that the file starts with `---` and contains these required fields:

```yaml
---
layout: session.njk
title: "BiP Session Summary — YYYY-MM-DD"
date: YYYY-MM-DD
description: "One-line summary of what was discussed."
---
```

- **layout** must be `session.njk`
- **title** should follow the pattern `"BiP Session Summary — YYYY-MM-DD"`
- **date** should be the ISO date matching the session (e.g., `2026-02-13`)
- **description** should be a brief summary of the session topics

If frontmatter is missing or incomplete, add or fix it before proceeding.

---

### Step 3: Build Standalone HTML + PDF

Run the build script to generate shareable standalone files:

```bash
./scripts/build.sh <session-dir>
```

This produces:
- `<session-dir>/session-summary.html` — self-contained HTML with embedded CSS
- `<session-dir>/session-summary.pdf` — print-styled PDF

Verify both files are created. If PDF generation fails (weasyprint not installed), note it but continue — HTML is sufficient.

---

### Step 4: Build the Eleventy Site

Run the Eleventy build to compile the full site:

```bash
npx eleventy
```

Check the output for errors. The session summary should appear in the `_site/` output directory.

---

### Step 5: Test Locally

Start the Eleventy dev server for the user to preview:

```bash
npx eleventy --serve --port=9091
```

Tell the user the site is available at `http://localhost:9091/` and ask them to verify the new session page looks correct. Wait for their confirmation before proceeding.

**Important**: Use port 9091 to avoid conflicts with other dev servers.

---

### Step 6: Commit Changes

Stop the dev server if still running, then commit using a feature branch workflow:

1. Make sure you are on a feature branch (not `main` — there is a pre-commit hook that blocks direct commits to main). If on main, create a branch:
   ```bash
   git checkout -b publish/<session-dir>
   ```
2. Stage the session files:
   ```bash
   git add <session-dir>/*-session-summary.md
   git add <session-dir>/session-summary.html
   git add <session-dir>/session-summary.pdf
   ```
   Also stage any new screenshots or images referenced in the summary.
3. Do NOT stage `_site/` — it is generated and should be in `.gitignore`.
4. Commit with a descriptive message:
   ```
   Add session summary for YYYY-MM-DD
   ```

---

### Step 7: Push and Create PR

1. Push the branch to origin:
   ```bash
   git push -u origin <branch-name>
   ```
2. Switch GitHub CLI user if needed:
   ```bash
   gh auth switch --user matt-wright86
   ```
3. Create a pull request:
   ```bash
   gh pr create --title "Add session summary for YYYY-MM-DD" --body "Publishes the BiP session summary for YYYY-MM-DD to the site."
   ```
4. Merge the PR:
   ```bash
   gh pr merge --squash --delete-branch
   ```

---

### Step 8: Verify Deployment

After merging, the GitHub Actions workflow will automatically deploy to GitHub Pages.

1. Check the workflow status:
   ```bash
   gh run list --limit 1
   ```
2. If the run is still in progress, wait and check again:
   ```bash
   gh run watch
   ```
3. Once deployed, tell the user the session is live and provide the URL pattern:
   ```
   https://matt-wright86.github.io/bip/<session-dir>/
   ```

---

## Quick Reference

| Step | Command | What it does |
|------|---------|-------------|
| 3 | `./scripts/build.sh <dir>` | Standalone HTML + PDF |
| 4 | `npx eleventy` | Build Eleventy site |
| 5 | `npx eleventy --serve --port=9091` | Local preview |
| 7 | `gh pr create` / `gh pr merge --squash --delete-branch` | Ship it |
| 8 | `gh run watch` | Verify deployment |
