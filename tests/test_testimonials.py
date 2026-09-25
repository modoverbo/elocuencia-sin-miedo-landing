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
        self.assertIn("5,0/5 en 4 reseñas", hero)
        self.assertIn("Más de 1.200 lectores", hero)
        self.assertNotIn("Leer testimonios", hero)

    def test_hero_social_proof_typography_remains_readable_at_mobile_and_desktop_sizes(self):
        copy = re.search(r"\.social-proof-copy\s*\{([^{}]*)\}", self.css)
        stars = re.search(r"\.social-proof-stars\s*\{([^{}]*)\}", self.css)
        readers = re.search(r"\.social-proof-readers\s*\{([^{}]*)\}", self.css)
        self.assertIsNotNone(copy)
        self.assertIsNotNone(stars)
        self.assertIsNotNone(readers)
        self.assertRegex(copy.group(1), r"font-size\s*:\s*(?:1[0-9]|[2-9]\d)px")
        self.assertRegex(stars.group(1), r"font-size\s*:\s*(?:1[2-9]|[2-9]\d)px")
        self.assertRegex(readers.group(1), r"font-size\s*:\s*(?:1[0-9]|[2-9]\d)px")

    def test_hero_portraits_use_separate_local_assets_at_mobile_size(self):
        hero_avatar = re.search(r"\.social-proof-avatars\s+\.testimonial-avatar\s*\{([^{}]*)\}", self.css)
        self.assertIsNotNone(hero_avatar)
        self.assertRegex(hero_avatar.group(1), r"width\s*:\s*30px")
        self.assertRegex(hero_avatar.group(1), r"background-size\s*:\s*cover")
        self.assertRegex(hero_avatar.group(1), r"background-position\s*:\s*center")
        mobile = re.search(r"@media\s*\(max-width:\s*760px\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}", self.css)
        self.assertIsNotNone(mobile)
        self.assertRegex(mobile.group(1), r"\.social-proof-avatars\s+\.testimonial-avatar\s*\{[^}]*width\s*:\s*24px")
        self.assertNotRegex(mobile.group(1), r"\.social-proof-avatars\s+\.testimonial-avatar\s*\{[^}]*background-size\s*:\s*\d+px")

    def test_hero_social_proof_visibly_labels_its_example_figures(self):
        hero_start = self.html.index('<section class="hero"')
        hero_end = self.html.index("</section>", hero_start)
        hero = self.html[hero_start:hero_end]
        pill_start = hero.index('class="testimonial-social-proof"')
        pill_end = hero.index("</a>", pill_start)
        self.assertIn("EJEMPLO", hero[pill_start:pill_end])

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

    def test_testimonial_portrait_labels_identify_illustrative_fictional_people(self):
        for name in ("Santiago R.", "Valentina M.", "Daniel G.", "Isabel C."):
            with self.subTest(name=name):
                self.assertIn(f'aria-label="Retrato ilustrativo de una persona ficticia: {name}"', self.html)

    def test_testimonial_section_is_between_offer_and_author_and_uses_local_portraits(self):
        offer_start = self.html.index('<section class="offer ')
        reviews_start = self.html.index('<section class="testimonials ')
        author_start = self.html.index('<section class="author ')
        self.assertLess(offer_start, reviews_start)
        self.assertLess(reviews_start, author_start)
        self.assertEqual(self.html.count('id="resenas"'), 1)
        for name in ("santiago", "valentina", "daniel", "isabel"):
            with self.subTest(name=name):
                asset = f"assets/testimonials/{name}-demo.webp"
                avatar = re.search(rf"\n\.reader-{name}\s*\{{([^{{}}]*)\}}", self.css)
                self.assertIsNotNone(avatar)
                self.assertIn(asset, avatar.group(1))
                self.assertTrue((ROOT / asset).is_file())

    def test_demo_disclosure_identifies_fictional_testimonials_portraits_and_figures(self):
        reviews_start = self.html.index('id="resenas"')
        reviews_end = self.html.index("</section>", reviews_start)
        reviews = self.html[reviews_start:reviews_end]
        footer = self.html[self.html.index("<footer"):self.html.index("</footer>")]
        for text, region in (("personas, reseñas y cifras son ficticias e ilustrativas", reviews), ("evidencia verificada antes de vender", footer)):
            with self.subTest(text=text):
                self.assertIn(text, region)

    def test_author_claims_use_owner_supplied_facts_and_canonical_name(self):
        author_start = self.html.index('<section class="author ')
        author_end = self.html.index("</section>", author_start)
        author = self.html[author_start:author_end]
        self.assertIn("Arturo Valdés", author)
        self.assertIn("experto en comunicación efectiva y expresión oral", author)
        self.assertIn("más de 20 años", author)
        self.assertIn("más de 50.000 personas", author)

    def test_readme_sets_demo_evidence_boundary_without_claiming_hotmart_is_sandboxed(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("son ficticios e ilustrativos", readme)
        self.assertIn("evidencia verificada", readme)
        self.assertIn("H107735669O", readme)
        self.assertIn("entorno de pruebas", readme)

    def test_no_unsupported_aggregate_rating_or_review_count_is_added(self):
        self.assertNotRegex(self.html, r"(?i)\b(?:4\.9|4,9|1200\+|1\s?200\+|miles de reseñas)\b")
        self.assertNotRegex(self.html, r"(?i)(compra verificada|resultado garantizado|garantiza que)\b")

    def test_hero_social_proof_preserves_readers_and_review_sample_separately_on_mobile(self):
        mobile = re.search(r"@media\s*\(max-width:\s*760px\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}", self.css)
        self.assertIsNotNone(mobile)
        self.assertNotRegex(mobile.group(1), r"\.social-proof-(?:count|readers)\s*\{[^}]*display\s*:\s*none")
        self.assertIn('aria-label="Ver reseñas de ejemplo"', self.html)

    def test_hero_copy_and_primary_cta_match_the_approved_demo_message(self):
        hero = self.html[self.html.index('<section class="hero"'):self.html.index('</section>', self.html.index('<section class="hero"'))]
        self.assertIn("EBOOK DIGITAL · 156 PÁGINAS", hero)
        self.assertIn("Haz que tus ideas lleguen con claridad.", re.sub(r"<[^>]+>", "", hero))
        self.assertIn("Historias, ejemplos y ejercicios para ordenar lo que piensas y expresarlo en conversaciones reales.", hero)
        self.assertRegex(hero, r'id="hero-purchase-cta"[^>]*>QUIERO HABLAR CON CLARIDAD')

    def test_testimonial_cards_stack_on_mobile(self):
        mobile = re.search(
            r"@media\s*\(max-width:\s*760px\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}",
            self.css,
        )
        self.assertIsNotNone(mobile)
        self.assertRegex(mobile.group(1), r"\.testimonial-grid\s*\{[^}]*grid-template-columns\s*:\s*1fr")


if __name__ == "__main__":
    unittest.main()
