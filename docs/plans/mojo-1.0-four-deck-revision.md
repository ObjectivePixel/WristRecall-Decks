# Mojo 1.0 four-deck revision specification

Status: specification revised 2026-08-19 after adversarial review ([review](mojo-1.0-four-deck-revision-review-2.md)). All four decks were authored on 2026-08-28 — 370 cards against a 330–404 target — and none has yet been studied on device. The sequencing rule below (Fundamentals ships alone first) was deliberately overridden so the suite could be assessed as a unit.

## Scope and invariants

This project creates four new decks. The existing `decks/mojo-language` package is read-only source material and must not be modified. The **published** "Mojo Language" deck also stays in the catalog as-is (decided 2026-08-19); the new decks must therefore distinguish themselves by name and description, because the catalog will carry both 1.0 and beta-era Mojo content at the same time.

### Pinned sources

Only final-state sources are normative. All are reachable and were verified on 2026-08-19.

| Source | URL |
|---|---|
| Mojo v1.0.0 release notes (released 2026-08-11) | https://mojolang.org/releases/v1.0.0/ |
| Mojo manual | https://mojolang.org/docs/manual/ |
| Mojo language reference | https://mojolang.org/docs/reference/ |
| Mojo standard-library reference | https://mojolang.org/docs/std/ |
| Mojo roadmap (used only to exclude) | https://mojolang.org/docs/roadmap/ |
| MAX GPU guide, **pinned to MAX 26.5** | https://max.modular.com/gpu/intro-tutorial/ |
| MAX `layout` API | https://max.modular.com/api/mojo/layout |

`docs.modular.com/max/...` 307-redirects to `max.modular.com`; cite the latter.

Beta changelogs are not migration targets. Historical spellings appear only when needed to identify a stale source card. New cards teach the final 1.0 state, not the sequence of changes that produced it.

### Content rules

These three rules bind every card in every deck, and are enforced by `tools/check_decks.py` where mechanically checkable.

**R1 — No unimplemented features.** A concept gets a card only if it resolves to a manual, reference, or `std`/`max` page. Roadmap items do not. Confirmed exclusions, all listed unstarted on the roadmap and absent from the manual and reference:

| Excluded | Evidence |
|---|---|
| Struct extensions | Roadmap: "⬜ **Struct extensions**: Post-hoc type extension and better modular refactoring." Absent from the Structs manual page and the reference TOC. |
| `private` and other access-control modifiers | Roadmap: "⬜ **Access control features**: For example, `private` modifiers". Privacy in 1.0 is the underscore *convention* only — no card may imply a modifier exists. |
| Existentials / dynamic traits, algebraic data types and pattern matching, `match`/`switch`, classes and inheritance, untyped variables | Roadmap Phase 2/3. The Control flow page states outright: "Mojo currently does not support the equivalent of a Python `match` or C `switch` statement". |

A single Fundamentals card may state what Mojo 1.0 deliberately lacks (no `match`, no classes), framed as a fact about 1.0 rather than as a preview.

**R1a — `async` is a library, not a language fundamental.** Async needs care rather than exclusion. `std.runtime.asyncrt` ships in 1.0 — "the low level concurrency library", providing "low-level concurrency primitives for managing async coroutines, task groups, and parallel execution" — so `async def`, `await` and `TaskGroup` are real. But the manual's Functions page never mentions `async`, the release notes never mention it, it is outside the initial stable set, and the roadmap still lists "⬜ **First-class `async` support**: Fully integrated with Mojo's type and memory models" as unstarted. So: no async in Fundamentals, and async cards live in **Libraries** sourced from the `std.runtime.asyncrt` reference, carrying the R2 marker.

**R2 — Experimental and unstable APIs are marked or excluded.** The 1.0 stable set is deliberately small — `Deinitable`, `Movable`, `Copyable`, `Array`, `List`, `Span`, `String`, `Bool`, `Optional`. **Interior origins are explicitly experimental**: the release notes introduce them as "a new experimental feature known as _interior origins_." Cards on experimental APIs must carry an in-card marker (a red `{#C62828}Experimental in 1.0.{/}` line) or be dropped. Under a 1.x policy that is only "mostly additive", these are the likeliest cards in the suite to go stale, and flashcards are the worst medium for content that moves.

**R3 — Deprecated spellings never appear as the preferred API.** This one is load-bearing and cannot be left to the eye: 1.0 ships "a deprecated alias and a compiler fix-it" for nearly every breaking change, so a card teaching `read`, `alias` or `.mojopkg` still *compiles*. Nothing but the automated scan in `tools/check_decks.py` will catch it. The scan's term list is in that script, not in this document, so it can be extended without a spec revision.

## Outputs

Deck ids omit the language version. The id is the folder name and the release-tag prefix, and is paired with a uuid that must never change; `mojo-1-0-fundamentals` would be permanently wrong at Mojo 1.1. The language version lives in `version` and `description`, exactly as `mojo-language` already does it.

