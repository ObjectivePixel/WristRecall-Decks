#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
COMPILER="$SCRIPT_DIR/DeckCompiler"
DECKS_DIR="$REPO_ROOT/decks"
OUTPUT_DIR="$REPO_ROOT/output"

if [ ! -x "$COMPILER" ]; then
    echo "Error: DeckCompiler binary not found at $COMPILER" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

DECK_IDS=("$@")

if [ "${#DECK_IDS[@]}" -gt 0 ]; then
    for deck_id in "${DECK_IDS[@]}"; do
        echo "==> Compiling $deck_id..."
        "$COMPILER" --standalone --decks-dir "$DECKS_DIR" --deck "$deck_id" \
            --export-wristdeck --output-dir "$OUTPUT_DIR"
        echo ""
    done
else
    echo "==> Compiling all decks..."
    "$COMPILER" --standalone --decks-dir "$DECKS_DIR" \
        --export-wristdeck --output-dir "$OUTPUT_DIR"
    echo ""
fi

echo "Done. Output in $OUTPUT_DIR/:"
ls -lh "$OUTPUT_DIR"/*.wristdeck 2>/dev/null || true
