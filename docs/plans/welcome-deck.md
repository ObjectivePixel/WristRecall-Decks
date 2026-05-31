# Welcome / How-to-Use Deck — Plan (DRAFT, pending James's review)

> Status: **DRAFT-PENDING-REVIEW.** The deck source under `decks/welcome/` is written but
> the card copy must be reviewed and approved by James before anything is compiled into a
> shipping `.wristdeck` or committed/released.

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
# Full shipping build (do NOT run for this draft until approved):
./tools/compile.sh welcome   # → output/welcome.wristdeck
```

## 2. Proposed deck metadata

| Field | Value | Notes |
|---|---|---|
| `id` | `welcome` | folder name |
| `uuid` | `07AF2948-3D9B-4990-9BF0-EE29E7954731` | generated; keep stable |
| `name` | **Welcome to WristRecall** | |
| `description` | "Learn how to use WristRecall in ten quick cards — your wrist, your decks, your daily streak." | |
| `category` | **Getting Started** | *new category* (existing: Programming, Geography). Confirm with James — alternative: "General". |
| `gradientColors` | `["#1E3A8AFF", "#10A37FCC"]` | blue→teal, the AUTHORING.md sample palette; friendly/neutral, distinct from the three existing decks. |
| `imageName` | `welcome_deck` | **cover art not yet created** — placeholder gradient until artwork supplied. |
| `version` | `1.0.0` | |

**Icon / cover suggestion:** a wrist/watch glyph or a single flashcard with a checkmark on the
blue→teal gradient; must read clearly at ~100px tile size. (Asset TODO — see checklist.)

## 3. Card outline (DRAFT — 10 cards, 3 topics)

Designed to double as a gentle **Learn-mode** deck: each card teaches one concept, builds on the
previous, and the backs use teal `#0F766E` key-insight callouts. No code fences (not a code deck).

**Topic 1 — The Basics** (cards 1–4)
1. What is WristRecall? → flashcards on your wrist; study without your phone once installed.
2. How does a flashcard work? → read, recall in your head, tap to flip and reveal.
3. Marking right/wrong → swipe right = correct, swipe left = missed; be honest.
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

## 3a. NEEDS JAMES TO CONFIRM AGAINST LIVE APP

Card 6 ("How do I get more decks?") was **corrected** during review — see card 6 note above.
While reviewing, two more cards describe specific UI/hardware behavior that has **not been
verified against the live app** and should be confirmed before approval:

- **Card 3 (marking right/wrong).** Copy currently says: grade by **swiping** — *right = correct,
  left = missed*. Confirm against the live app: (a) is grading actually a **swipe** gesture, or is
  it **tap a "Got it" / "Missed" button**? (b) If it is a swipe, are the directions right=correct /
  left=missed (not reversed)? Update card 3's front + back (text and markdown) if either is wrong.
- **Card 9 (daily habit).** Copy currently says you can add **both** a **watch complication** *and*
  a **Home Screen widget**. Confirm the app actually ships **both** surfaces (a watchOS
  complication AND an iOS Home Screen widget). If only one exists, drop the other from card 9.

## 4. Open question — deck identity (tracked; do not block)

James has **not yet confirmed** whether this Welcome deck is the **same** deck as:
- the **"Learn WristRecall"** deck used to test **Quiz v2 Learn mode**, and
- the deck **replacing Mojo** as the built-in/default deck.

This draft is designed so it *could* serve all three roles (default deck + gentle Learn-mode
deck), but they may need to diverge:
- If it must teach Quiz v2 *Learn mode mechanics* specifically, a card or two may need to mention
  Learn-mode UI that differs from the standard flip/swipe flow described here.
- If it ships in the **Mojo whitelabel edition**, branding/wording referencing "WristRecall" by
  name may need a whitelabel variant (the plan notes this deck "may be excluded from the Mojo
  whitelabel edition").

**Needs from James:** (a) confirm whether Welcome == Learn WristRecall == new built-in default;
(b) confirm the `category` name ("Getting Started" vs "General"); (c) supply or approve cover art.

## 5. Task checklist

- [x] Explore repo; document deck format, manifest schema, v2 compile path, markdown subset.
      *Acceptance: format section above matches AUTHORING.md and observed mojo/us-states sources.*
- [x] Create `decks/welcome/deck.json` manifest with stable UUID and matching counts.
      *Acceptance: `cardCount`/`topicCount` match content; every card ID in exactly one topic.*
- [x] Author `decks/welcome/cards.json` — 10 cards, v2 markdown, plain-text fallbacks, beginner tone.
      *Acceptance: each card has front/back text + markdown; `code_snippet: null`; teal callouts.*
- [x] Mark the deck clearly as DRAFT-PENDING-REVIEW (folder `README.md`).
      *Acceptance: README warns not to compile/commit/ship before James's review.*
- [x] Validate draft is well-formed with DeckCompiler (no shipping artifact).
      *Acceptance: compiler reports 10 cards / 3 topics, 0 errors; no `.wristdeck` left in repo.*
- [ ] James reviews & approves the 10-card copy (and tone/voice).
      *Acceptance: explicit sign-off from James on the card text.*
- [ ] Resolve deck-identity open question (Welcome vs Learn WristRecall vs new built-in default).
      *Acceptance: James confirms whether these are one deck or separate; plan updated.*
- [ ] Confirm `category` value ("Getting Started" vs "General") and gradient/branding.
      *Acceptance: James picks; deck.json updated if needed.*
- [ ] Create/supply 1024×1024 cover image `assets/welcome_deck.jpg`.
      *Acceptance: file present; recognizable at ~100px tile.*
- [ ] After approval: compile shipping `.wristdeck` and wire as the app's default deck.
      *Acceptance: `./tools/compile.sh welcome` succeeds; default-deck integration tracked separately.*

Checklist: **5 / 10 done.**
