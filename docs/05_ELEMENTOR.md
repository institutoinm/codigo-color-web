# 05 — DISEÑO EN ELEMENTOR
## Código Color · Instrucciones de construcción de la landing: sistema de diseño, contenedores, widgets, responsive, plantillas y frontera con el código

> **Estado:** Entregado, pendiente de aprobación del cliente.
> **Regla:** Esta fase explica **cómo montar en Elementor** el copy de la Fase 4 sobre el wireframe de la Fase 3, sin reescribir contenido. El código real (GSAP, Orbe Three.js, schema PHP) es Fase 6; aquí solo se prepara su contenedor y su frontera.
> **Depende de:** FASE 0 (arquitectura D, child theme, cachés), FASE 1 (paleta, tipografía, 31 módulos, movimiento), FASE 3 (wireframe), FASE 4 (copy, precios, schema) y documento 08 (especificación de imágenes).
> **Rol asumido:** Arquitecto WordPress/Elementor senior + Diseñador de sistema.
> **Constructor:** Elementor Pro 3.20+ sobre Hello Elementor + child theme `codigo-color-child`. Contenedores **Flexbox** (no secciones/columnas legacy).

---

## ÍNDICE

- **A.** Principios de construcción y frontera Elementor / código
- **B.** Sistema de diseño: Global Colors
- **C.** Sistema de diseño: Global Fonts y presets tipográficos
- **D.** Ajustes globales del sitio (layout, breakpoints, botones, espaciado)
- **E.** Configuración base de contenedor
- **F.** Construcción módulo por módulo (1-31 + S)
- **G.** El Orbe Cromático en Elementor (contenedor + data-attributes)
- **H.** Módulo de Servicios y precios (sección guardable)
- **I.** Bloque de autoridad — Cristina Barriga
- **J.** Sistema de 100 FAQs en Elementor
- **K.** Animaciones: Motion Effects nativo vs GSAP (Fase 6)
- **L.** Responsive y mobile-first
- **M.** Qué NO va en Elementor (código y schema, Fase 6)
- **N.** Plantillas guardables, exportación e importación
- **O.** Qué queda editable y qué no tocar
- **P.** Checklist y entregables para Fase 6

---

## A. PRINCIPIOS DE CONSTRUCCIÓN Y FRONTERA ELEMENTOR / CÓDIGO

### A.1 La frontera (heredada de Fase 0)

| Vive en Elementor (editable sin código) | Vive en código versionado (GitHub → SiteGround) |
|-----------------------------------------|--------------------------------------------------|
| Textos, titulares, CTAs, precios, FAQs, imágenes, vídeos, formularios | Sistema visual `cc-*.css`, JS modular (`cc-*.js`), Orbe Three.js, schema JSON-LD (PHP) |
| Estructura de contenedores y su disposición | Tokens de diseño base, fuentes locales, encolado condicional |
| Clases CSS aplicadas (campo "Clases CSS" de cada contenedor) | Definición de lo que esas clases hacen |

**Regla de oro:** Elementor **aplica** clases `cc-*`; nunca **define** el sistema visual. Un cambio de texto jamás toca GitHub; un cambio de animación jamás toca Elementor.

### A.2 Convención de clases

Cada módulo lleva su clase raíz `cc-<modulo>` en el contenedor de sección (p. ej. `cc-hero`, `cc-manifesto`, `cc-service`, `cc-faq`). Los elementos internos usan BEM ligero: `cc-faq__category`, `cc-faq__item`, `cc-pricing__card`. Estas clases son el **contrato** con el CSS/JS de Fase 6.

### A.3 Orden de trabajo recomendado

1. Cargar Global Colors y Global Fonts (B, C) — **antes** de construir nada.
2. Configurar Site Settings (D).
3. Construir módulo a módulo (F) con sus clases.
4. Guardar cada módulo como plantilla (N).
5. Dejar los contenedores `cc-color-orb` y de schema preparados para Fase 6 (G, M).

---

## B. SISTEMA DE DISEÑO: GLOBAL COLORS

