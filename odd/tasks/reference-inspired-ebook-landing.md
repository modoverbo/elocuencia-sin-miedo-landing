# Reference-inspired ebook sales landing

Redesign the Elocuencia sin miedo sales page around a clearer first-screen value proposition and one repeated checkout path, while retaining its dark, cream, and yellow Modo Verbo identity and working interactive preview.

## Objective and problem

The current landing needs a stronger sales hierarchy inspired by the flow of srluizferraz.com without copying its text, claims, price, testimonials, rating, person, or visual identity. Arturo must remain visibly identified on the first screen even as deeper content follows a clearer sales-page sequence.

## Scope and constraints

- Feature identity: `reference-inspired-ebook-landing`.
- Authorized scope: first-screen structure/copy, consistent purchase-CTA placement, product offer card, later section ordering, preview-open/touch feedback, generated Arturo-with-book asset, and testimonial presentation only when real attributable testimonials are supplied. The user has now approved extending this same feature with T6–T9: corrected-PDF cover/page assets, green-gold brand/hero restyle, sticky header and post-hero purchase bar, and a truthful review link/section only where source evidence supports it.
- T1–T6 established the original Modo Verbo dark/cream/yellow look; the user has now approved replacing that visual system with the supplied green/gold ebook identity in T7 while preserving interactive book controls and the existing checkout target.
- Repeat one same-style, same-label primary checkout CTA at key conversion points (header, hero, offer, sticky mobile CTA, closing CTA). Remove secondary marketing CTAs such as “Explorar el libro”; functional preview navigation remains.
- Use author surname `Valdéz` exactly, including the accent. Keep Arturo identified/visible in the first screen.
- Owner-provided offer assertions for this work: one-time payment, immediate ebook access, 7-day guarantee. Present as owner-supplied terms, not independently verified checkout facts.
- The ebook is PDF, 156 pages. Do not invent a numeric price, discount, or other offer term.
- No fake testimonials, quotes, ratings, named buyers, credentials, or unsupported promises. T4 must wait for real attributable customer wording and permission/context to identify it.
- Reference structure to adapt: hero → problem → method/content → offer → testimonials → author → FAQ/closing CTA. Preserve the functioning preview; retain Arturo in the first-screen hierarchy even if a deeper author section moves later.
- No analytics/Clarity, checkout clicks, push, PR, or deployment.
- Delivery strategy: `single-pr`; the user explicitly approved a `size:exception` for this new reference-inspired redesign as one PR exceeding 400 authored changed lines. This is not authorization to create a PR, push, merge, or deploy. Each task closes with a Conventional Commit on this feature branch.
- Initial forecast: approximately 300 authored changed lines across the tasks, generated image excluded; this T1-era estimate is superseded by T2’s actual cumulative count below. Estimates are advisory, not hard task caps.

## Working configuration

- Organic TDD: test-first RED → GREEN → REFACTOR for behavior and structural changes.
- Strict TDD marker is enabled in workspace instructions; use the requested regression suite: `python3 -m unittest discover -s tests -v`, plus `node --test tests/test_preview_swipe_cue.js`.
- Browser visual checks: mobile 320px and 390px; desktop 1280px. `git diff --check` at task closure.
- RDD is disabled for this clone; do not start a review lifecycle or change the setting.

## Tasks

### T1 — First-screen sales hierarchy, repeated CTA, and offer card

- [x] Establish a reference-inspired first screen that keeps Arturo identified while clarifying the ebook's value proposition.
- [x] Repeat the existing checkout CTA style/label and target in the header, hero, offer card, fixed mobile banner, and closing conversion point; remove secondary marketing CTA buttons while preserving functional preview controls.
- [x] Add a brand-consistent offer card with PDF, 156 pages, and owner-provided one-time payment, immediate access, and 7-day guarantee claims; do not show a price or discount.
- [x] Update `Arturo Valdéz` spelling and add focused regression tests.

**Acceptance criteria**

- Arturo's name including `Valdéz` is visible and identified on the first screen.
- The hero communicates the ebook value and a primary checkout action without competing marketing buttons.
- All primary purchase buttons use the same copy and current Hotmart destination; preview navigation still works.
- The offer card states PDF / 156 pages / one-time payment / immediate access / 7-day guarantee without numeric price, discount, or unsupported assertions beyond the supplied owner terms.
- Python suite, Node preview tests, `git diff --check`, and specified viewport checks pass; no checkout is clicked.

**Route and trigger evidence:** delegated direct writer; preparation spans current markup, responsive styles, and regression tests and modifies multiple non-trivial files, so delegated mapping/preparation and one writer are required.

**Progress / verification:** Implementation and automated checks complete; viewport verification is partial. RED: before source edits, `python3 -m unittest discover -s tests -p 'test_author_section.py' -v` failed for the expected old hero/author order and secondary hero button. GREEN: `python3 -m unittest discover -s tests -v` — 7 passed; `node --test tests/test_preview_swipe_cue.js` — 3 passed; `git diff --check` — passed. Browser review in the available fixed mobile CUA viewport showed Arturo Valdéz and the primary CTA on the first screen, the CTA clear of the sticky banner after tightening narrow-mobile vertical spacing, the offer card terms visible in one column, and the preview responding to its “Abrir la muestra” control. No checkout was clicked. This sub-agent browser surface did not expose viewport resizing or desktop view, so the requested exact 320px / 390px / 1280px checks remain unverified; do not report them as passed. Source/test diff is 196 authored changed lines; with this 91-line ODD document, T1 is approximately 287 authored changed lines, below the advisory ~400-line forecast.

