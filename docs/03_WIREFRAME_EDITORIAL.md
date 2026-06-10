# 03 — WIREFRAME EDITORIAL
## Código Color · Estructura de scroll, jerarquía visual, intención psicológica, narrativa, CTAs y notas mobile-first de la landing (31 módulos)

> **Estado:** Entregado, pendiente de aprobación del cliente.
> **Regla:** Esta fase no genera código ni copy final. Define el **orden, el ritmo, la jerarquía y la intención** de cada bloque: el plano editorial sobre el que la Fase 4 escribe los textos y la Fase 5 construye en Elementor.
> **Depende de:** FASE 0 (arquitectura D), FASE 1 (31 módulos, sistema de movimiento, Orbe, SEO/GEO), FASE 2 (benchmark) y documento 08 (fotografía/vídeo y familias F1-F6).
> **Rol asumido:** Director de arte editorial + Diseñador UX/CRO + Narrador de scroll.

---

## ÍNDICE

- **A.** Principios del wireframe (rejilla, ritmo, narrativa global)
- **B.** Mapa de altura y ritmo (desktop + mobile)
- **C.** Wireframe módulo por módulo (1-31)
- **D.** Bloque de autoridad — Cristina Barriga (ubicación y tratamiento)
- **E.** Camino de conversión (arquitectura de CTAs / CRO)
- **F.** Narrativa de scroll completa (el arco en una lectura)
- **G.** Sistema de 100 FAQs en el wireframe
- **H.** Notas mobile-first transversales
- **I.** Mapa de animación por módulo (resumen)
- **J.** Checklist de validación y entregables para Fase 4

---

## A. PRINCIPIOS DEL WIREFRAME

### A.1 La regla de oro

**Una idea por viewport** (lógica Apple, Fase 2). Cada pantalla completa transmite un solo mensaje, con un solo elemento visual dominante y un solo nivel de jerarquía tipográfica protagonista. Nada compite con nada. Si un bloque necesita dos ideas, son dos bloques.

### A.2 Sistema de rejilla

| Dispositivo | Rejilla | Margen lateral | Ancho de contenido | Gutter |
|-------------|---------|----------------|--------------------|--------|
| Desktop (≥1200px) | 12 columnas | 80-120px | máx. 1280px (texto 680px) | 24px |
| Tablet (768-1199px) | 8 columnas | 48px | fluido | 20px |
| Mobile (<768px) | 4 columnas | 20-24px | 100vw - margen | 16px |

- **Espacio negativo ≥ 40%** de cada viewport clave (heredado de Fase 1). El aire es el lujo.
- **Línea de texto ≤ 68 caracteres** (DM Sans, body), titulares serif (Cormorant) a sangre o casi.
- **Ritmo vertical:** padding de sección fluido `clamp(80px, 12vh, 200px)`; las secciones "respiran" más que una landing convencional.

### A.3 Narrativa global de scroll (el arco)

El scroll cuenta **una transformación**, no una lista de servicios. Cinco actos (heredados de Fase 1 A.2):

```
ACTO I  · LLEGADA      (mods 1-2)   silencio, casi monocromo, el Orbe respira
ACTO II · TENSIÓN      (mods 3-5)   el problema → giro → definición citable
ACTO III· COMPRENSIÓN  (mods 6-21)  método, estaciones, dimensiones, aplicación (el color despierta)
ACTO IV · CONFIANZA    (mods 22-27) autoridad de Cristina Barriga + para quién + 100 FAQs
ACTO V  · ACCIÓN       (mods 28-31) vuelta al silencio "encendido" + CTA + ecosistema
```

El color en pantalla sigue ese arco: **entra casi ausente, despierta en el Acto III, y en el Acto V queda integrado y sereno** (la paleta ya "encendida"). El Orbe Cromático es el hilo: nace entero (1), se descompone en estaciones (9), y reaparece en miniatura como firma en el cierre (29).

### A.4 Convenciones de este wireframe

Cada módulo se describe con: **posición y altura · intención psicológica · layout y jerarquía · recurso visual (familia F1-F6 del doc 08) · movimiento (nivel 1-5, Fase 1 E.16) · CTA · nota mobile**. Las cotas de altura son orientativas (validar en Fase 5).

---

## B. MAPA DE ALTURA Y RITMO

Estimación de "pantallas" (1 viewport ≈ 900px desktop / 760px mobile). Sirve para dimensionar el esfuerzo de scroll y el reparto de CTAs.