> Elementor → Site Settings → Global Colors. Se mapea la paleta de Fase 1. Los nombres son los de la marca; los slots "System" de Elementor se reutilizan para no duplicar.

| Slot Elementor | Nombre marca | HEX | Uso |
|----------------|--------------|-----|-----|
| Primary | Negro Tinta | `#1A1A1A` | Texto principal, secciones de contraste |
| Secondary | Oro Suave | `#C4A882` | Acento primario: CTAs, filos, detalles |
| Text | Carbón | `#2D2D2D` | Texto secundario, captions |
| Accent | Oro Profundo | `#8B6F47` | Hovers, texto sobre claros, autoridad |
| Custom 1 | Blanco Editorial | `#FFFFFF` | Lienzo base |
| Custom 2 | Crudo Atelier | `#FAF8F5` | Fondo principal alterno |
| Custom 3 | Gris Cálido | `#F2F0ED` | Fondos de bloque/capítulo |
| Custom 4 | Oro Claro | `#E8D5B7` | Halos, fondos de acento suaves |
| Custom 5 | Primavera | `#D4A853` | Color estacional (solo narrativa) |
| Custom 6 | Verano | `#8BA7C4` | Color estacional |
| Custom 7 | Otoño | `#C4622D` | Color estacional |
| Custom 8 | Invierno | `#2D3E5C` | Color estacional |

**Regla cromática (Fase 1):** el 90% de la página vive en neutros + oro (slots Primary/Secondary/Text/Accent + Custom 1-4). Los estacionales (Custom 5-8) **solo** aparecen en módulos 9-13 y donde la narrativa hable de estaciones.

---

## C. SISTEMA DE DISEÑO: GLOBAL FONTS Y PRESETS TIPOGRÁFICOS

> Site Settings → Global Fonts. Fuentes **servidas localmente** desde el child theme (Fase 0), no desde Google CDN, para rendimiento y privacidad. En Elementor se referencian como Custom Fonts ya registradas por el child theme.

| Slot Elementor | Fuente | Uso |
|----------------|--------|-----|
| Primary | **Cormorant Garamond** (400, 500, ital 400) | Titulares display, H1-H3 |
| Secondary | **DM Sans** (400, 500) | Cuerpo de texto, leads |
| Text | DM Sans | Párrafos, captions |
| Accent | Cormorant Garamond *Italic* | Citas, frases-manifiesto |

### C.1 Presets tipográficos (escala fluida de Fase 1)

| Preset (clase / uso) | Fuente | Tamaño | Interlineado | Tracking |
|----------------------|--------|--------|--------------|----------|
| Hero | Cormorant | `clamp(3rem, 8vw, 7rem)` | 1.05 | -0.02em |
| H1 | Cormorant | 56px (mobile 40) | 1.1 | -0.01em |
| H2 | Cormorant | 44px (mobile 32) | 1.15 | -0.01em |
| H3 | Cormorant | 32px (mobile 26) | 1.2 | normal |
| H4 / label-grande | Cormorant | 24px | 1.3 | normal |
| Lead | DM Sans | 18px | 1.6 | normal |
| Body | DM Sans | 16px | 1.6 | normal |
| Caption | DM Sans | 12px | 1.4 | +0.02em |
| Label / botón | DM Sans 500 | 12-14px, UPPERCASE | 1.2 | +0.08em |

- **Medida de texto:** máx. 68 caracteres por línea (limitar ancho del contenedor de texto a ~680px, ver E).
- Aplicar presets vía Global Typography; nunca tamaños sueltos por widget salvo excepción justificada.

---

## D. AJUSTES GLOBALES DEL SITIO

> Site Settings → Layout / Buttons / Background.

