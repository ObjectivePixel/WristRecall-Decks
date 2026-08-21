# WristRecall Deck Cover Style Guide

Use these rules whenever creating, revising, prompting, or evaluating a WristRecall deck cover.

## Overarching art direction

Every cover must feel at home in a clean, colourful, modern iOS app. The visual character should be quietly futuristic: precise geometry, generous space, crisp silhouettes, controlled colour, subtle layering, and polished restraint. It should feel intelligent and contemporary rather than childish, whimsical, nostalgic, ornamental, or corporate.

When rules compete, prioritize in this order:

1. Recognition at the implemented thumbnail size.
2. Clean iOS-native clarity and restraint.
3. One distinctive literal hero object.
4. Controlled futuristic colour and layering.
5. Decorative polish.

## Core principles

1. **Design for the implemented deck icon first.** The cover is displayed as a small rounded-square icon beside deck information. It must remain understandable at approximately 100 x 100 px. A detail that is unreadable at that size must not be essential.
2. **One subject means one hero illustration.** Choose one literal, instantly recognizable object that communicates the deck topic. Prefer a distinctive real-world object over a generic abstract pictogram. Avoid collages, scenes, and competing objects.
3. **Use a polished flat vector-style hero.** Build it from simple geometric shapes, predominantly solid fills, clean silhouettes, slightly softened forms, selective broad internal structure, and high contrast. Aim for a refined flat editorial icon illustration rather than an ultra-minimal UI glyph or a dimensional object render.
4. **Avoid unsuitable rendering.** Do not use photorealism, 3D rendering, bevels, embossed edges, glossy highlights, metallic reflections, realistic materials, textures, complex lighting, fine outlines, or tiny decorative details.
5. **Make the hero dominant.** Its bounding box should occupy approximately 55-65% of the canvas width and height, sit near the optical centre, and remain recognizable at thumbnail size. Do not make it small merely to create negative space.
6. **Use a light neutral base.** Prefer off-white, very pale grey, or an extremely pale tinted background for a clean, cohesive iOS-like appearance.
7. **Readability outranks decorative detail, but preserve defining structure.** The hero must read from its silhouette and characteristic construction. Keep broad features that make the object unmistakable—for example, the hinged top, striped blocks, and writing lines of a clapperboard. Remove only details that do not aid recognition.
8. **Distinguish structural detail from surface detail.** Repeated cells, slots, stripes, panels, or openings may be used when they define the object. Avoid feather texture, eye highlights, tiny markings, ornament, or shading added merely for polish.
9. **Do not impose an artificially low shape count.** Use as many broad geometric shapes as the recognizable structure requires, while ensuring every important feature remains visible at 100 x 100 px. Merge, enlarge, or omit features that collapse into noise.
10. **Use the blur test.** When viewed small or slightly blurred, the topic should still be identifiable from the large silhouette, major internal divisions, and contrast.

## Composition

11. **Design for a rounded-square display mask, but export a normal square.** Keep the complete hero and every essential detail within the central 64% of the canvas: at least 18% inward from every edge. Keep all four corners entirely nonessential because the interface will round or crop them. The source image itself must remain a full-bleed square with sharp 90-degree outer corners.
11. **Use an image-only composition.** Do not include a deck title, subtitle, labels, numbers, captions, or other text. The hero symbol alone must communicate the topic.
12. **Do not include a logo or publisher mark.** The WristRecall logo is a style reference only and must never appear on the cover.
13. **Preserve breathing room around the hero.** Keep all essential parts away from the edge and corner crop zones. The pale background must fill the entire square canvas to every edge and corner. Nonessential background cards may extend into those zones.
14. **Use optical balance.** Adjust asymmetric symbols by eye rather than relying solely on mathematical centring.

## Text

15. **Do not use text.** Covers must contain no title, subtitle, typography, lettering, numbers, or generated pseudo-text.
16. **Do not reserve a text zone.** The surrounding interface already displays the deck title and description. Use the icon canvas for one larger, clearer hero and generous crop protection.

## Colour

