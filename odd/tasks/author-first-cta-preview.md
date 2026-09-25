# Author-first landing and preview discoverability

Move the Arturo author section ahead of the hero, strengthen primary call-to-action visibility, and make the book preview's swipe affordance easier to discover. Keep the existing dark, cream, and yellow brand; do not invent author credentials. Analytics and Clarity are out of scope.

## Scope and constraints

- Feature identity: `author-first-cta-preview`
- Authorized scope: landing author/hero order and presentation, primary CTA sizing/copy, book-preview swipe discoverability, responsive brand layout, circular portrait cropping, and focused regression tests.
- Preserve existing `.gitignore` and `.engram/` changes; do not revert or rewrite them.
- Fixed mobile CTA copy: `Quiero hablar con claridad`.
- Keep book navigation controls visually secondary to the primary CTA.
- Add a one-time preview swipe cue that stops after user interaction and respects reduced-motion preferences.
- No analytics or Clarity integration in this feature.
- Mobile brand layout: center the existing wordmark in the full mobile header; repeat the wordmark centered in the fixed banner's left segment, with the yellow CTA on the right and its label centered in both axes.
- Preserve desktop layout, existing navigation/checkout semantics, and avoid horizontal overflow at 320px, 375px, and 390px viewports.
- Delivery strategy: `single-pr` with the user's explicit `size:exception` approval for this feature's >400-line range; do not push or create a PR. Close each implementation task with its own Conventional Commit on the feature branch.
- Forecast: approximately 160 authored changed lines across implementation and tests (generated files excluded); planning estimate only, not a hard cap.

## Working configuration

- Organic TDD mode: follow test-first RED → GREEN → REFACTOR from the `superpowers:test-driven-development` skill.
- Source distinction: the workspace instructions contain a `Strict TDD Mode: enabled` marker, while the recorded SDD-init result says `strict_tdd=false` because there is no explicitly configured runner. This is organic work, not an SDD apply phase; use the observed baseline command below and do not claim SDD strict mode is enabled.
- Configured workspace test command: none established.
- Observed baseline command: `python3 -m unittest discover -s tests -v` — 2 tests passed. This is observed baseline evidence, not a configured project command.
- Applicable check for each task: `python3 -m unittest discover -s tests -v`, plus focused browser/manual interaction checks for the visible mobile CTA and preview interaction where automated coverage cannot exercise rendering or motion behavior.

## Tasks

### T1 — Author-first presentation and primary CTAs

- [x] Move and redesign Arturo's full author section before the hero, preserving the existing dark/cream/yellow brand and using only supplied biographical facts.
- [x] Modestly enlarge primary CTA buttons while keeping book controls secondary; use the fixed mobile CTA copy `Quiero hablar con claridad`.
- [x] Add/update regression tests for section order, CTA text, and primary-versus-secondary affordance where the existing test structure supports them.

**Acceptance criteria**

- The complete author section appears before the hero.
- Author presentation stays within the existing palette and contains no invented credentials or claims.
- Primary CTA buttons are modestly more prominent; book navigation controls remain secondary.
- The mobile CTA displays exactly `Quiero hablar con claridad`.
- Relevant automated tests fail before implementation for the intended missing behavior, then pass after the minimal implementation; the full applicable check is green.

**Route and trigger evidence:** delegated direct writer; preparation spans multiple source/test files and implementation is expected to touch at least two non-trivial files, meeting the ODD mapping/preparation and writer delegation triggers.

**Progress / verification:** Completed. Test-first RED: after updating the tests and before implementation, `python3 -m unittest discover -s tests -v` failed as expected (2 failures: author section was still sixth rather than first; the mobile CTA lacked `Quiero hablar con claridad`). A mobile visual pass exposed that a later desktop grid rule overrode the earlier one-column mobile rule; a focused regression test then failed until a final mobile override was added. GREEN: final `python3 -m unittest discover -s tests -v` — 3 tests passed; `git diff --check` — passed. Browser visual check at 390 × 844 confirmed author-before-hero, a single-column author layout, visible mobile CTA copy, and no horizontal overflow (document width 375px). No checkout interaction was performed. Authored source/test diff: 102 changed lines (additions plus deletions; generated files excluded).

**Rollback boundary:** Revert T1's `index.html`, `styles.css`, and `tests/test_author_section.py` changes together to restore the previous section order, CTA sizing/copy, and expectations. Leave `.gitignore`, `.engram/`, and all T2 preview-cue behavior untouched.

**RDD outcome:** Parent assessed the committed T1 range as medium risk with `review_due=false` and `review_due_reason=under_budget` (177 changed lines including the task document). The unrelated `.engram/config.json` was excluded using the parent-authorized inventory `sha256:118d4e3ed063111db6d7dad8e8d480a021860c2d592f8a6f4b7b3b4870da9cef`; no review lifecycle was due.

