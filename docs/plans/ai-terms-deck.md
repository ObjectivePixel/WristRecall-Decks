# AI Terms deck — plan

> **STATUS: DRAFT — NOT FINAL.** This deck ships with WristRecall **Mojo Edition**
> (the built-in extra deck). It is the long-pole content item for getting Mojo
> Edition into the App Store. Before this deck is treated as final / released,
> the gates at the bottom of this file **must** be cleared by James.

## Source / spec

Project plan, Decks page:

> "AI Terms - new deck. Scrape the Modular blog and build list of terms.
> Questions must be reviewed before deck is committed."

The Modular blog (https://www.modular.com/blog) could not be fetched in this
environment, so this draft was authored from well-established AI / ML /
GPU-computing terminology, themed for the Mojo / Modular audience (Mojo is
Modular's language; the deck leans into GPU kernels, SIMD, occupancy,
quantization, KV-cache, etc.). **The term list and house wording still need to
be cross-checked against the Modular blog** — see gates below.

## Metadata

| Field | Value |
|-------|-------|
| `id` | `ai-terms` |
| `name` | AI Terms |
| `uuid` | `4DE499FA-FEB0-46D0-BF20-1453CA14163C` (stable — do not change between releases) |
| `category` | Programming |
| `version` | `0.1.0` (pre-release draft; bump to 1.0.0 at final commit) |
| `gradientColors` | `#6D28D9FF` → `#06B6D4CC` (purple → cyan; distinct from existing decks) |
| `imageName` | `ai_terms_deck` (1024×1024 JPG, **PLACEHOLDER art**) |
| `cardCount` / `topicCount` | 30 / 4 |
| `sourceFileName` | `cards.json` |
| `moreInfoURL` | https://www.modular.com/blog |

## Topic grouping & term list (30 cards, 4 topics)

### Fundamentals (cards 1–7)
1. Tensor — multi-dimensional array; shape + dtype; core ML data structure.
2. Neural network — layers of weighted sums + non-linear activations.
3. Parameters — learnable weights; "7B" = 7 billion; drives size/memory.
4. Embedding — dense vector; similar items sit close; powers search/RAG.
5. Token — unit a model reads/generates; sub-word; the billing/throughput unit.
6. Hyperparameter — config set before training (LR, batch size) vs learned weights.
7. Overfitting — memorizing training noise; train loss down, val loss up.

### GPU & Performance (cards 8–17)
8. GPU — thousands of cores for parallel matrix math; AI workhorse.
9. GPU kernel — function run in parallel on the GPU; Mojo's core use case.
10. SIMD — Single Instruction, Multiple Data; first-class type in Mojo.
11. Throughput vs latency — volume/time vs time-per-request; the serving trade-off.
12. Memory-bound vs compute-bound — bottleneck is data movement vs arithmetic.
13. FLOPs vs FLOP/s — count of operations vs rate; training budget vs chip speed.
14. GPU occupancy — active warps / max; helps hide latency; max ≠ fastest.
15. Mixed-precision training — fp16/bf16 math, fp32 where stability matters.
16. Quantization — int8/int4 weights; smaller/faster inference, some accuracy cost.
17. Operator/kernel fusion — merge ops into one kernel to cut memory traffic.

### Model Architectures (cards 18–23)
18. Transformer — parallel self-attention architecture behind modern LLMs.
19. Attention — each token weighs every other via query/key/value.
20. Multi-head attention — parallel heads specializing in different relationships.
21. Mixture of Experts (MoE) — router activates few experts/token; sparse capacity.
22. Context window — max tokens attended to at once; attention cost grows ~O(n²).
23. RNN — sequential, stateful; limits parallelism vs transformers.

### Training & Inference (cards 24–30)
24. Training vs inference — learning weights (fwd+bwd) vs running forward only.
25. Backpropagation — gradients via chain rule, backward through the net.
26. Gradient descent / learning rate — step downhill; step size is most-tuned knob.
27. KV-cache — cached keys/values for past tokens; top inference memory driver.
28. RAG — retrieve docs via embeddings, inject into prompt; reduces hallucination.
29. Fine-tuning — continue training on focused data; LoRA = tiny adapters.
30. Hallucination — fluent but wrong output; mitigated by grounding/RAG.

## Card format conventions followed (v2)

- `front.text` + `front.markdown`; `back.text` + `back.markdown`.
- `back.code_snippet`: `null` (no code fences needed for definition cards).
- `back.formatting.inline_code_terms`: `[]`.
- Each back: a `##` headline + exactly one teal `{#0F766E}…{/}` key-insight callout.
- Every card ID appears in exactly one topic; counts match the manifest.

## Task checklist

- [x] Create worktree + branch `content/ai-terms-deck` off `origin/main`.
- [x] Study v2 format from `decks/mojo-language/`.
- [x] Author 30 cards across 4 topics (`decks/ai-terms/cards.json`).
- [x] Write manifest (`decks/ai-terms/deck.json`) — stable uuid, distinctive gradient.
- [x] Add PLACEHOLDER 1024×1024 cover (`assets/ai_terms_deck.jpg`, stamped).
- [x] Write this plan.
- [x] Validate-only compile (no `--export-wristdeck`), confirm 0 errors.
- [x] Commit + push `content/ai-terms-deck` (DRAFT).
- [ ] **GATE:** James reviews every question/answer for accuracy (see below).
- [ ] **GATE:** Cross-check term list & wording against the Modular blog.
- [ ] **GATE:** Replace placeholder cover with final art.
- [ ] Bump `version` 0.1.0 → 1.0.0, then final commit / release.

## Gates — MUST clear before this is final (for James)

1. **Review the questions/answers.** Per spec, "Questions must be reviewed
   before deck is committed." Every front/back here is AI-authored from general
   knowledge and needs a human accuracy pass before release.
2. **Cross-check against the Modular blog** (https://www.modular.com/blog) for
   house terminology and any Modular/Mojo-specific terms worth adding or
   rewording (e.g. MAX, the engine/runtime vocabulary, GenAI serving terms).
   This environment couldn't fetch the blog, so the list is from general ML
   knowledge — confirm coverage and naming.
3. **Cover art TODO.** `assets/ai_terms_deck.jpg` is a 1024×1024 PLACEHOLDER
   (purple→cyan gradient stamped "PLACEHOLDER — not final art"). The manifest
   requires a non-null `imageName`, so a placeholder is in place to let the deck
   compile and import. Replace with final art before release.