| Deck id | Deck name | Prerequisite | Target cards |
|---|---|---|---:|
| `mojo-fundamentals` | Mojo 1.0 Fundamentals | None | 100–118 |
| `mojo-advanced` | Mojo 1.0 Advanced Language & Systems | Fundamentals | 112–134 |
| `mojo-libraries` | Mojo 1.0 Libraries, Interop & Tools | Fundamentals; Advanced recommended for FFI | 78–100 |
| `mojo-gpu` | Mojo 1.0 GPU Programming with MAX | Fundamentals; memory/metaprogramming portions of Advanced | 40–52 |

Expected suite size: **330–404 cards**, derived from the per-topic ranges below rather than asserted independently of them. Counts are planning ranges, not quotas. Atomicity and durable usefulness take priority over reaching a particular number.

Prerequisites have nowhere to live in the manifest — no deck in this repo has an ordering field — so each is stated as the opening clause of the deck `description`, e.g. "Start here" / "Builds on Mojo 1.0 Fundamentals."

### Sequencing

**Fundamentals is authored, validated, released and listed in the README before Advanced starts.** Each deck ships independently. Four decks landing together is a much worse failure mode than one deck landing four times, and the first deck is where the authoring conventions get found.

## Source-card disposition

The detailed 180-row matrix is in [mojo-1.0-source-card-matrix.csv](mojo-1.0-source-card-matrix.csv). Source ids run 1–181 with 29 absent — that gap is real, the shipped deck skips it too, and it is not to be "fixed".

| Destination | Adapt | Rewrite | Merge | Placed |
|---|---:|---:|---:|---:|
| Fundamentals | 59 | 7 | 1 | 67 |
| Advanced Language & Systems | 36 | 38 | 0 | 74 |
| Libraries, Interop & Tools | 24 | 9 | 4 | 37 |
| GPU Programming with MAX | 0 | 0 | 0 | 0 |
| **Total placed** | **119** | **54** | **5** | **178** |
| Omitted (no destination) | — | — | — | 2 |

Omitted rows carry no destination, so per-deck tallies computed from the CSV no longer over-count Fundamentals. After merges collapse 5 concepts into 2–3 cards, roughly **173 concepts carry forward** — against a target of 330–404, so this is 160–230 net-new cards, and since every adapted concept is re-authored from scratch, effectively the whole suite is written fresh. Treat "revision" as provenance, not as a workload estimate.

"Adapt" does not mean copy verbatim. Every adapted concept gets newly authored final-1.0 wording and examples. "Rewrite" flags a known semantic or API conflict. "Merge" consolidates overlapping prompts, and both halves of a merge share a `merge_group` value in the CSV. "Omit" removes a non-atomic summary, a tutorial-specific recipe, or a concept that does not exist in 1.0.

### Evidence requirement

Every row carries an `evidence` value: a source URL plus either `changed: <what>` or `confirmed unchanged`. Boilerplate rationales are forbidden. In the original matrix, 122 of 180 rows shared one byte-identical rationale, all of them Adapt — the classification that means nobody looks at the row again — so the column carried no information exactly where a missed conflict is unrecoverable. A spot-check found real misclassifications in it (async, `alias`, imports); the Fundamentals rows have now been re-checked individually, and **the Advanced and Libraries rows are re-checked at the start of their own deck's authoring phase**, not before.

## Four-deck blueprint

### 1. Mojo 1.0 Fundamentals

Goal: enough language fluency to read and write ordinary Mojo programs without requiring systems-programming knowledge.

Every topic is pinned to a source. Note that **Strings has no manual page of its own** — it is a subsection of Types, so string cards source from Types plus the `std` reference.

