# Ajustes de CTA, carrusel y tipografía de la landing

## Objetivo y problema

Atender los tres comentarios del propietario sobre la preview móvil: el CTA de la muestra no está centrado y tiene un enlace redundante; los controles del carrusel están a la derecha y no permiten detener una reproducción automática; la barra de desplazamiento queda demasiado cerca de la tarjeta. Comparar todas las familias tipográficas y sus combinaciones con el HTML de referencia antes de cambiar fuentes.

## Alcance autorizado

- Trabajar directamente en `main`, sin crear ramas.
- Centrar «QUIERO EL LIBRO» y retirar solamente el enlace «EXPLORA LA MUESTRA INTERACTIVA». Conservar el flipbook y sus controles.
- Centrar los controles del carrusel, añadir reproducción automática por defecto y un control central de pausa/reanudación. Respetar la preferencia de movimiento reducido.
- Separar visualmente la tarjeta del testimonio de la barra horizontal inferior.
- Cambiar tipografía únicamente si la comparación con `/home/julian/Descargas/elocuencia-sin-miedo-nueva-landing (2).html` demuestra una diferencia real.
- No hacer push, despliegue remoto ni abrir el checkout.

## Modo y estrategia

- TDD estricto: activado por `AGENTS.md`. Observar RED → GREEN → REFACTOR antes de cerrar cada cambio de comportamiento.
- Runner: `python3 -m unittest discover -s tests -p 'test_*.py'` y `node --test tests/*.js`.
- QA: preview local móvil de 360–390 px y escritorio; comprobar reproducción, pausa, reanudación y movimiento reducido.
- Ruta: implementación delegada. El mapeo requirió referencia, HTML, CSS, JS y pruebas; la escritura abarca varios archivos no triviales.
- Estrategia de entrega: `ask-on-risk`. Pronóstico inicial ~150–250 líneas authored (adiciones + eliminaciones, excluidos generados), inferior al umbral orientativo de ~400; sin PR solicitado.

## Tareas

- [x] T1 — Simplificar el CTA de la muestra y dar aire a la barra del carrusel. El enlace redundante se retiró sin alterar el flipbook; el CTA queda centrado mediante su wrapper móvil y el scrollbar tiene 12 px adicionales de separación. RED: dos pruebas nuevas fallaron antes del cambio de fuente. GREEN: Python 45/45, Node 8/8, `git diff --check` limpio. Comprobación independiente Python 45/45; preview a 384 px confirma centro de CTA 184,49 px frente a centro de contenido 184,5 px, enlace redundante ausente, flipbook presente y `padding-bottom: 12px`. Ruta delegada por preparación multiarchivo y cambios en HTML/CSS/tests. Commit: pendiente.
- [ ] T2 — Añadir reproducción automática controlable al carrusel. Criterios: controles anterior/pausa-siguiente centrados, avance automático por defecto, pausa y reanudación accesibles, comportamiento correcto con movimiento reducido y navegación manual. Confirmar RED/GREEN, suites completas y QA local. Ruta delegada por cambios no triviales en HTML/CSS/JS/tests.
- [ ] T3 — Cerrar la auditoría tipográfica de referencia. Criterio: comparar familias, pesos y papeles tipográficos de todas las secciones; corregir únicamente diferencias demostradas y verificar que no se alteren las combinaciones existentes por suposición. Ruta delegada como parte de la implementación y comprobación.

## Progreso y siguiente paso

- `main` limpio en `743501a` al comenzar. No hay autorización de push ni despliegue.
- Mapeo de solo lectura completado: referencia y landing usan DM Sans para sans/cuerpo y Playfair Display para serif editorial; no se detectó todavía un desajuste de familias. La barra señalada es el scrollbar horizontal del carrusel, no un elemento independiente.
- T1 implementada y verificada localmente; pendiente registrar su commit. Siguiente paso: T2 con pruebas RED antes de incorporar autoplay y su control de pausa/reanudación.
