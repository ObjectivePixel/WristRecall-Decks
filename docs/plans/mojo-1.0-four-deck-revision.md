# Mojo 1.0 four-deck revision specification

Status: planning complete; card authoring has not started.

## Scope and invariants

This project creates four new decks. The existing `decks/mojo-language` package and the installed "Mojo Language" deck are read-only source material and must not be modified.

Only final-state sources are normative:

- [Mojo v1.0.0 release notes](https://mojolang.org/releases/v1.0.0/)
- [Final Mojo 1.0 manual](https://mojolang.org/docs/manual/)
- [Final Mojo language reference](https://mojolang.org/docs/reference/)
- [Final Mojo standard-library reference](https://mojolang.org/docs/std/)
- [Current MAX GPU developer guide](https://max.modular.com/gpu/intro-tutorial/)

Beta changelogs are not migration targets. Historical spellings appear only when needed to identify a stale source card. New cards teach the final 1.0 state, not the sequence of changes that produced it.

## Outputs

| Proposed id | Deck name | Prerequisite | Target cards |
|---|---|---|---:|
| `mojo-1-0-fundamentals` | Mojo 1.0 Fundamentals | None | 105–120 |
| `mojo-1-0-advanced` | Mojo 1.0 Advanced Language & Systems | Fundamentals | 115–135 |
| `mojo-1-0-libraries-tools` | Mojo 1.0 Libraries, Interop & Tools | Fundamentals; Advanced recommended for FFI | 75–90 |
| `mojo-gpu-max` | GPU Programming with Mojo & MAX | Fundamentals and the memory/metaprogramming portions of Advanced | 60–75 |

Expected suite size: approximately 355–420 cards. Counts are planning ranges, not quotas. Atomicity and durable usefulness take priority over reaching a particular number.

## Source-card disposition

The detailed 180-row matrix is in [mojo-1.0-source-card-matrix.csv](mojo-1.0-source-card-matrix.csv).

| Destination | Adapt | Rewrite | Merge | Omit | Source concepts |
|---|---:|---:|---:|---:|---:|
| Fundamentals | 59 | 7 | 1 | 2 | 69 |
| Advanced Language & Systems | 36 | 38 | 0 | 0 | 74 |
| Libraries, Interop & Tools | 27 | 6 | 4 | 0 | 37 |
| GPU Programming with Mojo & MAX | 0 | 0 | 0 | 0 | 0 |
| **Total** | **122** | **51** | **5** | **2** | **180** |

"Adapt" does not mean copy verbatim. Every adapted concept gets newly authored final-1.0 wording and examples. "Rewrite" flags a known semantic or API conflict. "Merge" consolidates overlapping prompts. "Omit" removes a non-atomic summary or tutorial-specific recipe. The GPU deck is new coverage rather than a migration of source cards.

## Four-deck blueprint

### 1. Mojo 1.0 Fundamentals

Goal: enough language fluency to read and write ordinary Mojo programs without requiring systems-programming knowledge.

| Topic | Planned cards | Coverage |
|---|---:|---|
| Functions and arguments | 16–19 | `def`, arguments versus parameters, defaults, positional-only and keyword-only arguments, variadics, `var **kwargs`, forwarding, overloads, result types, `raises` and `async` introductions |
| Variables, literals, and types | 15–18 | required `var` declarations, `comptime`, inference, numeric and string literals, `Int`/`Scalar` model, conversions, `Optional`, tuples |
| Operators and expressions | 10–13 | arithmetic, comparison, identity, membership, logical short-circuiting, ternary expressions, walrus bindings, precedence |
| Control flow, errors, and contexts | 17–20 | `if`, `comptime if` introduction, loops, `break`, `continue`, comprehensions, `try`/`except`/`else`/`finally`, typed errors, `with` |
| Structs and methods | 18–21 | fields, initialization, `Self`, methods, mutability, static methods, operators, subscripts, conversions, decorators, extensions |
| Strings and core collections | 17–20 | `String`/`StringSpan`, bytes/codepoints/graphemes, default grapheme iteration, `Array` versus `List`, dictionaries, sets, slicing and bounds |
| Modules and conventions | 9–11 | modules, packages, explicit imports, relative imports, re-exports, docstrings, naming and privacy conventions |

Deliberate additions absent from the source include operators as a coherent topic, `break`/`continue`, comprehensions, walrus binding, `**kwargs`, final import resolution, and list-expression materialization to `Array`.

### 2. Mojo 1.0 Advanced Language & Systems

Goal: teach Mojo's ownership, type-system, metaprogramming, and low-level programming model.

| Topic | Planned cards | Coverage |
|---|---:|---|
| Ownership, references, and origins | 15–18 | `imm`, `mut`, `var`, `ref`, `out`, `deinit`, transfer sigil, exclusivity, origin inference/unions/interiors, address spaces |
| Lifecycle and initialization | 14–17 | synthesized and custom initializers, copy/move, `__deinit__`, ASAP destruction, deep/partial initialization, `Deinitable`, explicitly destroyed values |
| Pointers and allocation | 28–34 | unified `Pointer`, `OwnedPointer`, `ArcPointer`, nullability, pointer/pointee states, `Layout`, `Allocation`, `ThinAllocation`, unsafe operations, foreign pointers |
| Traits, generics, and constraints | 19–23 | refinement/composition, associated members, conditional conformance, `where`, diagnostic messages, type equality, parameter packs |
| Metaprogramming and reflection | 16–20 | compile-time evaluation, parameterization, materialization, partial/unbound types, `rebind`, `reflect[T]`, `reflect_fn` |
| Closures, lambdas, and function values | 11–14 | capture lists and conventions, `thin`, closure traits, function literal types, lambda syntax/defaults/effects, runtime closure values |
| SIMD, atomics, and low-level types | 9–12 | `Scalar`/`SIMD`, `SIMDLength`, alignment/`size_of`, atomic ordering, memory-oriented operations |

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
| Stable library surface | 12–16 | stability markings and durable APIs around `Array`, `List`, `Span`, `String`, `Bool`, `Optional` and lifecycle traits |
| Collections, iterators, and text | 14–18 | owned/borrowed iteration, iterator adapters, linear elements, `deinit_with`, `Variant`, `StringDict`, Unicode views |
| Python from Mojo | 7–9 | importing Python, `PythonObject`, conversions, NumPy transfer/borrowing, error translation |
| Mojo from Python | 7–10 | `PythonModuleBuilder`, `PythonTypeBuilder`, exported functions/types, callback signatures and safe pointers |
| C FFI and runtime | 10–14 | `abi("C")`, `external_call`, variadics, `OwnedDLHandle`, C strings, shared libraries, `initialize_runtime` |
| Compilation, packaging, and tools | 13–17 | run/build, targets, feature toggles, debugger, tests, notebooks, `mojo precompile`/`.mojoc`, package workflows |
| I/O, system, and measurement | 8–11 | files, paths, environment, timing, benchmarking, randomness, process/system APIs |

The standard-library deck is curated rather than an API encyclopedia. Stable APIs and concepts that transfer between APIs receive priority.

### 4. GPU Programming with Mojo & MAX

Goal: progress from the hardware/execution model through useful kernels and modern layout abstractions.

| Topic | Planned cards | Coverage |
|---|---:|---|
| GPU architecture and execution | 9–11 | accelerators, SMs, grids, blocks, warps, threads, SIMT, divergence |
| Device runtime and kernel launch | 9–11 | `DeviceContext`, kernel functions, compilation/enqueueing, grid/block dimensions, asynchronous streams |
| Host and device memory | 10–13 | `HostBuffer`, `DeviceBuffer`, copies, ownership, synchronization, memory spaces |
| Blocks, warps, and synchronization | 10–13 | barriers, shared memory, block collectives, warp operations and safety rules |
| Layouts and TileTensor | 14–18 | shape/stride mapping, row/column/tiled layouts, coordinate mapping, `TileTensor` views, loads/stores |
| Debugging, correctness, and performance | 8–11 | GPU assertions/debugging, bounds, race reasoning, coalescing, occupancy, portability, fixed-width kernel arguments |

The deck teaches the final 1.0 boundary: host/runtime GPU APIs are in `max.gpu`, low-level primitives remain in `std.gpu` where documented, and `layout` ships with MAX.

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
| Interior origins | Card cluster | Advanced / Ownership and origins |
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
| Legacy closure decorators deprecated | Rewrite source concepts | Advanced / Closures |
| Explicit closure-trait conformance | Card | Advanced / Closures |
| Bare `**kwargs` invalid; require `var **kwargs` | Card | Fundamentals / Functions |
| Trailing `where` replaces parameter-list `where` | Card | Advanced / Constraints |
| Struct fields cannot hide `UnsafeAnyOrigin` | Card | Advanced / Origins and pointers |
| Method `self` must have type `Self` | Cluster | Fundamentals / Structs |
| Overloads cannot differ only by argument convention | Card | Fundamentals / Functions |
| Reserved words rejected as function names | Cluster | Fundamentals / Identifiers |
| Restricted newlines in declarations/imports | Cluster | Fundamentals / Syntax |

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
| Interior origins across collections and buffers | Card cluster | Advanced / Origins |
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
| `SIMD` `size` parameter renamed `length` | Audit | Advanced / SIMD |
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
| Packaging | Libraries / Packaging |
| GPU introduction and architecture | GPU / Architecture |
| GPU fundamentals | GPU / Runtime and memory |
| Block/warp operations and synchronization | GPU / Synchronization |
| GPU debugging | GPU / Debugging |
| TileTensor | GPU / TileTensor |
| Layouts and LayoutTensor concepts | GPU / Layouts |

The language reference is a second-pass completeness check for identifiers, keywords, literals, numeric types, operators, expressions, statements, declarations, docstrings, decorators, and inline MLIR. Inline MLIR is likely an explicit exclusion unless the authoring review identifies a durable, broadly useful concept.

## Authoring and validation gates

Before any new deck is considered complete:

1. Every one of the 180 source rows has exactly one disposition.
2. Every externally relevant final 1.0 release-note entry has a ledger disposition.
3. Every final manual section maps to at least one topic or an explicit exclusion.
4. Every card cites or can be traced to final Mojo/MAX documentation during authoring.
5. No answer teaches a deprecated spelling as the preferred final API.
6. Cards are atomic enough for watch-sized review.
7. The four manifests use new ids and UUIDs; the source deck remains byte-for-byte unchanged.
8. Each new deck passes the repository compiler's count/topic/format validation.
9. A final search checks for stale spellings such as `UnsafePointer`, `__del__`, `StringSlice`, `InlineArray`, `ImplicitlyDestructible`, `read`, `@parameter`, `.mojopkg` and `mojo package`. Historical mentions must be deliberate replacement guidance.
10. Human review is required before release because API accuracy and card granularity are content decisions, not merely compiler-valid JSON.

## Next implementation phase

After approval of this specification:

1. Freeze topic names and target card lists.
2. Author Fundamentals first.
3. Author Advanced, including the pointer, lambda, and conditional-conformance clusters.
4. Author Libraries/Interop/Tools.
5. Author the GPU/MAX deck against current MAX guides.
6. Compile and validate all four without installing over or editing the source deck.
