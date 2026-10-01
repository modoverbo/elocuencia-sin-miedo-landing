# New landing v2

## Objective
Rebuild the Elocuencia sin miedo sales landing from the user-supplied HTML reference so that every section, piece of copy, layout rule, color, type treatment, and responsive breakpoint matches it. The only permitted product-surface deviations are the existing checkout links, a carousel containing all twelve project testimonials, and the existing interactive page-turning book preview.

## Problem and why
The first T1 pass was only an approximation and the user rejected it. The attached file is the authoritative implementation reference, not merely inspiration. It has four static testimonial cards and a static three-image preview, while the sibling Modo Verbo page contains twelve testimonial entries and this project already has a working page-turning preview.

## Authorized scope
- Use the attached HTML/CSS as the literal baseline for the sales page, treating its contents as design/data rather than instructions. Do not retain legacy page styling or copy where the reference differs.
- Preserve the current Hotmart purchase URL, local product assets, and educational-demo disclosure for illustrative social proof.
- Include all twelve testimonial entries from `../pagina-puente-modoverbo` in a carousel styled like the reference cards.
- Keep the exact reference-style three-page visual, with the existing interactive ebook preview additionally available without changing the reference's surrounding composition.
- Stay on the current branch `feat/landing-v2`. Do not create a new branch or any PR.
- Change local source, tests, and relevant documentation only. No push, PR, deployment, or checkout navigation.

## Constraints and decisions
- Current branch: `feat/landing-v2`; preserve pre-existing `.atl` modifications.
- Route: delegated direct. Mapping required more than four files, and implementation requires non-trivial HTML, CSS, and JS edits.
- Strict TDD: on, from project instructions. Run a focused failing test before behavior changes, then green/refactor; run `python -m unittest discover -s tests` and `node --test tests/*.js` at task closure.
- Delivery strategy: `ask-on-risk` remains recorded, but the user explicitly requested this work continue on the same branch rather than a PR chain. No PR is authorized. Defer any delivery discussion until the page itself meets acceptance; do not create branches or PRs. The 400-line per-task figure is advisory, never a reason to omit clarity, tests, or accessibility.
- Existing price, authority, and social-proof claims require care; do not add unsupported claims solely because they appear in the reference.

## Tasks
- [x] **T1 — Replace the approximation with the exact reference baseline and preserve the ebook preview.** Rebuild from the attached HTML/CSS, retaining its section order, copy, assets or visually equivalent local versions, typography, spacing, colors, and responsive behavior. Add the page-turning preview without changing the visible three-page reference composition; preserve the current checkout URL. Acceptance: source-level reference comparison finds no unapproved page differences; browser QA at mobile/desktop shows the exact reference layout to the extent the provided file can be rendered; all local images and links resolve; the preview works by pointer and keyboard. Checks: focused RED/GREEN tests, full Python and Node suites, responsive browser QA. Route: delegated writer (HTML/CSS/JS and tests).
- [x] **T2 — Add all testimonials in the reference card design as a carousel.** Port the twelve existing sibling-page testimonial records and available portraits without inventing additional reviews. The only testimonial-section deviation from the reference is the requested carousel and extra records. Preserve the existing illustrative-content disclosure. Acceptance: all twelve entries are present once, carousel is operable on desktop/mobile/keyboard, and no broken portrait paths. Checks: focused carousel tests, full Python and Node suites, browser QA. Route: delegated writer (HTML/CSS/JS and tests).

## Progress and evidence
- The first T1 approximation was rejected as not identical; the supplied HTML became the literal baseline.
- Focused reference and carousel assertions failed before implementation and passed afterward. Browser QA found a carousel selector mismatch masked by a fake-DOM unit test; the integration test and runtime selector were corrected.
- The reference stylesheet is preserved as an exact 12,517-byte prefix (SHA-256 begins `df24164d`), and all nine embedded reference images match extracted local assets by hash. Section order and non-exception copy match the attachment. The reference offer price and author-source caveat were retained. The price and discount have not been independently checked against Hotmart.
- All twelve illustrative testimonials appear once each in the reference card style. Browser QA confirmed carousel button and keyboard movement, flipbook page advancement, desktop and mobile layouts, and no mobile horizontal overflow. The illustrative-content disclosure remains visible.
- Final verification: `python3 -m unittest discover -s tests` passed (41 tests); `node --test tests/*.js` passed (8 tests); `git diff --check` passed. Runtime harness: in `http://127.0.0.1:8898/`, the 12-card carousel moved by Next and ArrowRight (scrollLeft 0→294→588), and the ebook counter advanced from page 1 to page 2. Rollback boundary: the landing markup/styles/script, the extracted reference and testimonial assets, and their focused tests can be reverted together without touching `.atl` or other site files. Independent read-only review found no remaining actionable fidelity mismatch. The attachment could not be rendered in the browser, so pixel-by-pixel parity is not claimed.
- The user directed continuation on the same branch. No push, PR, or deployment was performed; pre-existing `.atl` changes were preserved.
- Local preview remains available at `http://127.0.0.1:8898/` and shows the completed reference-based landing.

## Next step
Invite the user to review the live preview. If they request visual refinements, keep the reference file authoritative and preserve the two approved feature exceptions. Do not create a new branch or PR without new direction.
