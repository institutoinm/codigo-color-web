# Auditorías previas a la entrega

Se hicieron tres auditorías independientes. Cada fallo encontrado se corrigió y se volvió a comprobar.

## Auditoría 1 · Técnica (Blender, GLB y web)

| Comprobación | Herramienta | Resultado |
|---|---|---|
| Validez de los 9 GLB (3 fuente, 3 web, 3 móvil) | `gltf-validator` (Khronos) | ✔ 0 errores. Avisos: tangentes generadas (three.js las calcula) y extensión meshopt no validable |
| Animaciones y morph targets en los GLB | `gltf-validator` | ✔ escalonadas a 12 poses/s; shape keys en las escenas 02 y 03 |
| Peso web | `gltf-transform` | ✔ 0,56–0,87 MB escritorio y 0,39–0,67 MB móvil (−80 % frente al original) |
| Carga y scroll en escritorio (1366×800) y móvil (390×844) | Playwright + Chromium | ✔ sin errores de JavaScript ni scroll horizontal |
| Piezas tocables y resaltado por paso | Prueba funcional en `tools/test/smoke.mjs` | ✔ ADN: 24 piezas tocables, se resaltan las 6 del subtono. Piel: 4 gotas. Rueda: 3 gotas |
| Reproducibilidad | Semillas deterministas (`stable_seed`) | ✔ el render, el .blend y el GLB salen idénticos en cada ejecución |

**Fallos encontrados y corregidos**
1. El material 4D (Voronoi Smooth F1) hacía el render 20 veces más lento → texturas 3D.
2. Las UV del pedestal y de las cuñas eran degeneradas, lo que daba texturas planas o verdes → UV cilíndricas o planas calculadas por código.
3. El exportador añadía `KHR_materials_sheen`, un velo blanco en three.js → eliminado en la exportación web.
4. La shape key creada en último lugar quedaba con valor 1 por defecto (gota alargada) → se inicializa a 0.
5. `hash()` de Python cambiaba la geometría en cada ejecución → semilla CRC32.

## Auditoría 2 · SEO técnico y accesibilidad

| Comprobación | Cristina Barriga | INM |
|---|---|---|
| Título ≤ 65 caracteres | ✔ 59 | ✔ 64 |
| Descripción de 120 a 160 caracteres | ✔ 151 | ✔ 133 |
| Un solo H1, `lang="es"`, canonical | ✔ | ✔ |
| JSON-LD válido | ✔ Person, ProfessionalService, WebPage, DefinedTermSet, VideoObject, 3DModel, FAQPage | ✔ EducationalOrganization, WebPage, LearningResource, 2 × VideoObject, FAQPage |
| FAQ visible idéntica a FAQPage | ✔ | ✔ |
| axe-core (WCAG 2.1 AA + buenas prácticas) | ✔ sin violaciones | ✔ sin violaciones |

**Fallos encontrados y corregidos:** títulos y descripciones demasiado largos, y contraste insuficiente en las tarjetas
inactivas (tenían opacidad 0,35; ahora el paso activo se marca con borde y desplazamiento).

## Auditoría 3 · Revisión independiente de código, accesibilidad y contenido

La hizo un agente revisor sin acceso a mis conclusiones, sólo al código. Hallazgos y correcciones:

| Gravedad | Hallazgo | Corrección |
|---|---|---|
| Alta | Los `extras` de Blender están en el nodo padre, así que los toques y el resaltado del ADN no funcionaban | Búsqueda de metadatos y nombres en los antecesores. Verificado con la prueba funcional |
| Alta | El botón del primer paso no activaba su paso | Posición exacta del paso: `stepScroll(i)` |
| Media | El 3D cambiaba de paso antes que el texto | Mapeo con n−1 tramos, centrado en cada tarjeta |
| Media | Se perdía el resaltado si el GLB cargaba a mitad del capítulo | `updateStep(true)` tras la carga |
| Media | El respaldo por capítulo no activaba el vídeo ni liberaba WebGL | `startVideos()` y `renderer.dispose()` |
| Media | «Ver completa» no se podía interrumpir | `autoKill: true` |
| Media | Las tarjetas tapaban los botones y el panel en móvil | Capa `.clay-overlay` propia por encima de las tarjetas y más margen inferior |
| Baja | Pitch excluido de «moving»; `Vector3` nuevos en cada fotograma; documentación imprecisa | Corregido |
| A11y | `aria-live` con `hidden`; canvas con `role="img"` siendo interactivo | El panel siempre está presente y sólo cambia el texto; `aria-roledescription` |
| SEO | El INM no tenía transcripción ni `og:video` | Añadidos, en el HTML y en el JSON-LD |
| Contenido | Afirmaciones sanitarias demasiado categóricas, «modelados a mano», subtono sin neutro, nombre interno en inglés, CTA incoherente, gramática | Reescrito: semipermanencia y retoques, efecto Tyndall, «puede atenuarse», subtono neutro u oliva, CTA a contacto |

## Verificación final con los vídeos renderizados

- 6 vídeos (3 escenas × 16:9 y 9:16, MP4 H.264 + WebM VP9, 0,09–0,50 MB) y 12 pósteres WebP/JPG generados con Blender (Cycles).
- Prueba completa en escritorio y móvil: sin errores ni recursos 404.
- Prueba con `prefers-reduced-motion: reduce`: se muestra el vídeo con controles y sin reproducción automática. Al revisarla se
  vio que en móvil aparecía el póster horizontal dentro del vídeo vertical; corregido (el póster vertical se elige por código).
- Los .blend llevan las texturas horneadas empaquetadas: se abren sin archivos externos.

## Limitaciones conocidas (aceptadas)

- `prefers-reduced-motion` se evalúa al cargar la página, no si se cambia durante la visita.
- La información de cada pieza también está en el texto visible, pero no hay un recorrido por teclado pieza a pieza.
- Google ya no muestra FAQ enriquecidas para la mayoría de webs; el marcado se mantiene por su valor para AEO y GEO.
- Los textos del INM deben validarlos sus formadores antes de publicarse.
