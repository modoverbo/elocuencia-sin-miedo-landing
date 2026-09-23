# Landing de venta — Elocuencia sin miedo

Sitio estático e independiente. Para verlo localmente:

```powershell
python -m http.server 4173 --directory landing
```

Abrir `http://localhost:4173`. Para publicar, subir el contenido de `landing/` a un hosting estático con HTTPS. **No publicar el PDF completo:** la carpeta incluye únicamente imágenes de las páginas 1–13, la página 14 reducida y difuminada de forma irreversible y la portada para otras secciones. La muestra termina antes del texto del capítulo 1.

Para regenerar estas imágenes desde `output/pdf/Elocuencia sin miedo.pdf`, ejecutar `tools/render_landing_preview.py` con el Python del entorno de trabajo y Poppler disponible. Verificar antes de publicar que no haya imágenes legibles de la página 14 ni páginas posteriores en `landing/assets/`.

## Checkout

Los botones usan el enlace de oferta facilitado por el productor (`H107735669O`, oferta `s5txzdcx`) y cargan el widget oficial de Hotmart. El `href` mantiene un destino directo si el widget no se carga. Probar en el dominio publicado que abre la oferta y muestra el importe correcto antes de recibir tráfico. Hotmart advierte que el widget no es compatible con ofertas que usan *upsell*; si esta oferta lo usa, conviene dejar los botones como enlaces directos al checkout.

## Decisiones editoriales

- Propuesta de valor concreta, escenarios reconocibles, recorrido del contenido, muestra real, ajuste de expectativas, oferta y preguntas frecuentes.
- Sin precio inventado, testimonios ficticios, cuentas regresivas ni promesas de resultados garantizados.
- La vista previa empieza con la portada cerrada y usa [StPageFlip 2.0.7](https://github.com/Nodlik/StPageFlip) (licencia MIT incluida en `assets/vendor/`) para mostrar dos páginas enfrentadas en PC y una en celular. Permite avanzar o retroceder con botones y gestos; un toque amplía una página legible. En la página 14 difuminada aparece la invitación a continuar en Hotmart. No avanza automáticamente y respeta movimiento reducido.
- Todas las imágenes del libro proceden del PDF final; el mockup de la portada es una composición CSS, no una fotografía de una edición impresa inexistente.

## Referencias de investigación

- [Hotmart: widget de checkout](https://help.hotmart.com/es/article/360004829631/como-configurar-o-widget-da-pagina-de-pagamento-)
- [Hotmart: integración y limitación con upsells](https://help.hotmart.com/en/article/43449924104205/como-associar-uma-pagina-do-hotmart-pages-como-pagina-de-vendas-do-meu-produto)
- [Baymard: claridad del producto](https://baymard.com/blog/ecommerce-ux-audit)
- [Baymard: incertidumbre antes del pago](https://baymard.com/blog/payment-ux)