| Ajuste | Valor |
|--------|-------|
| Content width (boxed) | 1280px |
| Ancho de texto recomendado | 680px (contenedor interno) |
| Espaciado entre widgets | 0 (se controla con gap de contenedor) |
| Breakpoints | Mobile ≤767 · Tablet ≤1024 · Desktop ≥1200 · (opcional Mobile Extra ≤360) |
| Padding de sección | fluido `clamp(80px, 12vh, 200px)` vertical · `clamp(20px, 6vw, 120px)` lateral |
| Botón primario | Fondo Oro Suave `#C4A882`, texto Negro Tinta, label uppercase +0.08em, padding 18/36, radio 0-2px, hover → Oro Profundo `#8B6F47` |
| Botón secundario | Fantasma: borde 1px Negro Tinta, fondo transparente, hover relleno sutil |
| Botón terciario | Texto con subrayado animado (sin caja) |
| Animación global de botón | transición 200ms ease (CSS nativo, nivel 1) |

---

## E. CONFIGURACIÓN BASE DE CONTENEDOR

> Todos los módulos son **contenedores Flexbox**. Patrón estándar:

- **Contenedor de sección (raíz):** `width: Full Width`, `content width: Boxed 1280`, dirección `column`, `align-items: center`, padding de sección (D), clase `cc-<modulo>`.
- **Contenedor de contenido:** ancho máx. 680px para texto puro; 1280px para spreads imagen+texto. `gap` 24px desktop / 16px mobile.
- **Spreads editoriales (zigzag):** contenedor hijo en `row` (desktop) que pasa a `column` en mobile; se alterna el orden (`order`) por módulo para el efecto zigzag de la Fase 3.
- **Espacio negativo:** los módulos del Acto I-II llevan padding vertical en el extremo alto del clamp (respiración de Fase 1).

---

## F. CONSTRUCCIÓN MÓDULO POR MÓDULO

> Por cada módulo: **clase raíz · fondo · estructura/widgets · movimiento (nivel) · nota**. Texto exacto = Fase 4. Imágenes con especificación del doc 08 (AVIF/WebP, `srcset`, lazy salvo LCP). Movimiento: lo marcado **[E]** se hace con Elementor Motion Effects; **[GSAP]/[3D]** se prepara aquí y se implementa en Fase 6.

### Acto I — Llegada

| Mód | Clase raíz | Fondo | Estructura / widgets | Movimiento |
|-----|-----------|-------|----------------------|------------|
| 1 Hero | `cc-hero` | Crudo Atelier `#FAF8F5` + contenedor `cc-color-orb` (G) | Heading (H1 Hero preset) · Text (lead) · Button×2 · Microcopy · contenedor vacío del Orbe detrás (z-index 0) | [3D] Orbe + [GSAP] revelado H1 · LCP = H1 (no lazy) |
| 2 Manifiesto | `cc-manifesto` | Crudo Atelier | Heading (Accent, Cormorant ital, gran tamaño), centrado, máx 680 | [GSAP] revelado palabra a palabra |

### Acto II — Tensión

| Mód | Clase raíz | Fondo | Estructura / widgets | Movimiento |
|-----|-----------|-------|----------------------|------------|
| 3 Problema | `cc-editorial` | Blanco | Contenedor `row` (texto izq / Image der), zigzag | [E] entrance fade-up + [GSAP] parallax imagen |
| 4 Solución | `cc-editorial` | Blanco | Contenedor `row` invertido (Image izq / texto der) | [GSAP] desaturado→color (scrub) o [E] fade |
| 5 Qué es | `cc-definition` | Gris Cálido `#F2F0ED` | Heading H2 · Text (lead, definición citable) · Button secundario · Image discreta | [E] fade-in suave |

### Acto III — Comprensión