**Commit evidence:** `e69bb4a05d94881abfa9e47b0a63bd4d42445b3b` — `feat(landing): unify purchase CTA and offer card` on `codex/reference-inspired-ebook-landing`.

### T2 — Persistent preview gesture affordance

- [x] Show a clearly animated, non-intercepting finger/swipe affordance over the cover/pages while the preview is in the viewport and has not been interacted with.
- [x] Keep the affordance repeating/persistent long enough to be noticed (not a one-shot 1.35s arrow); pause it when the preview leaves the viewport and resume on re-entry until first interaction.
- [x] Dismiss it immediately on first relevant pointer, keyboard, or preview-control interaction; preserve `Abrir la muestra` and user-controlled StPageFlip. Never turn pages automatically.
- [x] Under reduced-motion preference, show a static accessible instruction instead of motion.
- [x] Add focused viewport entry/exit, persistence/dismissal, reduced-motion, and markup regression coverage; verify visual/functional behavior without obstructing vertical scroll, book touch input, preview controls, or checkout CTAs.

**Acceptance criteria:** cue displays over the book surface without intercepting input, activates only when visible and not previously interacted with, repeats until interaction, pauses/resumes with visibility, disappears on interaction, and remains static and accessibly described for reduced motion. Preview controls remain fully user-controlled. Python and Node tests plus available viewport checks pass; no checkout is clicked.

**Dependency:** T1; retain original interactive preview.

**Route and trigger evidence:** delegated direct writer; behavior touches the JavaScript lifecycle, preview markup/styles, and Node/Python regression tests, all non-trivial; preparation and implementation are performed by the single writer.

**Delivery forecast:** Final pre-commit `git diff --numstat main` reports 375 authored changed lines cumulatively for T1+T2, including the tracked feature document, below the advisory ~400-line threshold. This T2 work unit closed below the threshold. The user later explicitly approved a `size:exception` for the full reference-inspired redesign as one PR; this does not authorize PR creation, push, merge, or deploy.

**Progress / verification:** RED before production changes: Node preview lifecycle — 2 expected failures; focused Python suite — 1 expected cue-markup failure. GREEN: `node --test tests/test_preview_swipe_cue.js` — 4 passed; `python3 -m unittest discover -s tests -v` — 7 passed; `git diff --check` — passed. Browser checks at 320 / 390 / 1280 px showed no horizontal overflow (document widths 305 / 375 / 1265 px); at 320 and 390 the repeating cue is visible over the book with the static instruction and clear of the sticky CTA/controls, and desktop preview view shows the cue over the cover. CSS/DOM readback confirmed `pointer-events:none` and a repeating 1.8s animation. Clicking only the functional “Abrir la muestra” control advanced to page 2 and dismissed the cue; no checkout was clicked. Reduced-motion static instruction is covered by the Python markup check and Node preference lifecycle test.

**Commit evidence:** `9d2290806f11ccf0e744c1373f613cb0278a9c95` — `feat(preview): add persistent swipe affordance` on `codex/reference-inspired-ebook-landing`.

### T3 — Generated Arturo-with-book visual

- [x] Inspect `assets/arturo-modoverbo.png` as the identity reference and `assets/cover.webp` as the cover reference; generate a new editorial/illustrative portrait of Arturo holding this book with the existing Modo Verbo palette. Do not invent title text, endorsements, ratings, promises, or unrelated props; preserve the cover design and inspect title/face/hands before selection.
- [x] Save the selected asset under a new descriptive path in `assets/`; never overwrite either reference. Integrate it only in the deeper author section. Preserve `assets/arturo-modoverbo.png` in the first-screen hero.
- [x] Add meaningful Spanish alt text and a visible caption identifying the image as an AI-generated illustration, not a documentary photograph.
- [x] Add a focused regression test covering local asset existence, generated-image alt/caption, and the original hero portrait source.
- [x] Check responsive behavior for 320px, 390px, and 1280px when available; if exact viewports are unavailable, record that limitation honestly and verify the image/CSS aspect-ratio relationship.

**Acceptance criteria:** generated asset is an illustrative enhancement based on the supplied identity and cover references; title, face, and hands are visually acceptable; it appears only in the deeper author section with an accurate visible generated/illustrative disclosure; original circular portrait remains the hero image. Python and Node suites, `git diff --check`, and available responsive crop checks pass. Generated binary image is excluded from authored-line delivery totals.

**Dependency:** T1. Do not modify the original portrait source.

**Route and trigger evidence:** delegated direct writer; requires image generation plus non-trivial markup, style, and regression-test changes.

