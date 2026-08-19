# Adversarial review — Mojo 1.0 four-deck revision specification

Reviewed: `docs/plans/mojo-1.0-four-deck-revision.md` and `docs/plans/mojo-1.0-source-card-matrix.csv` on branch `agent/mojo-1-0-four-deck-spec` (commit 27930c6), against `main` at 95eb616.

Verdict: **the disposition work is sound; the execution plan is not yet executable.** The 180-row matrix is arithmetically clean and the deck split is well argued, but four issues block authoring (unreachable sources, unrunnable validation, version-locked deck IDs, no retirement plan for the deck this supersedes), and the traceability ledger uses a topic taxonomy that does not match the blueprint it is supposed to feed.

## What holds up

Stated so the criticism below is read in proportion:

- The CSV is internally consistent and was checked mechanically: 180 rows, covering exactly the 180 card IDs shipped in `decks/mojo-language/mojophrases.json`, one disposition each, no duplicates, no gaps. The action and destination counts reproduce the spec's summary table exactly (Adapt 122 / Rewrite 51 / Merge 5 / Omit 2; Fundamentals 69 / Advanced 74 / Libraries 37 / GPU 0).
- The four-way split is defensible and the prerequisite chain is coherent. Fundamentals-without-systems-knowledge is the right cut line.
- "Beta changelogs are not migration targets; new cards teach the final 1.0 state, not the sequence of changes" is the correct invariant, and it is applied consistently.
- The lambda cluster (10 enumerated cards) and the conditional-conformance list are specified at a level you can actually author against. They are the model the rest of the plan should follow, and mostly does not.
- Explicit exclusions with reasons (telemetry defaults, LSP behavior, narrow additive APIs like `List.capacity()`) are good discipline.
- Source deck read-only, new IDs and UUIDs — correct, and it protects installed users from an overwrite.

## Blocking

### B1. Every normative source is unreachable from the environment that will author the cards

The spec names five normative sources. All are blocked by this session's network egress policy:

```
https://mojolang.org/releases/v1.0.0/     -> 403 CONNECT (policy denial)
https://mojolang.org/docs/manual/         -> 403 CONNECT (policy denial)
https://max.modular.com/gpu/intro-tutorial/ -> 403 CONNECT (policy denial)
```

Both `curl` and `WebFetch` are refused. That makes gate 4 ("every card cites or can be traced to final Mojo/MAX documentation during authoring") unexecutable here, and it means the ~90 release-note claims in the traceability ledger are, right now, unverifiable assertions. The ledger is the load-bearing artifact of the entire plan — if a single ledger row is wrong, every card downstream of it teaches a wrong API with full confidence.

Fix one of: widen the egress allowlist for `mojolang.org` and `max.modular.com`; or vendor dated snapshots of the release notes and the relevant manual/reference pages into `docs/sources/` and make *those* the normative artifact, with the fetch date recorded. The second option is better regardless — it makes the ledger auditable by a reviewer a year from now.

### B2. Validation gate 8 cannot run outside one machine

`tools/DeckCompiler` is `Mach-O 64-bit arm64` — macOS on Apple Silicon only. There is no `.github/` directory and no CI of any kind. So "each new deck passes the repository compiler's count/topic/format validation" is a manual gate that only the maintainer's laptop can execute. Four decks and ~400 cards will be authored, reviewed and committed with no automated check that `cardCount` matches, that `topicCount` matches, that every card ID appears in exactly one topic, or that the JSON parses.

Fix: add a portable checker (a ~100-line Python script is enough) covering manifest/content consistency, ID uniqueness, topic partitioning, and the gate-9 stale-spelling scan, and wire it to CI. Keep DeckCompiler as the final packaging gate, not the only gate.

### B3. Deck IDs bake the language version in

`mojo-1-0-fundamentals`, `mojo-1-0-advanced`, `mojo-1-0-libraries-tools`. The deck ID is the folder name, the release-tag prefix (`<deck-id>-v<version>`), and is paired with a UUID that AUTHORING.md says must never change between releases. When Mojo 1.1 or 2.0 ships you get one of two bad outcomes: keep the ID and it is permanently wrong, or mint a new ID and UUID, which the app treats as a different deck — the user's existing progress does not follow.

The repo's own convention already solves this: `mojo-language` carries `"version": "1.1.2"` in the manifest and puts the language version in the *description* ("Core concepts of the Mojo programming language (v1.0.0b1, May 2026)"). Do the same — `mojo-fundamentals`, `mojo-advanced`, `mojo-libraries`, `mojo-gpu` — and let `name`, `description` and `version` carry the 1.0.

Related: `mojo-gpu-max` breaks the naming family, and "GPU Programming with Mojo & MAX" does not read or sort as a sibling of three "Mojo 1.0 …" decks.

