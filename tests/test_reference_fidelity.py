import hashlib
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReferenceMarkupParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = []
        self.current_section = None
        self.section_depth = 0
        self.all_text = []
        self.testimonial_cards = 0
        self.teaser_pages = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = attributes.get("class", "").split()
        if tag == "section":
            self.sections.append({"classes": classes, "text": []})
            self.current_section = self.sections[-1]
            self.section_depth = 1
        elif self.current_section and tag == "section":
            self.section_depth += 1
        if "testimonial" in classes:
            self.testimonial_cards += 1
        if "preview-teaser-page" in classes:
            self.teaser_pages += 1

    def handle_endtag(self, tag):
        if tag == "section" and self.current_section:
            self.section_depth -= 1
            if self.section_depth == 0:
                self.current_section = None

    def handle_data(self, data):
        if data.strip():
            normalized = " ".join(data.split())
            self.all_text.append(normalized)
            if self.current_section:
                self.current_section["text"].append(normalized)


class ReferenceFidelityTests(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.script = (ROOT / "script.js").read_text(encoding="utf-8")
        self.parser = ReferenceMarkupParser()
        self.parser.feed(self.html)

    def test_sales_sections_follow_the_literal_reference_order(self):
        self.assertEqual(
            [section["classes"] for section in self.parser.sections],
            [
                ["section", "problem"],
                ["statement"],
                ["section", "mechanism"],
                ["section", "preview"],
                ["section"],
                ["section", "transformation"],
                ["section", "author"],
                ["section", "testimonials"],
                ["section", "offer"],
                ["section", "faq"],
                ["final"],
            ],
        )

    def test_reference_headlines_and_copy_are_preserved(self):
        page_text = " ".join(self.parser.all_text)
        normalized_page_text = page_text.casefold()
        for phrase in (
            "Lo que piensas merece sonar tan claro como lo tienes en la cabeza.",
            "Sabes lo que quieres decir. Decirlo es otra historia.",
            "No necesitas otra personalidad. Necesitas aprender a expresar mejor la que ya tienes.",
            "De la idea a la conversación.",
            "Elocuencia sin miedo.",
            "Un libro para usar.",
            "Dejar de pensar “no sé cómo decirlo” y empezar a saber por dónde empezar.",
            "Mira, lo que dicen quienes lo han leído.",
            "Empieza a hablar con más claridad.",
            "Antes de comprar, resuelve tus dudas.",
            "Tu siguiente conversación puede empezar aquí",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.casefold(), normalized_page_text)

    def test_reference_body_copy_remains_intact_outside_the_approved_exceptions(self):
        page_text = " ".join(self.parser.all_text).casefold()
        for phrase in (
            "Ensayas la frase en tu cabeza y, cuando llega tu turno, la conversación ya cambió.",
            "La elocuencia no consiste en usar palabras difíciles. Consiste en conseguir que una buena idea llegue con claridad a otra persona.",
            "Llévalo a reuniones, propuestas, límites, entrevistas y conversaciones reales.",
            "Dentro encontrarás ideas, ejemplos y ejercicios para que hablar mejor deje de sentirse como algo que tienes que improvisar y empiece a convertirse en una habilidad que puedes entrenar.",
            "No está pensado para que subrayes frases bonitas y lo olvides. Está pensado para volver a él cuando tengas una conversación concreta que quieras mejorar.",
            "La diferencia no es convertirte en otra persona. Es aprender a encontrar, ordenar y expresar la idea.",
            "El enfoque de este libro es práctico: observar una situación real, ensayar un cambio y descubrir qué ayuda a que tu mensaje llegue.",
            "Una herramienta práctica para volver a tus conversaciones reales y trabajar la forma en que expresas lo que piensas.",
            "US$28",
            "50% DE DESCUENTO",
            "US$14",
            "pago único",
            "Precio final del producto. Pueden aplicar impuestos según país.",
            "+50.000",
            "Personas formadas, según la información actual de la marca",
            "¿Necesito experiencia hablando en público? No. El recorrido parte de conversaciones cotidianas y avanza hacia situaciones como reuniones, entrevistas, propuestas, límites y respuestas difíciles.",
            "Empieza con una conversación real. Lee, practica y descubre una forma más clara de expresar lo que piensas.",
        ):
            with self.subTest(phrase=phrase):
                self.assertTrue(phrase.casefold() in page_text, phrase)
        offer_markup = (
            '<div class="old">US$28</div><span class="discount">50% DE DESCUENTO</span>'
            '<div class="price">US$14 <small>pago único</small></div>'
        )
        self.assertTrue(offer_markup in self.html, "reference offer markup must remain intact")

    def test_reference_design_tokens_and_key_layout_rules_are_present(self):
        expected_tokens = (
            "--ink:#111310;--muted:#656861;--paper:#f5f2ea;--paper2:#ebe6da;"
            "--green:#062f29;--green2:#0b4038;--gold:#d4aa3a;"
            "--line:rgba(17,19,16,.13);--white:#fffdf7;--shadow:0 25px 70px rgba(0,0,0,.16)"
        )
        self.assertIn(expected_tokens.replace(" ", ""), self.css.replace(" ", ""))
        for declaration in (
            "font-family:'DM Sans',sans-serif",
            "width:min(1160px,calc(100% - 40px))",
            "grid-template-columns:1.03fr .97fr",
            "background:radial-gradient(circle at 75% 40%,#15574c 0,#07352f 36%,#032620 75%)",
            "grid-template-columns:.85fr 1.15fr",
            "@media(max-width:1100px)",
            "@media(max-width:900px)",
            "@media(max-width:560px)",
        ):
            with self.subTest(declaration=declaration):
                self.assertIn(declaration.replace(" ", ""), self.css.replace(" ", ""))

    def test_complete_reference_stylesheet_remains_the_exact_css_prefix(self):
        reference_styles = self.css.split("\n/* Approved product exceptions:", 1)[0].strip()
        self.assertEqual(len(reference_styles), 12517)
        self.assertEqual(
            hashlib.sha256(reference_styles.encode("utf-8")).hexdigest(),
            "df24164d459a806f253ad633c82d4c324327ce7a96b829d215b3c11d3c390004",
        )

    def test_only_approved_product_exceptions_are_added_to_reference_surfaces(self):
        self.assertEqual(self.parser.testimonial_cards, 12)
        self.assertEqual(self.parser.teaser_pages, 3)
        self.assertIn('id="interactive-preview"', self.html)
        self.assertIn('id="preview-next"', self.html)
        self.assertIn('id="preview-previous"', self.html)
        self.assertIn('id="preview-replay"', self.html)
        self.assertIn('data-testimonial-next', self.html)
        self.assertIn('data-testimonial-previous', self.html)
        self.assertIn("ArrowRight", self.script)
        self.assertIn("prefers-reduced-motion", self.css)

    def test_reduced_motion_disables_the_reference_book_float_animation(self):
        reduced_motion = self.css.split("@media (prefers-reduced-motion: reduce)", 1)[1].split("\n}", 1)[0]
        self.assertIn(".book { animation: none !important; }", reduced_motion)

    def test_hotmart_destination_and_illustrative_testimonial_disclosure_are_preserved(self):
        expected_checkout = "https://pay.hotmart.com/H107735669O?checkoutMode=2&off=s5txzdcx"
        self.assertIn(expected_checkout.replace("&", "&amp;"), self.html)
        self.assertIn("Demo educativa", self.html)
        self.assertIn("los testimonios y retratos son ficticios e ilustrativos", self.html)

    def test_local_image_references_resolve(self):
        for src in re.findall(r"(?:src|href)=\"(assets/[^\"]+)\"", self.html):
            with self.subTest(src=src):
                self.assertTrue((ROOT / src.split("?", 1)[0]).is_file(), src)


if __name__ == "__main__":
    unittest.main()