14. **Use a restrained palette.** Combine one dark anchor colour, one primary subject colour, and no more than two or three supporting accents.
15. **Draw inspiration from the logo palette.** Suitable families include lime, lavender, blue, cyan, teal, purple, orange, and charcoal.
16. **Do not use the whole brand palette at once.** Select two to four coordinated colour families for each cover.
17. **Keep colours bright but controlled.** Prefer clear, slightly softened colours rather than harsh neon tones.
18. **Maintain strong separation.** The hero and background shapes must remain distinct through contrast or clear negative-space boundaries.
19. **Keep colour sophisticated.** Use colourful accents deliberately, with cooler digital hues and restrained warm counterpoints. Avoid candy colours, rainbow treatment, juvenile primary-colour combinations, or excessive saturation.

## Brand-inspired background motif

19. **Base every cover background on one approved reference.** Use one of the seven user-provided backgrounds `BG_01.jpg` through `BG_07.jpg` as the sole background reference. The result may use the exact file or a very close recreation of its card arrangement, scale, cropping, overlap, palette, and light neutral base. Do not invent a substantially different background composition or combine elements from multiple references.
20. **Choose the reference uniformly at random for each new deck.** At the beginning of a new deck-cover workflow, randomly select one of `BG_01.jpg`, `BG_02.jpg`, `BG_03.jpg`, `BG_04.jpg`, `BG_05.jpg`, `BG_06.jpg`, or `BG_07.jpg`, giving every option an equal chance. Do not choose according to the deck topic, hero colour, personal preference, convenience, or perceived suitability. Do not default to or deliberately favour any reference. Record the selected reference in the working prompt so it remains consistent through that deck's concept and refinement stages.
21. **Keep one selected background direction throughout a deck workflow.** Use the randomly selected reference for all four panels of the initial concept sheet and for the final selected cover. Refinements must retain that background direction unless the user explicitly asks to change or reroll it. A new deck starts a new independent random selection.
22. **Keep background cards pale and atmospheric.** Preserve the selected reference's light, desaturated lime, lavender, aqua and coral treatment, low contrast, and gentle layering. The background should fill the full square and must never compete with the hero for attention.
23. **Preserve the reference's confident overlap and cropping.** Keep its oversized rounded diamond/card language, edge cropping, and broad spatial rhythm close enough that the chosen source remains readily identifiable. Only minor generative variation is permitted.
24. **Do not reconstruct the logo.** Never add its cream glyph, dark lead card, exact fan arrangement, or complete composition. The approved background references contain only the permitted atmospheric card language.
25. **Keep the hero independent.** The hero communicates the deck topic; the reference-based background provides the brand atmosphere and must not become a second subject.

## Effects and consistency

24. **Keep dimensional effects extremely restrained.** Prefer flat fills. If needed, use only a barely perceptible tonal shift within a large shape and one very soft, shallow separation shadow. The hero must read as a flat vector illustration at first glance.
25. **Avoid volumetric rendering.** Do not use bevelled edges, rim lighting, specular shine, jewel-like facets, realistic gold or metal, deep cast shadows, glossy surfaces, cinematic lighting, or heavily rendered finishes.
26. **Build a family of covers.** Keep the background treatment, hero scale and placement, corner softness, spacing, and graphic weight consistent. Change the hero and accent palette for each deck.

## Target visual character

The preferred result should feel like the approved clapperboard reference:

- One large, literal and immediately recognizable object.
- A bold dark silhouette with a small number of broad, meaningful internal divisions.
- Enough structural detail to give the object character, but no ornamental micro-detail.
- Confident asymmetric shape or gesture when natural to the subject.
- Approximately four large, pale and desaturated rounded diamonds framing and overlapping behind the hero without competing for attention.
- Clear foreground/background separation created mainly by colour value and silhouette, with flat fills and only minimal tonal polish.
- More like a polished editorial icon or app illustration than a schematic diagram, corporate pictogram, sticker, or generic UI symbol.
- Futuristic through precision, spacing, layering and controlled digital colour—not through neon glow, sci-fi machinery, chrome, holograms or visual effects.
- Friendly enough to feel approachable, but never cute, cartoonish, toy-like or overly playful.

## Quality checks

Approve a cover only after checking it at:

