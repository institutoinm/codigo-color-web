# Estrategia de contenido · SEO, GEO, AEO, CRO, SXO y AIO

Se aplica a las dos páginas creadas:

| Página | URL propuesta | Intención de búsqueda principal |
|---|---|---|
| `web/cristinabarriga/adn-del-color.html` | cristinabarriga.com/adn-del-color/ | Informativa → transaccional: «análisis de color personal», «subtono cálido o frío» |
| `web/inm/micropigmentacion-ciencia.html` | institutonacionaldemicropigmentacion.es/ciencia-del-pigmento/ | Informativa profesional → formación: «profundidad pigmento micropigmentación», «neutralizar cejas grises» |

> Las URL definitivas y los enlaces de CTA (`/contacto/`, `/servicios/`, `/formacion/`) son provisionales: deben ajustarse a
> la arquitectura real de cada web según el documento maestro.

## SEO (buscadores clásicos)

| Elemento | Aplicado |
|---|---|
| `<title>` | Palabra clave al principio, marca al final, menos de 65 caracteres |
| Meta description | 150–160 caracteres con beneficio y entidad |
| Un único `<h1>` y jerarquía H2/H3 | Sí; los pasos de la animación son H3 indexables en el HTML |
| Canonical, robots con `max-image-preview:large` y `max-video-preview:-1` | Sí |
| Open Graph y Twitter Card con póster 1280×720 | Sí |
| Texto alternativo descriptivo en pósteres; `aria-label` en lienzo y vídeo | Sí |
| Rendimiento (LCP = póster precargado con `fetchpriority`, 3D diferido) | Sí |
| Vídeo indexable: `VideoObject` con miniatura, duración, `contentUrl` y transcripción | Sí |

**Palabras clave semilla**
- Código Color: análisis de color personal, colorimetría personal, subtono cálido o frío, contraste personal, paleta de colores personal, asesora de imagen.
- INM: profundidad del pigmento en micropigmentación, capas de la piel micropigmentación, migración del pigmento, cejas grises o azuladas, neutralizar color micropigmentación, colorimetría micropigmentación, curso de micropigmentación.

## GEO (motores generativos: ChatGPT, Gemini, Perplexity, AI Overviews)

- **Entidades explícitas** en JSON-LD (`Person`, `ProfessionalService`, `EducationalOrganization`) y conectadas con `@id`.
- **Definiciones atómicas** (`DefinedTermSet` con las 4 dimensiones del color): frases autocontenidas fáciles de citar.
- **Datos concretos** en el texto (cuatro dimensiones, tres capas, par complementario azul–naranja).
- **Fecha de publicación y actualización** visibles para los rastreadores (`datePublished`, `dateModified`).
- Archivos `llms.txt` por web (en esta carpeta) con el resumen y las URL canónicas.

## AEO (motores de respuesta y búsqueda por voz)

- Bloque **«Respuesta rápida»** de 40–60 palabras justo después del H1 (marcado como `speakable`).
- **FAQ** con preguntas reales de búsqueda y respuestas de 2–3 frases, duplicadas en `FAQPage`.
- Preguntas formuladas como las haría una persona: «¿Cómo sé si mi subtono es cálido o frío?».

## CRO (conversión)

| Táctica | Dónde |
|---|---|
| CTA principal persistente en la cabecera | «Reserva tu análisis» / «Ver formación» |
| CTA contextual al final de cada animación (momento de máxima comprensión) | Último paso de cada capítulo |
| Banda de CTA final con opción principal y secundaria (menos compromiso) | «Reserva» + «Ver servicios»; «Solicita información» + «Habla con el Instituto» |
| Medición | Eventos `clay_scene_ready`, `clay_step_view`, `clay_step_button`, `clay_hotspot`, `clay_drag`, `clay_play`, `clay_cta_click` en `dataLayer` |

**Pruebas A/B sugeridas:** texto del CTA final («Reserva tu análisis de color» vs. «Descubre tu código»); animación arriba vs. debajo del bloque de respuesta; con y sin botón «Ver completa».

**KPI:** % de usuarios que llegan al último paso, clics en CTA por sesión con animación vs. sin ella, tiempo hasta el primer CTA.

## SXO (experiencia de búsqueda)

- La página responde a la intención en los primeros 100 px (H1 + respuesta rápida) antes de pedir interacción.
- El 3D es opcional: el contenido se entiende entero sin él (póster, textos, transcripción).
- Móvil primero: GLB ligero, vídeo vertical 9:16, botones de 44 px y en una fila desplazable.
- Respeta `prefers-reduced-motion` y Save-Data.
- Sin dependencias de terceros en tiempo de ejecución (sin CDN ni cookies externas).

## AIO (optimización para IA y asistentes)

- Contenido en HTML semántico, sin texto dentro de imágenes ni del canvas.
- Transcripciones textuales de cada animación (`<details>` y `VideoObject.transcript`).
- Datos de las piezas 3D (`extras` de glTF) con significado, no sólo geometría.
- Tono prudente y verificable en contenido sanitario (micropigmentación): sin cifras de profundidad no validadas, con aviso
  «Contenido divulgativo. No sustituye la valoración de un profesional cualificado».

## Pendiente de validar con el cliente

1. Dominio y rutas definitivas, enlaces de CTA y datos de contacto.
2. Tipografías y colores de marca del documento maestro (tokens `--clay-*`).
3. Revisión técnica de los textos de la escena 02 por los formadores del INM.
4. Integración con la analítica real (GA4 u otra) y el gestor de consentimiento.