| Mód | Clase raíz | Fondo | Estructura / widgets | Movimiento |
|-----|-----------|-------|----------------------|------------|
| 6 Diagnóstico | `cc-service` | Blanco | Spread: Image (F6) + lista (Icon List o contenedor) + Button primario · Caption | [E] entrance + [GSAP] viñetas escalonadas |
| 7 Experiencia | `cc-palette-grid` | Crudo Atelier | Grid de muestras (contenedores hijos) + Heading · contenedor `cc-palette-interactive` para JS | [GSAP/Lottie] microinteracción (Fase 6) |
| 8 Método | `cc-method` | Blanco | Pasos 01-05: contenedores con Heading numerado (Cormorant) + Text · línea de progreso (`cc-method__progress`) | [GSAP] reveal por paso + línea scroll |
| 9 Universo | `cc-universe` | Negro Tinta `#1A1A1A` (capítulo) | Full-bleed · contenedor del Orbe extendido + 4 accesos estacionales (anclas) | [3D] Orbe→4 halos / fallback [E] |
| 10-13 Estaciones | `cc-season-card` | 10-12 claro · **13 Negro Tinta** | Bloque de color (Custom 5-8) + Image (F3/F1) + Heading H3 + Text + Caption + Button | [GSAP] barrido de color + reveal |
| 14 Dimensiones | `cc-dimensions` | Gris Cálido | Grid 2×2: 4 contenedores (Heading H3 + macro F2 + def. citable) | [E] entrance escalonado |
| 15 Beneficios | `cc-benefits` | Blanco | 3-4 beneficios (Heading + Text) + Image (F4) + Button primario | [E] fade-up tarjetas |
| 16-19 Aplicación | `cc-application` | alterno Blanco/Crudo | Zigzag Image(F4)/texto, 4 bloques + Button agrupado tras 19 | [GSAP] parallax alternado |
| 20 Antes/después | `cc-reveal` | Blanco | Díptico o Image Comparison (widget) + Microcopy "conceptual" | [GSAP] scrub del reveal / [E] slider mobile |
| 21 Vídeo | `cc-video-frame` | Negro Tinta | Video widget (self-hosted, WebM+MP4, póster, `preload=metadata`, sin audio, loop) + Heading overlay | [E/N3] loop diferido |

### Acto IV — Confianza

| Mód | Clase raíz | Fondo | Estructura / widgets | Movimiento |
|-----|-----------|-------|----------------------|------------|
| 22 Cristina Barriga | `cc-authority` | Crudo Atelier | Spread: Image retrato (F1, 4:5) + Heading + Text + Blockquote (cita Cormorant ital) + Button | [E] entrada serena |
| 23 Jerarquía/método | `cc-authority` | Crudo Atelier | Columnas editoriales (Text) + Image F6 + Microcopy nota de marca | [E] fade |
| 24 Para quién | `cc-for-who` | Blanco | 3-4 audiencias (Image 1:1 + Heading + Text) + Microcopy | [E] hover profundidad |
| **S Precios** | `cc-pricing` | Gris Cálido | 3 tarjetas + tarjeta regalo (ver H) | [E] hover elevación |
| 25-26 Formación | `cc-training` | Blanco | Bloque sobrio + Button terciario (lead capture) | [E] mínimo |
| 27 FAQs | `cc-faq` | Crudo Atelier | Acordeones por categoría + nav anclas + buscador (ver J) | nativo acordeón |

### Acto V — Acción

| Mód | Clase raíz | Fondo | Estructura / widgets | Movimiento |
|-----|-----------|-------|----------------------|------------|
| 28 CTA principal | `cc-cta` | Oro Claro `#E8D5B7` suave | Heading H2 + Text + Button primario (el más fuerte) + Button WhatsApp | [E] hover premium |
| 29 CTA final | `cc-cta` | Crudo Atelier | Heading (cierre, Cormorant ital) + Orbe miniatura (`cc-color-orb` reducido) + Button | [GSAP] reveal + Orbe respira |
| 30 Confianza | `cc-trust` | Blanco | Franja de señales (Icon/Text) + Microcopy anti-medicalización | [E] mínimo |
| 31 Enlaces satélite | `cc-footer-links` | Gris Cálido | Grid thumbnails (Image 1:1 + anchor descriptivo) | [E] hover |

---

## G. EL ORBE CROMÁTICO EN ELEMENTOR

> El equipo edita textos y CTAs del hero sin saber que existe Three.js. El Orbe se controla por **data-attributes** (Fase 1 E.4); el JS (`cc-color-orb.js`) se implementa en Fase 6.

**Cómo se construye en Elementor (módulo 1 y 9, miniatura en 29):**

