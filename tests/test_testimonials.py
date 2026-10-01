import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestimonialParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.current = None
        self.field = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = attributes.get("class", "").split()
        if tag == "article" and "testimonial" in classes:
            self.current = {"text": "", "name": "", "meta": "", "image": "", "alt": ""}
            self.cards.append(self.current)
        elif self.current and tag == "img":
            self.current["image"] = attributes.get("src", "")
            self.current["alt"] = attributes.get("alt", "")
        elif self.current and tag == "strong":
            self.field = "name"
        elif self.current and tag == "small":
            self.field = "meta"
        elif self.current and tag == "p":
            self.field = "text"

    def handle_endtag(self, tag):
        if tag in ("strong", "small", "p"):
            self.field = None
        if tag == "article":
            self.current = None

    def handle_data(self, data):
        if self.current and self.field:
            self.current[self.field] += data.strip()


class TestimonialSectionTests(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.script = (ROOT / "script.js").read_text(encoding="utf-8")
        self.parser = TestimonialParser()
        self.parser.feed(self.html)

    def test_reference_testimonial_heading_and_card_order_are_preserved(self):
        section_start = self.html.index('<section class="section testimonials"')
        section_end = self.html.index('<section class="section offer"', section_start)
        section = self.html[section_start:section_end]
        self.assertIn("Mira, lo que dicen quienes", section)
        self.assertIn("lo han leído.", section)
        self.assertEqual(len(self.parser.cards), 12)
        self.assertEqual(
            [card["name"] for card in self.parser.cards],
            ["Santiago R.", "Valentina M.", "Daniel G.", "Isabel C.", "Camila R.", "Lucía P.",
             "Diego A.", "Mariana T.", "Andrés C.", "Sofía V.", "Javier M.", "Pilar N."],
        )

    def test_first_four_reference_quotes_are_retained_and_extra_eight_are_present(self):
        expected_quotes = (
            "Qué libro tan brutal. La verdad no pensé que me fuera a servir tanto, pero desde que lo empecé a leer he notado un cambio real en la forma en la que me expreso. Ahora me siento mucho más seguro hablando en público y en mi trabajo. Súper recomendado.",
            "Amooo este libro! De verdad me ha ayudado un montón a perder el miedo de hablar y a organizar mejor mis ideas. Los ejercicios son muy prácticos y fáciles de aplicar. Ya no me trabo tanto cuando tengo que presentar en la universidad. Me encantó.",
            "Excelente contenido. Me gustó mucho que no se queda solo en teoría, sino que da herramientas reales para el día a día. Lo he aplicado en reuniones de trabajo y he recibido comentarios muy positivos sobre mi forma de comunicar. Vale totalmente la pena.",
            "No soy de leer muchos libros, pero este sí me atrapó. Está escrito de forma sencilla, se entiende fácil y está lleno de ejemplos útiles. Me ha servido un montón para expresarme mejor en mi vida personal también. Lo súper recomiendo!",
            "En el café me toca repetir el menú mil veces. Antes sentía que sonaba apurada; ahora respiro y hago pausas. Todavía me trabo con algunos nombres, pero ya no me da tanta pena.",
            "Yo tenía las ideas... pero en reunión me daba miedo interrumpir. Estoy ensayando una frase corta y ya. Me falta, sí, pero me sirve.",
            "Leo en el bus a ratitos. Me gustan los ejemplos porque no suenan a discurso de político jaja.",
            "Cuando presento algo en el grupo, se me va el aire. Practiqué el ejercicio de respirar y me acuerdo de aflojar los hombros. No soy experta, pero voy más tranquila.",
            "Llevo años atendiendo gente en el taller. Me quedé con lo de escuchar antes de responder; me baja un poco las revoluciones cuando alguien llega molesto.",
            "Me dio risa leer en voz alta sola en casa, pero bueno, nadie estaba mirando 😅. Repetí una frase y ya no la digo como robot.",
            "Haber si algún día logro hablar sin irme por las ramas 🙈. Por ahora estoy practicando cerrar una idea antes de saltar a la otra.",
            "En el centro cultural me invitaron a presentar el grupo y dije que sí antes de pensarlo mucho. Me llevé dos ideas apuntadas; con eso ya sentí piso.",
        )
        self.assertEqual(tuple(card["text"] for card in self.parser.cards), expected_quotes)

    def test_each_testimonial_has_a_local_fictional_portrait_and_attribution(self):
        self.assertEqual(len(self.parser.cards), 12)
        for card in self.parser.cards:
            with self.subTest(name=card["name"]):
                self.assertTrue(card["name"])
                self.assertTrue(card["meta"])
                self.assertIn("Retrato ficticio de", card["alt"])
                self.assertTrue((ROOT / card["image"]).is_file(), card["image"])

    def test_carousel_has_keyboard_region_and_previous_next_controls(self):
        self.assertIn('id="testimonial-track"', self.html)
        self.assertIn('role="region"', self.html)
        self.assertIn('tabindex="0"', self.html)
        self.assertIn('data-testimonial-previous', self.html)
        self.assertIn('data-testimonial-next', self.html)
        self.assertIn("ArrowLeft", self.script)
        self.assertIn("ArrowRight", self.script)

    def test_carousel_is_touch_scrollable_and_reduced_motion_aware_at_mobile_sizes(self):
        self.assertIn("scroll-snap-type:xmandatory", self.css.replace(" ", ""))
        self.assertIn("overscroll-behavior-inline:contain", self.css.replace(" ", ""))
        self.assertIn("grid-auto-columns:100%", self.css.replace(" ", ""))
        self.assertIn("prefers-reduced-motion:reduce", self.css.replace(" ", ""))

    def test_scrollbar_is_separated_from_the_testimonial_cards(self):
        self.assertRegex(
            self.css,
            r"\.testimonial-grid\s*\{[^}]*padding-bottom:\s*12px",
        )

    def test_demo_disclosure_identifies_the_testimonials_and_portraits_as_fictional(self):
        self.assertIn("Demo educativa: los testimonios y retratos son ficticios e ilustrativos", self.html)
        self.assertIn("no son reseñas verificadas", self.html)
        self.assertIn("son ficticios e ilustrativos", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_author_claims_remain_the_existing_brand_copy(self):
        author_start = self.html.index('<section class="section author"')
        testimonials_start = self.html.index('<section class="section testimonials"')
        author = self.html[author_start:testimonials_start]
        self.assertIn("Arturo Valdés", author)
        self.assertIn("más de 20 años", author)
        self.assertIn("+50.000", author)
        self.assertIn("Personas formadas, según la información actual de la marca", author)

    def test_review_carousel_does_not_claim_verified_purchase_or_aggregate_rating(self):
        self.assertNotRegex(self.html, r"(?i)compra verificada|resultado garantizado|garantiza que")
        self.assertNotRegex(self.html, r"(?i)4 opiniones de lectores")

    def test_checkout_destination_matches_existing_project_url(self):
        checkout_links = re.findall(r'href="(https://pay\.hotmart\.com/H107735669O\?checkoutMode=2&amp;off=s5txzdcx)"', self.html)
        self.assertGreaterEqual(len(checkout_links), 4)


if __name__ == "__main__":
    unittest.main()
