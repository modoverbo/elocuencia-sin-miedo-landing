import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT = "https://pay.hotmart.com/H107735669O?checkoutMode=2&off=s5txzdcx"
EXPECTED_SECTIONS = [
    "section problem", "statement", "section mechanism", "section preview", "section",
    "section transformation", "section author", "section testimonials", "section offer",
    "section faq", "final",
]


class LandingDocument(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = []
        self.elements = []
        self.ancestors = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = attributes.get("class", "").split()
        if tag == "section":
            self.sections.append(" ".join(classes))
        if tag in ("section", "div", "article", "dialog"):
            self.ancestors.append(classes)
        self.elements.append((tag, attributes, list(self.ancestors)))

    def handle_endtag(self, tag):
        if tag in ("section", "div", "article", "dialog"):
            for index in range(len(self.ancestors) - 1, -1, -1):
                del self.ancestors[index:]
                break


class LandingV2Tests(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.script = (ROOT / "script.js").read_text(encoding="utf-8")
        self.document = LandingDocument()
        self.document.feed(self.html)

    def test_literal_reference_section_order_is_preserved(self):
        self.assertEqual(self.document.sections, EXPECTED_SECTIONS)

    def test_offer_mockup_remains_inside_the_reference_offer_grid(self):
        offer_start = self.html.index('<section class="section offer"')
        offer_end = self.html.index("</section>", offer_start)
        offer = self.html[offer_start:offer_end]
        self.assertIn('class="wrap offer-grid"', offer)
        self.assertIn('src="assets/reference/offer-mockup.png"', offer)
        self.assertNotIn("offer-card", offer)

    def test_reference_copy_and_three_page_visual_remain_intact(self):
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", self.html)).casefold()
        self.assertIn("lo que piensas merece sonar tan claro como lo tienes en la cabeza", text)
        self.assertIn("empieza a hablar con más claridad", text)
        preview_start = self.html.index('<section class="section preview"')
        preview_end = self.html.index('<div class="interactive-preview"', preview_start)
        pages = re.findall(r'<img class="preview-teaser-page" src="([^"]+)"', self.html[preview_start:preview_end])
        self.assertEqual(pages, ["assets/edition/page-02.webp", "assets/edition/page-03.webp", "assets/edition/page-04.webp"])

    def test_page_turning_preview_is_separate_from_the_reference_three_page_visual(self):
        static_preview = self.html.index('<section class="section preview"')
        interactive_preview = self.html.index('<div class="interactive-preview"')
        benefits = self.html.index('<section class="section" id="incluye"')
        self.assertLess(static_preview, interactive_preview)
        self.assertLess(interactive_preview, benefits)
        self.assertIn('id="flipbook"', self.html)
        self.assertIn('id="preview-next"', self.html)
        self.assertIn("flipNext", self.script)

    def test_all_checkout_links_keep_the_existing_hotmart_destination(self):
        checkout_links = [attrs.get("href") for tag, attrs, _ in self.document.elements
                          if tag == "a" and "hotmart__button-checkout" in attrs.get("class", "").split()]
        self.assertGreaterEqual(len(checkout_links), 4)
        self.assertTrue(all(link == CHECKOUT for link in checkout_links))

    def test_offer_copy_matches_the_reference_while_keeping_the_hotmart_checkout(self):
        offer = self.html[self.html.index('<section class="section offer"'):self.html.index("</section>", self.html.index('<section class="section offer"'))]
        self.assertIn('<div class="old">US$28</div>', offer)
        self.assertIn("50% DE DESCUENTO", offer)
        self.assertIn("US$14", offer)
        self.assertIn("Precio final del producto. Pueden aplicar impuestos según país.", offer)
        self.assertIn("pay.hotmart.com/H107735669O?checkoutMode=2", offer)

    def test_reference_palette_spacing_and_responsive_layout_rules_are_retained(self):
        for declaration in (
            "--ink:#111310", "--green:#062f29", "--gold:#d4aa3a", "--paper:#f5f2ea",
            "grid-template-columns:1.03fr .97fr", "grid-template-columns:.85fr 1.15fr",
            "@media(max-width:1100px)", "@media(max-width:900px)", "@media(max-width:560px)",
        ):
            with self.subTest(declaration=declaration):
                self.assertIn(declaration.replace(" ", ""), self.css.replace(" ", ""))

    def test_reference_testimonial_disclosure_is_visible_in_styles(self):
        self.assertIn("Demo educativa: los testimonios y retratos son ficticios e ilustrativos", self.html)
        self.assertIn(".testimonials.demo-note{display:block", self.css.replace(" ", ""))


if __name__ == "__main__":
    unittest.main()
