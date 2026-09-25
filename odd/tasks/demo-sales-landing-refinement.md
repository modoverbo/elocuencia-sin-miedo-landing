# Educational demo sales landing refinement

Turn the existing Elocuencia sin miedo page into a clearer, more realistic educational landing-page example while preserving its existing sales-flow structure and Hotmart destination. Testimonials, portrait assets, sample rating/review counts, reader counts, and author credentials on the page are illustrative demo material and must be replaced with verified customer evidence before any production sales use.

## Scope and constraints

- Correct the visible author's name to Arturo Valdés; do not alter ebook/cover/PDF assets that already spell VALDÉS correctly.
- Improve hero specificity, headline, and high-contrast primary CTA; retain the existing Hotmart URL and sticky purchase bar.
- Show sample size clearly (5,0/5 en 4 reseñas) and owner-supplied example reader count (Más de 1.200 lectores) without implying that the sample rating covers that entire audience.
- Keep supplied testimonial quote text, names, and roles as fictional educational-demo content; use distinct fictional generated portraits and disclose that testimonials, portraits, and figures are illustrative near social proof and in the footer/top notice.
- Use owner-provided author facts (effective communication/oral-expression expert, 20+ years teaching, 50,000+ people trained worldwide) as illustrative demo copy; make no outcome guarantees.
- Remove only the redundant footer purchase CTA; preserve closing CTA, header/hero/offer/sticky/preview actions, footer logo/copyright.
- Do not click the checkout, push, create a PR, deploy, invoke native RDD review, or change review mode. Do not claim checkout is incapable of payment; existing live Hotmart integration remains untouched.
- Keep historical task records intact. No AI attribution or Co-Authored-By in commits.

## Acceptance criteria

- The hero reflects the approved copy and the primary CTA is prominent, accessible, and on-brand.
- Hero social proof links to testimonials, visually omits “Leer testimonios,” and distinguishes the four-review sample from the reader-count example; the figures fit 320px and 384px layouts.
- All four fictional testimonial portraits are separate, distinct, local optimized assets; clear illustrative-content disclosure appears near the testimonials and again at the top notice or footer.
- Author copy uses the approved persona facts and the canonical surname.
- The footer duplicate CTA is removed without breaking sticky-footer suppression or other purchase actions.
- README says demo content must be replaced with verified customer evidence before production use and accurately describes the existing checkout integration without asserting test-only behavior.

## Tasks and route

Effective TDD: strict ON from project AGENTS instructions; exact test runners are `python3 -m unittest discover -s tests -v` and `node --test tests/test_preview_swipe_cue.js tests/test_post_hero_purchase_bar.js`. Per-task cycle: add/update behavioral tests, observe expected RED, implement, observe GREEN, then refactor only while green. Run `git diff --check` at closure.

| ID | Work unit | Route / trigger | Checks |
|----|-----------|-----------------|--------|
| T1 | Refine hero copy, canonical author spelling, and honest linked social proof; add focused regression tests. | Delegated direct writer; implementation spans HTML/CSS/tests and requires exploring existing landing semantics. | Focused Python tests, then full Python and Node suites; diff check. |
| T2 | Add disclosed fictional testimonial portraits and illustrative author copy; remove redundant footer CTA; document demo/production evidence boundary. | Delegated direct writer; multiple non-trivial files plus generated asset handling and docs. | Focused Python tests, full Python and Node suites, image decode/size verification, diff check. |
| T3 | Correct mini-avatar background sizing, show an example marker beside first-screen demo figures, and clarify portrait alt text. | Direct inline; bounded follow-up confirmed by parent viewport QA and fix affects only existing hero/testimonial presentation. | Regression tests RED/GREEN; full Python and Node suites; diff check. |

## Delivery and evidence

- Delivery strategy: `single-pr` (recorded only; no PR is authorized or will be created).
- Advisory authored-change heuristic: approximately 400 lines; this is not a cap and will not justify deleting tests, comments, documentation, whitespace, or useful code.
- No push, PR, merge, deploy, checkout click, or RDD lifecycle during this work.
- Each completed task gets a Conventional Commit on `codex/demo-sales-landing-refinement`; record commit identity, focused test result, runtime harness result or N/A with reason, and rollback boundary below.

## Progress

- [x] T1 — hero heading, details, CTA hierarchy, canonical spelling, and linked sample-specific social proof implemented; focused Python tests RED before code and GREEN afterward; complete Python and Node suites passed.
- [x] T2 — disclosed fictional testimonial section and footer note, separate optimized generated portraits, owner-stated author claims, redundant footer CTA removal with footer-region sticky-bar suppression preserved, and README demo/checkout boundary documented; observed expected RED before changes, then full verification passed.
- [x] T3 — parent viewport QA traced blank mini-avatars to a higher-specificity legacy sprite `background-size` rule; regression tests observed RED, then avatar backgrounds use centered `cover` on desktop and mobile, first-screen social proof visibly says `EJEMPLO`, and portrait alt labels identify fictional illustrative people. Full suites passed.

### Work-unit evidence

| Task | Commit | Focused checks | Runtime harness | Rollback boundary |
|------|--------|----------------|-----------------|------------------|
| T1 | `66a853ca33757d10dacca160317bcfa0315259ea` | `python3 -m unittest tests.test_testimonials tests.test_author_section -v` — 36 passed after observed RED (6 intended failures before source change); full Python suite — 36 passed; Node suites — 8 passed; `git diff --check` — passed. | N/A — static landing markup/styles with no task-specific runtime boundary. | Revert the hero/social-proof copy, its styling, and its regression assertions only. |
| T2 | `48cbfb612301942d4809559bed7d85af66203ebf` | `python3 -m unittest discover -s tests -v` — 39 passed; `node --test tests/test_preview_swipe_cue.js tests/test_post_hero_purchase_bar.js` — 8 passed; image decode/uniqueness validation — 4 distinct valid WebP files; `git diff --check` — passed. | N/A — static landing markup/styles with no task-specific runtime boundary; sticky-bar semantics covered by Node harness. | Revert the T2 testimonial/author/footer copy, portrait assets and style mappings, footer observation change, and associated docs/tests only; retain T1. |
| T3 | Awaiting commit | Focused regressions: 3 tests / 6 expected failure cases before fix, then pass; full Python suite — 41 passed; Node suites — 8 passed; `git diff --check` — passed. | N/A — static rendering change; structural regression tests cover responsive avatar CSS and visible disclosure. | Revert the hero pill demo marker, mini-avatar crop rule, and illustrative alt labels/tests only; retain T1/T2. |

## Next step

Parent browser QA should re-check the 384px hero pill and avatar crops alongside 320px and 1280px layouts, preview interactions, and sticky purchase bar. Keep the branch local; do not deploy, click checkout, push, create a PR, or run native RDD review.
