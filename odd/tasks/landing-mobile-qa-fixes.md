# Ajustes visuales móviles de la landing

## Objetivo y problema

Corregir tres defectos señalados por el propietario en la preview móvil: las tres páginas estáticas duplican la muestra interactiva, la prueba social del hero no muestra fotos reconocibles ni queda centrada, y el mockup de la oferta tapa el texto de la garantía.

## Alcance autorizado

- Trabajar directamente en `main`; no crear ramas.
- Quitar únicamente las tres miniaturas estáticas de la sección de muestra. Conservar la muestra interactiva, su enlace y sus controles.
- Centrar el grupo de CTA y prueba social del hero en móvil y reutilizar los retratos que ya existen en el carrusel. No agregar ni alterar testimonios.
- Reubicar el mockup de la oferta dentro de su tarjeta para que no invada la lista de beneficios.
- No hacer push ni despliegue remoto; no abrir el checkout.

## Modo y estrategia

- TDD estricto: activado por `AGENTS.md` del proyecto. RED → GREEN → REFACTOR por cada corrección.
- Comprobaciones: `python3 -m unittest discover -s tests -p 'test_*.py'`; `node --test tests/*.js`; QA visual local en 360–390 px y escritorio.
- Ruta: implementación delegada; la lectura de preparación abarca `index.html`, `styles.css` y varios tests (disparadores de mapeo y escritura de 2+ archivos no triviales).
- Estrategia de entrega: `ask-on-risk`; estimación inicial <400 líneas authored, sin PR solicitado.

## Tareas

- [ ] T1 — Eliminar la tira de tres páginas estáticas y ajustar su layout. Criterio: no quedan miniaturas estáticas; el flipbook y sus controles siguen presentes. Pruebas RED/GREEN de estructura y checks de preview. Evidencia de commit: pendiente.
- [ ] T2 — Centrar CTA/prueba social del hero y mostrar los cuatro retratos ilustrativos existentes. Criterio: en móvil el grupo queda centrado y cada avatar tiene foto visible; se conserva la divulgación de ejemplos ilustrativos. Pruebas RED/GREEN de rutas/estilos y QA visual. Evidencia de commit: pendiente.
- [ ] T3 — Bajar el mockup de la oferta. Criterio: a 360–390 px y en tablet no cubre el texto «7 días de garantía» y permanece dentro de la tarjeta de precio. Pruebas RED/GREEN de estilos y QA visual. Evidencia de commit: pendiente.

## Progreso y siguiente paso

- Mapeo de solo lectura completado; `main` limpio en `0fff1c8` al comenzar.
- Siguiente paso: T1. Registrar el resultado real de cada comando, la QA visual y el commit antes de marcar una tarea.
