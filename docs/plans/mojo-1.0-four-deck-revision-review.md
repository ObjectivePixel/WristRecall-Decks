# Adversarial review — Mojo 1.0 four-deck revision specification

Reviewed: `docs/plans/mojo-1.0-four-deck-revision.md` and `docs/plans/mojo-1.0-source-card-matrix.csv` on branch `agent/mojo-1-0-four-deck-spec` (commit 27930c6), against `main` at 95eb616.

Verdict: **the ledger's technical content checks out against the shipped 1.0 documentation; the execution plan around it does not yet.** Every claim I was able to verify against the real v1.0.0 release notes was accurate, which is the hard part and the part most likely to be wrong. The problems are structural: one of the five normative source URLs does not exist, experimental features are treated as durable, several ledger items are scoped too narrowly, and the plan has no answer for validation, deck identity, or the beta-era deck it supersedes.

## How this review was grounded, and the limits of that

Claims below were checked against the published Mojo v1.0.0 release notes and manual rather than against prior knowledge of Mojo, which predates the 1.0 renames and would be actively misleading here.

One caveat on method, which is itself finding B1: **direct HTTP access to every documentation host is refused by this environment's egress policy.** Verified:

```
https://mojolang.org/releases/v1.0.0/          -> 403 CONNECT (policy denial)
https://mojolang.org/docs/manual/              -> 403 CONNECT (policy denial)
https://docs.modular.com/mojo/changelog/       -> 403 CONNECT (policy denial)
https://max.modular.com/gpu/intro-tutorial/    -> 403 CONNECT (policy denial)
```

`WebFetch` returns `EGRESS_BLOCKED` for the same hosts. Web *search* does reach the content and is what grounded this review — but it returns summaries and quoted fragments, not page text. That is adequate for checking discrete claims ("did `InlineArray` become `Array`?"); it is not adequate for authoring ~400 API-precise cards, which requires reading signatures, parameter names and examples off the reference pages.

## Verified accurate

Checked directly against the v1.0.0 release notes and manual. Every one held:

| Ledger claim | Status |
|---|---|
| Lambda expressions: typed parenthesized params, single-expression body, desugars to a nested `def` | Confirmed — `lambda (x: Int) {} -> Int: x + 1` |
| Omitted lambda return type defaults to `None` | Confirmed |
| Omitted capture list `imm`-captures free variables; capture-free lambda is `thin` | Confirmed |
| Capturing lambda is a runtime closure instance with no function type | Confirmed |
| List expressions construct `Array`, not `List` | Confirmed — motivated by removing implicit heap allocation |
| `InlineArray` → `Array` | Confirmed |
| `StringSlice` → `StringSpan` | Confirmed |
| `ImplicitlyDestructible` → `Deinitable`, destructor spelled `__deinit__()` | Confirmed |
| `read` → `imm` | Confirmed (`read` still compiles; deprecation is signalled, not yet applied) |
| Bare `**kwargs` must be spelled `var **kwargs` | Confirmed |
| Keyword variadics forwardable with Python-style `**` | Confirmed |
| `Int` is an alias for `Scalar[DType.int]`; `range()` unified into one dtype-parameterized family | Confirmed |
| `abi("C")` as a function effect for the C calling convention | Confirmed |
| Structs are `Movable` by default; `Movable where <cond>`; `Movable where False` opt-out | Confirmed |
| Type refinement from `where` clauses, `comptime if`, `comptime assert`, driven by `conforms_to()` | Confirmed |
| `mojo package` → `mojo precompile`; `.mojopkg` deprecated in favour of `.mojoc` | Confirmed |
| Import resolution order: source packages → `.mojoc` → source modules → legacy `.mojopkg` | Confirmed |
| Most GPU APIs rehomed from `std.gpu` to `max.gpu`; `layout` bundled with MAX | Confirmed |
| Initial stable API set with per-API stability markings | Confirmed |

That is a strong result for the part of the plan that is hardest to get right. The lambda cluster in particular — ten enumerated cards, including two claims specific enough to be falsifiable — is correct in every detail I could check. The rest of this review should be read against that: the ledger is substantially sound, and the fixes below are mostly structural.