| Acto | Módulos | Altura desktop aprox. | Altura mobile aprox. | Densidad |
|------|---------|------------------------|----------------------|----------|
| I — Llegada | 1-2 | 1,8 viewports | 2,0 | Muy baja (aire máximo) |
| II — Tensión | 3-5 | 2,4 viewports | 3,0 | Baja |
| III — Comprensión | 6-21 | 9-11 viewports | 13-15 | Media (el grueso) |
| IV — Confianza | 22-27 | 4-5 viewports (+FAQs plegadas) | 6-7 | Media-alta |
| V — Acción | 28-31 | 2,2 viewports | 2,8 | Baja |
| **Total** | **31** | **≈ 20-22 viewports** | **≈ 27-30** | — |

> Regla CRO: con ~20 viewports, **ningún tramo de más de 3 pantallas puede quedar sin una vía de conversión visible o accesible** (ver E). El scroll es largo a propósito (es un editorial), pero la salida a la acción nunca está a más de un gesto.

---

## C. WIREFRAME MÓDULO POR MÓDULO

> Leyenda movimiento: **N1** CSS · **N2** GSAP ScrollTrigger · **N3** Lottie/vídeo · **N4** Three.js (Orbe) · **N5** Spline (descartado). Familias foto según doc 08: **F1** retrato · **F2** macro · **F3** bodegón cromático · **F4** ambiente · **F5** luz abstracta · **F6** documental.

---

### ACTO I — LLEGADA

#### Módulo 1 · Hero editorial inmersivo
- **Posición / altura:** apertura. 1,0 viewport (full-bleed), sin scroll forzado para leer el H1.
- **Intención psicológica:** en <3s la usuaria debe sentir "esto es caro y es para mí". Silencio visual, galería de arte + laboratorio de luz. No vende: declara categoría.
- **Layout / jerarquía:** lienzo crudo (`#FAF8F5`). H1 serif enorme (Cormorant, `clamp(3rem,8vw,7rem)`) alineado a la izquierda o centrado bajo. El **Orbe Cromático** ocupa el tercio derecho/superior como único foco de color. Subtítulo DM Sans breve + CTA suave. Nada más.
- **Recurso visual:** Orbe (N4 con fallback N1 gradiente) sobre fondo F5; póster de vídeo de ambiente como capa inferior. Versión 9:16 en mobile (art direction del doc 08).
- **Movimiento:** N4 (Orbe respira en idle, parallax mínimo con cursor) + N2 (revelado del H1 línea a línea). El Orbe carga **post-LCP**; el LCP es el H1/fondo.
- **CTA:** primario suave — "Reservar diagnóstico" (estilo invitación, no botón gritón). Secundario fantasma — "Descubre el método" (scroll-ancla al módulo 8).
- **Mobile:** Orbe arriba (9:16), H1 debajo a sangre; CTA fijo dentro del flujo, no sticky aún.

#### Módulo 2 · Manifiesto Código Color
- **Posición / altura:** 0,8-1,0 viewport.
- **Intención psicológica:** conexión emocional inmediata; bajar el ritmo cardíaco, fijar el tono de marca. Es el "respiro" tras el impacto.
- **Layout / jerarquía:** una sola frase-manifiesto en Cormorant itálica, gran tamaño, centrada con muchísimo aire (≥60% vacío). Bloque citable por IA.
- **Recurso visual:** banda de luz/textura crudo F5 (21:9), casi monocroma, sutil. Sin foto de persona.
- **Movimiento:** N2 — revelado de texto palabra a palabra al entrar en viewport.
- **CTA:** ninguno (deliberado: este bloque solo enamora).
- **Mobile:** tipografía fluida menor, mismo aire proporcional.

---

### ACTO II — TENSIÓN

#### Módulo 3 · El Problema
- **Posición / altura:** 0,9 viewport.
- **Intención psicológica:** identificación ("me pasa a mí, llevo años usando colores que me apagan"). Genera la herida que el producto cura.
- **Layout / jerarquía:** asimétrico editorial (lógica Modern Huntsman): columna de texto a la izquierda (40 caracteres/línea), retrato a la derecha. Titular medio + 1 párrafo corto.
- **Recurso visual:** F1 retrato en clave **desaturada** ("antes de despertar el color"), piel real, luz neutra.
- **Movimiento:** N2 — parallax suave de la imagen; el texto sube ligeramente al entrar.
- **CTA:** ninguno (estamos en la tensión, no se vende todavía).
- **Mobile:** imagen full-width arriba, texto debajo.