1. Dentro del contenedor `cc-hero`, añadir un **contenedor hijo vacío** con:
   - **Clase CSS:** `cc-color-orb`
   - **Atributos personalizados** (Pro → Advanced → Attributes):
     - `data-cc-orb|on`
     - `data-cc-orb-colors|#C4A882,#D4A853,#8BA7C4,#C4622D,#2D3E5C`
   - Posición `absolute`, z-index 0 (detrás del H1).
2. El contenido editable (H1, lead, CTAs) va en un contenedor hermano con z-index 1.
3. **Fallback ya pintado:** el contenedor `cc-color-orb` lleva de fondo un **gradiente CSS** (definido en `cc-hero.css`, Fase 6) con los colores de marca → nunca hay hueco en blanco si el JS no carga.
4. **Apagar el Orbe sin deploy:** cambiar el atributo a `data-cc-orb|off` desde Elementor.
5. **Accesibilidad/SEO:** el contenedor del canvas será `aria-hidden="true"` (lo marca el JS); no contiene texto SEO.

---

## H. MÓDULO DE SERVICIOS Y PRECIOS (sección guardable `cc-pricing`)

> Copy y precios = Fase 4 (módulo S). Posicionamiento premium: 3 tarjetas visibles. Editable 100% en Elementor.

**Estructura:**
- Contenedor `cc-pricing` (fondo Gris Cálido) → Heading H2 + Lead.
- Contenedor `row` con **3 tarjetas** (`cc-pricing__card`), cada una contenedor `column`:
  - Heading H3 (nombre + precio) · Microcopy (duración/modalidad) · lista de inclusiones (Icon List) · Nota · Button.
  - **Tarjeta Signature** marcada `cc-pricing__card--featured` (badge "el más elegido", borde Oro Suave, leve elevación).
- Contenedor de **Tarjeta regalo** (`cc-pricing__gift`) full-width debajo: Lead emocional + Body + Button "Regalar Código Color".
- Microcopy legal suave al pie.

**Datos (de Fase 4, editables):** Online Express 180 € · Signature 590 € (featured) · Elite 1.290 € · Tarjeta regalo desde 590 €.
**Nota:** PRIVATE 2.500 € **no se construye** (aparcado); dejar la plantilla preparada para clonar una 4ª tarjeta si se decide activarla.
**Responsive:** 3 tarjetas en `row` desktop → `column` apiladas en mobile; la featured va **primera** en mobile.
**Movimiento:** hover de elevación (nivel 1, CSS); sin animaciones pesadas.

---

## I. BLOQUE DE AUTORIDAD — CRISTINA BARRIGA (`cc-authority`)

> Tratamiento de **spread de revista**, no tarjeta corporativa (doc 08 D.4, Fase 1 D.2). Copy = Fase 4 (módulos 22-23).

**Construcción (módulo 22):**
- Contenedor `cc-authority` (fondo Crudo Atelier), `row` desktop:
  - **Columna imagen (≈45%):** Image widget, retrato F1 4:5 (luz natural, fondo neutro), `srcset` doc 08, **no** lazy si entra pronto en viewport. ALT: "Cristina Barriga, directora de Código Color, especialista en colorimetría e imagen personal".
  - **Columna texto (≈55%):** Heading "Dirigido por Cristina Barriga" (H2 Cormorant) · Text (lead, texto corto D.4) · Text (body) · **Blockquote** con la cita en Cormorant *italic* (Accent) como pieza central · Button secundario.
- **Módulo 23** debajo: contenedor de columnas sobrias (Text) + Image F6 + Microcopy con la **nota anti-medicalización**.
- **Prohibido:** iconos de LinkedIn azules, sellos médicos, bio en tarjeta. Los perfiles (`sameAs`) viven en el schema (M), no como botones sociales chillones.
- **Mientras no haya retrato aprobado:** usar composición tipográfica + fondo F5 (puente), nunca stock genérico (doc 08 D.4).

---

## J. SISTEMA DE 100 FAQs EN ELEMENTOR (`cc-faq`)

> Contenido = `seo/faq-bank.md`. **Todo el texto debe existir en el HTML** aunque el acordeón esté plegado (Fase 1 / prompt maestro). Usar widget **Acordeón/Toggle** de Elementor (renderiza HTML plegado, válido para extractores).

