# Authoring a WristRecall deck

This guide walks through everything you need to author and ship a `.wristdeck` package — from folder layout to the v2 markdown card format to publishing a release. If you just want to *install* an existing deck, head back to the [README](README.md#install-a-deck).

## Repository layout

```
decks/
  <deck-id>/
    deck.json            # manifest (required)
    cards.json           # cards (filename matches sourceFileName)
    assets/
      <deck-id>_deck.jpg # 1024×1024 cover image (optional but recommended)
output/                  # compiler writes <deck-id>.wristdeck here (gitignored)
tools/
  DeckCompiler           # binary
  compile.sh             # convenience wrapper
```

Each deck lives in its own folder under `decks/`. The folder name is the deck's `id`.

## 1. Create the deck manifest

Create `decks/<deck-id>/deck.json`:

```json
{
  "id": "my-topic",
  "uuid": "<generate with `uuidgen`>",
  "name": "My Topic",
  "description": "A short one-liner shown in the deck browser.",
  "storeFileName": "my_topic",
  "imageName": "my_topic_deck",
  "gradientColors": ["#1E3A8AFF", "#10A37FCC"],
  "cardCount": 0,
  "topicCount": 0,
  "category": "General",
  "version": "1.0.0",
  "sourceFileName": "cards.json",
  "topicDefinitions": [
    { "name": "Topic Name", "cardIDs": [1, 2, 3] }
  ]
}
```

Field notes:

- **`uuid`** — stable UUID. Generate with `uuidgen`. Don't change this between releases.
- **`storeFileName`** — base filename for the compiled SQLite store inside the package (no extension).
- **`imageName`** — base filename of the cover image in `assets/` (no extension). Compiler looks for `assets/<imageName>.jpg`.
- **`gradientColors`** — two colors as `#RRGGBBAA` hex used for the deck's background gradient in the app.
- **`cardCount` / `topicCount`** — must match the actual content. The compiler will refuse to compile if they're off.
- **`topicDefinitions`** — maps topic display names to lists of card IDs. Every card ID must appear in exactly one topic.
- **`version`** — semver. Bump on every release. Used in the release tag (`<deck-id>-v<version>`).

## 2. Write the cards

Create `decks/<deck-id>/cards.json` (or whatever you set as `sourceFileName`):

```json
[
  {
    "id": 1,
    "front": {
      "text": "What is the capital of France?",
      "markdown": "What is the capital of **France**?"
    },
    "back": {
      "text": "Paris.",
      "markdown": "## Paris 🇫🇷\n\n{#0F766E}The City of Light — home to the Eiffel Tower and the Louvre.{/}",
      "code_snippet": null,
      "formatting": { "inline_code_terms": [] }
    }
  }
]
```

Each card has:

- **`id`** — unique integer, referenced from `topicDefinitions` in the manifest.
- **`front.text`** / **`back.text`** — plain-text fallback used by the v1 compiler path and as the accessibility label. Keep these short and self-contained.
- **`front.markdown`** / **`back.markdown`** — the v2 rich-text format actually rendered in the app (see below).
- **`back.code_snippet`** — legacy v1 field. With v2 markdown, embed code in fences inside `markdown` instead and leave this `null`.
- **`back.formatting.inline_code_terms`** — legacy v1 hint list of identifiers to render as inline code. Empty array is fine for v2.

## 3. The v2 markdown format

The card body supports a small subset of CommonMark plus one custom extension for color.

### Headings

Use `##` for the answer headline. Keep it short — it's the visual anchor.

```markdown
## 195 Countries 🌍
```

### Lists

Both ordered and unordered lists render natively.

```markdown
1. **Africa** — 54 countries
2. **Asia** — 48 countries
3. **Europe** — 44 countries
```

```markdown
- **`var`**: mutable variable
- **`comptime`**: compile-time constant
```

### Bold / italics / inline code

Standard CommonMark. Backticks for inline identifiers, `**bold**` for emphasis, `*italics*` for asides.

```markdown
The legacy `fn` keyword is **deprecated**.
```

### Code fences

Use triple backticks. Language identifiers are optional and currently ignored (no syntax highlighting in the watch renderer).

````markdown
```
def add(a: Int, b: Int) -> Int:
    return a + b
```
````

### Color callouts (custom)

Wrap text in `{#RRGGBB}...{/}` to tint it. Use sparingly — the rendered card has limited screen real estate, so colors carry weight.

```markdown
{#0F766E}**Pointer state and pointee state are independent.**{/}

{#C62828}Any access is **undefined behavior.**{/}
```

Conventions used by the existing decks:

| Color | Hex | Use for |
|-------|-----|---------|
| Teal | `#0F766E` | Context lines, key insights |
| Red  | `#C62828` | Warnings, "deprecated", undefined behavior, common mistakes |
| Blue | `#1A3A6B` | Trivia/aside callouts (US States deck) |

### Emojis

Plain Unicode emojis render fine — flags (🇫🇷), symbols (🌍, 🌊), tech mascots (🐍). The compiled SQLite store is UTF-8.

## 4. Add a cover image

Drop a 1024×1024 JPG at `decks/<deck-id>/assets/<imageName>.jpg`. The compiler bundles it into the `.wristdeck` package. If you skip it, the app falls back to a plain gradient.

The app uses the cover image as the deck's tile in the deck browser, so make sure it's recognizable at small sizes.

## 5. Compile

```bash
./tools/compile.sh <deck-id>
```

The script defaults to v2 markdown output. To compile every deck:

```bash
./tools/compile.sh
```

To force v1 (legacy text/code-snippet) output for testing:

```bash
./tools/compile.sh <deck-id> --format v1
```

The compiled package lands at `output/<deck-id>.wristdeck`.

For ad-hoc invocations you can call the binary directly:

```bash
./tools/DeckCompiler --standalone --decks-dir ./decks --deck <deck-id> \
    --export-wristdeck --output-dir ./output

./tools/DeckCompiler --help   # full options
```

## 6. Test on device

1. Send the `.wristdeck` to your iPhone (AirDrop, iCloud Drive, email — anything that lets you tap it).
2. Open it on iPhone — iOS will offer to open it in WristRecall.
3. WristRecall imports it; verify cards render correctly in the iPhone deck browser.
4. **Swipe left** on the deck → **Install on Watch**. Run a session on the watch and check that headings, lists, code fences, color callouts, and emojis all look right.

If a card looks wrong, edit the JSON, recompile, and re-import (importing the same `uuid` overwrites the existing copy on the device).

## 7. Contribute your deck

If you'd like your deck included in this repo:

1. Fork [`ObjectivePixel/WristRecall-Decks`](https://github.com/ObjectivePixel/WristRecall-Decks).
2. Add your deck under `decks/<your-deck-id>/`.
3. Open a PR. Include a screenshot or two of the deck in WristRecall if you can.
4. Once merged, a new release tag (`<deck-id>-v<version>`) is cut and the README catalog is updated to link to the download.

For deck requests or bug reports on existing decks, [open an issue](https://github.com/ObjectivePixel/WristRecall-Decks/issues).

## Reference: existing decks

Browse the existing decks for working examples of the v2 markdown format:

- [`decks/mojo-language/`](decks/mojo-language/) — programming reference; heavy use of code fences, inline code, and red callouts for UB/deprecation.
- [`decks/us-states/`](decks/us-states/) — short-answer trivia; ordered lists with bold leaders, blue accent callouts.
- [`decks/world-countries/`](decks/world-countries/) — mixed counts/capitals; flag emojis in headings, teal accents, red for tricky answers.
