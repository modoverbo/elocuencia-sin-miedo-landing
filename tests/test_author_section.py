import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SectionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "section":
            self.sections.append(attributes)
        elif tag == "img":
            self.images.append(attributes)


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


class AuthorSectionTests(unittest.TestCase):
    def test_author_portrait_is_circular_without_rectangular_frame(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        css = re.sub(r"/\*[\s\S]*?\*/", "", css)
        portrait_rules = re.findall(r"\.author-portrait\b[^{}]*\{([^{}]*)\}", css)
        self.assertTrue(portrait_rules, "Expected styles for the author portrait")

        effective_declarations = {}
        for rule in portrait_rules:
            for declaration in rule.split(";"):
                if ":" in declaration:
                    property_name, value = declaration.split(":", 1)
                    effective_declarations[property_name.strip().lower()] = value.strip().lower()

        self.assertEqual(effective_declarations.get("border-radius"), "50%")
        self.assertEqual(effective_declarations.get("border"), "none")
        self.assertEqual(effective_declarations.get("box-shadow"), "none")

    def test_author_section_precedes_hero_with_local_portrait(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SectionParser()
        parsed.feed(html)
        section_classes = [section.get("class", "") for section in parsed.sections]
        author = next(i for i, classes in enumerate(section_classes) if "author" in classes.split())
        hero = next(i for i, classes in enumerate(section_classes) if "hero" in classes.split())
        self.assertEqual(author, 0)
        self.assertLess(author, hero)
        self.assertIn("Arturo", html)
        self.assertIn("Modo Verbo", html)
        portrait = next(image for image in parsed.images if "author-portrait" in image.get("class", ""))
        self.assertTrue((ROOT / portrait["src"]).is_file())
        self.assertTrue(portrait.get("alt"))
        self.assertNotRegex(html, r"(?i)(20 años|50[ .]?000 personas|50 mil personas)")

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
            r'<span class="preview-swipe-cue" id="preview-swipe-cue" aria-hidden="true">↔</span>',
        )
        self.assertRegex(css, r"\.preview-swipe-cue\.is-animated\s*\{[^}]*animation:[^}]*\b1\s*;?")
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


if __name__ == "__main__":
    unittest.main()