**Progress / verification:** T3 complete. RED: focused `test_generated_author_book_illustration_is_disclosed_and_hero_keeps_original_portrait` failed before HTML/CSS changes because the deeper author image was not present. GREEN: `python3 -m unittest discover -s tests -p 'test_author_section.py' -v` — 8 passed; full Python suite — 8 passed; `node --test tests/test_preview_swipe_cue.js` — 4 passed; `git diff --check` — passed. Generated asset visually inspected at 1122×1402: Arturo likeness, complete cover, and hands are acceptable; the existing cover title/design are recognizable and no extra endorsement/rating text or props were introduced. A local browser load exposed the intended alt and disclosure caption in the accessibility tree. Exact 320 / 390 / 1280 viewport crops were not available through this browser surface; the image ratio is 1122:1402 (0.8003), effectively matching the CSS `aspect-ratio:4/5` (0.8), and `height:auto` preserves intrinsic proportions without an intentional crop. No checkout was clicked. Cumulative authored diff against `main` is 427 lines (generated PNG excluded). The user explicitly approved a `size:exception` for this new redesign as one PR; this only resolves the size threshold and does not authorize PR creation, push, merge, or deploy.

**Responsive QA follow-up:** A later review observed the light caption text crossing the yellow rotated author-photo background at 320px and 390px. Added a dark `var(--ink)` caption surface with `var(--paper)` text and padding; the focused regression test fails before this CSS and passes after it. Full Python suite — 12 passed; Node preview suite — 4 passed; `git diff --check` — passed. Parent's post-fix read-only browser measurements at 320 / 390 / 1280px report viewport inner widths 320 / 390 / 1280 and document scroll widths 305 / 375 / 1265, with no horizontal overflow. Caption computed background is `rgb(38, 40, 35)` and text is `rgb(249, 246, 237)` at all three sizes. The illustration's natural dimensions are 1122 × 1402; displayed sizes are 208 × 260, 263 × 329, and 364 × 455 respectively, preserving approximately 4:5. These are DOM/computed-style measurements, not post-fix screenshot evidence: the attempted hash-anchor smooth scroll was erratic, so no post-fix screenshot is claimed. No changes to the illustration or section layout.

**Responsive caption correction commit:** `f2cf2f9630bd06266944c78f077f9238bbb0f821` — `fix(landing): improve generated image caption contrast`.

**Commit evidence:** `db5016cb0750f97d98c80485381d1695ab1f3bb0` — `feat(landing): add disclosed author book illustration` on `codex/reference-inspired-ebook-landing`.

### T4 — Attributable testimonial content (blocked)

- [ ] Add review cards or quotes only after the owner supplies real attributable customer wording and explicit permission/context to identify and publish it.
- [ ] Do not add ratings, counts, stars, avatars/photos, outcomes, or endorsements without matching authorized source evidence.
- [x] Keep T4 blocked and display no testimonial content until the evidence is supplied; the T9 neutral empty state is not social proof.

**Acceptance criteria:** every displayed quote/card is attributable to supplied source material and permission and is not embellished; no invented stars, ratings, counts, people, images, or outcome claims.

**Dependency:** real approved testimonial material from the owner. This content task remains blocked until supplied; T9 may add only a truthful, empty review destination without it.

### T5 — Remaining reference-inspired section flow

- [x] Confirm the existing order follows hero → problem → method → preview/content → fit → offer → deeper author → FAQ → closing CTA; retain the real testimonial section as omitted until attributable material is supplied.
- [x] Add stable IDs to each major landing section, preserve all existing IDs, and ensure in-page links resolve.
- [x] Add consistent opening and closing sequence markers (`01 /` and `10 /`) while preserving the numbered section kickers between them.
- [x] Keep all purchase links on the same checkout destination, retain functional preview navigation, and prevent competing secondary marketing CTAs.

**Acceptance criteria:** visitors can follow the adapted hero → problem → method/content → offer → (real testimonials only, omitted until supplied) → deeper author → FAQ → closing CTA flow; stable internal section IDs are unique and all in-page links resolve; the interactive preview controls remain usable and all purchase links retain one label and target.

**Dependency:** T1; T4 remains blocked on genuine attributable customer quotes and permission/context, so no testimonial section or social-proof content is displayed.

**Route and trigger evidence:** delegated direct writer; preparation spanned section markup, page anchors, and structural tests, with two non-trivial files changed.

**Progress / verification:** T5 complete. RED before the markup edits: focused `python3 -m unittest discover -s tests -p 'test_author_section.py' -v` failed as expected because the hero and closing sections lacked sequence numbers and three landing sections lacked stable IDs; the no-testimonials regression passed. GREEN after markup changes: focused author/structure suite — 11 passed; full Python suite — 11 passed; `node --test tests/test_preview_swipe_cue.js` — 4 passed; `git diff --check` — passed. Existing source order already matched the requested hierarchy, so no unnecessary reorder was made. Added IDs `reconocimiento`, `para-ti`, and `cierre`, plus sequence markers `01 /` and `10 /`; existing preview IDs, controls, CTA label/destination, and no-secondary-marketing-CTA policy remain unchanged. Browser accessibility-tree inspection confirmed the full order, all purchase links point to the same Hotmart URL, the preview controls remain present, and no testimonial section is rendered. The available local browser screenshot showed the refreshed hero, circular Arturo portrait, and unchanged brand treatment. This CUA surface did not expose a viewport override, so exact 320px / 390px / 1280px visual checks remain unavailable and are not claimed as passed. No checkout was clicked.

**Responsive QA follow-up:** The caption-contrast issue discovered at 320px and 390px in the deeper author section is recorded under T3 and corrected with a dark caption surface. Parent's post-fix read-only DOM/computed-style measurements at 320px / 390px / 1280px confirm no horizontal overflow and the expected caption colors; exact dimensions and the screenshot limitation are recorded under T3.