1. **Estructura:** Heading H2 + contenedor con **11 categorías** (H3, `cc-faq__category`), cada una con su Acordeón de items (`cc-faq__item`: pregunta como título real, respuesta como contenido).
2. **Navegación:** menú de anclas superior (`cc-faq__nav`) con enlaces a cada categoría (`#faq-fundamentos`, `#faq-metodo`, …). Cada contenedor de categoría lleva su **CSS ID** correspondiente.
3. **Buscador opcional** (`cc-faq__search`): filtro JS sobre el HTML ya presente (Fase 6), **nunca** carga dinámica.
4. **Imágenes-respuesta:** solo en categorías 1, 3-6, 9 (doc 08 I.1), dentro del acordeón, **lazy**, `srcset` 400/800/1200, presupuesto ≤2-3 MB la sección.
5. **Diseño premium:** el acordeón se estiliza vía `cc-faq.css` (Fase 6) para que parezca editorial, no un footer de soporte.
6. **Schema FAQPage:** NO se mete por widget; va en PHP con las 13 priorizadas (M).
7. **Editabilidad:** añadir/editar/eliminar una FAQ se hace en el widget Acordeón sin tocar código; recordar reflejarlo en `faq-bank.md` (Fase 8).

---

## K. ANIMACIONES: MOTION EFFECTS NATIVO vs GSAP (FASE 6)

| Se hace en Elementor (nativo) | Se reserva para Fase 6 (GSAP/Three.js) |
|-------------------------------|------------------------------------------|
| Entrance animations (fade-up, fade-in) suaves | Revelado de texto palabra a palabra (mód 2) |
| Hover de botones/tarjetas (nivel 1) | Parallax fino y scrub (mód 3-4, 9, 20) |
| Sticky CTA (efecto sticky de contenedor) | Pin + scroll-scrub (mód 1, 9, 20) |
| Toggle de acordeón | Orbe Three.js (mód 1, 9, 29) |
| | Microinteracción de paleta (mód 7) |

- **Regla:** Elementor Motion Effects solo para lo ligero. Lo cinematográfico lo gobierna GSAP ScrollTrigger desde `cc-*.js` (Fase 1 E.5: GSAP es la única fuente de verdad del scroll). Desactivar la minificación que rompa GSAP (Fase 0).
- **Todo respeta `prefers-reduced-motion`** y anima solo `transform`/`opacity`.

---

## L. RESPONSIVE Y MOBILE-FIRST

- **Construir y validar primero a 375px** (Fase 3 H). Desktop es expansión.
- **Zigzag → vertical:** los contenedores `row` pasan a `column`; cuidar el `order` para mantener "imagen arriba / texto abajo" con lectura lógica.
- **Tipografía:** todos los presets usan `clamp()`; verificar que el Hero no desborde a 320px.
- **Imágenes:** activar art direction donde el recorte cambia (hero 9:16 mobile vs 16:9 desktop) usando visibilidad por dispositivo o `<picture>` desde plantilla del child theme (doc 08 K.6).
- **Movimiento reducido en mobile:** Orbe → fallback gradiente; scrub → fade; vídeo sin autoplay en gama baja.
- **Sticky CTA** en mobile desde el módulo 6 (discreto, se oculta sobre formularios).
- **Tap targets ≥44px**, CTAs full-width en mobile.

---

## M. QUÉ NO VA EN ELEMENTOR (CÓDIGO Y SCHEMA — FASE 6)

> Se prepara el contenedor/hook aquí; el contenido se implementa en Fase 6 en el child theme versionado.

1. **Schema JSON-LD** (Organization, Person con `sameAs` confirmados, Service con `OfferCatalog`, WebSite, BreadcrumbList, FAQPage de las 13): en `functions.php`/partial PHP, **no** en Elementor ni en plugins de SEO para las piezas críticas (Fase 4 E). Rank Math gestiona meta/breadcrumbs.
2. **CSS del sistema visual** (`cc-*.css`): define lo que hacen las clases aplicadas en Elementor.
3. **JS modular** (`cc-color-orb.js`, `cc-scroll-animations.js`, `cc-palette-interactive.js`, `cc-faq-filter.js`): encolado **condicional por página** (Fase 0).
4. **Fuentes locales:** registradas por el child theme; Elementor solo las referencia.
5. **`llms.txt`** en la raíz del dominio (artefacto Fase 4).