#### Módulo 4 · La Solución
- **Posición / altura:** 0,9 viewport.
- **Intención psicológica:** alivio y deseo. Giro narrativo: "existe un método, y es preciso".
- **Layout / jerarquía:** espejo del módulo 3 (texto derecha / imagen izquierda) para crear ritmo de zigzag editorial. La imagen empieza a **encenderse** en color.
- **Recurso visual:** F1/F5 — el mismo registro del 3 pero el color despierta (un acento de paleta entra).
- **Movimiento:** N2 — transición de desaturado→color ligada al scroll (scrub suave) si el rendimiento lo permite; si no, fade N1.
- **CTA:** micro-CTA textual ("Esto es Código Color ↓") que ancla al módulo 5.
- **Mobile:** mantiene el orden imagen-texto; el scrub se simplifica a fade.

#### Módulo 5 · Qué es Código Color
- **Posición / altura:** 0,7 viewport.
- **Intención psicológica:** comprensión y primera confianza. Es la **definición citable nº1** (para usuarios y LLMs).
- **Layout / jerarquía:** bloque definitorio centrado, fondo `#F2F0ED` para marcar "capítulo". Frase "Código Color es…" en lead (18px) destacado, rodeada de aire. Diseñado como featured snippet de párrafo (Fase 1 C.9).
- **Recurso visual:** F3/F5 — imagen-firma neutra con un acento de paleta, discreta (no roba protagonismo a la definición). Posible `alt=""` si es puramente decorativa.
- **Movimiento:** N1 — aparición suave; sin distracción (el texto es el protagonista, debe ser legible y extraíble).
- **CTA:** secundario — "Ver el método" (ancla al 8).
- **Mobile:** definición a sangre, tipografía cómoda; es de los bloques más leídos.

---

### ACTO III — COMPRENSIÓN (el color despierta)

#### Módulo 6 · Diagnóstico cromático
- **Posición / altura:** 1,0 viewport.
- **Intención psicológica:** entender el servicio central; primer punto de conversión "medio".
- **Layout / jerarquía:** spread editorial — imagen documental grande del drapeado + bloque de texto con 3 viñetas de lo que incluye.
- **Recurso visual:** F6 documental (tela junto al rostro, el efecto del color).
- **Movimiento:** N2 — parallax + revelado de viñetas escalonado.
- **CTA:** primario — "Reservar mi diagnóstico" (enlace a `/colorimetria-madrid/` en el futuro; ahora a formulario/WhatsApp).
- **Mobile:** imagen full-width, viñetas apiladas; CTA visible.

#### Módulo 7 · Experiencia interactiva de color
- **Posición / altura:** 1,0-1,2 viewport.
- **Intención psicológica:** memorabilidad y tiempo en página; "juega" con el color (engagement signal).
- **Layout / jerarquía:** grid interactivo de muestras/paleta; al hover/tap, las muestras reaccionan. Titular breve arriba.
- **Recurso visual:** F3 texturas de paleta + microanimación (N3 Lottie/CSS exportada).
- **Movimiento:** N2-N3 — aparición progresiva de la paleta + microinteracción por muestra. Respeta `prefers-reduced-motion`.
- **CTA:** ninguno directo (es exploración); refuerza deseo hacia los siguientes.
- **Mobile:** grid simplificado (menos muestras a la vez), interacción por tap; si el dispositivo es de gama baja → versión estática.

#### Módulo 8 · Método Código Color
- **Posición / altura:** 1,2 viewport.
- **Intención psicológica:** confianza por proceso; reducir incertidumbre ("hay un sistema, no es magia"). Snippet de lista (HowTo implícito).
- **Layout / jerarquía:** numeración elegante de pasos (01, 02, 03…) en Cormorant, ritmo lento tipo artesanía (lógica Urban Jürgensen). Cada paso = título + 1 frase.
- **Recurso visual:** F6 serie documental del proceso paso a paso (3-5 tomas).
- **Movimiento:** N2 — cada paso se revela al entrar; línea de progreso vertical que avanza con el scroll.
- **CTA:** secundario al final de los pasos — "Empezar el proceso".
- **Mobile:** pasos apilados verticalmente; la línea de progreso queda a la izquierda.

#### Módulo 9 · Universo cromático estacional (hub)
- **Posición / altura:** 1,2-1,5 viewport (pieza espectáculo).
- **Intención psicológica:** asombro; "este sistema es bello y ordenado". Es el clímax visual del Acto III.
- **Layout / jerarquía:** full-bleed. El **Orbe se descompone en 4 halos estacionales** (extensión opcional del N4, Fase 1 E.2). Cuatro accesos visuales a las estaciones.
- **Recurso visual:** F3+F5 composición de las 4 estaciones + halos (eco del Orbe). Si no hay Three.js extendido → versión vídeo/gradiente (N3/N1).
- **Movimiento:** N4 (Orbe→4 halos con scroll-scrub) o fallback N2/N3. Pin + scrub solo aquí, en 1 y en 20.
- **CTA:** navegación visual a cada estación (anclas internas a 10-13; futuros enlaces a satélites `/estaciones/`).
- **Mobile:** la descomposición se simplifica (4 tarjetas que entran en secuencia, sin WebGL pesado).

