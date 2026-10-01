import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT_URL = "https://pay.hotmart.com/H107735669O?checkoutMode=2&off=s5txzdcx"
REFERENCE_SECTIONS = [
    "section problem",
    "statement",
    "section mechanism",
    "section preview",
    "section",
    "section transformation",
    "section author",
    "section testimonials",
    "section offer",
    "section faq",
    "final",
]


class LandingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = []
        self.ids = []
        self.local_images = []
        self.local_links = []
        self.checkout_links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "section":
            self.sections.append(attributes.get("class", ""))
        element_id = attributes.get("id")
        if element_id:
            self.ids.append(element_id)
        if tag == "img":
            source = attributes.get("src", "")
            if source.startswith("assets/"):
                self.local_images.append(source)
        if tag == "a":
            href = attributes.get("href", "")
            if href.startswith("#"):
                self.local_links.append(href[1:])
            if "hotmart__button-checkout" in attributes.get("class", "").split():
                self.checkout_links.append(href)


class AuthorAndLandingTests(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.script = (ROOT / "script.js").read_text(encoding="utf-8")
        self.parser = LandingParser()
        self.parser.feed(self.html)

    def test_social_preview_keeps_its_absolute_versioned_cover(self):
        expected = "https://modoverbo.vercel.app/assets/edition/cover-social-v2.jpg"
        self.assertIn(f'property="og:image" content="{expected}"', self.html)
        self.assertIn(f'name="twitter:image" content="{expected}"', self.html)
        self.assertTrue((ROOT / "assets/edition/cover-social-v2.jpg").is_file())

    def test_stylesheet_url_has_a_cache_busting_version(self):
        self.assertIn('href="styles.css?v=20261001-reference-fidelity"', self.html)

    def test_reference_sections_keep_the_supplied_order(self):
        self.assertEqual(self.parser.sections, REFERENCE_SECTIONS)

    def test_hash_links_resolve_to_unique_existing_ids(self):
        self.assertEqual(len(self.parser.ids), len(set(self.parser.ids)))
        known_ids = set(self.parser.ids)
        self.assertTrue(self.parser.local_links)
        self.assertTrue(all(anchor in known_ids for anchor in self.parser.local_links))

    def test_reference_hero_keeps_its_book_mockup_and_checkout_action(self):
        hero_start = self.html.index('<header class="hero"')
        hero_end = self.html.index("</header>", hero_start)
        hero = self.html[hero_start:hero_end]
        self.assertIn('class="book" src="assets/edition/cover-mockup-transparent.png"', hero)
        self.assertIn('class="btn hotmart-fb hotmart__button-checkout"', hero)
        self.assertIn("12 ejemplos", hero)
        self.assertIn("ilustrativos", hero)

    def test_hero_illustrative_portraits_match_the_first_four_testimonials(self):
        hero = self.html[self.html.index('<header class="hero"'):self.html.index('</header>')]
        testimonials = self.html[self.html.index('<section class="section testimonials"'):]
        expected = [
            f"assets/testimonials/{name}-demo.webp"
            for name in ("santiago", "valentina", "daniel", "isabel")
        ]
        hero_portraits = re.findall(r'<img class="avatar-img" src="([^"]+)"', hero)
        testimonial_portraits = re.findall(r'<img class="testimonial-avatar" src="([^"]+)"', testimonials)
        self.assertEqual(hero_portraits, expected)
        self.assertEqual(testimonial_portraits[:4], expected)
        self.assertTrue(all((ROOT / path).is_file() for path in hero_portraits))

    def test_mobile_hero_conversion_group_centers_its_contents(self):
        hero = self.html[self.html.index('<header class="hero"'):self.html.index('</header>')]
        self.assertIn('<div class="hero-conversion">', hero)
        self.assertLess(hero.index('<div class="hero-conversion">'), hero.index('class="hero-rating"'))
        exception_styles = self.css.split('/* Approved product exceptions:', 1)[1]
        self.assertRegex(
            exception_styles,
            r'@media\s*\(max-width:\s*560px\)\s*\{\s*\.hero-conversion\s*\{'
            r'(?=[^}]*align-items:\s*center)(?=[^}]*text-align:\s*center)',
        )

    def test_preview_has_no_static_page_strip_and_keeps_the_flipbook_link(self):
        preview_start = self.html.index('<section class="section preview"')
        preview_end = self.html.index('<div class="interactive-preview"', preview_start)
        preview = self.html[preview_start:preview_end]
        self.assertNotIn('class="pages"', preview)
        self.assertNotIn('class="preview-teaser-page"', preview)
        self.assertIn('href="#interactive-preview"', preview)

    def test_interactive_flipbook_uses_the_corrected_local_page_manifest(self):
        manifest = json.loads((ROOT / "assets/edition/preview-manifest.json").read_text(encoding="utf-8"))
        expected = ["assets/edition/cover.webp"] + [
            f"assets/edition/page-{page:02d}.webp" for page in range(2, 14)
        ]
        self.assertEqual(manifest["preview_pages"], [
            {"pdf_page": page, "path": path} for page, path in enumerate(expected, start=1)
        ])
        preview_start = self.html.index('<div class="interactive-preview"')
        preview_end = self.html.index('<section class="section" id="incluye"', preview_start)
        preview = self.html[preview_start:preview_end]
        page_assets = [
            (int(page), path)
            for page, path in re.findall(
                r'<div class="preview-page[^\"]*" data-page="(\d+)"[^>]*>\s*<img src="([^\"]+)"',
                preview,
            )
            if int(page) <= 13
        ]
        self.assertEqual(page_assets, list(enumerate(expected, start=1)))

    def test_interactive_preview_has_keyboard_controls_and_reduced_motion_support(self):
        for element_id in ("interactive-preview", "flipbook", "preview-counter", "preview-previous", "preview-next", "preview-replay"):
            self.assertIn(f'id="{element_id}"', self.html)
        self.assertIn("keydown", self.script)
        self.assertIn("Enter", self.script)
        self.assertIn("prefers-reduced-motion", self.script)
        self.assertIn("prefers-reduced-motion", self.css)

    def test_author_and_offer_follow_the_reference_with_local_artwork(self):
        author = self.html.index('<section class="section author"')
        testimonials = self.html.index('<section class="section testimonials"')
        offer = self.html.index('<section class="section offer"')
        self.assertLess(author, testimonials)
        self.assertLess(testimonials, offer)
        self.assertIn('src="assets/edition/arturo-holding-book.webp"', self.html)
        self.assertIn('src="assets/reference/offer-mockup.png"', self.html)
        self.assertTrue((ROOT / "assets/reference/offer-mockup.png").is_file())

    def test_author_biography_preserves_existing_owner_supplied_facts(self):
        author = self.html[self.html.index('<section class="section author"'):self.html.index('<section class="section testimonials"')]
        for copy in (
            "Arturo Valdés",
            "+20",
            "Años enseñando expresión oral",
            "+50.000",
            "Personas formadas, según la información actual de la marca",
        ):
            self.assertIn(copy, author)

    def test_checkout_links_keep_the_existing_hotmart_destination(self):
        self.assertGreaterEqual(len(self.parser.checkout_links), 4)
        self.assertTrue(all(link.replace("&amp;", "&") == CHECKOUT_URL for link in self.parser.checkout_links))

    def test_offer_preserves_literal_reference_price_and_tax_copy(self):
        self.assertIn(
            '<div class="top"><b>50% DE DESCUENTO</b> · Precio especial: <b>US$14</b> '
            '· Pago único · Acceso inmediato a tu correo electrónico</div>',
            self.html,
        )
        for copy in (
            '<div class="old">US$28</div>',
            '<span class="discount">50% DE DESCUENTO</span>',
            '<div class="price">US$14 <small>pago único</small></div>',
            "Precio final del producto. Pueden aplicar impuestos según país.",
        ):
            self.assertIn(copy, self.html)

    def test_every_referenced_local_image_exists(self):
        self.assertTrue(self.parser.local_images)
        for source in self.parser.local_images:
            with self.subTest(source=source):
                self.assertTrue((ROOT / source).is_file())

    def test_editorial_reference_tokens_and_responsive_breakpoints_are_present(self):
        self.assertIn("--green:#062f29", self.css)
        self.assertIn("--gold:#d4aa3a", self.css)
        self.assertIn("--paper:#f5f2ea", self.css)
        self.assertIn("font-family:'DM Sans',sans-serif", self.css)
        self.assertIn("font-family:'Playfair Display',serif", self.css)
        for breakpoint in ("@media(max-width:1100px)", "@media(max-width:900px)", "@media(max-width:560px)"):
            self.assertIn(breakpoint, self.css)

    def test_footer_is_part_of_the_reference_document(self):
        self.assertIn('<footer class="footer">', self.html)
        self.assertIn("© 2026 · Pago procesado por Hotmart", self.html)
        self.assertIn(".footerin{display:flex;justify-content:space-between", self.css)


if __name__ == "__main__":
    unittest.main()
