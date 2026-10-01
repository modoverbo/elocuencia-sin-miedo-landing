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

- [x] T1 — Eliminar la tira de tres páginas estáticas y ajustar su layout. Criterio: no quedan miniaturas estáticas; el flipbook y sus controles siguen presentes. RED: `python3 -m unittest discover -s tests -p 'test_*.py'` falló como se esperaba (41 pruebas, 3 fallos por las miniaturas presentes). GREEN: 41/41; `node --test tests/*.js`: 8/8; `git diff --check`: limpio. QA local: a 390 px y 1280 px no aparecen miniaturas; el enlace, el flipbook y sus controles permanecen visibles, y el bloque introductorio ocupa una columna sin hueco lateral. Commit: `d6cd7de` (`fix(landing): remove duplicate static preview pages`). Rollback: revertir solo el markup de muestra, su override de layout y las pruebas de T1.
- [x] T2 — Centrar CTA/prueba social del hero y mostrar los cuatro retratos ilustrativos existentes. Criterio: en móvil el grupo queda centrado y cada avatar tiene foto visible; se conserva la divulgación de ejemplos ilustrativos. RED: `python3 -m unittest discover -s tests -p 'test_author_section.py'` tuvo 2 fallos esperados (17 pruebas: rutas SVG y grupo ausente). GREEN: 17/17; suite completa Python: 43/43; Node: 8/8; `git diff --check`: limpio. QA local: capturas a 360 y 390 px muestran botón, nota y cuatro retratos centrados; a 1280 px se conserva la alineación de escritorio. Las rutas coinciden, en orden, con los cuatro primeros retratos del carrusel. Commit: `19741c4` (`fix(landing): center mobile hero proof with portraits`). Rollback: revertir solo el grupo de conversión, las rutas de sus retratos, su estilo móvil y las pruebas de T2.
- [x] T3 — Mantener el mockup de la oferta dentro de la tarjeta de precio. Criterio: a 360–390 px y en tablet no cubre el texto «7 días de garantía», el precio ni el CTA. Se sustituyó el posicionamiento absoluto con desplazamiento negativo por flujo normal dentro de la tarjeta: así la separación se conserva en todos los breakpoints. RED: suite Python de 44 pruebas con 2 fallos esperados (mockup fuera del flujo y versión CSS anterior). GREEN focalizado: 2/2; suite completa Python: 44/44; Node: 8/8; `git diff --check`: limpio. QA local: geometría a 360, 390, 560, 900 y 1280 px confirma imagen cargada, contenida por la tarjeta y sin intersección con beneficio, insignia, precio ni CTA; capturas visuales revisadas a 390 y 1280 px. Se actualizó la versión de caché CSS a `20261001-mobile-fixes`. Commit: `93d2d98` (`fix(landing): keep offer mockup inside price card`). Rollback: revertir solo el override del mockup, la versión de CSS y las pruebas de T3.

## Progreso y siguiente paso

- Mapeo de solo lectura completado; `main` limpio en `0fff1c8` al comenzar.
- T1 completada en `d6cd7de`; 62 líneas authored (45 adiciones, 17 eliminaciones) en el primer work unit, incluido este documento inicial.
- T2 completada en `19741c4`; 36 líneas authored (33 adiciones, 3 eliminaciones) en el segundo work unit.
- T3 completada en `93d2d98`; 16 líneas authored (14 adiciones, 2 eliminaciones) en el tercer work unit. Total de los tres work units de implementación: 114 líneas authored, sin contar las actualizaciones posteriores de este documento.
- Todas las tareas están completas y verificadas localmente. Siguiente paso: revisión de la entrega; no se hizo push ni despliegue remoto.