#### Módulos 10-13 · Primavera / Verano / Otoño / Invierno
- **Posición / altura:** 1,0 viewport cada una (4 capítulos editoriales).
- **Intención psicológica:** identificación estacional ("¿cuál soy yo?"). Autoselección que cualifica.
- **Layout / jerarquía:** cada estación = spread de revista. Bloque de color a hex exacto (Primavera `#D4A853`, Verano `#8BA7C4`, Otoño `#C4622D`, Invierno `#2D3E5C`) + arquetipo de piel + caption técnico. **Invierno** usa sección oscura (`#1A1A1A`) para contraste de capítulo (lógica iPad Pro / Bleu de Chanel).
- **Recurso visual:** F3 bodegón de telas a hex + F1 arquetipo de piel (doc 08 D.2).
- **Movimiento:** N2 — el bloque de color "barre" al entrar; texto en revelado. Transición cromática entre estaciones (cálido→frío) al hacer scroll.
- **CTA:** micro-CTA por estación ("Ver paleta completa →", futuro satélite).
- **Mobile:** una estación por pantalla, color a sangre arriba, texto debajo; el zigzag se vuelve vertical.

#### Módulo 14 · Contraste · Temperatura · Saturación · Luminosidad
- **Posición / altura:** 1,0-1,2 viewport.
- **Intención psicológica:** demostrar profundidad técnica (E-E-A-T visual). "Esto tiene ciencia detrás". **Definiciones citables** de las 4 dimensiones.
- **Layout / jerarquía:** 4 bloques (2×2 desktop) tipo "specs como diseño" (lógica MacBook Pro): cada dimensión con cifra/concepto grande + macro + definición de 1 línea.
- **Recurso visual:** F2 — 4 macros que demuestran cada dimensión (piel/tela).
- **Movimiento:** N2 — los 4 bloques entran escalonados.
- **CTA:** ninguno (bloque de autoridad técnica).
- **Mobile:** 4 bloques apilados (1 columna); las macros mantienen 1:1.

#### Módulo 15 · Beneficios
- **Posición / altura:** 0,9 viewport.
- **Intención psicológica:** traducir técnica → vida real; deseo tangible ("comprar mejor, verte mejor, ahorrar errores").
- **Layout / jerarquía:** 3-4 beneficios en formato editorial limpio (no iconos de stock); titular + frase.
- **Recurso visual:** F4 imagen aspiracional sobria (vida real con color bien elegido).
- **Movimiento:** N1-N2 — aparición suave de tarjetas.
- **CTA:** primario — "Quiero mi paleta".
- **Mobile:** beneficios apilados; imagen de apoyo arriba.

#### Módulos 16-19 · Color aplicado a ropa / maquillaje / cabello / imagen profesional
- **Posición / altura:** 0,9 viewport cada uno (16-17-18 prioritarios; 19 eleva ticket).
- **Intención psicológica:** aplicabilidad y deseo ("esto cambia mi día a día"). El 19 cualifica a la audiencia profesional (ticket alto).
- **Layout / jerarquía:** zigzag editorial imagen/texto alternado, para no monotonizar 4 bloques seguidos. Cada uno: titular de aplicación + 1-2 frases.
- **Recurso visual:** F4 ambiente (armario, tocador, espejo) + F2 macro de fibra en cabello (18). El 19 con look profesional (F4/F1).
- **Movimiento:** N2 — parallax alternado; revelado de texto.
- **CTA:** secundario agrupado al final del bloque 19 ("Aplica tu color a todo →").
- **Mobile:** imagen-texto vertical; el 18 puede ser P2 (carga diferida).

#### Módulo 20 · Antes y después conceptual
- **Posición / altura:** 1,0 viewport (pieza scrub).
- **Intención psicológica:** visualizar la transformación **sin inventar casos**. Mismo rostro, dos paletas.
- **Layout / jerarquía:** díptico o reveal con cortinilla controlada por scroll. Etiquetado claramente como **conceptual** (sin claim de "cliente real"), por la restricción de Fase 1/doc 08 D.5.
- **Recurso visual:** F1 díptico (mismo rostro, dos paletas).
- **Movimiento:** N2 — scrub del reveal (la cortinilla avanza con el scroll). Pin breve.
- **CTA:** micro-CTA ("Imagina el tuyo").
- **Mobile:** reveal por tap/slider en vez de scrub fino.

