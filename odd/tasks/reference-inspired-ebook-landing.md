# Reference-inspired ebook sales landing

Redesign the Elocuencia sin miedo sales page around a clearer first-screen value proposition and one repeated checkout path, while retaining its dark, cream, and yellow Modo Verbo identity and working interactive preview.

## Objective and problem

The current landing needs a stronger sales hierarchy inspired by the flow of srluizferraz.com without copying its text, claims, price, testimonials, rating, person, or visual identity. Arturo must remain visibly identified on the first screen even as deeper content follows a clearer sales-page sequence.

## Scope and constraints

- Feature identity: `reference-inspired-ebook-landing`.
- Authorized scope: first-screen structure/copy, consistent purchase-CTA placement, product offer card, later section ordering, preview-open/touch feedback, generated Arturo-with-book asset, and testimonial presentation only when real attributable testimonials are supplied.
- Keep the existing Modo Verbo dark/cream/yellow brand and preserve interactive book controls and existing checkout target.
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

**Commit evidence:** `db5016cb0750f97d98c80485381d1695ab1f3bb0` — `feat(landing): add disclosed author book illustration` on `codex/reference-inspired-ebook-landing`.

### T4 — Real testimonial presentation

- [ ] Add testimonial cards only after the owner supplies real attributable customer quotes and permission/context to identify them.
- [ ] Until that evidence is supplied, leave the testimonial section absent or a non-testimonial placeholder; never fabricate social proof.

**Acceptance criteria:** each displayed quote is attributable to supplied source material and is not embellished; no invented stars, ratings, counts, or outcome claims.

**Dependency:** real approved testimonial material from the owner. This task is blocked until that material is supplied; do not ask during T1.

### T5 — Remaining reference-inspired section flow

- [ ] Reorder existing problem, method/content, offer, deeper author, FAQ, and closing conversion content to follow the reference-inspired sequence while preserving the original book-preview interaction and stable navigation targets.
- [ ] Keep all new or repeated purchase links on the same checkout destination and prevent competing secondary marketing CTAs.

**Acceptance criteria:** visitors can follow the adapted hero → problem → method/content → offer → (real testimonials only) → deeper author → FAQ/closing CTA flow; internal navigation IDs remain valid and existing interactive book preview remains usable.

**Dependency:** T1 and T4 evidence availability; T4 content may be omitted if not supplied.

## Next step

T1–T3 are committed. T3’s exact responsive viewport crops were unavailable; its CSS/intrinsic ratio evidence is recorded above. The user approved `single-pr` with a `size:exception` for this new feature. T5 remains; T4 depends on real attributable testimonial material. No PR, push, merge, or deployment is authorized.
