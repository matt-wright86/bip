#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/.."

# --- Validate arguments ---
if [ $# -lt 1 ]; then
  echo "Usage: $0 <session-dir>"
  echo "Example: $0 2-13-26"
  exit 1
fi

SESSION_DIR="$PROJECT_DIR/$1"

if [ ! -d "$SESSION_DIR" ]; then
  echo "Error: session directory not found: $SESSION_DIR"
  exit 1
fi

# --- Find the session summary markdown ---
MD_FILES=("$SESSION_DIR"/*-session-summary.md)

if [ ! -f "${MD_FILES[0]}" ]; then
  echo "Error: no *-session-summary.md found in $SESSION_DIR"
  exit 1
fi

MD_FILE="${MD_FILES[0]}"
echo "Source: $MD_FILE"

# --- Extract date from filename for title ---
BASENAME="$(basename "$MD_FILE")"
FILE_DATE="${BASENAME%-session-summary.md}"
PRETTY_DATE="$FILE_DATE"

# --- CSS paths ---
WEB_CSS="$SCRIPT_DIR/../templates/bip-web.css"
PRINT_CSS="$SCRIPT_DIR/../templates/bip-print.css"

# --- Strip YAML frontmatter (used by Eleventy, not Pandoc) ---
CLEAN_MD="$SESSION_DIR/.pandoc-input.md"
# Normalize CRLF to LF first, then strip YAML frontmatter so Pandoc doesn't render it as a title block
tr -d '\r' < "$MD_FILE" > "$CLEAN_MD"
FIRST_LINE=$(head -1 "$CLEAN_MD")
if [ "$FIRST_LINE" = "---" ]; then
  FRONTMATTER_END=$(tail -n +2 "$CLEAN_MD" | grep -n '^---$' | head -1 | cut -d: -f1)
  tail -n +"$((FRONTMATTER_END + 2))" "$CLEAN_MD" > "$CLEAN_MD.tmp"
  mv "$CLEAN_MD.tmp" "$CLEAN_MD"
fi

# --- Generate HTML ---
echo ""
echo "Generating HTML..."
if pandoc "$CLEAN_MD" \
  --standalone \
  --embed-resources \
  --resource-path="$SESSION_DIR" \
  --css="$WEB_CSS" \
  --toc --toc-depth=2 \
  -o "$SESSION_DIR/session-summary.html"; then
  SIZE=$(du -h "$SESSION_DIR/session-summary.html" | cut -f1)
  echo "  HTML: $SESSION_DIR/session-summary.html ($SIZE)"
else
  echo "  HTML generation failed."
fi

# --- Generate PDF ---
echo ""
echo "Generating PDF..."
if pandoc "$CLEAN_MD" \
  --standalone \
  --resource-path="$SESSION_DIR" \
  --css="$PRINT_CSS" \
  --pdf-engine=weasyprint \
  -o "$SESSION_DIR/session-summary.pdf"; then
  SIZE=$(du -h "$SESSION_DIR/session-summary.pdf" | cut -f1)
  echo "  PDF:  $SESSION_DIR/session-summary.pdf ($SIZE)"
else
  echo "  PDF generation failed."
fi

# --- Clean up temp file ---
rm -f "$CLEAN_MD"

echo ""
echo "Done."