#### Módulo 21 · Vídeo cinemático
- **Posición / altura:** 1,0 viewport.
- **Intención psicológica:** inmersión sensorial; percepción premium (textura, piel, tela, luz). Cierra el Acto III en clave emocional.
- **Layout / jerarquía:** vídeo a sangre con titular mínimo superpuesto (legibilidad garantizada con overlay sutil).
- **Recurso visual:** vídeo loop (WebM+MP4, <4MB, sin audio, `preload="metadata"`, póster optimizado — doc 08 K.8) F1/F2/F5.
- **Movimiento:** N3 — vídeo en loop, carga diferida por IntersectionObserver; `prefers-reduced-motion` → póster estático.
- **CTA:** ninguno (respiro sensorial antes de la confianza).
- **Mobile:** vídeo vertical o póster + play; nunca autoplay con datos si gama baja.

---

### ACTO IV — CONFIANZA

#### Módulo 22 · Cristina Barriga — dirección experta
- **Posición / altura:** 1,2 viewport (pieza de autoridad). Ver sección **D**.
- **Intención psicológica:** humanizar y dar criterio. "Hay una directora identificable detrás del método" (E-E-A-T, entidad Person).
- **Layout / jerarquía:** **spread editorial de revista** (no tarjeta corporativa): retrato grande F1 (luz natural, fondo neutro), nombre en Cormorant, claim "Dirigido por Cristina Barriga", 2-3 párrafos de visión + **cita en itálica** como pieza central.
- **Recurso visual:** F1 retrato de autoridad (doc 08 D.4). **Condicionado a la lista D.4 de Fase 1**: sin material aprobado, puente tipográfico + F5, nunca stock genérico.
- **Movimiento:** N1-N2 — entrada serena, sin efectismo (la autoridad no necesita espectáculo).
- **CTA:** secundario — "Conoce el método de Cristina Barriga" (futuro `/cristina-barriga/`).
- **Mobile:** retrato full-width arriba, texto debajo; la cita destaca.

#### Módulo 23 · Jerarquía profesional y método
- **Posición / altura:** 0,8 viewport.
- **Intención psicológica:** reforzar el criterio ("cómo se supervisa cada diagnóstico, por qué hay método"). Refuerza E-E-A-T.
- **Layout / jerarquía:** columnas editoriales sobrias (lógica Mac Studio: precisión sin teatro).
- **Recurso visual:** F6 documental del criterio experto (manos, drapeado, supervisión).
- **Movimiento:** N1 — mínimo.
- **CTA:** ninguno (continuidad con el 22).
- **Mobile:** columnas a una sola.

#### Módulo 24 · Para quién es
- **Posición / altura:** 0,9 viewport.
- **Intención psicológica:** autoselección y cualificación de leads ("esto es para mí": profesionales, novias, +40, profesionales de la imagen).
- **Layout / jerarquía:** 3-4 audiencias como variantes elegantes (lógica Apple Watch "hay uno para ti"), no como lista de bullets.
- **Recurso visual:** F1 — 3-4 retratos de arquetipos de audiencia (diversidad real, doc 08 D.1).
- **Movimiento:** N1 — hover/tap con profundidad sutil.
- **CTA:** por audiencia, suave ("Si eres…, empieza aquí").
- **Mobile:** carrusel horizontal o apilado.

#### Módulos 25-26 · Formación / Cursos
- **Posición / altura:** 0,7 viewport (sembrado, prioridad 3).
- **Intención psicológica:** plantar la línea futura sin distraer de la conversión principal. Autoridad docente.
- **Layout / jerarquía:** bloque sobrio "próximamente / lista de espera"; no compite con el diagnóstico.
- **Recurso visual:** F6/F3 imagen de aula/material editorial (puede ser P3 con puente premium).
- **Movimiento:** N1.
- **CTA:** terciario — "Apúntate a la lista de formación" (lead capture suave).
- **Mobile:** bloque compacto.

#### Módulo 27 · 100 FAQs técnicas organizadas
- **Posición / altura:** plegado ≈ 0,8 viewport; desplegado, mucho más. Ver sección **G**.
- **Intención psicológica:** resolver objeciones y demostrar dominio absoluto (maquinaria GEO/AEO). Permanencia.
- **Layout / jerarquía:** H2 + 8-12 categorías (H3) en acordeones; navegación de anclas entre categorías; buscador opcional (filtro JS sobre HTML ya presente).
- **Recurso visual:** imágenes-respuesta selectivas en categorías 1, 3-6, 9 (doc 08 I.1 / prompt maestro), lazy.
- **Movimiento:** N1 — acordeón; sin animación pesada (el contenido vive en HTML, doc 08 K.8).
- **CTA:** intercaladas 3-5 FAQs estrella pueden enlazar a CTA; cierre de sección con CTA a diagnóstico.
- **Mobile:** acordeones a sangre, una categoría visible a la vez; imágenes 100% width.