### B4. There is no retirement plan for the deck this replaces

The spec freezes `decks/mojo-language` as read-only and never says what happens to the *published* deck. It is currently listed in the README catalog with a live download link, and its content is exactly what the new decks exist to correct:

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

Gate 5 forbids teaching a deprecated spelling as the preferred final API — but it binds only the new decks. Ship the plan as written and the catalog offers both the wrong and the right API simultaneously, with the wrong one holding the most discoverable name ("Mojo Language") and a five-release track record. A user searching the catalog for "Mojo" gets five decks and no signal about which is current.

Decide now, in this spec: unlist it, rename it to something like "Mojo Language (1.0 beta — archived)", or supersede it in place by reusing its ID/UUID for Fundamentals so existing installs upgrade rather than fork.

## Substantive

### S1. The card-count arithmetic does not reconcile in any of the four decks

Summing each blueprint's per-topic ranges against the range stated in the Outputs table:

| Deck | Sum of topic ranges | Stated | Delta |
|---|---|---|---|
| Fundamentals | 102–122 | 105–120 | −3 / +2 |
| Advanced | 112–138 | 115–135 | −3 / +3 |
| Libraries | 71–95 | 75–90 | −4 / +5 |
| GPU | 60–77 | 60–75 | 0 / +2 |
| **Suite** | **345–432** | **355–420** | **−10 / +12** |

The spec says counts are "planning ranges, not quotas," which limits the damage — but they are also the only deck-level acceptance signal in the document, and they do not add up. Either derive the deck ranges from the topic ranges or drop the deck-level numbers.

### S2. The Adapt/Rewrite split is not trustworthy

122 of 180 rows (68%) carry a byte-identical rationale: *"Reuse the durable concept, re-authoring all wording and examples against final 1.0 documentation."* Every one of them is an Adapt. So for two-thirds of the corpus the matrix asserts "no semantic conflict with 1.0" and records no evidence for that claim — the rationale column carries zero information exactly where it matters most, because Adapt is the classification that means *nobody needs to look closely at this one*.

Spot-checking Adapt rows against the plan's own ledger finds rows sitting directly on top of changes the ledger itself grades as Card- or audit-level:

| Row | Source prompt (Adapt) | Ledger item it collides with |
|---|---|---|
| #74 | "How do you auto-generate copy and move constructors for a struct?" | "Structs are `Movable` by default; conditional and `where False` opt-out" — Card cluster |
| #180 | "How do you control the alignment of a struct?" | "`size_of()` returns aligned allocation size" — Card; plus the reflection field-offset fix |
| #174 | "How do you iterate a `List` mutably or consume it?" | "Owned iteration no longer requires `Copyable`" — Card; interior origins across collections |
| #173 | "How do you chain operations on an `Optional` without unwrapping it?" | "`Optional` is `Iterable`, not `Iterator`" — Card; linear `map`/`and_then` |
| #38 | "How do you find the optimal SIMD vector width…?" | "`SIMD` `size` parameter renamed `length`" — audit; `SIMDLength` — Card |
| #144, #152 | Set creation; trait required for `Dict` key / `Set` element | "Linear-safe `Dict`/`Set` insertion and clearing" — Card cluster; `Deinitable` rename |
| #114 | "Can you copy an `OwnedPointer`? How do you transfer ownership?" | "`OwnedPointer.into_inner()` … renames" — cluster/audit |
| #11, #36, #85, #127, #128 | Importing modules; custom modules; `__init__.mojo` packages; import aliases | "Explicit import resolution, relative imports, re-exports and search order" — Card cluster; `.mojopkg` / `mojo package` are on the gate-9 stale list |
| #30, #41, #58, #62 | String vs literal; native string formatting; TString; custom string representation | `StringSlice`→`StringSpan`; grapheme-cluster iteration; removed positional `StringLiteral` indexing; removed static `String.write()` |

That is roughly 15–20 rows where "Adapt" understates the work, which means the headline "51 rewrites" is low by a third or more. The five package/import rows are the clearest case: the packaging workflow changed enough that `.mojopkg` and `mojo package` are on the plan's own stale-spelling blocklist, yet all five source cards are marked as needing nothing but re-wording.

Fix: add an evidence column (source URL + anchor, and either "changed: X" or "confirmed unchanged"), forbid boilerplate rationales, and re-run the classification with the ledger's change list as a mechanical cross-check.

### S3. The ledger and the blueprint use different topic taxonomies

The blueprint freezes 27 topics (7 + 7 + 7 + 6). The traceability ledger routes items to roughly 49 distinct `Deck / Topic` labels, most of which are not topics:

- No counterpart in the blueprint: *Fundamentals / Identifiers*, *Fundamentals / Syntax*, *Advanced / Constraints*, *Advanced / Generics*, *Advanced / Address spaces*, *Advanced / Allocation*, *Advanced / Function values*, *Advanced / Numeric types*, *Advanced / Low-level types*, *Libraries / Stability*, *Libraries / Span*, *Libraries / Iteration*, *Libraries / Linear values*, *Libraries / Linear collections*, *Libraries / Variant*, *Libraries / Compilation*, *Libraries / Benchmarking*, *Libraries / Packaging*.
- Multiple aliases for one topic: *Advanced / Closures* vs *Advanced / Closures and lambdas*; *Advanced / Ownership* vs *Ownership and origins* vs *Origins* vs *Origins and pointers*; *Libraries / Python from Mojo* vs *Libraries / Python interop*; *Advanced / Traits* vs *Traits and lifecycle*.
- One item is routed to two decks at once: "`Int` aliases `Scalar[DType.int]` and stricter conversions" → *Fundamentals/Advanced numeric topics*.

`deck.json` requires `topicDefinitions` to place every card ID in exactly one named topic, so this ambiguity is not cosmetic — it becomes rework at manifest-assembly time, and it defeats any attempt to check per-topic card budgets against the ledger. Freeze the 27 names first (the spec's own step 1 of the next phase), then rewrite every ledger destination to use exactly one of them.

### S4. A coverage hole the ledger conceals: `math` has no home topic

Rows #47 and #153 merge into "one curated math-surface card" destined for the Libraries deck — whose seven topics are Stable library surface, Collections/iterators/text, Python from Mojo, Mojo from Python, C FFI and runtime, Compilation/packaging/tools, and I/O/system/measurement. None of them is a math bucket. The nearest fit ("I/O, system, and measurement") is a stretch for `sqrt`/`max`. Either add the topic or state that the math surface is deliberately dropped.

### S5. Merge semantics are underspecified

Of the five Merge rows, four form two clean pairs (#47+#153, #50+#104) with the partner named in prose. The fifth, #103 ("modulo operator for toroidal indexing"), names no partner — "fold the modulo example into durable operators/indexing coverage" is an absorb-and-drop, not a merge. The CSV has no merge-group column, so the pairing exists only in free text and no script can verify that both halves of a pair actually landed in one card.

### S6. Omitted rows still carry a destination deck

#83 and #181 are `Omit` but list "Mojo 1.0 Fundamentals" as `destination_deck`. Harmless in prose, but it means the column has two meanings, and any tally of source concepts per deck computed from the CSV over-counts Fundamentals by two. Use an empty destination, or a `—`.

### S7. Prerequisites have nowhere to live

The Outputs table assigns prerequisites ("Fundamentals; Advanced recommended for FFI"). No manifest in the repo has any ordering or prerequisite field — across all six decks the keys are `id`, `uuid`, `name`, `description`, `storeFileName`, `imageName`, `gradientColors`, `cardCount`, `topicCount`, `category`, `version`, `sourceFileName`, `topicDefinitions`, plus optional `moreInfoURL` / `aboutURL`. So the prerequisite chain will be a sentence inside `description`, which AUTHORING.md describes as "a short one-liner shown in the deck browser." Say explicitly how it is expressed, or drop it.

### S8. No policy on cross-deck duplication

Four decks install independently. `Array` alone is scheduled in Fundamentals/Collections (list expressions default to `Array`; `InlineArray` rename; slice aborts and negative indices), Advanced/Lifecycle (no longer `ImplicitlyCopyable` or `Defaultable`), Libraries/Stability, and Libraries/Linear values (non-`Movable` elements). A user who installs only Libraries never sees the Fundamentals framing the Libraries cards assume. The spec needs an explicit rule — which concepts may be restated across decks, in what framing, and which must not be.

### S9. The GPU deck violates the spec's own source invariant, and is the riskiest quarter

"Only final-state sources are normative" — but the fifth normative source is the *current* MAX GPU developer guide: unversioned, and on a release cadence independent of Mojo 1.0. This is also the deck with zero source rows, 60–75 greenfield cards, the fastest-moving API surface in the project, and the boldest unverified claim in the document ("host/runtime GPU APIs are in `max.gpu`, low-level primitives remain in `std.gpu` where documented, and `layout` ships with MAX"). Highest risk, thinnest evidence, no mitigation. Pin a MAX version in the deck description, author it last, and consider splitting it into its own project so it can version on MAX's cadence rather than Mojo's.

### S10. One ledger row is a deferred decision dressed as a disposition

"Volatile load behavior — *Covered only if a durable volatile-memory card survives authoring review.*" Gate 2 requires every relevant release-note entry to have a disposition. This one has a conditional. Decide it, or move it to an explicit open-questions list.

### S11. The gate-9 stale-spelling search is not usable as written

Two of the listed terms are unusable as plain substrings: `read` matches 73 times in the source deck, nearly all of them the English word, and `@parameter` (13) will match legitimate replacement guidance. `String`, `Span` and `List` fragments will match dozens of correct 1.0 identifiers. A gate with a ~90% false-positive rate gets waved through on its second run. Specify word-boundary regexes, scoped to code fences and inline-code spans, executed by the script from B2 rather than by a human running `grep`.

### S12. This is framed as a revision; it is mostly a new authoring project

180 source concepts, minus 2 omitted, minus ~3 net lost to merges ≈ 175 carried. Target is 355–420. That is 180–245 net-new cards — and the spec is explicit that even "Adapt" gets newly authored wording and examples, so all 175 carried concepts are rewritten too. In practice: ~400 cards written from scratch, against documentation that (per B1) cannot currently be opened.

There is no effort estimate, no per-deck definition of done, and no statement that the decks ship independently. Add one: Fundamentals is authored, validated, released and listed in the README *before* Advanced starts. Four decks landing together is a much worse failure mode than one deck landing four times.

### S13. Renderer constraints are absent

The watch renderer has no syntax highlighting (AUTHORING.md: language identifiers "are currently ignored"), and the existing Mojo deck sets the practical envelope: back-markdown median 270 characters, p90 651, max 1627; 99% of cards carry a code fence; the longest code line is 77 characters.

The plan's two densest clusters are exactly the ones that resist this format — Advanced/Pointers at 28–34 cards (pointer vs pointee state, `Layout`, `Allocation`, `ThinAllocation`, origin unions and interiors) and GPU/Layouts at 14–18 cards (shape/stride mapping, coordinate mapping, tiled layouts, `TileTensor` views). Layout algebra is inherently diagrammatic and there is no guidance on rendering it in ~650 characters of unhighlighted markdown on a 41mm screen. Add hard budgets to the gates — e.g. back markdown ≤ 700 characters, code lines ≤ 60 characters, fences ≤ 8 lines — and check them in the B2 script.

### S14. Nothing about actually shipping

The "next implementation phase" ends at "compile and validate." AUTHORING.md's flow does not: four 1024×1024 cover JPGs, `gradientColors`, `category`, `storeFileName`/`imageName`, deck-browser description copy, starting `version`, release tags `<deck-id>-v<version>`, README catalog rows with download links, and device testing on watch. Cover art for four decks is the long-lead item and is not mentioned anywhere.

### S15. Catalog composition is being changed as a side effect

The repo ships 6 decks. This adds 4, making 10 — of which 5 are Mojo, and 5 of the 6 Programming-category decks are Mojo. Half the catalog of a general-purpose community deck repo becomes one language. That may well be the right call, but it should be a decision in the spec rather than a consequence of it.

## Minor

- The matrix's `source_id` runs 1–181 across 180 rows because ID 29 is absent — which is correct, the shipped deck also skips 29. Worth a footnote so a future reader does not "fix" it.
- Gate 1 ("every one of the 180 source rows has exactly one disposition") is already satisfied by the committed CSV — verified. As a pre-completion gate it is a no-op; move it to the spec's own acceptance section.
- Gates 2 and 3 have no artifact to check against. The documentation coverage map is deck/topic-level, not section-level, so "every final manual section maps to at least one topic or an explicit exclusion" cannot be evidenced. Enumerate the manual's sections with a tick per section.
- Because merges collapse 5 concepts into 2–3 cards, "180 source concepts" is not the number of cards carried forward. State the carried-card figure explicitly.
- "Adapt" is doing double duty as both a provenance label and a workload estimate. Since every adapted card is fully re-authored, the two meanings diverge — worth separating.

## Recommended changes before authoring starts

1. Resolve source access (B1) — vendor dated snapshots into `docs/sources/` and cite them per row.
2. Add the portable validator + CI (B2), including the byte-for-byte check that `decks/mojo-language/` is unmodified, and the corrected stale-spelling regexes (S11).
3. Drop `1-0` from the deck IDs (B3).
4. Add a "Disposition of the existing Mojo Language deck" section (B4).
5. Re-derive the count table from the topic ranges (S1).
6. Add the evidence column to the CSV and re-classify the ~15–20 suspect Adapt rows (S2).
7. Freeze the 27 topic names and rewrite every ledger destination to use one of them (S3, S4).
8. Add the shipping checklist and the "Fundamentals ships first, alone" sequencing rule (S12, S14).
9. Add card-size budgets derived from the existing deck's numbers (S13).