## Blocking

### B1. Documentation hosts are unreachable from the authoring environment

Per the transcript above, `mojolang.org`, `docs.modular.com` and `max.modular.com` all return proxy 403s. Gate 4 ("every card cites or can be traced to final Mojo/MAX documentation during authoring") therefore cannot be executed as written from this environment; searching gets you paraphrases, not the `std` reference pages you need for exact signatures.

Fix: widen the egress allowlist for `mojolang.org` and `docs.modular.com`, or vendor dated snapshots of the release notes and the relevant manual/reference pages into `docs/sources/` and make those normative. The second is better regardless, because it makes the ledger auditable a year from now, when the live pages have moved on.

### B2. One of the five normative sources does not appear to exist

The spec names `https://max.modular.com/gpu/intro-tutorial/` as the GPU source. That host appears in no search result for any Modular documentation. The actual pages are:

- Get started with GPU programming — `https://docs.modular.com/mojo/manual/gpu/intro-tutorial/`
- Intro to GPUs / architecture — `https://docs.modular.com/gpu/architecture/`
- GPU programming fundamentals — `https://docs.modular.com/mojo/manual/gpu/fundamentals/` (also at `https://mojolang.org/docs/manual/gpu/fundamentals/`)

This matters more than a typo: the GPU deck is 60–75 greenfield cards with zero source rows, and its only cited source is a URL that was never opened. Correct the URL, and pin the MAX version — **MAX v26.5** is the release paired with Mojo 1.0 — instead of citing a "current" guide, which contradicts the spec's own "only final-state sources are normative" invariant.

### B3. Validation gate 8 cannot run outside one machine

`tools/DeckCompiler` is `Mach-O 64-bit arm64` — macOS on Apple Silicon only. There is no `.github/` directory and no CI. So "each new deck passes the repository compiler's count/topic/format validation" is a manual gate only the maintainer's laptop can execute, while ~400 cards get authored and committed with nothing checking that `cardCount` matches, that every card ID lands in exactly one topic, or that the JSON parses.

Fix: add a portable checker (~100 lines of Python) for manifest/content consistency, ID uniqueness, topic partitioning and the gate-9 spelling scan, and wire it to CI. Keep DeckCompiler as the final packaging gate, not the only gate.

### B4. Deck IDs bake the language version in

`mojo-1-0-fundamentals`, `mojo-1-0-advanced`, `mojo-1-0-libraries-tools`. The deck ID is the folder name and the release-tag prefix, paired with a UUID that AUTHORING.md says must never change between releases. Mojo 1.1 nightlies are already shipping. At 1.1 you get either a permanently wrong ID or a new ID and UUID, which the app treats as a different deck — user progress does not follow.

The repo already solves this: `mojo-language` carries `"version": "1.1.2"` and puts the language version in the description. Do the same — `mojo-fundamentals`, `mojo-advanced`, `mojo-libraries`, `mojo-gpu`.

Related: `mojo-gpu-max` breaks the family, and "GPU Programming with Mojo & MAX" neither reads nor sorts as a sibling of three "Mojo 1.0 …" decks.

### B5. No retirement plan for the deck this replaces

The spec freezes `decks/mojo-language` as read-only and never says what happens to the *published* deck, which is listed in the README catalog with a live download link. Its content is exactly what the new decks exist to correct:

| Stale spelling | Occurrences in shipped `mojophrases.json` |
|---|---:|
| `UnsafePointer` | 92 |
| `read` (convention keyword, plus English false positives) | 73 |
| `__del__` | 36 |
| `@parameter` | 13 |
| `.mojopkg` | 12 |
| `CollectionElement` | 12 |
| `mojo package` | 10 |
| `StringSlice` | 8 |
| `InlineArray` | 6 |
| `ImplicitlyDestructible` | 2 |

Gate 5 forbids teaching a deprecated spelling as the preferred final API — but binds only the new decks. Ship as written and the catalog offers both the wrong and the right API at once, with the wrong one holding the most discoverable name ("Mojo Language") and five releases of history. Decide in this spec: unlist, rename to "Mojo Language (1.0 beta — archived)", or supersede in place by reusing the ID/UUID for Fundamentals so existing installs upgrade rather than fork.

