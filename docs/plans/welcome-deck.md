# Welcome / How-to-Use Deck — Plan

The onboarding deck source under `decks/welcome/`: a 10-card "how to use WristRecall" deck
that doubles as the built-in default deck and a Quiz-v2 Learn-mode example.

## 1. Deck format findings

This repo authors decks as plain JSON, compiled to a `.wristdeck` (zipped SQLite store +
`manifest.json` + cover image) by `tools/DeckCompiler` (Mach-O arm64 binary; wrapper
`tools/compile.sh`). Reference example: `decks/mojo-language/`.

**Folder layout** (`decks/<deck-id>/`):
- `deck.json` — the manifest (required). Folder name = deck `id`.
- `cards.json` — the cards (filename must match the manifest's `sourceFileName`).
- `assets/<imageName>.jpg` — optional 1024×1024 cover image.
- Compiler output goes to `output/` (gitignored).

**Manifest (`deck.json`) fields:**
- `id` (folder name), `uuid` (stable, `uuidgen`; never change between releases).
- `name`, `description` (one-liner in the deck browser).
- `storeFileName` — base name of the compiled SQLite store (no extension).
- `imageName` — base name of cover image in `assets/` (no extension).
- `gradientColors` — `["#RRGGBBAA", "#RRGGBBAA"]`, two-stop background gradient.
- `cardCount` / `topicCount` — **must match actual content** or the compiler refuses.
- `category`, `version` (semver, bump per release), `sourceFileName`.
- Optional: `moreInfoURL`, `aboutURL`.
- `topicDefinitions` — array of `{ "name": ..., "cardIDs": [...] }`. **Every card ID must
  appear in exactly one topic.**

**Cards (`cards.json`)** — array of `{ id, front, back }`:
- `id` — unique integer, referenced by `topicDefinitions`.
- `front.text` / `back.text` — plain-text fallback (accessibility label / non-markdown).
- `front.markdown` / `back.markdown` — the rich text actually rendered.
- `back.code_snippet` — legacy; leave `null` (embed code in markdown fences instead).
- `back.formatting.inline_code_terms` — legacy hint; empty array `[]` is fine.

**Markdown subset** (CommonMark + one extension):
- `##` for the answer headline (short — it's the visual anchor).
- Ordered/unordered lists; `**bold**`, `*italics*`, `` `inline code` ``; ``` ``` ``` fences.
- Custom color callout: `{#RRGGBB}...{/}`. Conventions: teal `#0F766E` = key insight/context,
  red `#C62828` = warnings/mistakes, blue `#1A3A6B` = trivia asides.
- Plain Unicode emoji render fine (UTF-8 store).

**Compile path (v2-only).** `compile.sh` always passes `--format v2` (markdown lives in
`prompt`/`answer`; legacy `codeSnippet`/`highlightTerms` left empty). v1 still exists in the
binary as a flag but the repo's tooling is v2-only.

```bash
# Validate WITHOUT producing a shipping artifact (writes SQLite to a temp/output dir only):
./tools/DeckCompiler --standalone --decks-dir ./decks --deck welcome --format v2 --output-dir <tmp>
# Full shipping build:
./tools/compile.sh welcome   # → output/welcome.wristdeck
```

## 2. Proposed deck metadata

| Field | Value | Notes |
|---|---|---|
| `id` | `welcome` | folder name |
| `uuid` | `07AF2948-3D9B-4990-9BF0-EE29E7954731` | generated; keep stable |
| `name` | **Welcome to WristRecall** | |
| `description` | "Learn how to use WristRecall in ten quick cards — your wrist, your decks, your daily streak." | |
| `category` | **Getting Started** | the deck's category (existing categories: Programming, Geography). |
| `gradientColors` | `["#1E3A8AFF", "#10A37FCC"]` | blue→teal, the AUTHORING.md sample palette; friendly/neutral, distinct from the three existing decks. |
| `imageName` | `welcome_deck` | Final cover at `assets/welcome_deck.jpg` (1024×1024, blue→teal gradient + flashcard with checkmark glyph). Note: `imageName` is a **required, non-null String** in `DeckCompiler` — removing or nulling it makes the compiler `keyNotFound`/`valueNotFound` fatal-error, so a real asset must exist for the manifest to be internally consistent. |
| `version` | `1.0.0` | |

**Icon / cover:** a flashcard with a checkmark on the blue→teal gradient; reads clearly at
~100px tile size.

## 3. Card outline (10 cards, 3 topics)

Designed to double as a gentle **Learn-mode** deck: each card teaches one concept, builds on the
previous, and the backs use teal `#0F766E` key-insight callouts. No code fences (not a code deck).

**Topic 1 — The Basics** (cards 1–4)
1. What is WristRecall? → flashcards on your wrist; study without your phone once installed.
2. How does a flashcard work? → read, recall in your head, tap to flip and reveal.
3. Marking right/wrong → tap **Got it** = remembered, tap **Missed** = didn't; be honest.
4. Why cards come back → spaced repetition; missed cards return sooner, known cards spaced out.

**Topic 2 — Studying & Decks** (cards 5–7)
5. What is a deck? → a set of cards on one subject; pick one and study.
6. Getting more decks → **CORRECTED:** find decks on the WristRecall decks site / GitHub repo,
   download a `.wristdeck` file, and open it to import. (Earlier draft wrongly said "browse the
   in-app deck library / download free community decks" — there is **no remote registry / in-app
   store**; the app's MCP `wristrecall_decks` capability states "No remote registry," and the
   "Deck Browser" shows *installed* decks, not a discovery store.)
7. Studying on Apple Watch → Deck Browser → swipe left → Install on Watch; syncs over.

**Topic 3 — Habits & Help** (cards 8–10)
8. Session length → short and often beats long and rare; a minute or two counts.
9. Building a daily habit → add complication/widget for one-tap start; keep your streak.
10. Progress & help → check accuracy/streak in Stats, Help pages for tips; "you're ready!"

## 3a. UI/hardware behavior — RESOLVED

Card 6 ("How do I get more decks?") was **corrected** during review — see card 6 note above.
Two more cards describing specific UI/hardware behavior were corrected during review:

- **Card 3 (marking right/wrong).** Grading is **buttons, not a swipe**: after the answer is
  shown the user taps **Got it** (remembered) or **Missed** (didn't). Card 3's front + back
  (text and markdown) reflect this.
- **Card 9 (daily habit).** The app ships **both** surfaces, so card 9 covers both: a watchOS
  **complication** on the watch face AND an iOS **Home Screen widget**.

## 4. Deck identity — RESOLVED

This is **one deck serving all three roles.** The Welcome deck **IS**:
- the **"Learn WristRecall"** deck used to test **Quiz v2 Learn mode**, **and**
- the deck **replacing Mojo** as the built-in/default deck, **and**
- the standalone "how to use" deck.

Name: **"Welcome to WristRecall"** (`deck.json` `name` field and deck README). No separate
Learn-mode / default variants are needed; the single deck works in all three contexts.

## 5. Task checklist

- [x] Explore repo; document deck format, manifest schema, v2 compile path, markdown subset.
      *Acceptance: format section above matches AUTHORING.md and observed mojo/us-states sources.*
- [x] Create `decks/welcome/deck.json` manifest with stable UUID and matching counts.
      *Acceptance: `cardCount`/`topicCount` match content; every card ID in exactly one topic.*
- [x] Author `decks/welcome/cards.json` — 10 cards, v2 markdown, plain-text fallbacks, beginner tone.
      *Acceptance: each card has front/back text + markdown; `code_snippet: null`; teal callouts.*
- [x] Add a folder `README.md` describing the deck.
      *Acceptance: README documents the deck's purpose, format, topics, and category.*
- [x] Validate the deck is well-formed with DeckCompiler (no shipping artifact).
      *Acceptance: compiler reports 10 cards / 3 topics, 0 errors; no `.wristdeck` left in repo.*
- [x] Resolve deck-identity question (Welcome vs Learn WristRecall vs new built-in default).
      *Acceptance: ONE deck serves all three roles, named "Welcome to WristRecall"; plan/README/deck.json aligned.*
- [x] Set `category` to **Getting Started** and confirm gradient/branding.
      *Acceptance: deck.json category is "Getting Started".*
- [x] Add 1024×1024 cover image `assets/welcome_deck.jpg` (final art).
      *Acceptance: final blue→teal cover with flashcard + checkmark glyph; no placeholder stamp.*

Checklist: **7 / 7 done.**
