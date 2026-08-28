# Adversarial review — Mojo 1.0 four-deck specification (independent pass)

Target: `docs/plans/mojo-1.0-four-deck-revision.md` + `docs/plans/mojo-1.0-source-card-matrix.csv` on `agent/mojo-1-0-four-deck-spec` (27930c6), against `main` @ 95eb616.

A prior review exists on `claude/mojo-deck-spec-review-2nvzpc`. This pass was run independently and then reconciled with it; see [Corrections to the prior review](#corrections-to-the-prior-review) — two of its four blocking findings do not hold.

**Verdict: the migration ledger is sound, the blueprint is not.** Everything the spec says about what *changed* in 1.0 checks out. The problems are in what it says the decks should *contain*: three planned clusters cover features that do not exist in Mojo 1.0, the stale-spelling gate misses the deprecations most present in the source deck, and the GPU deck duplicates a deck this repo already ships.

## What was verified, and how

Mechanical checks against the shipped deck (`decks/mojo-language/mojophrases.json`, 180 cards):

- All 180 `source_prompt` values match the shipped card fronts exactly; all 180 `source_topic` values match `topicDefinitions`. **Zero mismatches.** The matrix is not invented.
- `source_id` spans 1–181 with 29 absent — correct, the shipped deck also skips 29. Add a footnote so nobody "fixes" it.
- Action/destination tallies reproduce the summary table exactly (Adapt 122 / Rewrite 51 / Merge 5 / Omit 2; Fundamentals 69 / Advanced 74 / Libraries 37).

Documentation checks (all five normative hosts fetched successfully from this environment): release notes, manual TOC, functions/variables/operators/structs/pointers manual pages, language-reference TOC, roadmap, MAX `layout` API index, MAX GPU intro tutorial.

Confirmed accurate in the ledger: `imm` for `read`; `__deinit__`; `StringSlice`→`StringSpan`; `InlineArray`→`Array`; `ImplicitlyDestructible`→`Deinitable`; `Pointer`/`UnsafePointer` unification; structs `Movable` by default; `var **kwargs`; `SIMDLength`; `OwnedKwargsDict`→`StringDict`; accelerator APIs to the `max` package; `layout` bundled with MAX; `.mojoc` precompilation; stable API set with per-API markings. Also confirmed real, against doubt: the walrus operator, and `Layout` / `Allocation` / `ThinAllocation` as genuine 1.0 pointer APIs.

## Blocking

### B1. Three planned clusters teach features Mojo 1.0 does not have

The spec's first invariant is that only final-state sources are normative. The blueprint breaks it.

| Planned coverage | Actual 1.0 status |
|---|---|
| Fundamentals / Structs: "decorators, **extensions**" | Not implemented. Absent from the manual's Structs page and from the language-reference TOC. The roadmap lists it unstarted: "⬜ **Struct extensions**: Post-hoc type extension and better modular refactoring." |
| Fundamentals / Functions: "`raises` and **`async`** introductions" | **Corrected on re-check — see the note below.** Not unimplemented, but not Fundamentals material either. |
| Fundamentals / Modules: "naming and **privacy** conventions" | Convention only — "⬜ **Access control features**: For example, `private` modifiers" is unstarted. Safe if the cards teach the underscore convention; wrong if any card implies a modifier. |

**Correction on async.** My first pass called async unimplemented, inferring it from the roadmap. Checking `std` directly, `std.runtime.asyncrt` does ship in 1.0 — "the low level concurrency library", providing "low-level concurrency primitives for managing async coroutines, task groups, and parallel execution" — so `async def`, `await` and `TaskGroup` are real, and source cards #64 and #110 are not teaching a phantom. What holds: the manual's Functions page never mentions `async`, the release notes never mention it, it is outside the initial stable set, and "⬜ **First-class `async` support**: Fully integrated with Mojo's type and memory models" is still unstarted. Second correction, same finding: I wrote that the matrix "agrees with" the blueprint by scheduling #64 and #110 into Fundamentals. It does not — both rows were **already routed to Libraries**. The real defect is narrower and points the other way: the *blueprint* claims async coverage in Fundamentals/Functions that its own matrix never supported. So what survives is a blueprint/matrix inconsistency plus a stability caveat — drop async from Fundamentals, keep the two Libraries rows, verify them against the `std.runtime.asyncrt` reference rather than the manual, and mark them experimental. Struct extensions and `private` remain hard exclusions.

Fix: add an explicit rule — no card for a roadmap or unimplemented feature — and a gate requiring every topic bullet in the blueprint to resolve to a manual, reference or `std`/`max` page before authoring starts. Reclassify #64 and #110.

### B2. Gate 9's stale-spelling scan misses the deprecations that are actually in the source deck

Measured over the 180 shipped cards (cards containing each term):

| Term | Cards | In gate 9's list? |
|---|---:|---|
| `UnsafePointer` | 20 | yes |
| `__del__` | 8 | yes |
| `@parameter` | 4 | yes |
| `CollectionElement` | 3 | **no** |
| `fn` | 2 | **no** |
| `InlineArray` / `StringSlice` / `.mojopkg` / `mojo package` | 2 each | yes |
| `ImplicitlyDestructible` | 1 | yes |

**Correction on `alias`.** My first pass reported six `alias` cards, five of them Adapt, and called that a misclassification. Re-scanning *inside code fences and inline-code spans only*, the `alias` keyword appears in **zero** cards — every hit was the English word ("`Self` is a type alias for the enclosing struct"), and the shipped deck already uses `comptime`. Retracted: no `alias` problem exists in the source deck and no CSV row changes for it. Keeping `alias` in the scan list is still worth it as a guard on *new* authoring, but it is not evidence of existing rot. This is precisely the failure mode the finding warns about — bare substring search over prose — and I walked into it.

Scoped correctly (code spans only), the real exposure is `UnsafePointer` 13 cards, `read` as a convention keyword 9, `__del__` 8, `@parameter` 4, `fn` 1. The final docs use `comptime` for compile-time values and `comptime if`/`comptime for` for compile-time control flow; `@parameter if`/`for` appear nowhere in the metaprogramming manual. `fn` is deprecated ("Use `def` for all function declarations. The `fn` keyword will be removed in a future release"). `CollectionElement` is superseded by the final trait set — the spec knows this (matrix rows #18, #63, #145 are Rewrite for exactly that reason) but never added the term to the scan.

As written, the gate would still pass a deck teaching `CollectionElement` or `fn`, neither of which it looks for.

Fix: add `alias`, `CollectionElement`, `fn`, `ConditionalType`, `trait_downcast_var`, `DType.invalid`, `OwnedKwargsDict` and SIMD `size=` to the scan; run it as word-boundary regexes scoped to code fences and inline-code spans, not bare substrings (`read` alone is unusable — it matches the English word throughout).

### B3. The GPU deck duplicates a deck this repo already ships, and the spec never mentions it

`decks/ai-terms` (74 cards, published, v0.1.3, described in the README as "for the Mojo / Modular ecosystem") already contains **32 GPU cards** across two topics:

- *GPU & Performance* (10): GPU, GPU kernel, SIMD, throughput vs latency, memory- vs compute-bound, FLOP/s, occupancy, mixed precision, quantization, operator fusion.
- *GPU & Kernels* (22): matmul, conv2d, CUTLASS, PTX, MLIR, tiling, HBM, registers, **thread**, **warp**, **thread block**, **grid**, **row-major layout**, **barrier**, plus a kernel-type taxonomy.

The proposed GPU deck's topic 1 ("accelerators, SMs, grids, blocks, warps, threads, SIMT, divergence", 9–11 cards), topic 4 ("barriers, shared memory, block collectives, warp operations", 10–13) and part of topic 5 ("row/column/tiled layouts") land on top of that. Roughly 20–25 of 60–75 planned cards restate an installed deck, for a user segment that overlaps almost completely.

The spec never names `ai-terms`. Decide in the spec: narrow the GPU deck to Mojo/MAX API material (`DeviceContext`, `HostBuffer`/`DeviceBuffer`, `TileTensor`, `max.gpu` vs `std.gpu`) and point at `ai-terms` for the hardware model, or state the duplication is deliberate because the decks install independently.

### B4. No disposition for the deck being superseded

`decks/mojo-language` is frozen as read-only source, and the *published* deck — README catalog, live download, five releases, the most discoverable name in the family — is never mentioned again. It teaches beta-era APIs at the scale in B2's table. Gate 5 ("no answer teaches a deprecated spelling as the preferred final API") binds only the new decks, so shipping as specified puts the wrong and the right API in the catalog simultaneously.

Note the mechanism this forecloses: AUTHORING.md states that importing the same `uuid` overwrites the existing copy on device. Superseding in place (reuse `mojo-language`'s id/uuid for Fundamentals, bump to 2.0.0) is the *only* option that upgrades existing installs; four new UUIDs strand every current user on beta content. "Read-only" is a sensible working-copy rule for the authoring phase, but it is being applied as a product decision. Make that decision explicitly — supersede, archive-and-rename, or unlist.

## Substantive

### S1. `**` forwarding: the release notes and the manual disagree at face value

The ledger schedules a Fundamentals card for "Forwarding keyword variadics with `**`". The 1.0 Functions manual says the opposite in plain terms: "Dictionary unpacking is not supported yet." The two are probably reconcilable — forwarding an existing `var **kwargs` pack is not unpacking an arbitrary dict at a call site — but the distinction is exactly the kind a flashcard flattens. Pin the precise supported form, with the doc anchor, before authoring.

### S2. Topic budgets are inherited from the beta deck, not derived from 1.0

Advanced allocates **28–34 cards to Pointers and allocation** — a quarter of the deck, its largest topic by a wide margin. That number tracks the source deck (24 pointer cards, its largest topic) rather than the final documentation, where Pointers is *two* manual pages ("Intro to pointers", "Using pointers") out of roughly 45. Metaprogramming — Compile-time evaluation, Parameterization, Traits, Parameterized declarations, Constraints, Materialization, Reflection, seven pages, plus most of the release's type-system changes — is split across topics totalling 35–43. Re-derive per-topic budgets from documentation weight plus release-note change surface, and say so; otherwise the new suite reproduces the old deck's shape under new names.

### S3. Interior origins are experimental and carry no marker

Release notes: "a new experimental feature known as _interior origins_." They are not in the stable API set (`Deinitable`, `Movable`, `Copyable`, `Array`, `List`, `Span`, `String`, `Bool`, `Optional` — "a deliberately small set"). The spec gives interior origins three ledger rows and a slot in the Advanced ownership topic with no caveat, while separately planning a card *about* stability markings. Under a 1.x policy that is only "mostly additive", experimental features are the likeliest content in the suite to go stale — and flashcards are the worst medium for that, because users memorise them. Add an experimental-API rule: exclude, or carry with an in-card marker.

### S4. Coverage map does not cover the manual it claims to

Checked against the live manual TOC. Unmapped sections: **Get started** (Quickstart, Tips for Python devs, System requirements) and **Tools / Mojo AI skills** — the latter is a real Tools page with no destination and no exclusion. Gate 3 ("every final manual section maps to at least one topic or an explicit exclusion") therefore fails on the day it is written. Separately, the map lists six GPU rows as "official final documentation areas", but the Mojo manual has no GPU section at all — that material lives in the MAX docs, which is fine, but the map should say which host each row comes from.

### S5. Card-count arithmetic does not reconcile

Summing the blueprint's own topic ranges:

| Deck | Sum of topics | Stated | Delta |
|---|---|---|---|
| Fundamentals | 102–122 | 105–120 | −3 / +2 |
| Advanced | 112–138 | 115–135 | −3 / +3 |
| Libraries | 71–95 | 75–90 | −4 / +5 |
| GPU | 60–77 | 60–75 | 0 / +2 |
| **Suite** | **345–432** | **355–420** | **−10 / +12** |

Ranges are "not quotas", but they are the only deck-level acceptance signal in the document. Derive the deck totals from the topics or drop them.

### S6. "Adapt" is an unevidenced assertion, on 68% of the corpus

122 of 180 rows carry one byte-identical rationale: *"Reuse the durable concept, re-authoring all wording and examples against final 1.0 documentation."* All are Adapt — the classification that means nobody looks at the row again. So the rationale column carries zero information precisely where a missed conflict is unrecoverable. B1 and B2 above are what a short spot-check surfaced (#64, #110, #21, #128). Add an evidence column (source URL + anchor, and either "changed: X" or "confirmed unchanged against <page>"), forbid boilerplate, and re-run the classification against the release-note change list.

### S7. CSV hygiene

- The two **Omit** rows (#83, #181) still carry `destination_deck = "Mojo 1.0 Fundamentals"`, so any per-deck tally computed from the CSV over-counts Fundamentals by two — the "69 source concepts" figure is really 67. Blank the destination.
- The five **Merge** rows have no merge-group column, so pairings exist only in prose and no script can check that both halves landed in one card.
- Because merges collapse ~5 concepts into 2–3 cards, "180 source concepts" is not the number carried forward (~175). State the carried figure, since it sets the net-new authoring load (~180–245 cards).

### S8. Nothing verifies the decks except a macOS-only binary

`tools/DeckCompiler` is `Mach-O 64-bit arm64`; there is no `.github/` and no CI in the repo. Gate 8 is a manual step on one laptop, while ~400 cards get authored. Add a portable checker (manifest/content counts, ID uniqueness, topic partitioning, the B2 spelling regexes, card-size budgets, plus a byte-for-byte check that `decks/mojo-language/` is unmodified) and run it in CI; keep DeckCompiler as the packaging gate, not the only gate.

Load-bearing detail: because 1.0 ships "a deprecated alias and a compiler fix-it" for nearly every breaking change, a card teaching `read` or `.mojopkg` still *compiles*. Nothing but this scan will catch it. The migration mechanism itself (deprecated aliases + fix-its + the 1.x stability policy) is also durable, teachable content the spec omits entirely — it is the single most useful thing for this suite's actual audience, who are upgrading beta-era code.

### S9. No renderer budget, for content that needs one

Measured across the shipped Mojo deck: back markdown mean 343 chars, median 270, max 1627; **179 of 180 cards carry a code fence**; the renderer has no syntax highlighting (AUTHORING.md: language identifiers "are currently ignored"). The two densest planned clusters — Advanced/Pointers (28–34) and GPU/Layouts+TileTensor (14–18, covering shape/stride mapping, coordinate mapping, tiled layouts, `TileTensor` *and* `LayoutTensor`, loads and stores) — are the most diagrammatic material in the suite and get no guidance on fitting a 41mm screen. Set hard budgets (back markdown ≤ ~700 chars, code fences ≤ 8 lines, code lines ≤ 60 chars) and check them in the S8 script.

### S10. Prerequisites have nowhere to live

The Outputs table assigns prerequisite chains. No manifest in this repo has an ordering or prerequisite field — across all six decks the keys are `id`, `uuid`, `name`, `description`, `storeFileName`, `imageName`, `gradientColors`, `cardCount`, `topicCount`, `category`, `version`, `sourceFileName`, `topicDefinitions`, plus optional `moreInfoURL` / `aboutURL`. Either express the chain in `description` (which AUTHORING.md calls "a short one-liner") and say so, or drop it.

### S11. The plan stops before shipping

"Next implementation phase" ends at "compile and validate". AUTHORING.md's flow does not: four 1024×1024 cover JPGs (the long-lead item, unmentioned), `gradientColors`, `category`, `storeFileName`/`imageName`, deck-browser copy, starting `version`, release tags `<deck-id>-v<version>`, README catalog rows, on-device testing. Add the checklist, and state that each deck ships independently — Fundamentals authored, validated, released and listed *before* Advanced starts. Four decks landing together is a far worse failure mode than one deck landing four times.

### S12. Catalog composition changes as a side effect

Six decks become ten, of which five are Mojo and five of six Programming-category decks are Mojo. That may be right for this repo; it should be a stated decision rather than a consequence.

## Corrections to the prior review

The review on `claude/mojo-deck-spec-review-2nvzpc` is largely sound and its S2/S3/S4/S6–S17 findings stand. Two of its four blocking findings do not:

- **Its B1 ("documentation hosts are unreachable") is environment-specific.** From this session, `mojolang.org`, `docs.modular.com` and `max.modular.com` all fetch normally; this review is grounded in full page text, not search summaries. Do not restructure the spec around an egress limitation of one sandbox. The vendoring recommendation still has independent merit — a dated snapshot makes the ledger auditable later — but it is a nice-to-have, not a blocker.
- **Its B2 ("the GPU source URL does not exist") is wrong.** `https://max.modular.com/gpu/intro-tutorial/` resolves: "Get started with GPU programming", a ten-step vector-addition tutorial covering `DeviceContext`, kernel launch, grid/block dimensions, `HostBuffer`, device memory and `TileTensor` views — precisely the GPU deck's material. Its suggested replacement runs backwards: `docs.modular.com/max/...` 307-redirects *to* `max.modular.com`. The residual point is valid — pin the MAX version (26.5) instead of citing a "current" guide, which does contradict the spec's own final-state-sources invariant.
- Its B5 (retirement plan) and my B4 are the same finding, independently reached.

## Recommended order of work

1. Strike `extensions` and any `private` implication from the blueprint; relocate async to Libraries and reclassify matrix #64 and #110 (B1).
2. Extend the gate-9 term list and make it a scoped-regex script rather than a human grep (B2).
3. Decide the `ai-terms` boundary and rescope the GPU deck (B3).
4. Write a "disposition of the published Mojo Language deck" section — supersede in place is the only path that upgrades existing installs (B4).
5. Add the evidence column and re-classify the Adapt rows against the release-note change list, starting with the import/packaging and async rows (S6).
6. Add the experimental-API rule and mark interior origins (S3).
7. Re-derive topic budgets from documentation weight; fix the count arithmetic (S2, S5).
8. Add the portable validator + CI, card-size budgets, and the shipping checklist with "Fundamentals ships first, alone" (S8, S9, S11).
9. Add the deprecated-alias / fix-it / stability-policy migration material to the Libraries deck (S8).
10. Pin MAX 26.5; fix `**`-forwarding scope; close the coverage-map gaps (S1, S4).

## Sources

- [Mojo v1.0.0 release notes](https://mojolang.org/releases/v1.0.0/) — released 11 Aug 2026
- [Mojo manual](https://mojolang.org/docs/manual/) — [functions](https://mojolang.org/docs/manual/functions/), [variables](https://mojolang.org/docs/manual/variables/), [operators](https://mojolang.org/docs/manual/operators/), [structs](https://mojolang.org/docs/manual/structs/), [using pointers](https://mojolang.org/docs/manual/pointers/using-pointers/), [comptime evaluation](https://mojolang.org/docs/manual/metaprogramming/comptime-evaluation/)
- [Mojo language reference](https://mojolang.org/docs/reference/)
- [Mojo roadmap](https://mojolang.org/docs/roadmap/)
- [MAX GPU intro tutorial](https://max.modular.com/gpu/intro-tutorial/), [MAX `layout` API](https://max.modular.com/api/mojo/layout)
- [Struct extensions proposal](https://github.com/modular/modular/blob/main/mojo/proposals/struct-extensions.md)
