# WristRecall Decks

Community flashcard decks for [WristRecall](https://apps.apple.com/app/wristrecall/id6742297565). Each deck compiles into a `.wristdeck` package that can be imported through the app's deck browser.

## Available decks

| Deck | Cards | Topics | Category |
|------|-------|--------|----------|
| Mojo Language | 165 | 15 | Programming |
| United States | 100 | 7 | Geography |
| Countries of the World | 60 | 9 | Geography |

## Compiling decks

### All decks

```bash
./tools/compile.sh
```

### A specific deck

```bash
./tools/compile.sh us-states
```

Compiled `.wristdeck` packages are written to `output/`.

### Compiler CLI

The `DeckCompiler` binary can also be used directly:

```bash
# Single deck
./tools/DeckCompiler --standalone --decks-dir ./decks --deck us-states \
    --export-wristdeck --output-dir ./output

# All decks
./tools/DeckCompiler --standalone --decks-dir ./decks \
    --export-wristdeck --output-dir ./output

# Full options
./tools/DeckCompiler --help
```

## Adding a new deck

1. Create a directory under `decks/` named with the deck ID (e.g. `decks/my-topic/`).
2. Add a `deck.json` manifest. Required fields:

   ```json
   {
     "id": "my-topic",
     "uuid": "<generate a UUID>",
     "name": "My Topic",
     "description": "...",
     "storeFileName": "my_topic",
     "imageName": "my_topic_deck",
     "gradientColors": ["#RRGGBBAA", "#RRGGBBAA"],
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

   - `uuid` must be a stable UUID string. Generate one with `uuidgen`.
   - `cardCount` and `topicCount` should match the actual content.
   - `topicDefinitions` maps topic names to card IDs from the source file.

3. Add the source flashcard JSON file (referenced by `sourceFileName`). Cards
   carry both v1 fields (`text`, `code_snippet`) and a v2 `markdown` field —
   the compiler picks the active path via `--format`:

   ```json
   [
     {
       "id": 1,
       "front": {
         "text": "Question?",
         "markdown": "Question?"
       },
       "back": {
         "text": "Answer.",
         "markdown": "## Answer\n\nWith **markdown** support — lists, code fences, and `{#0F766E}colored callouts{/}`.",
         "code_snippet": null,
         "formatting": { "inline_code_terms": [] }
       }
     }
   ]
   ```

4. Optionally add an `assets/` directory with a deck image (referenced by
   `imageName`, e.g. `assets/my_topic_deck.jpg`, 1024×1024 JPG).

5. Run `./tools/compile.sh my-topic` and import the `.wristdeck` from
   `output/`. The script defaults to v2 markdown output; pass `--format v1`
   to compile the legacy text/code-snippet path.

## License

See [LICENSE](LICENSE).
