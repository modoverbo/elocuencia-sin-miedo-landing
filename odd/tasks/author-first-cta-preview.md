# Author-first landing and preview discoverability

Move the Arturo author section ahead of the hero, strengthen primary call-to-action visibility, and make the book preview's swipe affordance easier to discover. Keep the existing dark, cream, and yellow brand; do not invent author credentials. Analytics and Clarity are out of scope.

## Scope and constraints

- Feature identity: `author-first-cta-preview`
- Authorized scope: landing author/hero order and presentation, primary CTA sizing/copy, book-preview swipe discoverability, and focused regression tests.
- Preserve existing `.gitignore` and `.engram/` changes; do not revert or rewrite them.
- Fixed mobile CTA copy: `Quiero hablar con claridad`.
- Keep book navigation controls visually secondary to the primary CTA.
- Add a one-time preview swipe cue that stops after user interaction and respects reduced-motion preferences.
- No analytics or Clarity integration in this feature.
- Delivery strategy: `single-pr`; do not push or create a PR. Close each implementation task with its own Conventional Commit on the feature branch.
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

**Commit evidence:** pending until the T1 work-unit commit is created; record its identity in the post-commit document/mirror update.

### T2 — One-time swipe discoverability cue

- [ ] Add a one-time swipe animation/cue to the book preview to signal horizontal discoverability.
- [ ] Stop the cue after the user's first relevant interaction and suppress motion when `prefers-reduced-motion` is active.
- [ ] Add regression tests for cue lifecycle and reduced-motion behavior where supported by the existing test structure.

**Acceptance criteria**

- The preview communicates that it can be swiped without displacing or obscuring the primary CTA.
- The cue runs at most once and stops immediately after user interaction with the preview.
- Users requesting reduced motion do not receive the animated cue.
- Test-first RED → GREEN → REFACTOR is observed for the behavior; the full applicable check is green.

**Route and trigger evidence:** delegated direct writer; this task requires preparation across implementation and test files and is part of the multi-file writer scope.

**Progress / verification:** Not started. No implementation verification yet. Baseline only: `python3 -m unittest discover -s tests -v` — 2 tests passed before feature work.

**Commit evidence:** pending.

## Next step

After the parent reads back this task document and its Engram mirror, implement T1 then T2 test-first. Update this document and mirror after each task with observed outcomes, exact checks, and commit identities. Do not push or create a PR.
