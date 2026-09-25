import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestimonialSectionTests(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.css = (ROOT / "styles.css").read_text(encoding="utf-8")

    def test_hero_social_proof_links_to_the_testimonial_section(self):
        hero_start = self.html.index('<section class="hero"')
        hero_end = self.html.index("</section>", hero_start)
        hero = self.html[hero_start:hero_end]
        self.assertRegex(hero, r'<a\b[^>]*href="#resenas"[^>]*>')
        self.assertIn("4 testimonios de lectores", hero)
        self.assertIn("Leer testimonios", hero)

    def test_hero_social_proof_typography_remains_readable_at_mobile_and_desktop_sizes(self):
        copy = re.search(r"\.social-proof-copy\s*\{([^{}]*)\}", self.css)
        stars = re.search(r"\.social-proof-stars\s*\{([^{}]*)\}", self.css)
        link = re.search(r"\.social-proof-link\s*\{([^{}]*)\}", self.css)
        self.assertIsNotNone(copy)
        self.assertIsNotNone(stars)
        self.assertIsNotNone(link)
        self.assertRegex(copy.group(1), r"font-size\s*:\s*(?:1[1-9]|[2-9]\d)px")
        self.assertRegex(stars.group(1), r"font-size\s*:\s*(?:1[2-9]|[2-9]\d)px")
        self.assertRegex(link.group(1), r"font-size\s*:\s*(?:1[1-9]|[2-9]\d)px")

    def test_hero_portrait_sprite_uses_scaled_full_face_crops(self):
        hero_avatar = re.search(r"\.social-proof-avatars\s+\.testimonial-avatar\s*\{([^{}]*)\}", self.css)
        self.assertIsNotNone(hero_avatar)
        self.assertRegex(hero_avatar.group(1), r"background-size\s*:\s*296px\s+592px")
        for name, position in (
            ("santiago", r"-30px\s+-170px"),
            ("valentina", r"-30px\s+-299px"),
            ("daniel", r"-30px\s+-429px"),
            ("isabel", r"-30px\s+-551px"),
        ):
            with self.subTest(name=name):
                crop = re.search(rf"\.social-proof-avatars\s+\.reader-{name}\s*\{{([^{{}}]*)\}}", self.css)
                self.assertIsNotNone(crop)
                self.assertRegex(crop.group(1), rf"background-position\s*:\s*{position}")

        mobile = re.search(r"@media\s*\(max-width:\s*760px\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}", self.css)
        self.assertIsNotNone(mobile)
        self.assertRegex(mobile.group(1), r"\.social-proof-avatars\s+\.testimonial-avatar\s*\{[^}]*background-size\s*:\s*213px\s+426px")
        for name, position in (
            ("santiago", r"-22px\s+-122px"),
            ("valentina", r"-22px\s+-215px"),
            ("daniel", r"-22px\s+-309px"),
            ("isabel", r"-22px\s+-397px"),
        ):
            with self.subTest(mobile_name=name):
                crop = re.search(rf"\.social-proof-avatars\s+\.reader-{name}\s*\{{([^{{}}]*)\}}", mobile.group(1))
                self.assertIsNotNone(crop)
                self.assertRegex(crop.group(1), rf"background-position\s*:\s*{position}")

    def test_four_exact_owner_supplied_quotes_and_attributions_are_displayed(self):
        reviews_start = self.html.index('id="resenas"')
        reviews_end = self.html.index("</section>", reviews_start)
        reviews = self.html[reviews_start:reviews_end]

        expected = (
            ("SANTIAGO R.", "INGENIERO", "26", "Qué libro tan brutal. La verdad no pensé que me fuera a servir tanto, pero desde que lo empecé a leer he notado un cambio real en la forma en la que me expreso. Ahora me siento mucho más seguro hablando en público y en mi trabajo. Súper recomendado."),
            ("VALENTINA M.", "ESTUDIANTE", "22", "Amooo este libro! De verdad me ha ayudado un montón a perder el miedo de hablar y a organizar mejor mis ideas. Los ejercicios son muy prácticos y fáciles de aplicar. Ya no me trabo tanto cuando tengo que presentar en la universidad. Me encantó."),
            ("DANIEL G.", "MARKETING", "29", "Excelente contenido. Me gustó mucho que no se queda solo en teoría, sino que da herramientas reales para el día a día. Lo he aplicado en reuniones de trabajo y he recibido comentarios muy positivos sobre mi forma de comunicar. Vale totalmente la pena."),
            ("ISABEL C.", "EMPRENDEDORA", "31", "No soy de leer muchos libros, pero este sí me atrapó. Está escrito de forma sencilla, se entiende fácil y está lleno de ejemplos útiles. Me ha servido un montón para expresarme mejor en mi vida personal también. Lo súper recomiendo!"),
        )
        self.assertEqual(reviews.count("testimonial-card"), 4)
        for name, role, age, quote in expected:
            with self.subTest(name=name):
                self.assertIn(name, reviews)
                self.assertIn(f"{role} · {age}", reviews)
                self.assertIn(quote, reviews)

    def test_testimonial_section_is_between_offer_and_author_and_uses_local_portraits(self):
        offer_start = self.html.index('<section class="offer ')
        reviews_start = self.html.index('<section class="testimonials ')
        author_start = self.html.index('<section class="author ')
        self.assertLess(offer_start, reviews_start)
        self.assertLess(reviews_start, author_start)
        self.assertEqual(self.html.count('id="resenas"'), 1)
        self.assertIn("assets/testimonials-readers.png", self.css)
        self.assertTrue((ROOT / "assets/testimonials-readers.png").is_file())
        self.assertRegex(self.css, r"\.testimonial-avatar\s*\{[^}]*background-image\s*:\s*url\(['\"]?assets/testimonials-readers\.png")

    def test_no_unsupported_aggregate_rating_or_review_count_is_added(self):
        self.assertNotRegex(self.html, r"(?i)\b(?:4\.9|4,9|1200\+|1\s?200\+|más de 1200|miles de reseñas)\b")
        self.assertNotRegex(self.html, r"(?i)(compra verificada|resultado garantizado|garantiza que)\b")

    def test_testimonial_cards_stack_on_mobile(self):
        mobile = re.search(
            r"@media\s*\(max-width:\s*760px\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}",
            self.css,
        )
        self.assertIsNotNone(mobile)
        self.assertRegex(mobile.group(1), r"\.testimonial-grid\s*\{[^}]*grid-template-columns\s*:\s*1fr")


if __name__ == "__main__":
    unittest.main()