**Commit evidence:** `fbf91aca9d8133648f1d66dcb7f73c091fc435d2` — `feat(landing): complete reference-inspired section flow` on `codex/reference-inspired-ebook-landing`.

### T6 — Corrected cover and interactive preview asset refresh

- [x] Use the corrected final 156-page PDF at `../ebook-elocuencia-sin-miedo/output/pdf/Elocuencia sin miedo - Verde y oro - Portada corregida.pdf` as the source of truth; confirm page count and render its cover plus pages 1–13 into optimized, accurately ordered local assets.
- [x] Import the supplied flat-cover, 3D mockup, and Arturo-holding-the-book images from `/home/julian/Descargas/` into descriptive repository assets without altering unrelated original portrait or generated-author assets.
- [x] Replace the existing preview page assets and offer/cover references with the refreshed corrected-edition assets; keep all asset references local and ensure the digital ebook offer remains clearly digital (no physical-product implication).
- [x] Preserve StPageFlip, all existing preview DOM IDs/controls, persistent gesture cue, reduced-motion behavior, and user-controlled interaction.
- [x] Add failing-first regression coverage for corrected cover/page assets, ordered 13-page preview references, image existence, and retained preview interaction.

**Acceptance criteria:** rendered assets demonstrably come from the final corrected 156-page PDF, include cover and pages 1–13 in correct order, have appropriate optimized dimensions/format without visible degradation, and load locally through the current offer/preview references. No physical-copy promise, invented price, discount, testimonial, or rating is introduced. Run `python3 -m unittest discover -s tests -v`, `node --test tests/test_preview_swipe_cue.js`, and `git diff --check`; document generated filenames and sizes.

**Dependency:** T1–T5; source PDF and supplied images are user-provided inputs. T7 consumes the imported Arturo image for the green-gold hero restyle.

**Route and trigger evidence:** delegated direct writer; PDF rendering/asset optimization, HTML asset wiring, regression tests, and this task record span multiple files and need source preparation.

**Progress / verification:** T6 complete. RED before production edits: `python3 -m unittest discover -s tests -p 'test_author_section.py' -k corrected_edition -v` failed because `assets/edition/preview-manifest.json` did not yet exist. GREEN after wiring the corrected assets: focused regression passed; `python3 -m unittest discover -s tests -v` — 13 passed; `node --test tests/test_preview_swipe_cue.js` — 4 passed; `git diff --check` — passed. `pdfinfo` confirmed the source PDF contains 156 pages at 540 × 720 pt. The first 13 PDF pages (cover included) were rendered at 900 × 1200 and visually inspected at representative pages (cover, page 6, page 13); the resulting WebP assets are locally referenced in the existing cover/preview/zoom/inside/offer markup. The preview manifest preserves PDF-page mapping 1–13, including the cover as page 1. Supplied product photos are preserved as local optimized WebP assets for T7. Existing page 14 blurred lock panel, StPageFlip initialization and page limits, DOM IDs, gesture cue, reduced-motion behavior, and user controls were not changed. The offer already clearly states “Ebook digital en PDF”; no physical-product language or new commercial claims were added. Browser viewport visual checks were not run for this asset-only task; no browser result is claimed. No checkout was clicked.


**Interactive preview browser follow-up:** Parent verified at 390px by scrolling to the preview controls and activating only the functional “Abrir la muestra” control (no checkout). The corrected PDF's page 2 appeared visually; `#preview-counter` read “Página 2 de 156”; `.preview-swipe-cue` had class `is-dismissed`; only `.preview-page[data-page="2"]` was visible; and the fixed purchase bar remained hidden around the controls. This complements the earlier asset/page mapping verification with direct browser interaction evidence. No checkout was clicked.

**New asset sizes:** `assets/edition/cover.webp` — 309,510 bytes; `page-02.webp` — 64,728; `page-03.webp` — 57,590; `page-04.webp` — 49,926; `page-05.webp` — 36,332; `page-06.webp` — 122,960; `page-07.webp` — 96,154; `page-08.webp` — 126,422; `page-09.webp` — 113,018; `page-10.webp` — 118,138; `page-11.webp` — 82,056; `page-12.webp` — 60,558; `page-13.webp` — 125,228; `cover-flat-reference.webp` — 441,100; `cover-mockup.webp` — 290,876; `arturo-holding-book.webp` — 208,476. All rendered edition pages are 900 × 1200; supplied source assets retain their native pixel dimensions. Manifest: `assets/edition/preview-manifest.json`.

**Commit evidence:** `736d14726717e1de9b244c452699a98d0a30963a` — `feat(preview): refresh assets from corrected ebook edition` on `codex/reference-inspired-ebook-landing`.

### T7 — Green-gold visual identity and Arturo hero