## Substantive

### S1. Experimental features are treated as durable, and the spec has no policy for them

**Interior origins are experimental in 1.0.** The release notes introduce them as "a new experimental feature," and they are not in the initial stable API set. The spec gives them three ledger rows — "Interior origins" (Card cluster, Advanced/Ownership), "Interior origins across collections and buffers" (Card cluster, Advanced/Origins), and interior coverage inside the ownership topic list — with no caveat anywhere.

The spec has a rule for deprecated spellings (gate 5) and none for experimental ones, even though it separately plans a card on "per-API stability markings," so it knows the stability tiers exist. Under a 1.x policy that is "primarily additive" but explicitly reserves the right to break, an experimental feature is the single most likely thing in the suite to be wrong within a year — and flashcards are the worst medium for content that changes, because users memorise them. Add a rule: experimental and unstable APIs are either excluded, or carried with an explicit marker in the card.

### S2. The Adapt/Rewrite split is not trustworthy — now confirmed, not just suspected

122 of 180 rows (68%) carry a byte-identical rationale: *"Reuse the durable concept, re-authoring all wording and examples against final 1.0 documentation."* All are Adapt. So for two-thirds of the corpus the matrix asserts "no semantic conflict with 1.0" and records no evidence — the rationale column carries zero information exactly where it matters, because Adapt is the classification meaning *nobody needs to look at this again*.

Checking Adapt rows against the verified 1.0 changes rather than against the spec's own ledger, the misclassifications are confirmed:

| Row(s) | Source prompt, marked Adapt | Verified 1.0 change it collides with |
|---|---|---|
| #11, #36, #85, #127, #128 | Importing native modules; importing local Python files; custom modules; `__init__.mojo` packages; import aliases | `mojo package` → `mojo precompile`; `.mojopkg` → `.mojoc`; a new four-step import resolution order |
| #74 | "Auto-generate copy and move constructors for a struct" | Structs are now `Movable` by default; opt-out is `Movable where False` |
| #38 | "Find the optimal SIMD vector width at compile time" | `size` → `length` throughout; `SIMDLength` added |
| #174 | "Iterate a `List` mutably or consume it" | Interior origins: element references are invalidated by `append`/`pop`, and the lifetime checker now rejects holding one across a mutation |
| #173 | "Chain operations on an `Optional` without unwrapping" | `Optional` is `Iterable`, not `Iterator`; linear `map`/`and_then` |
| #144, #152 | Set creation; trait required for `Dict` key / `Set` element | `ImplicitlyDestructible` → `Deinitable`; linear-safe `Dict`/`Set` |
| #30, #41, #58, #62 | String vs literal; native formatting; TString; custom string representation | `StringSlice` → `StringSpan`; grapheme-cluster iteration; removed positional `StringLiteral` indexing; removed static `String.write()` |
| #114 | "Can you copy an `OwnedPointer`?" | `OwnedPointer.into_inner()` and the `as_imm()` family renames |
| #180 | "Control the alignment of a struct" | `size_of()` now returns aligned allocation size |

That is ~15–20 rows where Adapt understates the work, so the headline "51 rewrites" is low by a third or more. The five import/packaging rows are the clearest: the command, the file extension, and the resolution order all changed, and all five cards are marked as needing nothing but re-wording.

Fix: add an evidence column (source URL + anchor, plus either "changed: X" or "confirmed unchanged"), forbid boilerplate rationales, and re-run the classification against the release-note change list.

### S3. `size` → `length` is scoped far too narrowly

The ledger has one row: "`SIMD` `size` parameter renamed `length` | Audit | Advanced / SIMD". The release notes describe it as **"size becomes length throughout,"** part of a deliberate "one name, and one type, per concept" consolidation. It reaches `Array`, `Span` and the collections — i.e. Fundamentals cards, not just the Advanced SIMD topic. Re-scope it as a suite-wide audit.

While there: "one name, one type per concept" is the organizing principle behind half the renames in this release and is itself a durable, highly teachable card. The spec never states it.