**Commit evidence:** `e7154245ec3a5ea1936aabb39e9be1f8447fee00` — `feat(landing): move author before hero and strengthen CTAs` on `codex/author-first-cta-preview`.

### T2 — One-time swipe discoverability cue

- [x] Start the one-time swipe cue only after the preview enters the viewport. Reopened after the parent found that the original load-time animation could finish before a visitor reached the below-fold book preview; corrected with observer and fallback coverage.
- [x] Stop the cue after the user's first relevant interaction and suppress motion when `prefers-reduced-motion` is active.
- [x] Add regression tests for cue lifecycle and reduced-motion behavior using the existing Node test runner and Python markup suite.

**Acceptance criteria**

- The preview communicates that it can be swiped without displacing or obscuring the primary CTA.
- The cue remains pending until the preview is visible; use `IntersectionObserver` with a viewport-checking scroll/resize fallback.
- The cue runs at most once and stops immediately after user interaction with the preview.
- Users requesting reduced motion do not receive the animated cue.
- Test-first RED → GREEN → REFACTOR is observed for the behavior; the full applicable check is green.

**Route and trigger evidence:** delegated direct writer; preparation spans implementation, markup, CSS, and lifecycle tests, and the task modifies multiple non-trivial files.

**Progress / verification:** Original T2 implementation committed as `a07cfd81f0aa5d85b80dca508d168b52d8f2e07f`, but the parent later identified a behavior gap: the cue started when `script.js` loaded, so its one-shot animation could be consumed before the below-fold preview became visible. Reopened and corrected the visibility-trigger criterion in `0267e556a16c0c566eefaca1c23a0680c8d2bbb2`. Correction RED before correction source changes: `node --test tests/test_preview_swipe_cue.js` — 3 tests failed (cue animated before visibility; no observer lifecycle; fallback animated before visibility). Correction GREEN: `node --test tests/test_preview_swipe_cue.js` — 3 passed; `python3 -m unittest discover -s tests -v` — 4 passed; `git diff --check` — passed. Tests cover pending state until observer visibility, reduced motion becoming active while pending (which disconnects the observer), and scroll fallback when `IntersectionObserver` is absent. Browser check at 390 × 844 confirmed the cue had no animation at page load while preview top was 5,487px, started once preview entered the viewport (top 170px; animation `preview-swipe-cue-nudge`), and stopped on the preview-next interaction (`is-dismissed`, no animation); mobile CTA remained `Quiero hablar con claridad`, document width 375px. No checkout action was performed. Browser-level reduced-motion emulation was unavailable; load-time and pre-visibility changes are covered by Node tests.

**Rollback boundary:** The original T2 commit `a07cfd81f0aa5d85b80dca508d168b52d8f2e07f` adds the cue. Revert the corrective visibility-trigger commit to restore the prior load-time start behavior; revert both T2 commits together to remove the cue and tests. Leave T1 author/CTA behavior, `.gitignore`, and `.engram/` untouched.

**Commit evidence:** Original: `a07cfd81f0aa5d85b80dca508d168b52d8f2e07f` — `feat(preview): add one-time swipe discovery cue`. Correction: `0267e556a16c0c566eefaca1c23a0680c8d2bbb2` — `fix(preview): start swipe cue when book is visible` on `codex/author-first-cta-preview`.

### T3 — Center mobile wordmark and fixed CTA

- [x] Center the header wordmark across the full mobile header width without changing desktop navigation or branding.
- [x] Replace the fixed banner's plain-text brand with the existing accessible wordmark, centered in the left segment; keep the yellow CTA on the right with centered label text.
- [x] Verify no horizontal overflow at 320px, 375px, and 390px; retain accessible link names and checkout target.

**Acceptance criteria**

- At mobile widths, the header wordmark is horizontally centered against the viewport, not merely aligned to the left content edge.
- The fixed banner presents the same wordmark centered in its left segment and the yellow CTA in its right segment.
- CTA text is centered horizontally and vertically, fully visible, and remains `Quiero hablar con claridad`.
- Header/footer/navigation and checkout semantics are preserved; the desktop layout remains unchanged.
- Browser layout checks at 320px, 375px, 390px, and desktop show no horizontal overflow or overlap.
- Test-first RED → GREEN → REFACTOR is observed and all specified automated checks pass.

**Route and trigger evidence:** delegated direct writer; preparation and implementation span HTML, responsive CSS, semantic regression tests, and multi-viewport verification, satisfying the ODD multi-file writer and preparation triggers.