---

### ACTO V — ACCIÓN

#### Módulo 28 · CTA principal
- **Posición / altura:** 0,7 viewport.
- **Intención psicológica:** conversión clara tras haber enamorado y demostrado. El momento de pedir la acción.
- **Layout / jerarquía:** bloque centrado, fondo de acento suave; un único CTA dominante + vía alternativa (WhatsApp/formulario).
- **Recurso visual:** F5 — vuelta al silencio con la paleta ya "encendida" (banda de luz integrada).
- **Movimiento:** N1 — hover premium del botón.
- **CTA:** **primario, el más fuerte de la página** — "Reservar diagnóstico cromático".
- **Mobile:** CTA full-width; aquí sí, **sticky CTA** puede activarse a partir de este punto si no lo estaba antes.

#### Módulo 29 · CTA final editorial
- **Posición / altura:** 0,8 viewport.
- **Intención psicológica:** cierre emocional; última conversión para quien necesitaba sentir antes de actuar.
- **Layout / jerarquía:** frase-manifiesto de cierre (Cormorant itálica) + el **Orbe en miniatura** como firma de marca + CTA elegante.
- **Recurso visual:** F5 + Orbe miniatura (cierra el círculo narrativo del módulo 1).
- **Movimiento:** N2 — revelado sereno; el Orbe miniatura "respira".
- **CTA:** primario repetido en clave editorial ("Empieza tu Código Color").
- **Mobile:** a sangre, Orbe pequeño centrado.

#### Módulo 30 · Sección de confianza
- **Posición / altura:** 0,6 viewport.
- **Intención psicológica:** credibilidad **sin testimonios inventados** (señales verificables: garantías del proceso, qué incluye, modalidad).
- **Layout / jerarquía:** franja sobria de señales reales tratadas con dirección de arte.
- **Recurso visual:** F3 señales verificables (no sellos médicos, doc 08 A.5 exclusiones).
- **Movimiento:** N1.
- **CTA:** ninguno (refuerzo, no venta).
- **Mobile:** franja apilada.

#### Módulo 31 · Enlaces a futuras páginas satélite
- **Posición / altura:** 0,6 viewport (pre-footer).
- **Intención psicológica:** preparar el ecosistema y repartir autoridad (enlazado interno editorial, no footer masivo).
- **Layout / jerarquía:** grid de thumbnails con anchor descriptivo a cada satélite (módulo 9→estaciones, 6→colorimetría Madrid, 22→Cristina Barriga, 25-26→formación).
- **Recurso visual:** F3/F5 thumbnails 1:1.
- **Movimiento:** N1 — hover con profundidad.
- **CTA:** enlaces internos (flujo de autoridad, Fase 1 C.5).
- **Mobile:** grid 2 columnas.

---

## D. BLOQUE DE AUTORIDAD — CRISTINA BARRIGA

### D.1 Ubicación óptima en el scroll

**Módulos 22-23, en el Acto IV (Confianza), justo antes de las 100 FAQs y los CTAs finales.** Justificación de CRO/narrativa: la usuaria llega habiendo (1) sentido el problema, (2) comprendido el método y (3) visto la profundidad técnica. Es el momento exacto para poner rostro y criterio: la autoridad convierte la comprensión en confianza, y la confianza en acción. Ponerla antes (en la llegada) sería "sobre nosotros" prematuro; ponerla después de los CTAs la desperdiciaría.

### D.2 Cómo aparece sin romper la estética premium

- **Como firma editorial de revista, no como bio corporativa** (doc 08 D.4, Fase 1 D.2): retrato de dirección de arte (luz natural, fondo neutro), tipografía serif, cita en itálica como pieza central.
- **Nunca:** tarjeta con iconos de LinkedIn azules, sello de "equipo médico", bio genérica, atrezo de clínica.
- **Refuerzo distribuido:** su criterio "firma" también las FAQs de categoría 9 (módulo 27) y es la voz del manifiesto (módulo 2), sin repetir su foto.

### D.3 Bloqueo declarado

La versión **definitiva** de los módulos 22-23 **no se redacta ni se fotografía** sin cerrar la **lista D.4 de Fase 1** (titulaciones confirmables, trayectoria, `sameAs`, retrato editorial, frase de visión, ciudad/modalidad). Hasta entonces, el wireframe reserva el espacio con un **puente** tipográfico + F5. No se inventa nada.

