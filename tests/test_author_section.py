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
    def test_landing_sections_follow_sales_flow_with_sequential_kickers(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SalesLandingParser()
        parsed.feed(html)

        expected_order = ["hero", "recognition", "journey", "preview", "inside", "fit", "offer", "author", "faq", "closing"]
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
        self.assertEqual(kicker_numbers, [f"{number:02d}" for number in range(1, 11)])

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

    def test_first_screen_author_portrait_stays_circular_without_frame(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        hero_portrait = re.search(r"\.hero-author-portrait\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(hero_portrait, "Expected a circular first-screen author portrait")
        declarations = dict(
            declaration.split(":", 1)
            for declaration in hero_portrait.group(1).split(";")
            if ":" in declaration
        )
        self.assertEqual(declarations.get("border-radius"), "50%")

    def test_sales_hero_leads_and_identifies_author_with_portrait(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SalesLandingParser()
        parsed.feed(html)
        hero = next(section for section in parsed.sections if "hero" in section["attributes"].get("class", "").split())
        author = next(section for section in parsed.sections if "author" in section["attributes"].get("class", "").split())
        self.assertEqual(parsed.sections[0], hero)
        self.assertGreater(parsed.sections.index(author), parsed.sections.index(hero))
        self.assertIn("Arturo Valdéz", " ".join(hero["text"]))
        portrait = next(image for image in hero["images"] if "hero-author-portrait" in image.get("class", ""))
        self.assertTrue((ROOT / portrait["src"]).is_file())
        self.assertEqual(portrait.get("alt"), "Arturo Valdéz, autor de Elocuencia sin miedo")
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
        mobile_cta = re.search(r'<div class="mobile-buy">(.*?)</div>', html, re.DOTALL)
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
        reduced_motion = css[css.rfind("@media(prefers-reduced-motion:reduce){"):]
        self.assertRegex(reduced_motion, r"\.preview-swipe-cue\.is-animated\s*\{[^}]*animation\s*:\s*none")

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

    def test_generated_author_book_illustration_is_disclosed_and_hero_keeps_original_portrait(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        author_start = html.index('<section class="author ')
        author_end = html.index("</section>", author_start)
        author_markup = html[author_start:author_end]
        hero = html[html.index('<section class="hero"'):author_start]

        self.assertTrue((ROOT / "assets/arturo-valdez-holding-elocuencia-sin-miedo.png").is_file())
        self.assertRegex(
            author_markup,
            r'<img class="author-book-illustration" src="assets/arturo-valdez-holding-elocuencia-sin-miedo\.png"[^>]*alt="Ilustración generada con IA de Arturo Valdéz sosteniendo Elocuencia sin miedo">',
        )
        self.assertRegex(
            author_markup,
            r'<figcaption class="generated-image-caption">Ilustración generada con IA; representa a Arturo con su libro\.</figcaption>',
        )
        self.assertIn('src="assets/arturo-modoverbo.png"', hero)
        self.assertNotIn("arturo-valdez-holding-elocuencia-sin-miedo.png", hero)

    def test_generated_image_caption_has_a_dark_contrast_surface(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        caption_rule = re.search(r"\.generated-image-caption\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(caption_rule)
        declarations = caption_rule.group(1)
        self.assertRegex(declarations, r"background\s*:\s*var\(--ink\)")
        self.assertRegex(declarations, r"color\s*:\s*var\(--paper\)")
        self.assertRegex(declarations, r"padding\s*:")


if __name__ == "__main__":
    unittest.main()