- [x] Inspect the supplied ebook brand-kit board at `../ebook-elocuencia-sin-miedo/assets/reference/brand-kit.png`; ground the landing palette and type choices in its documented swatches and examples: Verde Petróleo `#0F3D3A`, Verde Bosque `#174236`, Dorado Editorial `#D4AF37`, Marfil `#F8F6EF`, Gris Piedra `#A7A29A`, Negro Suave `#1A1A1A`; Playfair Display headlines and Montserrat body text.
- [x] Replace the landing's legacy bright-yellow/Poppins identity with the new green/gold editorial system across the hero, header, problem/method/content sections, preview, offer card, deeper author section, FAQ, closing CTA, and footer. Load the approved font families with sensible fallbacks and `font-display: swap`.
- [x] Restructure only the hero presentation: compact author identification, a benefit-led headline, supporting Spanish copy, one existing checkout CTA, and the supplied `assets/edition/arturo-holding-book.webp` as the prominent first-screen visual in an elegant arch/frame. Use descriptive, non-documentary alt text; do not imply the ebook purchase includes a physical copy.
- [x] Keep the original neutral `assets/arturo-modoverbo.png` for the deeper author section and remove the previously generated old-cover illustration/caption from the visible landing.
- [x] Correct stale cover alt text to describe the actual corrected green/gold book cover. Keep the existing digital-PDF label on the offer/mockup.
- [x] Preserve the T6 cover/page asset mapping, preview interactivity and controls, all CTA wording/destination, owner-provided offer terms, section order, and testimonial omission. Do not add ratings, quotes, endorsements, customer counts, or unsupported claims.
- [x] Add failing-first regression coverage for new brand tokens/fonts, supplied hero image and accurate alt, absence of the old-cover illustration and legacy font/bright-yellow tokens, unchanged digital offer / corrected preview invariants, and preview-caption spacing.

**Acceptance criteria:** the supplied brand-kit board grounds the visual system; the first screen identifies Arturo and features the supplied book-holding image; green/gold colors and Playfair Display/Montserrat are coherent across every major section with contrast and fallback typography; old Poppins/bright-yellow and the old-cover generated author image are no longer part of visible landing markup/styles. CTA label/destination, owner offer terms, corrected cover and preview page order/behavior, and section order remain unchanged. No physical-copy promise, invented price, rating, quote, or endorsement is added. Validate at 320px / 390px / 1280px where browser tooling permits; otherwise record that limitation for parent QA. Run `python3 -m unittest discover -s tests -v`, `node --test tests/test_preview_swipe_cue.js`, and `git diff --check`.

**Dependency:** T6 corrected edition assets and supplied brand/image references.

**Route and trigger evidence:** delegated direct writer; restyling spans non-trivial HTML, global/section CSS, focused regression tests, and task evidence.

**Progress / verification:** T7 implementation complete. The inspected brand-kit board supplied the six approved colors and Playfair Display/Montserrat pairing. Hero now introduces Arturo compactly and features the supplied 1536×1024 Arturo-with-book image in a gold arch; headline and supporting Spanish copy are benefit-led. The original neutral portrait remains in the deeper author section; the old generated illustration/caption was removed. Section palettes, offer card, preview, footer and controls use the green/gold/cream system; the offer mockup is explicitly labeled “EBOOK DIGITAL · PDF · 156 PÁGINAS” and retains the owner-provided terms. No numeric price, fake review, rating, endorsement, or physical-copy promise was added. CTA label/Hotmart target, 13 corrected PDF page assets, preview IDs/controls, section order and testimonial omission remain intact.

RED was observed first for brand/hero assertions before source edits (expected missing palette/font tokens and supplied hero image); the hero test also failed on DOM order before its responsive image-first structure was implemented. Browser review of the available desktop view exposed the preview chapter label and page counter running together; the new focused caption-layout test failed before its CSS rule, then passed after adding a 12px flex gap. A corrected T6 regression assertion now accommodates the T7 offer mockup replacing the old cover image, while still checking cover presence in preview and zoom references. GREEN: `python3 -m unittest discover -s tests -p 'test_author_section.py' -v` — 15 passed; `python3 -m unittest discover -s tests -v` — 15 passed; `node --test tests/test_preview_swipe_cue.js` — 4 passed; `git diff --check` — passed. Browser visual inspection used the available desktop screenshot (~1264×890, not an exact 1280 override): hero/arch and supplied cover image rendered; preview page/controls rendered; caption and page counter are separated. Exact 320px / 390px / 1280px viewport overrides were unavailable in this browser control surface; parent responsive QA remains pending. Runtime harness: local-browser visual check, no checkout click. Rollback boundary: revert T7 changes to `index.html`, `styles.css`, and `tests/test_author_section.py`; corrected edition assets and T6 preview lifecycle remain unchanged. No checkout was clicked.

**Commit evidence:** `441840d49146208a21aa4e76dd7cae3680b37120` — `feat(landing): apply green-gold editorial identity` on `codex/reference-inspired-ebook-landing`.

**Responsive QA follow-up:** Parent's exact viewport checks verified 320px / 390px / 1280px document scroll widths of 305px / 375px / 1265px respectively, with no horizontal overflow. At each top viewport the green-gold Arturo hero/CTA is visible; the site header is sticky, the owner-terms strip is in normal flow, and the purchase bar is `display:none` while the hero is visible. Screenshots were captured for 320px top, after-hero, preview-controls and footer states, 390px / 1280px top, and desktop post-scroll; not every measured state has a screenshot. This supersedes the earlier pending exact viewport note. No checkout was clicked.

### T8 — Sticky navigation and post-hero purchase bar