---

## N. PLANTILLAS GUARDABLES, EXPORTACIÓN E IMPORTACIÓN

- **Guardar cada módulo como plantilla** (Save as Template) con nombre `CC — NN Nombre` (p. ej. `CC — 22 Autoridad`). Permite reutilizar en satélites futuros sin rehacer.
- **Plantillas clave reutilizables en el ecosistema:** `cc-pricing`, `cc-faq` (categoría tipo), `cc-authority`, `cc-season-card`, `cc-cta`.
- **Exportación:** exportar plantillas a JSON y **versionarlas** en el repo (`templates/elementor/*.json`) como respaldo y para staging→producción (Fase 0). El contenido vive en la BD; el JSON es copia de seguridad estructural.
- **Importación a staging** de SiteGround antes de producción; purga de cachés en orden Elementor → SiteGround → Cloudflare tras publicar (Fase 0).
- **Global Kit** (Site Settings) también se exporta para clonar el sistema de diseño en nuevos sitios/satélites.

---

## O. QUÉ QUEDA EDITABLE Y QUÉ NO TOCAR

| ✅ Editable libremente en Elementor | ⛔ No tocar (rompe el sistema) |
|-------------------------------------|--------------------------------|
| Todos los textos, titulares, precios, FAQs | Las clases `cc-*` (son el contrato con el CSS/JS) |
| Imágenes y vídeos (respetando specs doc 08) | Los `data-cc-orb*` salvo on/off y colores |
| CTAs, enlaces, formularios | El contenedor vacío del Orbe (no meter contenido dentro) |
| Orden de tarjetas, añadir/quitar FAQs | Global Colors/Fonts sin avisar (afecta a todo) |
| Activar/desactivar Orbe (`data-cc-orb`) | IDs de ancla de las categorías FAQ (los usa la nav y el schema) |

> Documentar esta tabla en `docs/MANTENIMIENTO.md` (Fase 0) para el equipo no técnico.

---

## P. CHECKLIST Y ENTREGABLES PARA FASE 6

### P.1 Validación de Fase 5

- [ ] Global Colors y Global Fonts cargados antes de construir (B, C).
- [ ] Cada módulo con su clase raíz `cc-*` correcta (F).
- [ ] Contenedor `cc-color-orb` con data-attributes y fallback de gradiente (G).
- [ ] Módulo de precios con 3 tarjetas + regalo, Signature featured (H).
- [ ] Bloque de autoridad como spread, sin iconos sociales chillones (I).
- [ ] 100 FAQs en acordeón con HTML presente, anclas e IDs (J).
- [ ] Responsive validado a 375px en todos los módulos (L).
- [ ] LCP = H1 del hero, no lazy; resto de imágenes lazy con dimensiones (doc 08 K.8).

### P.2 Lo que la Fase 6 debe codificar

- `cc-*.css` (sistema visual de cada clase) y fuentes locales.
- `cc-color-orb.js` (Three.js) + fallbacks; `cc-scroll-animations.js` (GSAP ScrollTrigger); `cc-palette-interactive.js`; `cc-faq-filter.js`.
- Schema JSON-LD en PHP (Fase 4 E), con `sameAs` y `OfferCatalog` ya confirmados.
- Encolado condicional por página y exclusiones de minificación (Fase 0).

### P.3 Bloqueos

1. **Aprobación del cliente** de Fases 0-5.
2. **Assets fotográficos** producidos según doc 08 (al menos los P1) para poblar los módulos; mientras, usar placeholders marcados.
3. **Retrato editorial de Cristina Barriga** aprobado para el módulo 22 (si no, puente tipográfico).

> **Siguiente fase:** FASE 6 — Código (CSS/JS modular `cc-*`, Orbe Three.js, schema PHP), una vez aprobada esta Fase 5.
