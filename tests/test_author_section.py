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
    def test_author_section_sits_between_fit_and_offer_with_local_portrait(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parsed = SectionParser()
        parsed.feed(html)
        section_classes = [section.get("class", "") for section in parsed.sections]
        fit = next(i for i, classes in enumerate(section_classes) if "fit" in classes.split())
        author = next(i for i, classes in enumerate(section_classes) if "author" in classes.split())
        offer = next(i for i, classes in enumerate(section_classes) if "offer" in classes.split())
        self.assertEqual(author, fit + 1)
        self.assertEqual(offer, author + 1)
        self.assertIn("Arturo", html)
        self.assertIn("Modo Verbo", html)
        portrait = next(image for image in parsed.images if "author-portrait" in image.get("class", ""))
        self.assertTrue((ROOT / portrait["src"]).is_file())
        self.assertTrue(portrait.get("alt"))
        self.assertNotRegex(html, r"(?i)(20 años|50[ .]?000 personas|50 mil personas)")

    def test_mobile_hero_actions_have_equal_touch_targets(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertRegex(css, r"\.hero-actions\s*\{[^}]*justify-content\s*:\s*center")
        self.assertRegex(css, r"\.hero-actions\s*>\s*a\s*\{[^}]*min-height\s*:\s*(?:4[4-9]|[5-9]\d)px")
        self.assertRegex(css, r"\.hero-actions\s*>\s*a\s*\{[^}]*min-width\s*:")


if __name__ == "__main__":
    unittest.main()