| Topic | Planned cards | Source | Coverage |
|---|---:|---|---|
| Functions and arguments | 15–18 | manual/functions, reference/function-declarations | `def`, arguments versus parameters, defaults, positional-only and keyword-only arguments, variadics, `var **kwargs` and its forwarding form, overloads (including "cannot differ only by argument convention"), result types, `raises`. **No `async`** — see rule R1a; async is Libraries material. `fn` appears only as replacement guidance — deprecated in favour of `def` and slated for removal. |
| Variables, literals, and types | 15–18 | manual/variables, manual/types, manual/metaprogramming/comptime-evaluation | required `var`, `comptime` values (**`alias` is gone — replacement guidance only**), inference, the sized integer and float families, `IntLiteral`/`FloatLiteral`, `comptime Int = Scalar[DType.int]`, no implicit narrowing or widening plus explicit `cast()`, `Bool`, tuples, `Optional` |
| Operators and expressions | 10–13 | manual/operators, reference/expressions | arithmetic, comparison, bitwise, boolean short-circuiting, membership, identity, string operators, ternary conditional, assignment operators, walrus binding, precedence |
| Control flow, errors, and contexts | 16–19 | manual/control-flow, manual/errors, reference/expressions, release notes | `if`, `comptime if`, `while`, `for`, `break`/`continue`, `else` on loops, list/set/dict comprehensions, the reworked unified `range()` family and its rejected forms, `try`/`except`/`else`/`finally`, typed errors, `Error` is `ImplicitlyCopyable`, `with`. One card may state that 1.0 has no `match`/`switch`. |
| Structs and methods | 16–19 | manual/structs, reference/struct-declarations | fields, initialization, `Self` (method `self` must have type `Self`), methods, mutability, making a struct `Copyable`, static methods, operator and special methods, subscripts, conversions, decorators, structs compared to Python classes. **No extensions.** |
| Strings and core collections | 17–20 | manual/types §Strings, std reference | `String`/`StringSpan`, `StringLiteral`, bytes/codepoints/graphemes, default grapheme-cluster iteration, `Array` versus `List`, list expressions materialize to `Array`, dictionaries, sets, slicing and bounds (invalid contiguous slices abort; negative-index rules) |
| Modules and conventions | 11–13 | manual/packages, release notes §import resolution | modules, packages, `__init__.mojo`, explicit imports, relative imports, re-exports, the four-step import search order, `mojo precompile` and `.mojoc`, docstrings, naming conventions, privacy-by-underscore convention |

Topic sum: **100–120**; deck target 100–118 after merges.

Deliberate additions absent from the source deck: operators as a coherent topic, `break`/`continue`, comprehensions, walrus binding, `var **kwargs`, final import resolution, list-expression materialization to `Array`, and the `alias`→`comptime` and `fn`→`def` replacements.

Removed from the original plan: struct extensions (R1), and `async` introductions (R1a — relocated to Libraries).

### 2. Mojo 1.0 Advanced Language & Systems

Goal: teach Mojo's ownership, type-system, metaprogramming, and low-level programming model.

Topic budgets are re-derived from documentation weight plus release-note change surface, not inherited from the source deck's shape. The original plan gave Pointers 28–34 cards — a quarter of the deck, its largest topic by a wide margin — which tracked the beta deck's 24 pointer cards rather than the final docs, where Pointers is two manual pages out of roughly 45 while metaprogramming and the type system span seven. Pointers comes down; traits, constraints and metaprogramming go up.