- [x] Add a top offer strip in normal document flow with only the owner-provided digital ebook terms (payment once, immediate access, 7-day guarantee); never invent price/discount or imply a physical copy. Make the header sticky beneath/after the strip so the strip scrolls away.
- [x] Keep the bottom purchase bar hidden/inert while the hero is visible, show it after the hero exits on both desktop and mobile, and hide it again on reverse scroll. Respect keyboard focus when hiding, accessibility tree state, and prefers-reduced-motion.
- [x] Suppress the bottom bar while preview controls or footer content are in view; preserve page/footer access in the viewport lifecycle behavior.
- [x] Confirm in browser at 320px / 390px / 1280px that the responsive bar does not cover controls/footer or introduce horizontal overflow.
- [x] Reuse the exact existing purchase CTA label and destination; preserve preview/navigation links and controls. Do not add social proof, checkout clicks, or unrelated T9 work.
- [x] Add failing-first Python structure/style and Node lifecycle tests for top-strip/header order, hero visibility state, reverse scroll, preview/footer suppression, focus transfer/inert state, reduced motion, and consistent purchase destination/label.

**Acceptance criteria:** the offer strip scrolls away normally and contains only the owner-provided ebook terms; header remains sticky after the strip scrolls away; the purchase bar is absent/inert during hero visibility, appears after hero exit on desktop and mobile, hides on reverse scroll and while preview controls/footer are in view, and never hides a focused action without an accessible focus destination. Reduced motion disables the bar transition. The exact purchase label and Hotmart URL stay consistent, preview controls still work, and no content/footer/control is obstructed or horizontally overflowed at 320px / 390px / 1280px. Run full Python/Node suites and `git diff --check`; do not click checkout.

**Dependency:** T6–T7.

**Route and trigger evidence:** delegated direct writer; sticky and viewport lifecycle behavior involves markup, styles, JavaScript, responsive and accessibility regression coverage.


**Progress / verification:** T8 implementation and automated checks are complete; exact viewport/browser QA is pending parent verification. Added the owner-term strip in document flow and made the site header sticky; the strip itself has no invented price or discount. The checkout bar begins `hidden`, `inert`, and `aria-hidden`, becomes available only after the hero exits and both protected-region IntersectionObserver states are known and outside view, and hides while preview controls or footer are visible. A scroll/resize geometry fallback is used without IntersectionObserver. When suppression would hide a focused bar action, focus moves without scrolling to the visible hero CTA, preview “Abrir libro” control, or footer checkout CTA as applicable. CSS disables its transition for reduced-motion users, and the mobile bar uses a grid layout to preserve its two-column treatment.

TDD evidence: RED was observed in the focused Node lifecycle suite when it showed the bar before the protected regions had initial viewport state and when focus incorrectly returned to the hero CTA instead of the visible preview control. After implementation, focused Node lifecycle suite — 4 passed. The existing preview Node suite needed its fake DOM expanded to model the new shared page-visibility watcher; after adapting that harness, `node --test tests/test_preview_swipe_cue.js` — 4 passed. Python markup assertions initially encoded pre-T8 mobile markup/reduced-motion structure; they were updated to assert the current hidden/inert bar, responsive layout and reduced-motion behavior. GREEN: `python3 -m unittest discover -s tests -v` — 16 passed; `node --test tests/test_preview_swipe_cue.js` — 4 passed; `node --test tests/test_post_hero_purchase_bar.js` — 4 passed; `git diff --check` — passed. CTA label and Hotmart destination remain consistent; no checkout clicked, no T9/social-proof content added. This worker could not access an available browser surface for 320px / 390px / 1280px screenshot/visual validation; parent visual measurements remain pending and are not claimed as passed.

**Commit evidence:** `521e8a61616ebdbdcf8fa40d41d78545381846ab` — `feat(landing): add accessible post-hero purchase bar` on `codex/reference-inspired-ebook-landing`.

**Parent responsive QA follow-up:** At 320px / 390px / 1280px, document scroll widths were 305px / 375px / 1265px (no horizontal overflow). On initial hero view the bottom purchase bar is `display:none`; the terms strip remains in normal flow and the sticky header stays at top 0. At 320px after scrolling two pages, hero bottom was -600, terms strip bottom -1432, header top 0, and the bar used `display:grid` at y=672 with height 68px without covering content. When preview controls were visible (top 295 / bottom 339), the bar was `aria-hidden=true` / `display:none`; when footer was visible at y=448, the bar was likewise hidden. At 390px after scroll the bar used grid and header remained top 0; pressing Home returned `scrollY=0` and hid the bar. At 1280px after scroll the bar used `display:flex` at y=706, with header top 0 and no overflow. Screenshots exist for 320px top / after-hero / preview-controls / footer, 390px and 1280px top, plus desktop post-scroll; screenshots were not captured for every measured state. The first desktop scroll started from a preview hash state, but the observed header/bar state was valid. No checkout was clicked.

### T9 — Truthful reader-opinions link and empty state

- [x] Add a neutral, non-purchase hero text link/pill labeled “Opiniones de lectores” that targets a real local `#resenas` section; do not style or describe it as a competing checkout CTA.
- [x] Insert the section after the offer and before the deeper author section, with a truthful empty state saying reviews for this edition will be shown only when publishable content and authorization are confirmed; make clear no reviews are currently shown.
- [x] Add an accessible heading/anchor target with focus support and scroll margin beneath the sticky header; preserve the existing section order, primary CTA label/destination, offer terms, and preview/sticky behavior.
- [x] Add failing-first structural assertions for link/target/order/empty-state copy, absence of ratings/quotes/counts/photos, and accessible in-page navigation.
- [x] Keep real review cards/quotes blocked under T4 until the owner supplies attributable source wording and permission/context; do not invent ratings, quotes, buyers, photos, counts, or outcomes.