- Full resolution for finish and alignment.
- Approximately 300 x 300 px for ordinary browsing.
- Approximately 100 x 100 px for immediate recognition.
- Approximately 100 x 100 px with slight blur, confirming that the silhouette and major colour blocks still communicate the subject.
- A simulated center crop that removes the outer 18% on every edge.
- A rounded-square mask matching the implemented deck icon.
- The unmasked source file, confirming that it is a full square with no baked-in rounded corners, transparency, black corner fill, border, or external padding.
- The icon placed beside the deck title and description, ensuring it adds visual identification rather than repeating interface text.

At the smallest size and after the crop test, the complete hero must still be clear and recognizable.

## Final file specification

- Final selected cover files must be exported at exactly **1024 x 1024 pixels**.
- Final selected cover files must use the **JPEG (.jpg)** format with high-quality compression.
- JPEGs must be opaque RGB images with the pale background filling every edge and corner; never simulate transparency with black or another corner colour.
- Use a descriptive filename ending in `.jpg`.
- Concept selection sheets are temporary review artifacts and do not need to follow the final-cover file specification.

## Companion theme gradient

Every final cover must be accompanied by a two-colour theme gradient for the surrounding deck interface.

1. **Use one approved preset for every new deck.** At the beginning of each new deck-cover workflow, select exactly one gradient from the approved preset library below. Use its listed hexadecimal values unchanged and in the stated start-to-end order. Do not invent an ad hoc gradient when an approved preset applies.
2. **Choose presets uniformly at random.** Give every approved preset an equal chance. Do not choose according to the deck topic, background reference, personal preference, convenience, or perceived suitability. Do not default to teal, charcoal, grey, or any other familiar combination. Record the selected preset in the working prompt and keep it consistent through concept generation, refinement, and final delivery. A new deck starts a new independent random selection; reroll only when the user explicitly requests it.
3. **Keep the hero palette independent from the gradient.** Do not use the selected gradient to inspire, constrain, or recolour the hero. Choose the hero palette solely to maximize literal accuracy, silhouette clarity, internal feature separation, contrast against the selected background, recognition at approximately 100 x 100 px, and consistency with the overall WristRecall illustration style. A visually unrelated hero and interface gradient is acceptable when each performs its own function clearly.
4. **Keep all selections independent.** Randomly select the approved background reference and approved gradient preset separately. Do not pair them intentionally by perceived compatibility, and do not alter the hero's most readable and recognizable palette to coordinate with either selection. If contrast against the background is insufficient, improve foreground/background separation without borrowing colours from the theme gradient or changing the preset values.
5. **Use exactly two gradient colours.** The surrounding interface gradient must contain only the two colours specified by the chosen preset.
6. **Keep white text legible everywhere.** The approved values have been selected for white interface text. If implementation or interpolation changes, revalidate both endpoints and the entire blended gradient and maintain at least a 4.5:1 contrast ratio with white.
7. **Keep the gradient controlled.** Avoid neon, rainbow, metallic, muddy, or additional colours. The gradient should feel clean, colourful, modern, iOS-native, and quietly futuristic.
8. **Provide the preset name and exact values.** When delivering a final cover, state the selected preset name and its two hexadecimal colours in start-to-end order.

### Approved gradient preset library

- **Forest Lime:** `#014222` → `#4F6618`
- **Plum Lavender:** `#492650` → `#654A91`
- **Burnt Orange Plum:** `#A84400` → `#492650`
- **Lime Teal:** `#536C1F` → `#096F73`
- **Lavender Teal:** `#624A8D` → `#096F73`
- **Forest Teal:** `#014222` → `#096F73`
- **Orange Lavender:** `#A84400` → `#654A91`
- **Orange Ember:** `#7A2F00` → `#A84400`
- **Charcoal Forest:** `#242424` → `#014222`
- **Charcoal Plum:** `#242424` → `#492650`
- **Charcoal Lavender:** `#242424` → `#654A91`
- **Charcoal Lime:** `#242424` → `#4F6618`
- **Charcoal Teal:** `#242424` → `#096F73`
- **Charcoal Orange:** `#242424` → `#A84400`

## Concept selection workflow

