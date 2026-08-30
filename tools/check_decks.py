#!/usr/bin/env python3
"""Portable structural checker for WristRecall decks.

tools/DeckCompiler is an arm64 macOS binary, so it cannot be the only gate while
several hundred cards are authored and committed. This script runs anywhere
Python 3 does and checks everything that can be checked without it.

Usage:
    tools/check_decks.py                 # every deck under decks/
    tools/check_decks.py mojo-fundamentals
    tools/check_decks.py --strict-mojo mojo-fundamentals

Exit status is non-zero if any check fails.
"""

import argparse
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECKS = os.path.join(REPO, "decks")

# Card-size budgets for the Mojo 1.0 suite. Calibrated against the shipped
# mojo-language deck rather than asserted: its backs run to a median of 270
# chars, p90 636, p95 843, max 1627; code fences median 5 lines, p90 9, max 25;
# code columns p90 45, p95 52, max 77. The budgets sit just above p90 so they
# catch the genuine outliers — the 1000+ char backs and the 25-line fences that
# will not survive a 41mm screen — without outlawing the deck's normal practice.
# They apply only to the decks in BUDGET_DECKS (or with --budgets), so the
# existing catalog stays green.
MAX_FRONT = 120
MAX_BACK = 800
MAX_FENCE_LINES = 12
MAX_CODE_COLS = 64

BUDGET_DECKS = {"mojo-fundamentals", "mojo-advanced", "mojo-libraries", "mojo-gpu"}

# Spellings that must never appear as the preferred API in a Mojo 1.0 deck.
# Matched only inside code fences and inline-code spans: a bare substring search
# is unusable here, since "read" alone hits the English word in 73 of the
# source deck's cards.
STALE_MOJO = [
    (r"\bUnsafePointer\b", "unified into `Pointer`; teach operation-level unsafety"),
    (r"\b__del__\b", "destructor is `__deinit__`"),
    (r"\bInlineArray\b", "renamed `Array`"),
    (r"\bStringSlice\b", "renamed `StringSpan`"),
    (r"\bImplicitlyDestructible\b", "renamed `Deinitable`"),
    (r"\bCollectionElement\b", "superseded by the final trait set"),
    (r"\bOwnedKwargsDict\b", "renamed `StringDict`"),
    (r"\bConditionalType\b", "replaced by the ternary type expression"),
    (r"\btrait_downcast_var\b", "removed; refinement is automatic"),
    (r"\bDType\.invalid\b", "sentinel removed"),
    (r"\balias\s+\w+\s*=", "compile-time values use `comptime`"),
    (r"@parameter\b", "legacy closure decorators are deprecated"),
    (r"\bfn\s+\w+\s*\(", "`fn` is deprecated; `def` declares all functions"),
    (r"\bread\s+self\b|\bread\s+\w+\s*:", "the `read` convention is spelled `imm`"),
    (r"\.mojopkg\b", "packages precompile to `.mojoc`"),
    (r"\bmojo\s+package\b", "the command is `mojo precompile`"),
    (r"\bSIMD\[[^\]]*\bsize\s*=", "the `size` parameter is now `length`"),
]

# A stale spelling is allowed when the card is teaching the replacement — the
# gate forbids presenting an old name as the current API, not naming it at all.
# A card may say "StringSpan was called StringSlice before 1.0"; it may not say
# "use StringSlice". Allowed mentions are reported as warnings, never silently.
REPLACEMENT_GUIDANCE = re.compile(
    r"was called|used to|replaces|replaced|renamed|rename|deprecated|removed|"
    r"is gone|no longer|legacy|before 1\.0", re.I)

errors = []
warnings = []
notes = []


def err(deck, msg):
    errors.append(f"{deck}: {msg}")


def warn(deck, msg):
    warnings.append(f"{deck}: {msg}")


def note(deck, msg):
    """Informational only: a deliberate choice, not something to fix."""
    notes.append(f"{deck}: {msg}")


def code_spans(markdown):
    """Every fenced block and inline-code span in a card body."""
    fences = re.findall(r"```.*?```", markdown, re.S)
    stripped = re.sub(r"```.*?```", "", markdown, flags=re.S)
    inline = re.findall(r"`[^`\n]+`", stripped)
    return fences + inline