**Acceptance criteria:** the hero link resolves to an in-page `#resenas` empty-state section after the offer and before the author; the copy clearly communicates that no reviews are displayed yet and that only authorized, publishable material may appear. No fake or implied existing reviews, rating, star display, count, quote, person, photo, or endorsement appears. The text link is subordinate to and distinct from the existing checkout CTA. The anchor is keyboard-accessible, named by its heading, focused/landed accessibly, and not obscured by the sticky header. Existing section anchors, offer terms, preview controls/cue, sticky purchase bar, and purchase CTA label/destination remain unchanged.

**Dependency:** current T6–T8 implementation. Genuine attributable review material and permission/context remain a separate T4 dependency and are not required for this truthful empty state.

**Route and trigger evidence:** delegated direct writer; update spans hero markup, section structure, anchor styles, focused regression tests, and task evidence.

**Progress / verification:** T9 implementation complete. RED before source edits: `python3 -m unittest discover -s tests -p 'test_author_section.py' -k reader_opinions -v` failed because the hero review link did not exist; the focused section-flow test also failed because the `reviews` section was absent. GREEN: `python3 -m unittest discover -s tests -v` — 17 passed; `node --test tests/test_preview_swipe_cue.js` — 4 passed; `node --test tests/test_post_hero_purchase_bar.js` — 4 passed; `git diff --check` — passed. Added the non-button hero text link and a local `#resenas` section after offer and before author, with explicit no-reviews-yet and authorization wording, a named heading, `tabindex=-1`, `scroll-margin-top`, and visible focus styling. Updated subsequent section numbers through `11 /`; all internal links resolve, the purchase CTA label/target and T6–T8 preview/sticky behavior are unchanged, and no ratings, quote cards, buyer photos, counts, or endorsements are present. Real testimonials remain blocked under T4. Browser UI could not be attached for local visual verification (Brave and in-app browser unavailable to this worker); no visual/browser click is claimed. No checkout was clicked.

**Commit evidence:** `1c506934e0e1d988eaa263b93afd0d7eb3a836d9` — `feat(landing): add truthful reader opinions section` on `codex/reference-inspired-ebook-landing`.

**Parent browser QA follow-up (390px):** Confirmed the hero link “Opiniones de lectores ↓” and the `#resenas` section are present, with no star glyphs. Clicking only the in-page review link changed the URL hash to `#resenas`; the section began 112px below the sticky header bottom at 69px, and its text explicitly states that no reviews are shown without source/permission. The screenshot confirmed the truthful empty state; the bottom purchase bar remained visible without covering section text. Document scroll width was 375px at a 390px viewport, with no horizontal overflow. This is parent-provided browser evidence; no checkout was clicked.

**QA documentation commit:** `7ca715c86e55f9a77d3d4383b802aadb3aadd9a3` — `docs(odd): record reader opinions browser QA`.

## User-feedback correction record (2026-09-25)

The user rejected the prior T7/T8/T9 presentation despite recorded responsive/browser checks. Preserve those records as historical evidence, but treat the page-level visual conclusions in the T7 and T8 QA notes and the T9 empty-state QA as superseded for the requested redesign. The implementation defect is that non-preview edition images carried fixed 900×1200 attributes while global CSS only constrained width, allowing their intrinsic 1200px height to overflow 315px containers; fixed image frames and the mini-book also permitted overflow. The resulting image pile-up obscured section boundaries and collided with the footer. The site header hid its purchase CTA on mobile, and the first hero portrait did not match the requested original solo portrait. T10 replaces the broad landing presentation while retaining preview behavior and existing honest commercial claims. No testimonial/review section or hero opinions link remains until genuine publishable content is supplied.

## T10 — Rebuild coherent reference-inspired landing structure

- [x] Rebuild the sales-page markup and styles as a coherent hierarchy matching the supplied reference structure; remove broken overlapping art grids rather than layering compensating CSS overrides.
- [x] Restore the compact centered first screen: original solo Arturo portrait (`assets/arturo-modoverbo.png`) cropped circularly without black square corners; visible gold frame and `Arturo Valdéz` caption; warm ivory centered Playfair headline with restrained italic green emphasis; concise supporting copy; one broad green/gold `Quiero hablar con claridad` checkout CTA; owner-provided payment/access/7-day terms beneath. Remove the large portrait-book hero, two-column/dark hero, opinions link, and any fabricated social proof.
- [x] Keep a thin dark terms strip in normal flow and sticky ivory logo/header with compact checkout CTA at every breakpoint, including 320px; wrap/reflow its text instead of hiding the CTA.
- [x] Follow the reference sequence with restrained fact band (156 pages, PDF, practical exercises, 7-day terms only), problem, four fine-gold method cards, brief editorial dark statement band (not attributed as a quote), benefits/content, preserved preview, proportional offer card/mockup, deeper author section, FAQ, centered closing CTA, simple dark stacked footer.
- [x] Use supplied book mockup proportionally in the offer and supplied `assets/edition/arturo-holding-book.webp` later in author section. All non-preview images preserve natural aspect ratio with responsive dimensions; dedicated StPageFlip page sizing remains untouched.
- [x] Omit `#resenas`, reader opinions links, and any reviews section while no genuine attributable review source and permission exist. Remove secondary marketing buttons such as “Ver muestra”/“Explorar”; preserve functional preview controls.
- [x] Preserve exact Hotmart URL `https://pay.hotmart.com/H107735669O?checkoutMode=2&off=s5txzdcx`, repeated primary CTA text, owner-provided one-time payment/immediate access/7-day guarantee, 156-page PDF claim, all 13 corrected preview pages plus lock page, StPageFlip settings, zoom, keyboard/touch behavior, persistent non-intercepting cue, reduced-motion support, post-hero purchase bar and its preview/footer/focus suppression behavior.
- [x] Add failing-first regression coverage for solo first-screen portrait and later holding image; sticky mobile header CTA; missing testimonial/review/secondary marketing content; responsive non-preview image sizing and non-overlapping footer; reference sequence; CTA/terms; unchanged preview integrity and purchase-bar lifecycle.

