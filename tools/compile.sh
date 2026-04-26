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

# Default to v2 output format. Callers can override with --format v1.
FORMAT="v2"
DECK_IDS=()
while [ $# -gt 0 ]; do
    case "$1" in
        --format)
            FORMAT="$2"
            shift 2
            ;;
        *)
            DECK_IDS+=("$1")
            shift
            ;;
    esac
done

if [ "${#DECK_IDS[@]}" -gt 0 ]; then
    for deck_id in "${DECK_IDS[@]}"; do
        echo "==> Compiling $deck_id (format: $FORMAT)..."
        "$COMPILER" --standalone --decks-dir "$DECKS_DIR" --deck "$deck_id" \
            --format "$FORMAT" --export-wristdeck --output-dir "$OUTPUT_DIR"
        echo ""
    done
else
    echo "==> Compiling all decks (format: $FORMAT)..."
    "$COMPILER" --standalone --decks-dir "$DECKS_DIR" \
        --format "$FORMAT" --export-wristdeck --output-dir "$OUTPUT_DIR"
    echo ""
fi

echo "Done. Output in $OUTPUT_DIR/:"
ls -lh "$OUTPUT_DIR"/*.wristdeck 2>/dev/null || true