| Topic | Planned cards | Source | Coverage |
|---|---:|---|---|
| Ownership, references, and origins | 15–18 | manual/value-ownership/* | `imm`, `mut`, `var`, `ref`, `out`, `deinit`, transfer sigil, exclusivity, origin inference and unions, address spaces. Interior origins are **experimental** and carry the R2 marker. |
| Lifecycle and initialization | 14–17 | manual/value-lifecycle/* | synthesized and custom initializers, copy/move, `__deinit__`, ASAP destruction, deep and partial initialization, `Deinitable`, explicitly destroyed values |
| Pointers and allocation | 20–24 | manual/pointers/* | unified `Pointer`, `OwnedPointer`, `ArcPointer`, nullability via `Optional[Pointer]`, `OpaquePointer`, pointer versus pointee state, `Layout`, `Allocation`, `ThinAllocation`, the `unsafe_*` operation family, pointer subtraction and `offset_from()`, foreign pointers |
| Traits, generics, and constraints | 22–26 | manual/metaprogramming/{traits,parameterized-declarations,constraints}, reference/trait-declarations | refinement and composition, associated members, conditional conformance, trailing `where`, diagnostic messages, `==`/`!=` type equality, parameter packs, `TypeList.all_conforms_to()` |
| Metaprogramming, materialization, and reflection | 18–22 | manual/metaprogramming/{comptime-evaluation,parameterization,materialization,reflection} | compile-time evaluation, `comptime if`/`comptime for`, parameterization, materialization, partial and unbound types, ternary type expressions, `rebind`, `reflect[T]`, `reflect_fn` |
| Closures, lambdas, and function values | 12–15 | manual/advanced-functions/*, reference/{closure,lambda} | capture lists and conventions, `thin`, closure traits, function literal types, lambda syntax/defaults/effects, runtime closure values, dynamic function pointers with unbound parameters |
| SIMD, atomics, and low-level types | 11–14 | std reference | `Scalar`/`SIMD`, `SIMDLength`, the `size`→`length` rename, alignment and `size_of()`, atomic ordering, memory-oriented operations |

Topic sum: **112–136**; deck target 112–134 after merges.

#### Required lambda coverage

Lambdas are a first-class planned cluster, not a single glossary card:

1. Final lambda grammar and typed parameters.
2. Single-expression body and absence of `return`.
3. Return-type behavior, including the fixed `None` default.
4. Lambda versus nested `def`.
5. Explicit and omitted capture lists.
6. Omitted capture list as immutable capture of free variables.
7. Capture-free lambda as a `thin` function value.
8. Capturing lambda as a runtime closure instance without a function type.
9. Effects and compatibility with higher-order APIs.
10. Relationship to deprecated legacy `@parameter` closures, expressed only as replacement guidance where a source card requires it.

#### Required conditional-conformance coverage

The final suite must explicitly cover:

- Structs are `Movable` by default.
- `Movable where condition` narrows movability.
- `Movable where False` opts out of implicit movability.
- Conditional `Deinitable` and explicit destruction.
- `where (condition, "message")` diagnostics.
- `==` and `!=` for type equality.
- Refinement through `conforms_to()` and `TypeList.all_conforms_to()`.
- The final 1.0 fix ensuring a `where False` opt-out is respected inside generic functions.

### 3. Mojo 1.0 Libraries, Interop & Tools

Goal: teach stable/high-value library surfaces and the workflows required to build, test, package, and integrate Mojo code.

| Topic | Planned cards | Coverage |
|---|---:|---|
| Stable surface and migration | 12–16 | stability markings and the initial stable set; the 1.x "mostly additive" policy; **deprecated aliases and compiler fix-its as the mechanical migration path**; "one name, one type per concept" as the principle behind the 1.0 renames |
| Collections, iterators, and text | 14–18 | owned/borrowed iteration, iterator adapters, linear elements, `deinit_with`, `Variant`, `StringDict`, Unicode views |
| Python from Mojo | 7–9 | importing Python, `PythonObject`, conversions, NumPy transfer and borrowing, error translation |
| Mojo from Python | 7–10 | `PythonModuleBuilder`, `PythonTypeBuilder`, exported functions and types, callback signatures and safe pointers |
| C FFI and runtime | 10–14 | `abi("C")`, `external_call`, C variadics, `OwnedDLHandle`, C strings, shared libraries, `initialize_runtime` |
| Compilation, packaging, and tools | 13–17 | run/build, compilation targets, feature toggles, `--fp-mode`, debugger, tests, notebooks, Mojo AI skills, `mojo precompile`/`.mojoc`, package workflows |
| Math, I/O, system, and runtime | 12–16 | the curated `math` surface, files, paths, environment, timing, benchmarking, randomness, process and system APIs, and `std.runtime.asyncrt` async/task-group material (R2-marked) |

Topic sum: **75–100**; deck target 78–100 after the merged rows land.

The standard-library deck is curated rather than an API encyclopedia. Stable APIs and concepts that transfer between APIs receive priority. Two changes from the original plan: the migration mechanism (deprecated aliases, fix-its, stability policy) is now first-class content rather than absent, and the `math` surface has an explicit home — previously two merged rows were routed to a deck with no topic that could hold them.

### 4. Mojo 1.0 GPU Programming with MAX

Goal: teach the Mojo/MAX GPU **API surface** — enough to write, launch and debug a kernel.

Scope narrowed on 2026-08-19. The repo already ships `ai-terms` (74 cards), whose *GPU & Performance* (10) and *GPU & Kernels* (22) topics already teach the generic hardware model: thread, warp, thread block, grid, barrier, occupancy, SIMD, tiling, row-major layout, HBM, registers, PTX, and a kernel-type taxonomy. Restating that here would duplicate an installed deck for an almost identical audience. This deck therefore assumes the hardware model and teaches the Mojo/MAX APIs on top of it; its description points at `ai-terms` for the underlying concepts.

| Topic | Planned cards | Coverage |
|---|---:|---|
| Device runtime and kernel launch | 10–13 | `DeviceContext`, kernel functions, compilation and enqueueing, grid and block dimensions in the API, asynchronous streams, fixed-width kernel arguments |
| Host and device memory | 10–13 | `HostBuffer`, `DeviceBuffer`, copies, ownership, synchronization, memory spaces |
| Layouts and TileTensor | 12–15 | shape/stride mapping, row/column/tiled layouts, coordinate mapping, `TileTensor` views, `LayoutTensor` and how the two relate, loads and stores |
| Package boundary, debugging, and correctness | 8–11 | host/runtime APIs in `max.gpu` versus the low-level primitives remaining in `std.gpu`; `layout` shipping with MAX; GPU assertions and debugging; bounds; race reasoning; portability |

Topic sum: **40–52**.

Dropped relative to the original plan: "GPU architecture and execution" (9–11) and most of "Blocks, warps, and synchronization" (10–13), as `ai-terms` coverage. Retained from the latter: only what is API-shaped — barrier and collective *calls*, shared-memory allocation, warp-operation safety rules.

Pinned to **MAX 26.5**, the release paired with Mojo 1.0. Citing a "current" guide would contradict the final-state-sources invariant.

## Final Mojo 1.0 release-note traceability ledger

Legend:

- **Card**: warrants one or more dedicated cards.
- **Cluster**: incorporated into a broader durable-concept card.
- **Audit**: affects examples/imports throughout the suite.
- **Exclude**: reviewed but not useful as a durable flashcard.

### Language enhancements

| Final 1.0 item | Disposition | Destination |
|---|---|---|
| Lambda expressions | Card cluster | Advanced / Closures and lambdas |
| Interior origins (**experimental**) | Card cluster, R2 marker | Advanced / Ownership and origins |
| List expressions default to `Array` | Card | Fundamentals / Collections |
| Structs are `Movable` by default; conditional and `where False` opt-out | Card cluster | Advanced / Traits and lifecycle |
| Forwarding keyword variadics with `**` | Card | Fundamentals / Functions |
| Calling dynamic function pointers with unbound parameters | Card | Advanced / Function values |
| `==` and `!=` type equality | Card | Advanced / Constraints |
| Constraint diagnostic messages | Card | Advanced / Constraints |
| `TypeList.all_conforms_to()` proof/refinement | Card | Advanced / Generics |
| Inferred `Trait` for `TypeList.of` | Cluster | Advanced / Parameter packs |
| Redundant trait-composition warning | Cluster | Advanced / Traits |
| Improved import-location diagnostics | Exclude | Diagnostic behavior, not a durable language rule |

### Language changes

| Final 1.0 item | Disposition | Destination |
|---|---|---|
| Explicit `var` required; implicit declarations deprecated | Card and audit | Fundamentals / Variables |
| `__deinit__` destructor spelling | Card and audit | Advanced / Lifecycle |
| Explicit import resolution, relative imports, re-exports and search order | Card cluster | Fundamentals / Modules |
| `imm` replaces `read` | Card and audit | Advanced / Ownership |
| `size_of()` returns aligned allocation size | Card | Advanced / Low-level types |
| Final `@explicit_destroy`/`Deinitable where False` behavior | Card cluster | Advanced / Lifecycle |
| Legacy closure decorators deprecated; `@parameter if`/`for` give way to `comptime if`/`for` | Rewrite source concepts; audit | Advanced / Closures; Fundamentals / Control flow |
| Explicit closure-trait conformance | Card | Advanced / Closures |
| Bare `**kwargs` invalid; require `var **kwargs` | Card | Fundamentals / Functions |
| Trailing `where` replaces parameter-list `where` | Card | Advanced / Constraints |
| Struct fields cannot hide `UnsafeAnyOrigin` | Card | Advanced / Origins and pointers |
| Method `self` must have type `Self` | Cluster | Fundamentals / Structs |
| Overloads cannot differ only by argument convention | Card | Fundamentals / Functions |
| Reserved words rejected as function names | Cluster | Fundamentals / Identifiers |
| Restricted newlines in declarations/imports | Cluster | Fundamentals / Syntax |
| `alias` gives way to `comptime` values | Card and audit | Fundamentals / Variables |
| `fn` deprecated; `def` declares all functions | Card and audit | Fundamentals / Functions |
| `CollectionElement` superseded by the final trait set | Audit | Advanced / Traits |

### Stable surface and type-system changes

| Final 1.0 item | Disposition | Destination |
|---|---|---|
| Initial stable API set and per-API stability markings | Card | Libraries / Stability |
| `ImplicitlyDestructible` renamed `Deinitable` | Card and audit | Advanced / Lifecycle |
| Reflection field-handle rename | Cluster | Advanced / Reflection |
| `ConditionalType` replaced by ternary type expression | Card | Advanced / Metaprogramming |
| `Error` becomes `ImplicitlyCopyable` | Cluster | Fundamentals / Errors |
| Relaxed positional-only `Equatable` implementations | Exclude | Narrow implementation compatibility detail |

### Pointers and memory

| Final 1.0 item | Disposition | Destination |
|---|---|---|
| `Pointer`/`UnsafePointer` unification and `unsafe_*` operations | Card cluster and audit | Advanced / Pointers |
| Explicit handling of `UnsafeAnyOrigin` widening | Card | Advanced / Origins |
| `as_imm()`, `OwnedPointer.into_inner()` and `ImmStaticOrigin` renames | Cluster/audit | Advanced / Pointers |
| `AddressSpace` module move | Audit plus card concept | Advanced / Address spaces |
| `unsafe_take_allocation()` returns `Allocation` | Card | Advanced / Allocation |
| Pointer subtraction/`offset_from()` | Card | Advanced / Pointers |

### Collections, iterators, and linear values

| Final 1.0 item | Disposition | Destination |
|---|---|---|
| `InlineArray` renamed `Array`; parameter names changed | Card and audit | Fundamentals / Collections |
| `Array` no longer `ImplicitlyCopyable` or `Defaultable` | Card | Advanced / Lifecycle |
| Invalid contiguous slices abort; negative-index behavior | Card | Fundamentals / Collections |
| Interior origins across collections and buffers (**experimental**) | Card cluster, R2 marker | Advanced / Origins |
| Negative `insert` indices rejected | Cluster | Fundamentals / Collections |
| `List.capacity()` method | Exclude | Narrow API spelling |
| `List.try_index()` | Exclude | Narrow additive API |
| Prelude `MutSpan`/`ImmSpan` aliases | Cluster | Libraries / Span |
| Span address-space parameter | Card | Advanced / Address spaces |
| `Span(unsafe_ptr=...)` and module move | Audit | Libraries / Span |
| Linear-safe `Dict`/`Set` insertion and clearing | Card cluster | Libraries / Linear collections |
| `Dict.fromkeys` accepts iterable | Exclude | Narrow additive API |
| Borrowed versus consuming `Dict` iteration constraints | Card | Libraries / Iteration |
| `Variant.unwrap` rename | Audit | Libraries / Variant |
| `Optional` is `Iterable`, not `Iterator` | Card | Libraries / Iteration |
| `BitSet` range/resizing additions | Exclude | Narrow additive API |
| `Tuple.consume_elements()` | Cluster | Libraries / Linear values |
| Conditional `Deinitable` collections and `deinit_with()` | Card cluster | Libraries / Linear values |
| `Array` supports non-`Movable` elements | Card | Libraries / Linear values |
| `Optional`/`Variant` support non-`Movable` elements and in-place construction | Card cluster | Libraries / Linear values |
| `OwnedKwargsDict` renamed `StringDict` | Card/audit | Libraries / Collections |
| Owned iteration no longer requires `Copyable` | Card | Libraries / Iteration |
| `Optional.deinit_assert_empty` and linear map/and_then | Cluster | Libraries / Linear values |
| Trivial-deinitialization helper rename | Cluster/audit | Advanced / Lifecycle |

### Strings and numeric types

| Final 1.0 item | Disposition | Destination |
|---|---|---|
| `StringSlice` renamed `StringSpan` | Card and audit | Fundamentals / Strings |
| String iteration yields grapheme clusters | Card | Fundamentals / Strings |
| `Int` aliases `Scalar[DType.int]` and stricter conversions | Card cluster | Fundamentals/Advanced numeric topics |
| `SIMDLength` | Card | Advanced / SIMD |
| `size` becomes `length` **throughout**, not only on `SIMD` | Card plus suite-wide audit | Advanced / SIMD; audits Fundamentals collections |
| Reworked unified `range()` family and rejected invalid forms | Card cluster | Fundamentals / Control flow |
| Direct integer-scalar construction from `Intable` | Exclude | Narrow conversion convenience |
| Scalar `repr()` spelling | Exclude | Presentation detail |

### Python, C FFI, system, and runtime

| Final 1.0 item | Disposition | Destination |
|---|---|---|
| Python binding APIs use safe `Pointer` signatures | Card/audit | Libraries / Mojo from Python |
| Final `PythonObject` operator behavior | Cluster | Libraries / Python from Mojo |
| NumPy copy and zero-copy borrowing helpers | Card | Libraries / Python interop |
| `raise_python_exception()` | Card | Libraries / Mojo from Python |
| `OwnedDLHandle` symbol/function lifetime and signature changes | Card cluster | Libraries / C FFI |
| C variadic `external_call` | Card | Libraries / C FFI |
| File creation honors umask/existing permissions | Exclude | Platform behavior better left to API docs |
| `initialize_runtime()` for shared libraries called by foreign hosts | Card | Libraries / C FFI |
| `chdir`/`fchdir` additions | Exclude | Narrow additive API |
| `Bencher.iter` takes final closure form | Cluster/audit | Libraries / Benchmarking |
| Unhandled-error stack-trace hint | Exclude | Diagnostic behavior |

### GPU/MAX boundary and tooling

| Final 1.0 item | Disposition | Destination |
|---|---|---|
| Accelerator host/runtime APIs moved from `std` to `max` | Card and audit | GPU / Runtime |
| `layout` bundled with MAX | Card and audit | GPU / Layouts |
| LSP docstring checking default | Exclude | Tool implementation behavior |
| Crash-reporting/telemetry defaults and event rename | Exclude | Telemetry implementation behavior |
| `--fp-mode` | Card | Libraries / Compilation |
| `--lld-path` | Exclude | Specialist linker override |

### Removed items

| Final 1.0 item | Disposition | Destination |
|---|---|---|
| Removed `DType.invalid` sentinel | Audit; cluster with valid dtype constraints | Advanced / Numeric types |
| Removed positional `StringLiteral` indexing | Cluster | Fundamentals / Strings |
| Removed static `String.write()` | Audit | Fundamentals / Strings |
| Removed `trait_downcast_var()` | Cluster with automatic refinement | Advanced / Constraints |

### Fixes

Every final 1.0 fix was reviewed. Fixes normally do not become cards because they describe compiler defects rather than language contracts. The following have durable semantic consequences and are covered:

| Fix area | Disposition |
|---|---|
| Conditional conformance through `Optional`/`Variant` | Covered by conditional-conformance and linear-container cards |
| Refinement inside `conforms_to()` branches and nested boolean expressions | Covered by type-refinement cards |
| Constrained `comptime` members and `where` elaboration | Covered by constraint cards |
| `where False` opt-out respected in generic functions | Explicitly covered by the `Movable where False` card cluster |
| Reflection field offsets for aligned layouts | Covered by reflection/alignment cards |
| Closure combinations of `*args`, keyword-only arguments and `**kwargs` | Covered by function/closure signature cards |
| Volatile load behavior | Covered only if a durable volatile-memory card survives authoring review |
| Pointer offset and import-resolution fixes | Covered by final pointer/import rules |
| Remaining compiler, LSP, completion, folding, base64 and build fixes | Excluded as implementation fixes, not flashcard concepts |

### Migration mechanism and stability policy

Absent from the original ledger, and the most directly useful material in the suite for its actual audience — people upgrading beta-era code.

| Final 1.0 item | Disposition | Destination |
|---|---|---|
| Nearly every breaking change ships a deprecated alias plus a compiler fix-it | Card | Libraries / Stable surface and migration |
| The 1.x stability policy is "mostly additive", with a deliberately small initial stable set | Card | Libraries / Stable surface and migration |
| "One name, and one type, per concept" as the principle behind the 1.0 renames | Card | Libraries / Stable surface and migration |

### Async: reclassified, not excluded

| Final 1.0 state | Disposition | Destination |
|---|---|---|
| `std.runtime.asyncrt` provides async coroutines, task groups and parallel execution | Card cluster, R2 marker | Libraries / Math, I/O, system, and measurement → see `runtime` |
| Language-level async is not first-class and is undocumented in the manual | Cluster | Libraries, same topic |

Source cards #64 (`async def` / `await`) and #110 (`TaskGroup`) were **already routed to Libraries** in the matrix — it was the Fundamentals blueprint, listing "`raises` and `async` introductions", that disagreed with it. The blueprint is the side that was wrong and has been corrected. Both rows change from Adapt to Rewrite: the concepts survive, but as library surface outside the stable set, to be verified against the `std.runtime.asyncrt` reference rather than the manual.

### Reviewed and excluded: not in Mojo 1.0

Recorded so the exclusion is a decision rather than an oversight. See rule R1.

| Item | Why excluded |
|---|---|
| Struct extensions | Roadmap, unstarted; no manual or reference page. |
| `private` and access-control modifiers | Roadmap, unstarted. Privacy is the underscore convention only. |
| Existentials / dynamic traits, ADTs and pattern matching, `match`/`switch`, classes, inheritance, untyped variables | Roadmap Phase 2/3. Permitted only as a single "what 1.0 does not have" card. |

## Documentation coverage map

| Official final documentation area | Deck/topic |
|---|---|
| Functions | Fundamentals / Functions |
| Variables, types, literals | Fundamentals / Variables and types |
| Operators and expressions | Fundamentals / Operators and expressions |
| Control flow | Fundamentals / Control flow |
| Errors and context managers | Fundamentals / Errors and contexts |
| Structs | Fundamentals / Structs |
| Modules and packages | Fundamentals / Modules |
| Value semantics and ownership | Advanced / Ownership |
| Lifetimes, origins, and references | Advanced / Origins |
| Value creation, destruction, and deep initialization | Advanced / Lifecycle |
| Compile-time evaluation and parameterization | Advanced / Metaprogramming |
| Traits, generics, constraints, and materialization | Advanced / Traits and constraints |
| Reflection | Advanced / Reflection |
| Pointers | Advanced / Pointers and allocation |
| Closures and lambda expressions | Advanced / Closures and lambdas |
| Python from Mojo | Libraries / Python from Mojo |
| Mojo from Python and Python types | Libraries / Mojo from Python |
| Calling C from Mojo | Libraries / C FFI |
| Compilation targets and feature toggles | Libraries / Tools |
| Debugging, testing, and notebooks | Libraries / Tools |
| Packaging | Libraries / Compilation, packaging, and tools |
| Mojo AI skills | Libraries / Compilation, packaging, and tools |
| Get started (Quickstart, Tips for Python devs, System requirements) | **Excluded** — install and orientation material, not durable flashcard content |
| Language basics / Overview | **Excluded** — an index page over topics covered individually |
| Reference / Mojo cheat sheets | **Excluded** — a summary of material covered card by card |
| Reference / Inline MLIR | **Excluded** unless authoring review finds a durable, broadly useful concept |
| GPU introduction and architecture (MAX docs, not the Mojo manual) | Partly `ai-terms`; API portions GPU / Runtime |
| GPU fundamentals (MAX docs) | GPU / Runtime and memory |
| Block/warp operations and synchronization (MAX docs) | GPU / Package boundary, debugging, and correctness |
| GPU debugging (MAX docs) | GPU / Package boundary, debugging, and correctness |
| TileTensor (MAX docs) | GPU / Layouts and TileTensor |
| Layouts and LayoutTensor concepts (MAX docs) | GPU / Layouts and TileTensor |

The language reference is a second-pass completeness check for identifiers, keywords, literals, numeric types, operators, expressions, statements, declarations, docstrings, decorators, and inline MLIR. Inline MLIR is likely an explicit exclusion unless the authoring review identifies a durable, broadly useful concept.

## Authoring and validation gates

Gates 1–3 are acceptance criteria on this specification and are already satisfied; the rest bind each deck before it is considered complete. Everything mechanically checkable is implemented in `tools/check_decks.py`, which runs in CI — `tools/DeckCompiler` is an arm64 macOS binary, so it cannot be the only gate while ~350 cards are authored and committed.

**Satisfied by this document**

1. Every one of the 180 source rows has exactly one disposition. *(Verified mechanically: 180 rows, exactly the 180 shipped card ids, no duplicates, tallies reproduce the summary table.)*
2. Every externally relevant final 1.0 release-note entry has a ledger disposition.
3. Every final manual section maps to at least one topic or an explicit exclusion.

**Per deck, before it ships**

4. Every card traces to a pinned source; the CSV `evidence` column is populated for that deck's rows.
5. No card teaches a deprecated spelling as the preferred final API, and no card teaches a feature outside 1.0 (R1). Experimental APIs carry the R2 marker.
6. Cards are atomic enough for watch-sized review, within the budgets enforced by `tools/check_decks.py`. These are calibrated against the shipped Mojo deck rather than asserted — its backs run to a median of 270 characters, p90 636, p95 843, max 1627; fences median 5 lines, p90 9, max 25; code columns p90 45, p95 52, max 77 — and sit just above p90 so they catch the outliers that will not survive a 41mm screen without outlawing normal practice:
   - front markdown ≤ 120 characters, back markdown ≤ 800
   - code fences ≤ 12 lines, code lines ≤ 64 columns

   Budgets apply only to the four new decks, so the existing catalog stays green. Run `./tools/check_decks.py --budgets` to see how the legacy decks would score (29 findings, all in `mojo-language`).
7. The manifest uses a new id and uuid; `decks/mojo-language/` is byte-for-byte unchanged.
8. `tools/check_decks.py` passes: manifest counts match content, card ids are unique, every id lands in exactly one topic, JSON parses, size budgets hold, and the stale-spelling scan is clean.
9. `./tools/compile.sh <deck-id>` produces a `.wristdeck`, and it has been imported and reviewed on a real watch.
10. Human review before release. API accuracy and card granularity are content decisions, not merely compiler-valid JSON.

The stale-spelling scan runs word-boundary regexes scoped to code fences and inline-code spans. Bare substring search is unusable here: `read` alone matches the English word in 73 of the source deck's cards, and scanning prose for `alias` produces six hits that are all the English word — the shipped deck's code contains the `alias` keyword exactly zero times. Scoped correctly, the beta deck's real exposure is `UnsafePointer` 13 cards, `read` as a convention keyword 9, `__del__` 8, `@parameter` 4, `fn` 1.

The term list lives in `tools/check_decks.py`, so it can grow without a spec revision. Running it against `decks/mojo-language` produces 39 findings, which is the ground truth it exists to catch:

```
./tools/check_decks.py --strict-mojo mojo-language
```

## Shipping checklist

Per deck, after gate 10. Cover art is the long-lead item and is supplied by the maintainer.

- [ ] `decks/<id>/deck.json` — id, fresh `uuid` (`uuidgen`), name, description opening with the prerequisite clause, `storeFileName`, `imageName`, `gradientColors`, `category: "Programming"`, `version`, `moreInfoURL`, `aboutURL`, `topicDefinitions`
- [ ] `decks/<id>/cards.json`
- [ ] `decks/<id>/assets/<imageName>.jpg` — 1024×1024, **supplied by the maintainer**; the deck compiles and validates without it but cannot be released
- [ ] `./tools/compile.sh <id>` clean
- [ ] on-device import and review
- [ ] release tag `<deck-id>-v<version>`
- [ ] README catalog row with cover, card/topic counts, description, download link

## Next implementation phase

Decisions taken 2026-08-19: the published Mojo Language deck stays in the catalog untouched; the GPU deck is narrowed to Mojo/MAX APIs; Fundamentals ships alone first; cover art comes from the maintainer.

1. Land `tools/check_decks.py` and its CI workflow.
2. Author `mojo-fundamentals` against the pinned sources, topic by topic.
3. Run gates 4–10; compile; test on device; release; add the README row.
4. Only then: re-check the Advanced CSV rows, author `mojo-advanced` (pointer, lambda and conditional-conformance clusters).
5. `mojo-libraries`, including the migration-mechanism topic.
6. `mojo-gpu` against MAX 26.5.

Open item, not blocking: the catalog will list "Mojo Language" (1.0 beta content) alongside "Mojo 1.0 Fundamentals". The new decks' names and descriptions carry the version to distinguish them, but the older deck holds the more discoverable name. Worth revisiting once Fundamentals ships.
