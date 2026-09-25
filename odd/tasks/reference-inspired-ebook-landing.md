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

### T4 — Real testimonial presentation

- [ ] Add testimonial cards only after the owner supplies real attributable customer quotes and permission/context to identify them.
- [ ] Until that evidence is supplied, leave the testimonial section absent or a non-testimonial placeholder; never fabricate social proof.

**Acceptance criteria:** each displayed quote is attributable to supplied source material and is not embellished; no invented stars, ratings, counts, or outcome claims.

**Dependency:** real approved testimonial material from the owner. This task is blocked until that material is supplied; do not ask during T1.

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

### T8 — Sticky navigation and post-hero purchase bar

- [x] Add a top offer strip in normal document flow with only the owner-provided digital ebook terms (payment once, immediate access, 7-day guarantee); never invent price/discount or imply a physical copy. Make the header sticky beneath/after the strip so the strip scrolls away.
- [x] Keep the bottom purchase bar hidden/inert while the hero is visible, show it after the hero exits on both desktop and mobile, and hide it again on reverse scroll. Respect keyboard focus when hiding, accessibility tree state, and prefers-reduced-motion.
- [x] Suppress the bottom bar while preview controls or footer content are in view; preserve page/footer access in the viewport lifecycle behavior.
- [ ] Confirm in browser at 320px / 390px / 1280px that the responsive bar does not cover controls/footer or introduce horizontal overflow (pending parent visual QA).
- [x] Reuse the exact existing purchase CTA label and destination; preserve preview/navigation links and controls. Do not add social proof, checkout clicks, or unrelated T9 work.
- [x] Add failing-first Python structure/style and Node lifecycle tests for top-strip/header order, hero visibility state, reverse scroll, preview/footer suppression, focus transfer/inert state, reduced motion, and consistent purchase destination/label.

**Acceptance criteria:** the offer strip scrolls away normally and contains only the owner-provided ebook terms; header remains sticky after the strip scrolls away; the purchase bar is absent/inert during hero visibility, appears after hero exit on desktop and mobile, hides on reverse scroll and while preview controls/footer are in view, and never hides a focused action without an accessible focus destination. Reduced motion disables the bar transition. The exact purchase label and Hotmart URL stay consistent, preview controls still work, and no content/footer/control is obstructed or horizontally overflowed at 320px / 390px / 1280px. Run full Python/Node suites and `git diff --check`; do not click checkout.

**Dependency:** T6–T7.

**Route and trigger evidence:** delegated direct writer; sticky and viewport lifecycle behavior involves markup, styles, JavaScript, responsive and accessibility regression coverage.


**Progress / verification:** T8 implementation and automated checks are complete; exact viewport/browser QA is pending parent verification. Added the owner-term strip in document flow and made the site header sticky; the strip itself has no invented price or discount. The checkout bar begins `hidden`, `inert`, and `aria-hidden`, becomes available only after the hero exits and both protected-region IntersectionObserver states are known and outside view, and hides while preview controls or footer are visible. A scroll/resize geometry fallback is used without IntersectionObserver. When suppression would hide a focused bar action, focus moves without scrolling to the visible hero CTA, preview “Abrir libro” control, or footer checkout CTA as applicable. CSS disables its transition for reduced-motion users, and the mobile bar uses a grid layout to preserve its two-column treatment.

TDD evidence: RED was observed in the focused Node lifecycle suite when it showed the bar before the protected regions had initial viewport state and when focus incorrectly returned to the hero CTA instead of the visible preview control. After implementation, focused Node lifecycle suite — 4 passed. The existing preview Node suite needed its fake DOM expanded to model the new shared page-visibility watcher; after adapting that harness, `node --test tests/test_preview_swipe_cue.js` — 4 passed. Python markup assertions initially encoded pre-T8 mobile markup/reduced-motion structure; they were updated to assert the current hidden/inert bar, responsive layout and reduced-motion behavior. GREEN: `python3 -m unittest discover -s tests -v` — 16 passed; `node --test tests/test_preview_swipe_cue.js` — 4 passed; `node --test tests/test_post_hero_purchase_bar.js` — 4 passed; `git diff --check` — passed. CTA label and Hotmart destination remain consistent; no checkout clicked, no T9/social-proof content added. This worker could not access an available browser surface for 320px / 390px / 1280px screenshot/visual validation; parent visual measurements remain pending and are not claimed as passed.

**Commit evidence:** pending work-unit commit.

### T9 — Evidence-backed review link or review section

- [ ] Add only a verified, owner-authorized review destination and/or supplied attributable review content; do not invent rating counts, stars, quotations, people, photos, or endorsements.
- [ ] If source and permission evidence are not available, keep the section omitted or use a neutral non-testimonial link only when its destination is verified and supplied; record the evidence for any displayed social proof.
- [ ] Keep any review action subordinate to the same primary purchase CTA and preserve privacy/accessibility expectations.

**Acceptance criteria:** every review link resolves to an owner-approved, verified destination; each displayed review item is attributable to supplied source evidence and permission/context. Otherwise, no review/social-proof claim is rendered. Run full Python/Node suites and `git diff --check`.

**Dependency:** verified review destination and, for any quotes/photos/ratings, real owner-supplied attributable content plus permission/context.

**Route and trigger evidence:** delegated direct writer; review-source validation and any resulting section/link need focused evidence and content regression tests.

## Next step

T1–T3, T5, and T6 are complete; T7 implementation and automated checks are complete, with exact responsive viewport QA pending parent verification. The caption contrast correction `f2cf2f9630bd06266944c78f077f9238bbb0f821` and parent's post-fix DOM/computed-style measurements at 320px / 390px / 1280px remain recorded under T3; no post-fix caption screenshot is claimed. T4 remains blocked until real attributable testimonial material and permission/context are supplied. T8 implementation and automated checks are prepared for work-unit commit; its 320px / 390px / 1280px browser QA is pending parent verification before T8 is fully closed. T9 remains dependent on verified, owner-approved review evidence/destination. The user approved `single-pr` with a `size:exception` for this feature; no PR, push, merge, or deployment is authorized.