### S4. The official migration mechanism is missing entirely

The release notes are explicit that "nearly every breaking change ships with a deprecated alias and a compiler fix-it, so migration is mechanical." The spec contains zero mentions of deprecated aliases, fix-its, or the 1.x stability policy (`grep -ic` returns 0 for each).

Two consequences. First, this is durable, high-value content for the Libraries/Tools deck — the mechanism by which a reader upgrades their own beta-era code — and it is exactly the audience this suite is being written for. Second, it undercuts gate 9's implicit safety net: because the old spellings still *compile*, a card that teaches `read` or `.mojopkg` produces working code and will never be caught by anything except that grep. That makes B3's automated checker load-bearing rather than nice-to-have.

### S5. Interior origins are specified as a mechanism, never as the rule a learner hits

The three ledger rows name the type-system machinery ("origin inference/unions/interiors"). The observable 1.0 behaviour is concrete and far more teachable: `List` returns element references bound to an interior origin, so `append()` or `pop()` invalidates them, and the lifetime checker rejects code holding an element reference across the mutation instead of letting it dangle after a reallocation. That failure — hit while writing an ordinary loop — is the card. The mechanism is the second card, not the first.

### S6. The `where False` fix looks mischaracterized

The spec describes it twice as "the final 1.0 fix ensuring a `where False` opt-out is respected inside generic functions." The release notes describe the fix as: a struct using `where False` to opt out of a builtin trait's implicit synthesis no longer spuriously fails to compile **when one of its fields also opts out of that same trait**. Those are different situations. Re-check against the release-note text before this becomes a card; a flashcard that states the wrong precondition is worse than no card.

### S7. The card-count arithmetic does not reconcile in any of the four decks

| Deck | Sum of topic ranges | Stated | Delta |
|---|---|---|---|
| Fundamentals | 102–122 | 105–120 | −3 / +2 |
| Advanced | 112–138 | 115–135 | −3 / +3 |
| Libraries | 71–95 | 75–90 | −4 / +5 |
| GPU | 60–77 | 60–75 | 0 / +2 |
| **Suite** | **345–432** | **355–420** | **−10 / +12** |

Counts are explicitly "planning ranges, not quotas," which limits the harm — but they are also the only deck-level acceptance signal in the document. Derive the deck ranges from the topic ranges, or drop them.

### S8. The ledger and the blueprint use different topic taxonomies

The blueprint freezes 27 topics (7 + 7 + 7 + 6). The ledger routes items to roughly 49 distinct `Deck / Topic` labels, most of which are not topics:

- No counterpart in the blueprint: *Fundamentals / Identifiers*, *Fundamentals / Syntax*, *Advanced / Constraints*, *Advanced / Generics*, *Advanced / Address spaces*, *Advanced / Allocation*, *Advanced / Function values*, *Advanced / Numeric types*, *Advanced / Low-level types*, *Libraries / Stability*, *Libraries / Span*, *Libraries / Iteration*, *Libraries / Linear values*, *Libraries / Linear collections*, *Libraries / Variant*, *Libraries / Compilation*, *Libraries / Benchmarking*, *Libraries / Packaging*.
- Aliases for one topic: *Advanced / Closures* vs *Closures and lambdas*; *Ownership* vs *Ownership and origins* vs *Origins* vs *Origins and pointers*; *Python from Mojo* vs *Python interop*; *Traits* vs *Traits and lifecycle*.
- One item routed to two decks at once: "`Int` aliases `Scalar[DType.int]`" → *Fundamentals/Advanced numeric topics*.

`deck.json` requires `topicDefinitions` to place every card ID in exactly one named topic, so this is rework at manifest-assembly time and it defeats any check of per-topic budgets against the ledger. Freeze the 27 names first, then rewrite every destination to use one of them.

### S9. A coverage hole the ledger conceals: `math` has no home topic

Rows #47 and #153 merge into "one curated math-surface card" destined for the Libraries deck, whose seven topics contain no math bucket (nearest is "I/O, system, and measurement", a stretch for `sqrt`/`max`). Add the topic or state that the math surface is deliberately dropped.