---

## E. CAMINO DE CONVERSIÓN (CRO)

### E.1 Reparto de CTAs a lo largo del scroll

| Punto | Módulo | Tipo de CTA | Fuerza |
|-------|--------|-------------|--------|
| Llegada | 1 | "Reservar diagnóstico" (suave) | Media |
| Tras definición | 5-6 | "Reservar mi diagnóstico" | Media-alta |
| Tras beneficios | 15 | "Quiero mi paleta" | Media-alta |
| Tras autoridad | 22 | "Conoce el método" (blando) | Baja |
| Cierre FAQs | 27 | CTA a diagnóstico | Media |
| **Conversión** | **28** | **"Reservar diagnóstico cromático"** | **Máxima** |
| Cierre emocional | 29 | "Empieza tu Código Color" | Alta |

### E.2 Reglas CRO

- **Un CTA visible (o accesible) por cada ≤3 viewports** (B). Entre módulos 9-21 (tramo largo de comprensión) hay CTAs en 15 y micro-CTAs en estaciones para no dejar "desierto" de conversión.
- **Sticky CTA en mobile** a partir del módulo 6 (o del 28 como mínimo), discreto, que no tape contenido; se oculta sobre el formulario.
- **Ningún CTA grita** (lógica quiet luxury, Fase 2 Silver Pinewood): la página seduce; el CTA es invitación. Pero el del módulo 28 es inequívocamente el dominante.
- **Jerarquía visual de botones:** primario (oro `#C4A882` sobre oscuro / oscuro sobre claro), secundario (fantasma con borde), terciario (texto con subrayado animado).

---

## F. NARRATIVA DE SCROLL COMPLETA (lectura única)

> La usuaria llega a un **lienzo casi monocromo** donde un único Orbe de luz respira (1). Una frase la detiene y la calma (2). Reconoce su problema en un rostro apagado (3), y siente el alivio cuando ese mismo rostro empieza a encenderse (4). Entiende, en una frase, qué es Código Color (5). Ve el diagnóstico real (6), juega con el color (7) y comprende que hay un método ordenado (8). Entonces el Orbe **se abre en cuatro estaciones** (9) y cada una se despliega como un capítulo de revista (10-13). Descubre que esto tiene ciencia —contraste, temperatura, saturación, luminosidad (14)— y traducción a su vida: ropa, maquillaje, cabello, presencia profesional (15-19). Visualiza su propia transformación (20) y se deja envolver por un vídeo sensorial (21). Justo cuando confía en el sistema, aparece **quién lo dirige** (22-23) y para quién es (24). Resuelve cada duda en las 100 FAQs (27) y, devuelta al silencio inicial —ahora con la paleta encendida— recibe **una sola invitación elegante a actuar** (28-29). El Orbe, en miniatura, firma el cierre.

---

## G. SISTEMA DE 100 FAQs EN EL WIREFRAME

- **Posición:** módulo 27, al final del Acto IV, **antes** de los CTAs finales (recomendación por defecto del prompt maestro: cerrar en conversión).
- **Estructura:** H2 + 8-12 categorías (H3) en acordeones; **el contenido vive en el HTML del DOM** aunque esté plegado (nunca carga por JS tras interacción).
- **Navegación:** anclas entre categorías (`#faq-fundamentos`, `#faq-metodo`…), buscador opcional como filtro JS sobre HTML presente.
- **Imágenes:** solo en categorías visuales (1, 3-6, 9), lazy, dentro del presupuesto de la sección (doc 08 K.9). Si no hay imagen a estándar editorial → la FAQ va **sin imagen** (mejor sin que mediocre).
- **CRO:** 3-5 FAQs estrella pueden destacarse en el cuerpo editorial y repetirse aquí (misma URL, sin canibalización).
- **Diseño:** debe verse **premium**, no como un footer de soporte técnico.
- **Entregable real (las 100 redactadas):** Fase 4. Aquí solo se reserva el contenedor y su estructura.

---

## H. NOTAS MOBILE-FIRST TRANSVERSALES

