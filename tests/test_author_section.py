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


class AuthorSectionTests(unittest.TestCase):
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
        mobile_rules = css[css.rfind("@media(max-width:760px){"):]
        self.assertTrue(mobile_rules)
        self.assertRegex(
            mobile_rules,
            r"\.author-grid\s*\{[^}]*grid-template-columns\s*:\s*1fr",
        )


if __name__ == "__main__":
    unittest.main()