### S10. Merge semantics are underspecified; omitted rows carry a destination

Of five Merge rows, four form two clean pairs (#47+#153, #50+#104) with the partner named in prose. The fifth, #103 (modulo for wrap-around indexing), names no partner — "fold into durable operators/indexing coverage" is an absorb-and-drop, not a merge. There is no merge-group column, so pairings live only in free text and no script can verify both halves landed in one card.

Separately, `Omit` rows #83 and #181 still list "Mojo 1.0 Fundamentals" as `destination_deck`, so any per-deck tally computed from the CSV over-counts Fundamentals by two. Use an empty destination.

### S11. Prerequisites have nowhere to live

The Outputs table assigns prerequisites ("Fundamentals; Advanced recommended for FFI"). No manifest in the repo has an ordering or prerequisite field — across all six decks the keys are `id`, `uuid`, `name`, `description`, `storeFileName`, `imageName`, `gradientColors`, `cardCount`, `topicCount`, `category`, `version`, `sourceFileName`, `topicDefinitions`, plus optional `moreInfoURL` / `aboutURL`. The chain will be a sentence inside `description`, which AUTHORING.md calls "a short one-liner shown in the deck browser." Say how it is expressed, or drop it.

### S12. No policy on cross-deck duplication

Four decks install independently. `Array` alone is scheduled in Fundamentals/Collections (list-expression default, `InlineArray` rename, slice aborts), Advanced/Lifecycle (no longer `ImplicitlyCopyable` or `Defaultable`), Libraries/Stability, and Libraries/Linear values (non-`Movable` elements). A user who installs only Libraries never sees the Fundamentals framing those cards assume. State which concepts may be restated across decks, in what framing, and which must not be.

### S13. This is framed as a revision; it is mostly new authoring

180 source concepts, minus 2 omitted, minus ~3 net lost to merges ≈ 175 carried, against a target of 355–420. That is 180–245 net-new cards — and since even "Adapt" gets newly authored wording and examples, all 175 carried concepts are rewritten too. Effectively ~400 cards written from scratch, against documentation that (per B1) cannot currently be opened directly.

No effort estimate, no per-deck definition of done, and no statement that the decks ship independently. Add one: Fundamentals is authored, validated, released and listed in the README *before* Advanced starts. Four decks landing together is a much worse failure mode than one deck landing four times.

### S14. Renderer constraints are absent

The watch renderer has no syntax highlighting (AUTHORING.md: language identifiers "are currently ignored"), and the existing Mojo deck sets the envelope: back-markdown median 270 characters, p90 651, max 1627; 99% of cards carry a code fence; longest code line 77 characters.

The plan's two densest clusters resist this format — Advanced/Pointers at 28–34 cards (pointer vs pointee state, `Layout`, `Allocation`, `ThinAllocation`, origin unions and interiors) and GPU/Layouts at 14–18 cards (shape/stride mapping, coordinate mapping, tiled layouts, `TileTensor` views). Layout algebra is inherently diagrammatic, and there is no guidance on expressing it in ~650 characters of unhighlighted markdown on a 41mm screen. Add hard budgets — back markdown ≤ 700 characters, code lines ≤ 60 characters, fences ≤ 8 lines — and check them in the B3 script.

### S15. Gate 9's stale-spelling search is not usable as written

Two listed terms are unusable as plain substrings: `read` matches 73 times in the source deck, nearly all the English word, and `@parameter` (13) will match legitimate replacement guidance. `String`, `Span` and `List` fragments will match dozens of correct 1.0 identifiers. A gate with a ~90% false-positive rate gets waved through on its second run. Specify word-boundary regexes scoped to code fences and inline-code spans, run by the B3 script rather than by a human with `grep`.

### S16. Nothing about actually shipping

The "next implementation phase" ends at "compile and validate." AUTHORING.md's flow does not: four 1024×1024 cover JPGs, `gradientColors`, `category`, `storeFileName`/`imageName`, deck-browser description copy, starting `version`, release tags `<deck-id>-v<version>`, README catalog rows with download links, and on-device testing. Cover art for four decks is the long-lead item and is unmentioned.

### S17. Catalog composition is being changed as a side effect

The repo ships 6 decks. This adds 4, making 10 — of which 5 are Mojo, and 5 of the 6 Programming-category decks are Mojo. Half the catalog of a general-purpose community deck repo becomes one language. That may be right, but it should be a decision in the spec rather than a consequence of it.

## Minor

- The matrix's `source_id` runs 1–181 across 180 rows because ID 29 is absent — correct, the shipped deck also skips 29. Worth a footnote so nobody "fixes" it.
- Gate 1 ("every one of the 180 source rows has exactly one disposition") is already satisfied by the committed CSV — verified mechanically: 180 rows, exactly the 180 shipped card IDs, no duplicates, and action and destination counts reproducing the summary table (Adapt 122 / Rewrite 51 / Merge 5 / Omit 2; Fundamentals 69 / Advanced 74 / Libraries 37). As a pre-completion gate it is a no-op; move it to the spec's acceptance section.
- Gates 2 and 3 have no artifact to check against. The documentation coverage map is deck/topic-level, not section-level, so "every final manual section maps to at least one topic or an explicit exclusion" cannot be evidenced. Enumerate the manual's sections with a tick per section.
- One ledger row is a deferred decision dressed as a disposition: volatile load behavior, "covered only if a durable volatile-memory card survives authoring review." Gate 2 requires a disposition. Decide it or move it to an open-questions list.
- Because merges collapse 5 concepts into 2–3 cards, "180 source concepts" is not the number of cards carried forward. State the carried figure.
- "Adapt" does double duty as a provenance label and a workload estimate; since every adapted card is fully re-authored, the two meanings diverge.
- `read` still compiles in 1.0 — deprecation is signalled, not applied. Worth a note wherever the ledger says `imm` "replaces" it.

## Recommended changes before authoring starts

1. Fix the GPU source URL to `docs.modular.com/mojo/manual/gpu/intro-tutorial/` and pin MAX v26.5 (B2).
2. Resolve source access (B1) — vendor dated snapshots into `docs/sources/` and cite them per row.
3. Add the portable validator + CI (B3), including a byte-for-byte check that `decks/mojo-language/` is unmodified and the corrected spelling regexes (S15).
4. Drop `1-0` from the deck IDs (B4).
5. Add a "Disposition of the existing Mojo Language deck" section (B5).
6. Add an experimental-API policy and mark interior origins accordingly (S1).
7. Add the evidence column to the CSV and re-classify the ~15–20 suspect Adapt rows, starting with the five import/packaging rows (S2).
8. Re-scope `size` → `length` as a suite-wide audit, and add a card for "one name, one type per concept" (S3).
9. Add the deprecation-alias and compiler fix-it migration story to the Libraries deck (S4).
10. Re-check the `where False` fix wording against the release notes (S6).
11. Freeze the 27 topic names and rewrite every ledger destination to use one of them (S8, S9).
12. Re-derive the count table from the topic ranges (S7).
13. Add card-size budgets, the shipping checklist, and the "Fundamentals ships first, alone" rule (S13, S14, S16).

## Sources

- [Mojo v1.0.0 release notes](https://mojolang.org/releases/v1.0.0/)
- [Modular 26.5: Mojo 1.0 is here!](https://www.modular.com/blog/modular-26-5-mojo-1-0-is-here)
- [Mojo manual — structs](https://mojolang.org/docs/manual/structs/), [parameterization](https://mojolang.org/docs/manual/parameters/), [modules and packages](https://mojolang.org/docs/manual/packages/), [packaging](https://mojolang.org/docs/tools/packaging/)
- [Mojo function declarations reference](https://mojolang.org/docs/reference/function-declarations/)
- [Get started with GPU programming](https://docs.modular.com/mojo/manual/gpu/intro-tutorial/), [Intro to GPUs](https://docs.modular.com/gpu/architecture/), [GPU programming fundamentals](https://docs.modular.com/mojo/manual/gpu/fundamentals/)
- [MAX v26.5 release notes](https://docs.modular.com/releases/v26.5/)
- [Mojo changelog](https://docs.modular.com/mojo/changelog/)