1. **Begin with one four-option concept sheet.** For each new deck cover, generate a single presentation page containing four distinct cover concepts arranged in a clear 2 x 2 grid.
2. **Treat the sheet as a selection artifact, not the deliverable.** The four panels may be lower-detail concept renders. Do not generate or save four separate final cover files at this stage.
3. **Vary meaningful design decisions without increasing detail.** Explore controlled differences in hero silhouette, simple construction, composition, colour balance, and background-card arrangement. Do not produce four trivial near-duplicates, and do not use intricacy as the source of variation.
4. **Keep the options comparable and thumbnail-readable.** Each panel must preview the same square proportions, crop-safe area, text-free cover treatment, and overall WristRecall visual language. Reject a concept before presentation if its small preview depends on fine detail.
5. **Label the panels clearly as A, B, C, and D on the surrounding concept sheet.** Labels belong to the presentation layout, never inside a proposed cover design.
6. **Ask the user which option they prefer and why.** The user may select one option or request a combination of specified features from several.
7. **Do not treat the concept sheet as final artwork.** Wait for the user's design decision before producing a deliverable cover.
8. **Generate only the selected direction as the final asset.** Create a new, fully rendered, high-quality 1:1 image following every production rule in this guide. Do not crop the chosen panel out of the concept sheet or merely upscale it.
9. **Deliver the final cover without concept labels or presentation furniture.** It must be a full-bleed 1024 x 1024 JPEG with sharp outer corners, ready for the user to save and implement.
10. **Refine the chosen direction when requested.** Preserve the selected concept's defining features and make only the agreed changes.

## Default generation brief

Create a square, image-only cover for a WristRecall learning deck about "[TOPIC]." The result must feel native to a clean, colourful, modern iOS app: quietly futuristic, precise, spacious, intelligent and polished, but not childish or overly playful. Use one large, literal and instantly recognizable hero object to communicate the topic without words. Render it as a polished flat vector-style editorial icon with simple geometric construction, clean softened edges, predominantly solid fills, broad meaningful internal structure, and high contrast. Preserve the object's defining construction instead of reducing it to a generic pictogram. The hero should occupy approximately 55-65% of the canvas and sit near the optical centre.

Before creating concepts for a new deck, make one uniform random selection from the seven approved user-provided background references `BG_01.jpg` through `BG_07.jpg`; every reference must have an equal chance, and the choice must not be influenced by topic, hero palette, preference, convenience, or perceived suitability. State the selected reference in the working prompt and use that same reference for all concept options and the final cover for this deck. Use either the exact selected image or a very close recreation of its arrangement, scale, cropping, overlaps, palette, and light neutral base. Do not combine references or invent a substantially different card arrangement. Minor generative variation is acceptable, but the selected source should remain readily identifiable. The background must fill the complete square canvas all the way to its four sharp outer corners. Do not bake a rounded mask into the image. Keep its pale cards low-contrast and atmospheric so they never compete with the hero.

Independently make one uniform random selection from the approved gradient preset library for the surrounding interface theme. Record its preset name and exact start-to-end hexadecimal values in the working prompt, and keep the same preset through all concepts, refinements, and final delivery. Do not alter its endpoint values or habitually favour teal, charcoal, grey, or any other family. Do not use the gradient to inspire, constrain, or recolour the hero. Choose the hero palette independently for literal accuracy, contrast, readability, and immediate recognition at thumbnail size.

Keep the complete hero and every meaningful detail within the central 64% of the canvas, leaving an 18% crop-safe margin on every side. Only nonessential background shapes may enter the crop zone. Keep the composition spacious, balanced, polished, friendly, and clearly recognizable at 100 x 100 px and after center-cropping.

Do not include any text, letters, numbers, pseudo-text, the WristRecall logo, its glyph, a publisher mark, or a reconstruction of the logo. Do not include baked-in rounded outer corners, transparent corners, black corner wedges, a border, or padding around the square. Avoid photorealism, 3D rendering, bevels, glossy or metallic highlights, faceted jewels, realistic materials, textures, dramatic lighting, deep shadows, clutter, multiple subjects, fine lines, tiny decorations, excessive gradients, cartoon faces, cute proportions, toy-like styling, stickers, candy colours, rainbow palettes, neon glow, chrome, holograms, ornamental flourishes, and novelty effects.