**Authorization/configuration:** User explicitly authorized this corrective rebuild on `codex/reference-inspired-ebook-landing`; no further approval is needed. Direct delegated single-writer route because rebuilding the markup, styles, and tests spans multiple non-trivial files. Strict TDD is enabled by workspace instructions (RED → GREEN → REFACTOR). RDD is disabled; do not run or enable it. Delivery remains `single-pr` with previously approved `size:exception`; no PR, push, merge, checkout click, or deploy. No remote operation is authorized.

**Acceptance criteria:** the landing has a restrained centered portrait-led first screen and coherent reference-inspired section sequence, with no oversized image overlap or footer collision, no hidden mobile header CTA at 320px, and no fabricated reviews or proof. All non-preview imagery remains proportional; StPageFlip's own page dimensions and all preview interactions remain intact. The same Hotmart path and owner-provided terms are retained with no numeric price, discount, unprovided bonus, urgency, or credential. Functional checks pass. Parent performs required browser QA at 320×740, 390×844, 384×824, and 1280×800 for every section and interactive preview; this task must leave that visual QA pending until parent reports it.

**Route and trigger evidence:** delegated direct writer; T10 touches multiple non-trivial markup/style/test files and combines source preparation with implementation.

**Progress / verification:** Implemented a centered solo-portrait hero using `assets/arturo-modoverbo.png`, a sticky ivory logo/header with its checkout CTA always present, restrained fact/problem/four-card method/statement/preview/content/offer/author/FAQ/closing/footer flow, proportional supplied mockup and later Arturo-with-book image, and a simple stacked footer. Removed the hero reviews link and empty review section. Rebuilt global CSS so all ordinary images use `max-width:100%; height:auto`; StPageFlip images retain their dedicated page width/height/object-fit rules. Preserved all preview IDs, 13 corrected edition pages plus the lock page, controls, zoom, cue/reduced-motion behavior, Hotmart URL, and post-hero bar lifecycle. RED: `python3 -m unittest discover -s tests -p 'test_author_section.py' -v` failed against the pre-rebuild markup with 7 failures and 2 errors, including the missing solo hero portrait, absent new section flow, and old opinion section. GREEN: `python3 -m unittest discover -s tests -v` — 19 passed; `node --test tests/test_preview_swipe_cue.js tests/test_post_hero_purchase_bar.js` — 8 passed; `git diff --check` — passed. Current diff is 883 authored additions plus deletions, including the task document; previously approved `single-pr`/`size:exception` applies. No checkout click, RDD, remote operation, PR, push, or deployment. Parent browser QA remains pending at 320×740, 390×844, 384×824, and 1280×800 across all sections and the interactive preview; no visual success claim is made here. Preserve T7/T8/T9 QA statements above as history only; do not use them to claim the new layout is visually validated.

**Commit evidence:** `169657c88e293516e868ee8c554e902e5a5cdba4` — `feat(landing): rebuild reference-inspired sales page` on `codex/reference-inspired-ebook-landing`.

## T10 cache-busting corrective follow-up (2026-09-25)

**Cause and scope:** Parent browser QA observed fresh HTML paired with the prior cached stylesheet in the already-open IAB tab. At 384px, that stale CSS hid the mobile header CTA and retained distorted portrait sizing. This follow-up changes only stylesheet cache identity plus its regression guard; no layout changes are included.

**RED:** `python3 -m unittest discover -s tests -p 'test_author_section.py' -k stylesheet_url -v` — failed as expected because `index.html` used an unversioned `styles.css` URL.

**GREEN:** Changed the landing stylesheet href to `styles.css?v=20260925-reference-v2`. `python3 -m unittest discover -s tests -v` — 20 passed; `node --test tests/test_preview_swipe_cue.js tests/test_post_hero_purchase_bar.js` — 8 passed; `git diff --check` — passed. Parent owns browser revalidation; this follow-up makes no visual QA claim.

**Commit evidence:** `bd7ec48752a579ad3af2bba7fd4ed86ab3f0f599` — `fix(landing): bust stale stylesheet cache` on `codex/reference-inspired-ebook-landing`.

## Next step

T10 implementation and functional checks are complete; close it with a Conventional Commit after final readback. Parent must verify the visual layout and preview at 320×740, 390×844, 384×824, and 1280×800 before treating the redesign as visually validated. T4 remains blocked until genuine attributable testimonial source wording and permission/context are supplied. The approved single-PR size exception authorizes no PR, push, merge, checkout click, or deployment.