1. **Mobile es el diseño base**, desktop es la expansión. Cada módulo se valida primero a 375px.
2. **Zigzag → vertical:** todos los layouts imagen/texto alternados colapsan a imagen-arriba / texto-abajo, manteniendo el orden de lectura lógico.
3. **Tipografía fluida:** `clamp()` en todos los titulares; el hero nunca desborda en 320px.
4. **Movimiento reducido en mobile:** N4 (Orbe) se simplifica o cae a fallback N1; N2 scrub se reduce a fades; vídeos sin autoplay en gama baja (doc 08 / Fase 1 E.11).
5. **Tap targets ≥ 44px**; CTAs full-width; sticky CTA discreto.
6. **Imágenes:** art direction real (9:16 en hero, recortes propios), `srcset`/`sizes` y AVIF→WebP→JPG (doc 08 K.6).
7. **Altura percibida:** ~27-30 viewports en mobile (B); por eso el reparto de CTAs y los micro-cierres por estación son críticos para no fatigar.
8. **Rendimiento:** lo pesado (Orbe, vídeo, imágenes bajo el pliegue) carga diferido; el LCP mobile es el H1/fondo del hero.

---

## I. MAPA DE ANIMACIÓN POR MÓDULO (resumen)

| Módulo | Nivel | Efecto principal | Pin/Scrub |
|--------|-------|------------------|:---------:|
| 1 Hero | N4 (+N2) | Orbe respira + revelado H1 | Pin+scrub |
| 2 Manifiesto | N2 | Revelado palabra a palabra | — |
| 3-4 Problema/Solución | N2 | Parallax + desaturado→color | Scrub (4) |
| 5 Definición | N1 | Aparición suave | — |
| 6 Diagnóstico | N2 | Parallax + viñetas | — |
| 7 Experiencia | N2-N3 | Paleta progresiva + microinteracción | — |
| 8 Método | N2 | Pasos + línea de progreso | — |
| 9 Universo | N4/N3 | Orbe → 4 halos | Pin+scrub |
| 10-13 Estaciones | N2 | Barrido de color + revelado | — |
| 14 Dimensiones | N2 | 4 bloques escalonados | — |
| 15 Beneficios | N1-N2 | Tarjetas | — |
| 16-19 Aplicación | N2 | Parallax alternado | — |
| 20 Antes/después | N2 | Reveal con cortinilla | Pin+scrub |
| 21 Vídeo | N3 | Loop diferido | — |
| 22-23 Autoridad | N1-N2 | Entrada serena | — |
| 24 Para quién | N1 | Hover profundidad | — |
| 25-26 Formación | N1 | — | — |
| 27 FAQs | N1 | Acordeón | — |
| 28 CTA | N1 | Hover premium | — |
| 29 CTA final | N2 | Revelado + Orbe miniatura | — |
| 30-31 Confianza/Enlaces | N1 | Hover | — |

> Reglas globales (Fase 1 E.16): todo respeta `prefers-reduced-motion`; nada anima propiedades de layout (solo `transform`/`opacity`); sin animación, la página sigue siendo legible y bella.

---

## J. CHECKLIST DE VALIDACIÓN Y ENTREGABLES PARA FASE 4

### J.1 Validación de Fase 3 (antes de pasar a copy)

- [ ] El orden de los 31 módulos respeta el arco de 5 actos (A.3 / F).
- [ ] Una idea por viewport en todos los bloques clave (A.1).
- [ ] Camino de conversión sin "desiertos" >3 viewports (E.2).
- [ ] Bloque de Cristina Barriga ubicado en Acto IV con tratamiento editorial (D).
- [ ] 100 FAQs reservadas antes de los CTAs finales (G).
- [ ] Cada módulo tiene familia fotográfica asignada (coherente con doc 08).
- [ ] Movimiento asignado por módulo con su fallback (I).
- [ ] Mobile-first validado a 375px en cada módulo (H).

### J.2 Lo que la Fase 4 debe producir sobre este plano

- H1/H2/H3 y textos completos de los 31 módulos según su intención psicológica.
- Las **100 FAQs** redactadas (anatomía de extracción) + banco maestro `seo/faq-bank.md`.
- Metadatos (título 55-60, descripción 140-155, slug), schema JSON-LD, `llms.txt`.
- ALT/title/caption de las imágenes principales (según doc 08 K).
- Bloque de Cristina Barriga **solo** con datos confirmados (lista D.4 de Fase 1).

### J.3 Bloqueos heredados que siguen abiertos

1. **Aprobación del cliente de Fases 0-2** (PR #1) y de este wireframe.
2. **Lista D.4 de Cristina Barriga** (bloquea módulos 22-23 definitivos y la Fase 4).
3. **Muestras físicas de tela** por estación (calibración de hex para módulos 9-13 y rodaje doc 08).
4. **Modalidad/ubicación confirmada** (Madrid presencial + online) para señales locales y CTAs.

> **Siguiente fase:** FASE 4 — Copy, SEO y GEO, una vez aprobado este wireframe y desbloqueada la información de Cristina Barriga.