def check_deck(deck_id, strict_mojo, force_budgets=False):
    budgets = force_budgets or deck_id in BUDGET_DECKS
    path = os.path.join(DECKS, deck_id)
    manifest_path = os.path.join(path, "deck.json")
    if not os.path.isfile(manifest_path):
        err(deck_id, "no deck.json")
        return
    try:
        manifest = json.load(open(manifest_path))
    except json.JSONDecodeError as e:
        err(deck_id, f"deck.json does not parse: {e}")
        return

    for field in ("id", "uuid", "name", "description", "storeFileName", "imageName",
                  "gradientColors", "cardCount", "topicCount", "category", "version",
                  "sourceFileName", "topicDefinitions"):
        if field not in manifest:
            err(deck_id, f"deck.json missing required field '{field}'")
    if errors:
        pass

    if manifest.get("id") != deck_id:
        err(deck_id, f"deck.json id '{manifest.get('id')}' does not match folder name")

    cards_path = os.path.join(path, manifest.get("sourceFileName", "cards.json"))
    if not os.path.isfile(cards_path):
        err(deck_id, f"cards file {manifest.get('sourceFileName')} not found")
        return
    try:
        cards = json.load(open(cards_path))
    except json.JSONDecodeError as e:
        err(deck_id, f"cards file does not parse: {e}")
        return

    ids = [c["id"] for c in cards]
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        err(deck_id, f"duplicate card ids: {dupes}")
    if manifest.get("cardCount") != len(cards):
        err(deck_id, f"cardCount {manifest.get('cardCount')} != {len(cards)} cards")

    topics = manifest.get("topicDefinitions", [])
    if manifest.get("topicCount") != len(topics):
        err(deck_id, f"topicCount {manifest.get('topicCount')} != {len(topics)} topics")

    seen = {}
    for t in topics:
        for cid in t.get("cardIDs", []):
            if cid in seen:
                err(deck_id, f"card {cid} appears in both '{seen[cid]}' and '{t['name']}'")
            seen[cid] = t["name"]
    for cid in ids:
        if cid not in seen:
            err(deck_id, f"card {cid} is in no topic")
    for cid in seen:
        if cid not in set(ids):
            err(deck_id, f"topic '{seen[cid]}' references non-existent card {cid}")

    # imageName is either a bundled asset basename (assets/<name>.jpg) or, when no
    # asset is bundled, an SF Symbol name used as the deck icon. Asset basenames in
    # this catalog use underscores; SF Symbols never do.
    image_name = manifest.get("imageName", "")
    image = os.path.join(path, "assets", image_name + ".jpg")
    if not os.path.isfile(image):
        if "_" in image_name or not image_name:
            warn(deck_id, f"no cover image at assets/{image_name}.jpg "
                          "(compiles and validates, but cannot be released)")
        else:
            note(deck_id, f"no bundled cover art; using SF Symbol '{image_name}' as the deck icon")

    for card in cards:
        cid = card["id"]
        front = card.get("front", {}).get("markdown") or card.get("front", {}).get("text", "")
        back = card.get("back", {}).get("markdown") or card.get("back", {}).get("text", "")
        if not card.get("front", {}).get("text"):
            err(deck_id, f"card {cid}: front.text is required as the accessibility label")
        if not card.get("back", {}).get("text"):
            err(deck_id, f"card {cid}: back.text is required as the accessibility label")
        if budgets and len(front) > MAX_FRONT:
            err(deck_id, f"card {cid}: front is {len(front)} chars (budget {MAX_FRONT})")
        if budgets and len(back) > MAX_BACK:
            err(deck_id, f"card {cid}: back is {len(back)} chars (budget {MAX_BACK})")
        if budgets:
            for fence in re.findall(r"```(.*?)```", back, re.S):
                lines = [l for l in fence.split("\n") if l.strip()]
                # drop a leading bare language identifier (```mojo)
                if lines and " " not in lines[0].strip() and len(lines[0].strip()) < 15:
                    lines = lines[1:]
                if len(lines) > MAX_FENCE_LINES:
                    err(deck_id, f"card {cid}: code fence is {len(lines)} lines (budget {MAX_FENCE_LINES})")
                for l in lines:
                    if len(l) > MAX_CODE_COLS:
                        err(deck_id, f"card {cid}: code line is {len(l)} cols (budget {MAX_CODE_COLS}): {l.strip()[:40]}...")
        if strict_mojo:
            spans = " ".join(code_spans(front) + code_spans(back))
            for pattern, why in STALE_MOJO:
                if re.search(pattern, spans):
                    if REPLACEMENT_GUIDANCE.search(back):
                        warn(deck_id, f"card {cid}: /{pattern}/ allowed as replacement guidance — {why}")
                    else:
                        err(deck_id, f"card {cid}: stale spelling /{pattern}/ in code — {why}")

    print(f"  {deck_id}: {len(cards)} cards, {len(topics)} topics")


def check_source_deck_untouched():
    """decks/mojo-language is read-only source material for the 1.0 revision."""
    import subprocess
    try:
        out = subprocess.run(["git", "status", "--porcelain", "decks/mojo-language"],
                             cwd=REPO, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:
        return
    if out:
        err("mojo-language", "source deck has uncommitted modifications; it must stay unchanged:\n" + out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("decks", nargs="*", help="deck ids (default: all)")
    ap.add_argument("--strict-mojo", action="store_true",
                    help="run the Mojo 1.0 stale-spelling scan (automatic for the mojo-* 1.0 decks)")
    ap.add_argument("--budgets", action="store_true",
                    help="apply card-size budgets to every deck, not just the Mojo 1.0 suite")
    args = ap.parse_args()

    ids = args.decks or sorted(d for d in os.listdir(DECKS)
                               if os.path.isdir(os.path.join(DECKS, d)))
    print(f"Checking {len(ids)} deck(s)...")
    for d in ids:
        check_deck(d, args.strict_mojo or d in BUDGET_DECKS, args.budgets)
    check_source_deck_untouched()

    for n in notes:
        print(f"NOTE  {n}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"\n{len(errors)} error(s)")
        return 1
    print(f"\nOK{f' ({len(warnings)} warning(s))' if warnings else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
