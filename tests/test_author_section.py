import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MobileBrandParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_header = False
        self.in_mobile_banner = False
        self.current_link = None
        self.header_wordmarks = []
        self.banner_links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = attributes.get("class", "").split()
        if tag == "header":
            self.in_header = True
        if tag == "div" and "mobile-buy" in classes:
            self.in_mobile_banner = True
        if tag == "a" and self.in_header and "wordmark" in classes:
            self.header_wordmarks.append(attributes)
        if tag == "a" and self.in_mobile_banner:
            self.current_link = {"attributes": attributes, "text": []}
            self.banner_links.append(self.current_link)

    def handle_data(self, data):
        if self.current_link is not None:
            self.current_link["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "a":
            self.current_link = None
        elif tag == "header":
            self.in_header = False
        elif tag == "div" and self.in_mobile_banner:
            self.in_mobile_banner = False


class SalesLandingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = []
        self.current_section = None
        self.in_header = False
        self.in_mobile_banner = False
        self.checkout_links = []
        self.marketing_buttons = []
        self.current_checkout_link = None
        self.offer_card_text = []
        self.offer_card_div_depth = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = attributes.get("class", "").split()
        if tag == "header":
            self.in_header = True
        elif tag == "section":
            self.current_section = {"attributes": attributes, "text": [], "images": []}
            self.sections.append(self.current_section)
        elif tag == "div" and "offer-card" in classes:
            self.offer_card_div_depth = 1
        elif tag == "div" and "mobile-buy" in classes:
            self.in_mobile_banner = True
        elif tag == "div" and self.offer_card_div_depth:
            self.offer_card_div_depth += 1
        elif tag == "img" and self.current_section is not None:
            self.current_section["images"].append(attributes)
        elif tag == "a":
            if "hotmart__button-checkout" in classes:
                self.current_checkout_link = {
                    "attributes": attributes,
                    "section": self.current_section,
                    "in_header": self.in_header,
                    "in_mobile_banner": self.in_mobile_banner,
                    "text": [],
                }
                self.checkout_links.append(self.current_checkout_link)
            if "button" in classes and "hotmart__button-checkout" not in classes:
                self.marketing_buttons.append(attributes)

    def handle_data(self, data):
        if self.current_section is not None:
            self.current_section["text"].append(data)
        if self.offer_card_div_depth:
            self.offer_card_text.append(data)
        if self.current_checkout_link is not None:
            self.current_checkout_link["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "section":
            self.current_section = None
        elif tag == "header":
            self.in_header = False
        elif tag == "div" and self.in_mobile_banner:
            self.in_mobile_banner = False
        elif tag == "div" and self.offer_card_div_depth:
            self.offer_card_div_depth -= 1
        elif tag == "a":
            self.current_checkout_link = None


class AuthorSectionTests(unittest.TestCase):
    def test_preview_caption_keeps_chapter_label_separate_from_page_counter(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        caption = re.search(r"\.stage-caption\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(caption, "Preview caption needs a layout rule that separates its labels")
        declarations = dict(
            declaration.split(":", 1)
            for declaration in caption.group(1).split(";")
            if ":" in declaration
        )
        self.assertEqual(declarations.get("display"), "flex")
        self.assertEqual(declarations.get("gap"), "12px")
        self.assertEqual(declarations.get("justify-content"), "space-between")

    def test_offer_strip_precedes_sticky_header_and_post_hero_bar_is_accessibly_hidden(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        strip_start = html.find('<div class="offer-strip"')
        self.assertGreater(strip_start, -1, "Expected the terms strip before the sticky header")
        header_start = html.index('<header class="site-header"')
        self.assertLess(strip_start, header_start)
        strip_end = html.index("</div>", strip_start)
        strip_text = re.sub(r"<[^>]+>", " ", html[strip_start:strip_end])
        for term in ("EBOOK DIGITAL", "PAGO ÚNICO", "ACCESO INMEDIATO", "7 DÍAS DE GARANTÍA"):
            with self.subTest(term=term):
                self.assertIn(term, strip_text)
        self.assertNotRegex(strip_text, r"(?i)(\$|\b\d+[.,]?\d*\s?(usd|cop|eur)|descuento|% off)")

        sticky_header = re.search(r"\.site-header\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(sticky_header)
        self.assertIn("position:sticky", sticky_header.group(1))
        self.assertIn("top:0", sticky_header.group(1))
        post_hero_bar = re.search(r'<div class="mobile-buy"[^>]*id="post-hero-buy"[^>]*>', html)
        self.assertIsNotNone(post_hero_bar)
        for attribute in ('hidden', 'inert', 'aria-hidden="true"'):
            self.assertIn(attribute, post_hero_bar.group(0))
        self.assertIn(".mobile-buy[hidden]{display:none!important}", css)
        self.assertIn(".mobile-buy:not([hidden]){display:flex;", css)
        self.assertIn(".mobile-buy:not([hidden]){display:grid;", css)
        self.assertIn('id="preview-controls"', html)
        self.assertIn('id="site-footer"', html)
        self.assertIn('id="preview-next"', html)
        self.assertIn('id="footer-purchase-cta"', html)
        self.assertIn("@media(prefers-reduced-motion:reduce)", css)

    def test_editorial_brand_uses_green_gold_palette_and_display_swap_fonts(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        root_tokens = re.search(r":root\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(root_tokens)
        declarations = dict(
            declaration.split(":", 1)
            for declaration in root_tokens.group(1).split(";")
            if ":" in declaration
        )
        expected_tokens = {
            "--petroleum": "#0F3D3A",
            "--forest": "#174236",
            "--gold": "#D4AF37",
            "--paper": "#F8F6EF",
            "--stone": "#A7A29A",
            "--ink": "#1A1A1A",
        }
        for token, color in expected_tokens.items():
            with self.subTest(token=token):
                self.assertEqual(declarations.get(token), color)

        self.assertRegex(html, r"fonts\.googleapis\.com/css2\?family=Playfair\+Display[^\"]*Montserrat[^\"]*display=swap")
        self.assertIn("font-family:var(--sans)", css)
        self.assertIn("font-family:var(--serif)", css)
        self.assertNotRegex(f"{html}\n{css}", r"(?i)poppins|--yellow|#f9db43|#ddaa19|#f3d75b|#ffde4b")
        self.assertRegex(css, r"\.hero\s*\{[^}]*background:[^}]*var\(--petroleum\)")
        self.assertRegex(css, r"\.preview\s*\{[^}]*background:var\(--petroleum\)")
        for color in ("#f9db43", "#ddaa19", "#ba8100", "#866b10", "#fff6d8", "#dcbf42", "#edcd52"):
            self.assertNotIn(color, f"{html}\n{css}")

    def test_corrected_edition_preview_uses_local_pdf_pages_in_order(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        manifest = json.loads((ROOT / "assets/edition/preview-manifest.json").read_text(encoding="utf-8"))
        preview_start = html.index('<section class="preview ')
        preview_end = html.index('<section class="inside ', preview_start)
        preview_markup = html[preview_start:preview_end]

        expected_assets = ["assets/edition/cover.webp"] + [
            f"assets/edition/page-{page:02d}.webp" for page in range(2, 14)
        ]
        self.assertEqual(manifest["source_pdf"], "Elocuencia sin miedo - Verde y oro - Portada corregida.pdf")
        self.assertEqual(manifest["source_page_count"], 156)
        self.assertEqual(
            manifest["preview_pages"],
            [{"pdf_page": page, "path": path} for page, path in enumerate(expected_assets, start=1)],
        )

        page_assets = [
            (int(page), path)
            for page, path in re.findall(
                r'<div class="preview-page[^\"]*" data-page="(\d+)"[^>]*>\s*<img src="([^\"]+)"',
                preview_markup,
            )
            if int(page) <= 13
        ]
        self.assertEqual(page_assets, list(enumerate(expected_assets, start=1)))
        self.assertIn('content="assets/edition/cover.webp"', html)
        self.assertIn('href="assets/edition/cover.webp"', html)
        self.assertGreaterEqual(html.count('src="assets/edition/cover.webp"'), 2)
        for path in expected_assets:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())
        for path in manifest["supplied_assets"]:
            with self.subTest(path=path):
                self.assertTrue((ROOT / "assets/edition" / path).is_file())

    def test_reader_opinions_anchor_targets_accessible_truthful_empty_state(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        review_link = re.search(
            r'<a class="review-link" href="#resenas"[^>]*>(.*?)</a>', html, re.DOTALL
        )
        self.assertIsNotNone(review_link, "Expected a neutral hero link to the local reviews section")
        self.assertIn("Opiniones de lectores", re.sub(r"<[^>]+>", "", review_link.group(1)))
        self.assertNotIn("button", review_link.group(0))

        parsed = SalesLandingParser()
        parsed.feed(html)
        sections_by_id = {section["attributes"].get("id"): section for section in parsed.sections}
        reviews = sections_by_id.get("resenas")
        self.assertIsNotNone(reviews, "Expected the reader-opinions empty-state section")
        self.assertEqual(reviews["attributes"].get("aria-labelledby"), "resenas-title")
        self.assertEqual(reviews["attributes"].get("tabindex"), "-1")
        copy = " ".join(reviews["text"]).lower()
        self.assertIn("no se muestran reseñas", copy)
        self.assertIn("autorización", copy)
        self.assertNotRegex(copy, r"(?:⭐|★|\b[1-5]\s*(?:estrellas?|/5)|\b\d+\s+(?:reseñas?|opiniones|lectores?))")
        self.assertEqual(reviews["images"], [])
        self.assertNotIn("<blockquote", html.lower())
        self.assertNotIn('class="review-card', html.lower())
        self.assertRegex(css, r"#resenas\s*\{[^}]*scroll-margin-top\s*:")
        self.assertRegex(css, r"#resenas:focus-visible\s*\{[^}]*outline")

    def test_landing_sections_follow_sales_flow_with_sequential_kickers(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SalesLandingParser()
        parsed.feed(html)

        expected_order = ["hero", "recognition", "journey", "preview", "inside", "fit", "offer", "reviews", "author", "faq", "closing"]
        actual_order = [
            next(
                name
                for name in expected_order
                if name in section["attributes"].get("class", "").split()
            )
            for section in parsed.sections
        ]
        self.assertEqual(actual_order, expected_order)

        kicker_numbers = []
        for section in parsed.sections:
            match = re.search(r"\b(\d{2})\s*/", " ".join(section["text"]))
            kicker_numbers.append(match.group(1) if match else None)
        self.assertEqual(kicker_numbers, [f"{number:02d}" for number in range(1, 12)])

    def test_landing_sections_have_unique_ids_and_internal_links_resolve(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SalesLandingParser()
        parsed.feed(html)

        section_ids = [section["attributes"].get("id") for section in parsed.sections]
        self.assertTrue(all(section_ids), "Each landing section needs a stable in-page anchor")
        self.assertEqual(len(section_ids), len(set(section_ids)))

        all_ids = set(re.findall(r'\bid="([^"]+)"', html))
        internal_targets = re.findall(r'href="#([^"]+)"', html)
        self.assertTrue(internal_targets)
        self.assertTrue(all(target in all_ids for target in internal_targets))

    def test_testimonial_section_remains_absent_without_attributable_content(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SalesLandingParser()
        parsed.feed(html)
        self.assertFalse(
            any(
                "testimonial" in " ".join(section["attributes"].values()).lower()
                for section in parsed.sections
            )
        )

    def test_hero_book_image_uses_an_arch_frame(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        hero_frame = re.search(r"\.hero-photo-frame\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(hero_frame, "Expected an editorial arch around the hero book image")
        declarations = dict(
            declaration.split(":", 1)
            for declaration in hero_frame.group(1).split(";")
            if ":" in declaration
        )
        self.assertRegex(declarations.get("border-radius", ""), r"48%")
        self.assertIn("var(--gold)", declarations.get("border", ""))

    def test_sales_hero_leads_and_identifies_author_with_portrait(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SalesLandingParser()
        parsed.feed(html)
        hero = next(section for section in parsed.sections if "hero" in section["attributes"].get("class", "").split())
        author = next(section for section in parsed.sections if "author" in section["attributes"].get("class", "").split())
        self.assertEqual(parsed.sections[0], hero)
        self.assertGreater(parsed.sections.index(author), parsed.sections.index(hero))
        self.assertIn("Arturo Valdéz", " ".join(hero["text"]))
        book_photo = next(image for image in hero["images"] if "hero-book-photo" in image.get("class", ""))
        self.assertTrue((ROOT / book_photo["src"]).is_file())
        self.assertEqual(book_photo.get("alt"), "Arturo Valdéz sosteniendo Elocuencia sin miedo")
        hero_text = " ".join(hero["text"])
        self.assertIn("Habla con claridad.", hero_text)
        self.assertIn("Conecta con las personas.", hero_text)
        self.assertIn("Haz que tus ideas importen.", hero_text)
        hero_markup = html[html.index('<section class="hero"'):html.index("</section>")]
        self.assertLess(hero_markup.index('class="hero-book-photo"'), hero_markup.index("<h1 id=\"hero-title\""))
        self.assertNotIn('class="floating-note"', hero_markup)
        self.assertNotRegex(html, r"(?i)(20 años|50[ .]?000 personas|50 mil personas)")

    def test_primary_purchase_cta_repeats_across_sections_and_offer_states_owner_terms(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SalesLandingParser()
        parsed.feed(html)

        self.assertFalse(parsed.marketing_buttons)
        self.assertGreaterEqual(len(parsed.checkout_links), 5)
        for link in parsed.checkout_links:
            visible_label = "".join(link["text"]).replace("↗", "").strip()
            self.assertEqual(visible_label, "Quiero hablar con claridad")
            self.assertEqual(
                link["attributes"].get("href"),
                "https://pay.hotmart.com/H107735669O?checkoutMode=2&off=s5txzdcx",
            )
        locations = {
            "header": any(link["in_header"] for link in parsed.checkout_links),
            "hero": any(link["section"] and "hero" in link["section"]["attributes"].get("class", "").split() for link in parsed.checkout_links),
            "offer": any(link["section"] and "offer" in link["section"]["attributes"].get("class", "").split() for link in parsed.checkout_links),
            "mobile banner": any(link["in_mobile_banner"] for link in parsed.checkout_links),
            "closing section": any(link["section"] and "closing" in link["section"]["attributes"].get("class", "").split() for link in parsed.checkout_links),
        }
        self.assertTrue(all(locations.values()), locations)

        offer_text = " ".join(parsed.offer_card_text).lower()
        for term in ("pdf", "156", "pago único", "acceso inmediato", "7 días de garantía"):
            self.assertIn(term, offer_text)
        self.assertNotRegex(offer_text, r"(?:\$|\b\d+[.,]\d{2}\b)")

    def test_primary_ctas_are_prominent_and_mobile_copy_is_benefit_led(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        mobile_cta = re.search(r'<div class="mobile-buy"[^>]*>(.*?)</div>', html, re.DOTALL)
        self.assertIsNotNone(mobile_cta)
        self.assertIn("Quiero hablar con claridad", mobile_cta.group(1))
        self.assertRegex(
            css,
            r"a\.button\.button-dark,\s*a\.button\.button-yellow,\s*a\.header-buy\s*\{[^}]*min-height\s*:\s*6[2-9]px",
        )
        self.assertRegex(
            css,
            r"\.hero-actions\s*>\s*a\.button-outline\s*\{[^}]*min-height\s*:\s*5[0-9]px",
        )
        self.assertRegex(
            css,
            r"\.preview-controls\s+button\s*\{[^}]*min-height\s*:\s*4[0-9]px",
        )

    def test_author_layout_collapses_to_one_column_on_mobile(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertRegex(
            css,
            r"@media\(max-width:760px\)[\s\S]*?\.author-grid\s*\{[^}]*grid-template-columns\s*:\s*1fr",
        )

    def test_preview_hint_contains_a_reduced_motion_aware_swipe_cue(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertRegex(
            html,
            r'<span class="preview-swipe-cue" id="preview-swipe-cue" aria-hidden="true"><span class="preview-swipe-arrows">↔</span><span class="preview-swipe-hand">👆</span></span>',
        )
        self.assertRegex(html, r'<p class="preview-hint">[^<]*Desliza para explorar[^<]*Toca una página para ampliarla\.')
        self.assertRegex(css, r"\.preview-swipe-cue\s*\{[^}]*position\s*:\s*absolute")
        self.assertRegex(css, r"\.preview-swipe-cue\s*\{[^}]*pointer-events\s*:\s*none")
        self.assertRegex(css, r"\.preview-swipe-cue\.is-animated\s*\{[^}]*animation:[^}]*infinite")
        reduced_motion_rules = re.findall(r"@media\(prefers-reduced-motion:reduce\)\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", css)
        self.assertTrue(reduced_motion_rules)
        self.assertRegex(
            "\n".join(reduced_motion_rules),
            r"\.preview-swipe-cue\.is-animated\s*\{[^}]*animation\s*:\s*none",
        )
        self.assertRegex(
            "\n".join(reduced_motion_rules),
            r"\.mobile-buy:not\(\[hidden\]\)\s*\{[^}]*transition\s*:\s*none",
        )

    def test_mobile_banner_keeps_accessible_wordmark_and_checkout_action(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = MobileBrandParser()
        parsed.feed(html)

        self.assertEqual(len(parsed.header_wordmarks), 1)
        self.assertEqual(parsed.header_wordmarks[0].get("href"), "#inicio")
        self.assertEqual(parsed.header_wordmarks[0].get("aria-label"), "Elocuencia sin miedo, inicio")
        self.assertEqual(len(parsed.banner_links), 2)

        brand = parsed.banner_links[0]["attributes"]
        action = parsed.banner_links[1]["attributes"]
        self.assertIn("wordmark", brand.get("class", "").split())
        self.assertEqual(brand.get("href"), "#inicio")
        self.assertEqual(brand.get("aria-label"), "Elocuencia sin miedo, inicio")
        self.assertEqual("".join(parsed.banner_links[1]["text"]).strip(), "Quiero hablar con claridad")
        self.assertIn("hotmart__button-checkout", action.get("class", "").split())
        self.assertTrue(action.get("href", "").startswith("https://pay.hotmart.com/"))

    def test_supplied_book_holding_image_leads_hero_and_neutral_portrait_stays_deeper(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        author_start = html.index('<section class="author ')
        author_end = html.index("</section>", author_start)
        author_markup = html[author_start:author_end]
        hero = html[html.index('<section class="hero"'):author_start]

        self.assertTrue((ROOT / "assets/edition/arturo-holding-book.webp").is_file())
        self.assertRegex(
            hero,
            r'<img class="hero-book-photo" src="assets/edition/arturo-holding-book\.webp"[^>]*alt="Arturo Valdéz sosteniendo Elocuencia sin miedo"[^>]*>',
        )
        self.assertIn('src="assets/arturo-modoverbo.png"', author_markup)
        self.assertIn('alt="Arturo Valdéz, autor de Elocuencia sin miedo"', author_markup)
        self.assertNotIn("arturo-valdez-holding-elocuencia-sin-miedo.png", html)
        self.assertNotIn("generated-image-caption", html)

    def test_offer_mockup_is_explicitly_labeled_digital_pdf(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        offer = html[html.index('<section class="offer '):html.index('<section class="author ')]
        self.assertIn('src="assets/edition/cover-mockup.webp"', offer)
        self.assertIn('alt="Mockup ilustrativo del ebook digital en PDF Elocuencia sin miedo"', offer)
        self.assertIn("EBOOK DIGITAL · PDF · 156 PÁGINAS", offer)
        self.assertIn("Pago único", offer)
        self.assertIn("Acceso inmediato", offer)
        self.assertIn("7 días de garantía", offer)


if __name__ == "__main__":
    unittest.main()
