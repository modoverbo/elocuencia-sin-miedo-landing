import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image


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


class SocialMetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metadata = {}
        self.canonical_urls = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "meta":
            key = attributes.get("property") or attributes.get("name")
            if key:
                self.metadata[key] = attributes.get("content")
        elif tag == "link" and attributes.get("rel") == "canonical":
            self.canonical_urls.append(attributes.get("href"))


class AuthorSectionTests(unittest.TestCase):
    def test_social_preview_uses_absolute_versioned_cover_metadata(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parser = SocialMetadataParser()
        parser.feed(html)
        expected_image = "https://modoverbo.vercel.app/assets/edition/cover-social-v2.jpg"

        self.assertEqual(parser.canonical_urls, ["https://modoverbo.vercel.app/"])
        self.assertEqual(parser.metadata.get("og:url"), "https://modoverbo.vercel.app/")
        self.assertEqual(parser.metadata.get("og:image"), expected_image)
        self.assertEqual(parser.metadata.get("og:image:type"), "image/jpeg")
        self.assertEqual(parser.metadata.get("og:image:width"), "1024")
        self.assertEqual(parser.metadata.get("og:image:height"), "1536")
        self.assertEqual(parser.metadata.get("twitter:card"), "summary_large_image")
        self.assertEqual(parser.metadata.get("twitter:image"), expected_image)
        self.assertTrue((ROOT / "assets/edition/cover-social-v2.jpg").is_file())

    def test_landing_stylesheet_url_has_a_cache_busting_version(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="styles.css?v=20260925-reference-v6"', html)

    def test_hash_navigation_reserves_space_beneath_sticky_header(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        document_rule = re.search(r"(?:^|})\s*html\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(document_rule)
        self.assertRegex(document_rule.group(1), r"scroll-padding-top\s*:\s*80px")
        self.assertRegex(document_rule.group(1), r"scroll-behavior\s*:\s*smooth")
        reduced_motion = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}",
            css,
        )
        self.assertIsNotNone(reduced_motion)
        self.assertRegex(reduced_motion.group(1), r"html\s*\{[^}]*scroll-behavior\s*:\s*auto")

    def test_reference_alignment_uses_a_larger_responsive_hero_portrait(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertRegex(css, r"\.hero-portrait-frame\s*\{[^}]*width\s*:\s*180px")
        mobile = re.search(r"@media\s*\(max-width:\s*600px\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}", css)
        compact = re.search(r"@media\s*\(max-width:\s*340px\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}", css)
        self.assertIsNotNone(mobile, "The portrait needs an explicit mobile size")
        self.assertIsNotNone(compact, "The smallest viewport needs a compact portrait size")
        self.assertRegex(mobile.group(1), r"\.hero-portrait-frame\s*\{[^}]*width\s*:\s*160px")
        self.assertRegex(compact.group(1), r"\.hero-portrait-frame\s*\{[^}]*width\s*:\s*144px")

    def test_method_cards_stack_in_one_column_on_mobile(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        mobile = re.search(r"@media\s*\(max-width:\s*600px\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}", css)
        self.assertIsNotNone(mobile, "Method-card mobile layout needs an explicit breakpoint")
        self.assertRegex(mobile.group(1), r"\.method-grid\s*\{[^}]*grid-template-columns\s*:\s*1fr")

    def test_offer_mockup_blends_its_white_background_into_the_ivory_card(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertRegex(css, r"\.mini-book\s+img\s*\{[^}]*mix-blend-mode\s*:\s*multiply")

    def test_checkout_actions_share_green_gold_reset_including_footer_and_closing(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        shared = re.search(r"a\.hotmart-fb\.hotmart__button-checkout\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(shared, "Hotmart checkout links need one local visual reset")
        for declaration in (
            r"background\s*:\s*var\(--forest\)\s*!important",
            r"color\s*:\s*var\(--paper\)\s*!important",
            r"border\s*:\s*1px solid var\(--gold\)\s*!important",
            r"box-shadow\s*:\s*none\s*!important",
        ):
            with self.subTest(declaration=declaration):
                self.assertRegex(shared.group(1), declaration)
        self.assertNotRegex(css, r"\.footer-cta\s*\{")
        self.assertNotRegex(css, r"\.closing\s+\.button\s*\{[^}]*background\s*:\s*var\(--gold\)")
        self.assertRegex(css, r"\.mobile-buy:not\(\[hidden\]\)\s*\{[^}]*background\s*:\s*var\(--paper\)")
        self.assertRegex(css, r"\.mobile-buy:not\(\[hidden\]\)\s*\{[^}]*color\s*:\s*var\(--forest\)")
        self.assertRegex(css, r"\.mobile-buy:not\(\[hidden\]\)\s+\.mobile-buy-wordmark\s*\{[^}]*color\s*:\s*var\(--forest\)")

    def test_header_checkout_action_keeps_ten_pixel_text_and_touch_height_at_320px(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertRegex(css, r"\.header-buy\s*\{[^}]*min-height\s*:\s*44px")
        mobile = re.search(r"@media\s*\(max-width:\s*440px\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}", css)
        compact = re.search(r"@media\s*\(max-width:\s*380px\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}", css)
        self.assertIsNotNone(mobile)
        self.assertIsNotNone(compact)
        self.assertRegex(mobile.group(1), r"\.header-buy\s*\{[^}]*min-height\s*:\s*44px")
        self.assertRegex(mobile.group(1), r"\.header-buy\s*\{[^}]*font-size\s*:\s*10px")
        self.assertNotRegex(compact.group(1), r"\.header-buy\s*\{[^}]*font-size\s*:\s*[0-9]px")

    def test_preview_caption_keeps_chapter_label_separate_from_page_counter(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        caption = re.search(r"\.stage-caption\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(caption, "Preview caption needs a layout rule that separates its labels")
        declarations = dict(
            (key.strip(), value.strip())
            for declaration in caption.group(1).split(";")
            if ":" in declaration
            for key, value in [declaration.split(":", 1)]
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
        self.assertRegex(sticky_header.group(1), r"position\s*:\s*sticky")
        self.assertRegex(sticky_header.group(1), r"top\s*:\s*0")
        post_hero_bar = re.search(r'<div class="mobile-buy"[^>]*id="post-hero-buy"[^>]*>', html)
        self.assertIsNotNone(post_hero_bar)
        for attribute in ('hidden', 'inert', 'aria-hidden="true"'):
            self.assertIn(attribute, post_hero_bar.group(0))
        self.assertRegex(css, r"\.mobile-buy\[hidden\]\s*\{[^}]*display\s*:\s*none")
        self.assertRegex(css, r"\.mobile-buy:not\(\[hidden\]\)\s*\{[^}]*display\s*:\s*flex")
        self.assertRegex(css, r"@media\s*\(max-width:\s*760px\)[\s\S]*?\.mobile-buy:not\(\[hidden\]\)\s*\{[^}]*display\s*:\s*grid")
        self.assertIn('id="preview-controls"', html)
        self.assertIn('id="site-footer"', html)
        self.assertIn('id="preview-next"', html)
        self.assertNotIn('id="footer-purchase-cta"', html)
        self.assertIn("Demo educativa", html)
        self.assertIn("© 2026 Elocuencia sin miedo.", html)
        self.assertRegex(css, r"@media\s*\(prefers-reduced-motion:\s*reduce\)")

    def test_editorial_brand_uses_green_gold_palette_and_display_swap_fonts(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        root_tokens = re.search(r":root\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(root_tokens)
        declarations = dict(
            (key.strip(), value.strip())
            for declaration in root_tokens.group(1).split(";")
            if ":" in declaration
            for key, value in [declaration.split(":", 1)]
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
        self.assertRegex(css, r"font-family\s*:\s*var\(--sans\)")
        self.assertRegex(css, r"font-family\s*:\s*var\(--serif\)")
        self.assertNotRegex(f"{html}\n{css}", r"(?i)poppins|--yellow|#f9db43|#ddaa19|#f3d75b|#ffde4b")
        self.assertRegex(css, r"\.hero\s*\{[^}]*background\s*:\s*var\(--paper\)")
        self.assertRegex(css, r"\.preview\s*\{[^}]*background\s*:\s*var\(--forest\)")
        for color in ("#f9db43", "#ddaa19", "#ba8100", "#866b10", "#fff6d8", "#dcbf42", "#edcd52"):
            self.assertNotIn(color, f"{html}\n{css}")

    def test_corrected_edition_preview_uses_local_pdf_pages_in_order(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        manifest = json.loads((ROOT / "assets/edition/preview-manifest.json").read_text(encoding="utf-8"))
        preview_start = html.index('<section class="preview ')
        preview_end = html.index('<section class="benefits ', preview_start)
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
        self.assertIn('src="assets/edition/cover.webp"', html)
        self.assertGreaterEqual(html.count('src="assets/edition/cover.webp"'), 2)
        for path in expected_assets:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())
        for path in manifest["supplied_assets"]:
            with self.subTest(path=path):
                self.assertTrue((ROOT / "assets/edition" / path).is_file())

    def test_authorized_reader_opinions_have_a_destination_and_not_an_invented_aggregate(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="#resenas"', html)
        self.assertIn('id="resenas"', html)
        self.assertEqual(html.count("class=\"testimonial-card\""), 4)
        self.assertNotRegex(html, r"(?i)\b(?:1200\+|1\s?200\+|más de 1200)\b")
    def test_landing_sections_follow_the_reference_sales_flow(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SalesLandingParser()
        parsed.feed(html)

        expected_order = ["hero", "facts", "recognition", "method", "statement", "preview", "benefits", "offer", "testimonials", "author", "faq", "closing"]
        actual_order = [
            next(name for name in expected_order if name in section["attributes"].get("class", "").split())
            for section in parsed.sections
        ]
        self.assertEqual(actual_order, expected_order)

        method = next(section for section in parsed.sections if "method" in section["attributes"].get("class", "").split())
        self.assertEqual(html.count('class="method-card'), 4)
        self.assertIn("Escuchar", " ".join(method["text"]))
        self.assertIn("Ordenar", " ".join(method["text"]))
        self.assertIn("Practicar", " ".join(method["text"]))
        self.assertIn("Aplicar", " ".join(method["text"]))
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

    def test_authorized_testimonial_section_is_between_offer_and_author(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SalesLandingParser()
        parsed.feed(html)
        sections = [section["attributes"].get("class", "").split() for section in parsed.sections]
        self.assertLess(next(i for i, classes in enumerate(sections) if "offer" in classes), next(i for i, classes in enumerate(sections) if "testimonials" in classes))
        self.assertLess(next(i for i, classes in enumerate(sections) if "testimonials" in classes), next(i for i, classes in enumerate(sections) if "author" in classes))

    def test_hero_uses_a_compact_centered_original_portrait(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        hero = html[html.index('<section class="hero"'):html.index('</section>', html.index('<section class="hero"'))]
        self.assertIn('src="assets/arturo-modoverbo.png"', hero)
        self.assertIn('alt="Arturo Valdés, autor de Elocuencia sin miedo"', hero)
        self.assertNotIn("hero-book-photo", hero)
        frame = re.search(r"\.hero-portrait-frame\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(frame)
        self.assertIn("50%", frame.group(1))
        self.assertIn("var(--gold)", frame.group(1))
        self.assertRegex(frame.group(1), r"width\s*:\s*(?:clamp|\d{2,3}px)")
    def test_sales_hero_centers_original_portrait_headline_and_primary_cta(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SalesLandingParser()
        parsed.feed(html)
        hero = next(section for section in parsed.sections if "hero" in section["attributes"].get("class", "").split())
        self.assertEqual(parsed.sections[0], hero)
        self.assertIn("Arturo Valdés", " ".join(hero["text"]))
        hero_text = re.sub(r"\s+", " ", " ".join(hero["text"]))
        self.assertIn("Haz que tus ideas lleguen con claridad.", hero_text)
        self.assertIn("QUIERO HABLAR CON CLARIDAD", hero_text)
        portrait = next(image for image in hero["images"] if "hero-portrait" in image.get("class", ""))
        self.assertEqual(portrait.get("src"), "assets/arturo-modoverbo.png")
        self.assertTrue((ROOT / portrait["src"]).is_file())
        self.assertIn("hero-author-caption", html)
        self.assertNotRegex(html, r"(?i)(resultado garantizado|garantiza que)")
    def test_primary_purchase_cta_repeats_across_sections_and_offer_states_owner_terms(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SalesLandingParser()
        parsed.feed(html)

        self.assertFalse(parsed.marketing_buttons)
        self.assertGreaterEqual(len(parsed.checkout_links), 5)
        for link in parsed.checkout_links:
            visible_label = "".join(link["text"]).replace("↗", "").strip()
            self.assertEqual(visible_label.casefold(), "quiero hablar con claridad")
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

    def test_primary_ctas_are_prominent_and_header_cta_stays_on_small_screens(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        header_cta = re.search(r'<a class="header-buy[^>]*>(.*?)</a>', html, re.DOTALL)
        self.assertIsNotNone(header_cta)
        self.assertIn("Quiero hablar con claridad", header_cta.group(1))
        self.assertRegex(css, r"\.header-buy\s*\{[^}]*min-height\s*:\s*44px")
        self.assertRegex(css, r"\.preview-controls\s+button\s*\{[^}]*min-height\s*:\s*4[0-9]px")
        self.assertNotRegex(css, r"@media\s*\(max-width:\s*(?:380|440)px\)[\s\S]*?\.header-buy\s*\{[^}]*display\s*:\s*none")
    def test_author_layout_collapses_to_one_column_on_mobile(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertRegex(
            css,
            r"@media\s*\(max-width:\s*760px\)[\s\S]*?\.section-heading,\s*\.preview-grid,\s*\.offer-card,\s*\.author-grid,\s*\.faq-grid,\s*\.testimonial-grid\s*\{[^}]*grid-template-columns\s*:\s*1fr",
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
        reduced_motion_rules = re.findall(r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", css)
        self.assertTrue(reduced_motion_rules)
        self.assertRegex(
            "\n".join(reduced_motion_rules),
            r"\.preview-swipe-cue\.is-animated\s*\{[^}]*animation\s*:\s*none",
        )
        self.assertRegex(
            "\n".join(reduced_motion_rules),
            r"\.mobile-buy:not\(\[hidden\]\)\s*\{[^}]*transition\s*:\s*none",
        )

    def test_mobile_header_keeps_brand_and_checkout_action(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = MobileBrandParser()
        parsed.feed(html)
        self.assertEqual(len(parsed.header_wordmarks), 1)
        self.assertEqual(parsed.header_wordmarks[0].get("href"), "#inicio")
        self.assertEqual(parsed.header_wordmarks[0].get("aria-label"), "Elocuencia sin miedo, inicio")
        self.assertEqual(len(parsed.banner_links), 2)
        self.assertIn("Quiero hablar con claridad", html[html.index('<header'):html.index('</header>')])
    def test_supplied_book_holding_image_is_in_later_author_section(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        author_start = html.index('<section class="author ')
        author_end = html.index("</section>", author_start)
        author_markup = html[author_start:author_end]
        hero = html[html.index('<section class="hero"'):author_start]
        self.assertTrue((ROOT / "assets/edition/arturo-holding-book.webp").is_file())
        self.assertNotIn('src="assets/edition/arturo-holding-book.webp"', hero)
        self.assertIn('src="assets/edition/arturo-holding-book.webp"', author_markup)
        self.assertIn('alt="Arturo Valdés sosteniendo Elocuencia sin miedo"', author_markup)
        self.assertIn('src="assets/arturo-modoverbo.png"', hero)
        self.assertNotIn("arturo-valdez-holding-elocuencia-sin-miedo.png", html)
    def test_offer_mockup_is_explicitly_labeled_digital_pdf(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        offer = html[html.index('<section class="offer '):html.index('<section class="author ')]
        self.assertIn('src="assets/edition/cover-mockup-transparent.png"', offer)
        self.assertIn('alt="Mockup ilustrativo del ebook digital en PDF Elocuencia sin miedo"', offer)
        self.assertIn("EBOOK DIGITAL · PDF · 156 PÁGINAS", offer)
        self.assertIn("Pago único", offer)
        self.assertIn("Acceso inmediato", offer)
        self.assertIn("7 días de garantía", offer)

    def test_offer_mockup_uses_transparent_png_asset(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        offer = html[html.index('<section class="offer '):html.index('<section class="author ')]
        self.assertIn('src="assets/edition/cover-mockup-transparent.png"', offer)
        self.assertIn('width="1305" height="1205"', offer)

        asset = ROOT / "assets/edition/cover-mockup-transparent.png"
        self.assertTrue(asset.is_file(), "The offer mockup image must exist")
        with Image.open(asset) as image:
            self.assertEqual(image.mode, "RGBA")
            self.assertEqual(image.size, (1305, 1205))
            self.assertEqual(image.getpixel((0, 0))[3], 0, "The outer background must be transparent")

    def test_all_non_preview_images_are_responsive_and_inside_layout_has_no_fixed_height_frames(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        global_image_rule = re.search(r"(?s)(?:^|})\s*img\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(global_image_rule)
        self.assertRegex(global_image_rule.group(1), r"max-width\s*:\s*100%")
        self.assertRegex(global_image_rule.group(1), r"height\s*:\s*auto")
        self.assertNotRegex(css, r"\.inside-image\s*,\s*\.inside-text\s*\{[^}]*height\s*:")
        self.assertNotIn('class="inside-image', html)
        self.assertEqual(html.count('class="method-card'), 4)
        self.assertRegex(css, r"\.method-card\s*\{[^}]*border\s*:\s*1px\s+solid[^}]*var\(--gold\)")

    def test_footer_is_a_stacked_grid_with_no_colliding_right_side_cluster(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        footer = html[html.index('<footer'):html.index('</footer>')]
        self.assertIn('id="site-footer"', footer)
        self.assertNotIn('class="footer-right"', footer)
        self.assertRegex(css, r"\.footer-inner\s*\{[^}]*display\s*:\s*grid")


if __name__ == "__main__":
    unittest.main()
