# WristRecall Decks

Community flashcard decks for **[WristRecall](https://apps.apple.com/app/wristrecall/id6760349779)** — the Apple Watch flashcard app.

> *Learn on your wrist. Remember everywhere.*

WristRecall lets you study any subject in quick, focused sessions right on your Apple Watch. This repository hosts ready-to-import `.wristdeck` files for the community, plus everything you need to author and ship your own decks.

[**Get WristRecall on the App Store →**](https://apps.apple.com/app/wristrecall/id6760349779)

---

<table>
  <tr>
    <td align="center" width="20%"><img src="assets/screenshots/watch_01_deck_list.png" alt="Deck list on Apple Watch" width="180"></td>
    <td align="center" width="20%"><img src="assets/screenshots/watch_03_flashcard_question.png" alt="Flashcard question on Apple Watch" width="180"></td>
    <td align="center" width="20%"><img src="assets/screenshots/watch_04_flashcard_answer.png" alt="Flashcard answer on Apple Watch" width="180"></td>
    <td align="center" width="20%"><img src="assets/screenshots/watch_08_stats_accuracy.png" alt="Accuracy stats on Apple Watch" width="180"></td>
  </tr>
  <tr>
    <td align="center"><sub>Pick a deck</sub></td>
    <td align="center"><sub>Quick-fire questions</sub></td>
    <td align="center"><sub>Tap to reveal</sub></td>
    <td align="center"><sub>Track accuracy</sub></td>
  </tr>
</table>

<p align="center">
  <img src="assets/screenshots/02_deck_browser.jpg" alt="iPhone deck browser" width="240">
  &nbsp;&nbsp;
  <img src="assets/screenshots/09_widget_home.jpg" alt="Home-screen widgets" width="240">
</p>

---

## Install a deck

The decks below ship as `.wristdeck` files. To install one on your watch:

1. **On your iPhone**, tap a deck's **Download** link below. WristRecall registers `.wristdeck` files, so iOS will offer to open the file in WristRecall directly.
2. WristRecall imports the deck and shows it in the **Deck Browser**.
3. **Swipe left** on the deck row → tap **Install on Watch**. The deck syncs to your Apple Watch over WatchConnectivity automatically.

> Don't have WristRecall yet? [Get it on the App Store](https://apps.apple.com/app/wristrecall/id6760349779) first — the `.wristdeck` extension is registered by the app, so the import flow only works once it's installed.

If a tap doesn't open WristRecall, save the file to **Files**, open it from there, and choose **Share → WristRecall**.

---

## Available decks

<table>
  <tr>
    <td width="120" align="center"><img src="decks/mojo-language/assets/mojo_deck.jpg" alt="Mojo Language deck cover" width="100"></td>
    <td>
      <strong>Mojo Language</strong> · 165 cards · 15 topics · Programming<br>
      Core concepts of the <a href="https://docs.modular.com/mojo/">Mojo</a> programming language — functions, value ownership, traits, pointers, metaprogramming, and the standard library.<br>
      <a href="https://github.com/ObjectivePixel/WristRecall-Decks/releases/download/mojo-language-v1.0.8/mojo-language-1.0.8.wristdeck"><strong>Download v1.0.8 ↓</strong></a> · <a href="https://github.com/ObjectivePixel/WristRecall-Decks/releases?q=mojo-language">All versions</a>
    </td>
  </tr>
  <tr>
    <td width="120" align="center"><img src="decks/us-states/assets/us_states_deck.jpg" alt="United States deck cover" width="100"></td>
    <td>
      <strong>United States</strong> · 100 cards · 7 topics · Geography<br>
      States and letters, capitals, and national parks — test your knowledge of the US.<br>
      <a href="https://github.com/ObjectivePixel/WristRecall-Decks/releases/download/us-states-v2.0.2/us-states-2.0.2.wristdeck"><strong>Download v2.0.2 ↓</strong></a> · <a href="https://github.com/ObjectivePixel/WristRecall-Decks/releases?q=us-states">All versions</a>
    </td>
  </tr>
  <tr>
    <td width="120" align="center"><img src="decks/world-countries/assets/world_countries_deck.jpg" alt="Countries of the World deck cover" width="100"></td>
    <td>
      <strong>Countries of the World</strong> · 60 cards · 9 topics · Geography<br>
      How many countries, continents, oceans, and landmasses make up our world — plus capitals and flags from every region.<br>
      <a href="https://github.com/ObjectivePixel/WristRecall-Decks/releases/download/world-countries-v1.0.2/world-countries-1.0.2.wristdeck"><strong>Download v1.0.2 ↓</strong></a> · <a href="https://github.com/ObjectivePixel/WristRecall-Decks/releases?q=world-countries">All versions</a>
    </td>
  </tr>
</table>

Each deck is independently versioned in [Releases](https://github.com/ObjectivePixel/WristRecall-Decks/releases).

---

## Want to make your own deck?

Decks are plain JSON plus an optional cover image. Run the bundled `DeckCompiler` and you get a `.wristdeck` file you can share or PR back to this repo.

See **[AUTHORING.md](AUTHORING.md)** — covers the folder layout, the v2 markdown card format (headings, lists, code fences, color callouts), the compile script, and how to contribute your deck.

## License

[MIT](LICENSE).