**Applicable checks:** `node --test tests/test_preview_swipe_cue.js`; `python3 -m unittest discover -s tests -v`; `git diff --check`; added focused mobile-brand structural tests; browser computed-layout checks at 320px, 375px, 390px, and desktop where available.

**Progress / verification:** Implemented test-first. Baseline before T3: `node --test tests/test_preview_swipe_cue.js` — 3 passed; `python3 -m unittest discover -s tests -v` — 4 passed; `git diff --check` — passed. RED after adding the banner structure test and before source changes: `python3 -m unittest discover -s tests -v` — 1 failure because the banner had only one anchor instead of the required wordmark and checkout links. GREEN after implementation/refactor: Node — 3 passed; Python — 5 passed; `git diff --check` — passed. The added HTML parser checks accessible wordmark and checkout links without source-string matching. A first green attempt exposed that an existing mobile author test incorrectly selected only the last `max-width:760px` block; it now checks the responsive rule independently of media-block ordering. Browser computed-layout and screenshots at 320px, 375px, 390px, and 1280px showed the mobile header logo centered (0px offset), banner wordmark centered in the left grid track (0px/0.01px offset), CTA text/box centered in both axes with exact copy and visible bounds, and no document overflow. Desktop nav and header CTA remain visible, mobile banner hidden, and wordmark remains in its desktop position.

**Rollback boundary:** Revert T3's mobile header/banner markup, responsive styles, focused tests, and task-record additions together; leave T1/T2 commits and `.gitignore`/`.engram/` untouched.

**Commit evidence:** `0e422e04231fd3da54bde41487fca3c95dc51e4f` — `fix(mobile): center brand and sticky CTA layout` on `codex/author-first-cta-preview`.

### T4 — Crop Arturo's portrait as a circle

- [x] Apply a circular CSS crop to the existing portrait image at mobile and desktop sizes; retain the shifted yellow accent and Arturo label outside the crop.
- [x] Remove the portrait's rectangular border and shadow without changing the source bitmap or surrounding author layout.
- [x] Add a focused regression check for circular shape and absent rectangular frame, and visually verify at 320px, 390px, and 1280px.

**Acceptance criteria**

- The portrait renders as a clean circle at mobile and desktop viewports while keeping the original supplied image unchanged.
- The shifted yellow accent remains visible behind the circle; the Arturo label remains readable and is not clipped by the crop.
- No rectangular portrait border or box shadow remains; surrounding author content and layout are unchanged.
- Focused regression, `python3 -m unittest discover -s tests -v`, `node --test tests/test_preview_swipe_cue.js`, and `git diff --check` pass; browser visual checks cover 320px, 390px, and 1280px where available.
- Test-first RED → GREEN → REFACTOR is observed for the portrait presentation.

**Route and trigger evidence:** delegated direct writer; preparation spans the portrait markup, responsive styles, regression tests, and visual verification, and implementation touches multiple non-trivial files, satisfying the ODD preparation and writer delegation triggers.

**Applicable checks:** focused portrait regression test; `python3 -m unittest discover -s tests -v`; `node --test tests/test_preview_swipe_cue.js`; `git diff --check`; browser computed-style/screenshot check at 320px, 390px, and 1280px.

**Progress / verification:** Completed test-first. Before source changes, verified the existing markup is `.author-photo > img.author-portrait` with a sibling `.author-photo-label`; the CSS added a rectangular border and box shadow to the image and positioned the yellow accent and label on the wrapper. The supplied `assets/arturo-modoverbo.png` was verified by the parent as an opaque RGB 1254×1254 image and remains unchanged. RED: `python3 -m unittest discover -s tests -p 'test_author_section.py' -v` — 1 intended failure because the portrait had no circular radius (`None` instead of `50%`); the existing five tests passed. GREEN: same focused command — 6 passed; `python3 -m unittest discover -s tests -v` — 6 passed; `node --test tests/test_preview_swipe_cue.js` — 3 passed; `git diff --check` — passed. Browser checks at 320px, 390px, and 1280px showed computed `border-radius: 50%`, `border: 0px none`, and `box-shadow: none`; the image remained square in its layout box, forming a circle crop. The shifted yellow accent remained visible behind the portrait and the complete Arturo label remained visible outside the crop. Screenshots showed no clipped portrait decoration at any tested width. No asset, CTA, preview, or tracking changes were made.

**Rollback boundary:** Revert T4's portrait presentation/test changes together, leaving T1–T3, the original image asset, `.gitignore`, and `.engram/` untouched.

**Commit evidence:** `1b65e8a` — `fix(author): crop portrait into a circle` on `codex/author-first-cta-preview`.

## Next step

T1, T2, T3, and T4 are implemented and verified; the latest work-unit commit is `1b65e8a`. RDD is disabled for this clone; do not run assessment or review. Do not push, create a PR, or deploy.
