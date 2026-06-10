# FASE 1 — ARQUITECTURA, DIRECCIÓN DE ARTE, JERARQUÍA EXPERTA Y ESTRATEGIA SEO/GEO
## Código Color · Concepto visual · 31 módulos · SEO/GEO/AEO · Cristina Barriga · Three.js y movimiento premium

> **Estado:** Entregado, pendiente de aprobación del cliente.
> **Regla:** Esta fase no genera código. Define el qué y el porqué; el cómo llega en Fases 5-6.
> **Depende de:** FASE 0 aprobada (arquitectura D híbrida).

---

## A. CONCEPTO VISUAL DEFINITIVO

### A.1 Nombre del concepto

**«Minimalismo Editorial Cromático Futurista»** — nombre de sistema.
**«El Despertar del Color»** — nombre de la experiencia narrativa de scroll.

La web no cuenta "qué vendemos". Cuenta una transformación: la usuaria entra en un lienzo casi monocromo, sereno y caro, y el color despierta progresivamente con su scroll hasta revelarse como un sistema ordenado: su paleta personal. La página entera es la demostración del producto: si la web te hace *sentir* lo que hace el color bien elegido, el servicio ya está medio vendido.

### A.2 Experiencia sensorial (cómo se siente)

1. **Llegada:** silencio visual. Fondo crudo, tipografía serif enorme, un único halo de color vivo y contenido (el Orbe Cromático). Sensación: galería de arte + laboratorio de luz.
2. **Descenso:** cada pantalla tiene UNA idea (lógica Apple). El color aparece como explosiones controladas: un bloque, una tela, una paleta, nunca caos.
3. **Comprensión:** las cuatro estaciones se despliegan como capítulos editoriales (lógica revista de moda: spreads, fotografía a sangre, pies de foto técnicos).
4. **Confianza:** la dirección experta de Cristina Barriga aparece como una firma editorial, no como un "sobre nosotros" corporativo.
5. **Acción:** el cierre devuelve al silencio inicial, ahora con la paleta "encendida", y un único CTA elegante.

Ritmo: lento, con respiración (espacio negativo ≥ 40% de cada viewport). Nada compite con nada.

### A.3 Paleta cromática de marca (8 colores con rol)

| Nombre | Hex | Rol |
|--------|-----|-----|
| Blanco Editorial | `#FFFFFF` | Neutro principal, lienzo base |
| Crudo Atelier | `#FAF8F5` | Neutro secundario, fondos alternos, calidez de papel |
| Gris Cálido | `#F2F0ED` | Fondos de bloque, separación sutil sin líneas |
| Negro Tinta | `#1A1A1A` | Texto principal y secciones de contraste editorial |
| Oro Suave | `#C4A882` | Acento primario de identidad: CTAs, detalles, filos |
| Oro Profundo | `#8B6F47` | Acento secundario: hovers, texto sobre claros, autoridad |
| Carbón | `#2D2D2D` | Texto secundario, captions, UI |
| Oro Claro | `#E8D5B7` | Fondos de acento, halos, estados suaves |

**Colores estacionales (uso intencional, nunca decorativo):**

| Estación | Hex | Carácter |
|----------|-----|----------|
| Primavera | `#D4A853` | Luz, claridad, calidez, vivacidad |
| Verano | `#8BA7C4` | Suavidad, frío, bruma, empolvado |
| Otoño | `#C4622D` | Profundidad, tierra, riqueza |
| Invierno | `#2D3E5C` | Contraste, frío, intensidad, definición |

Regla de uso: el 90% de la página vive en neutros + oro. Los colores estacionales solo aparecen cuando la narrativa habla de estaciones o paletas: así cada aparición de color tiene significado (es exactamente lo que enseña la colorimetría).

### A.4 Sistema tipográfico

| Uso | Fuente | Pesos | Notas |
|-----|--------|-------|-------|
| Display / titulares grandes | **Cormorant Garamond** (Google Fonts, servida localmente) | 400, 500, itálica 400 | Tracking -0.02em en cuerpos >44px; interlineado 1.05-1.1 |
| Subtítulos editoriales | Cormorant Garamond itálica | 400 | Para frases-manifiesto y citas |
| Cuerpo de texto | **DM Sans** (Google Fonts, local) | 400, 500 | Interlineado 1.6; máx. 68 caracteres por línea |
| Labels / UI / botones | DM Sans | 500, uppercase | Tracking +0.08em, tamaño 12-14px |

Escala (mobile-first, ya definida en tokens de Fase 0/prompt): hero fluido `clamp(3rem, 8vw, 7rem)`, h1 56px, h2 44px, h3 32px, h4 24px, body 16px, lead 18px, caption 12px.

Upgrade futuro opcional (no bloqueante): Freight Display Pro o Canela bajo licencia, sustituyendo solo la display. La arquitectura de variables lo permite cambiando un valor.

### A.5 Elemento firma

**El Orbe Cromático**: un volumen de luz y color vivo —ni esfera de plástico ni "bola 3D de plantilla"— que respira en el hero, reacciona sutilmente al cursor y, con el scroll, se descompone en las cuatro estaciones cromáticas. Es la traducción visual del método: *el color desordenado se convierte en sistema*.

- Aparece a tamaño completo solo en el hero/universo estacional.
- Reaparece en miniatura como motivo de marca: bullet de secciones, loader, favicon animado, firma del CTA final.
- Tiene versión estática (gradiente radial) para fallback, impresión y redes: la firma sobrevive sin WebGL.

### A.6 Referencias visuales usadas y qué se toma de cada una

| Referencia | Qué se toma (lógica, no estética) |
|------------|-----------------------------------|
| Apple Vision Pro / AirPods Pro / iPhone Pro | Scroll-scrubbing cinematográfico; una idea por pantalla; estructura deseo→comprensión→confianza→acción |
| Apple Watch / iPad Pro / MacBook Pro | Módulos visuales que explican sin saturar; mensajes de 5-9 palabras; transiciones de bloque suaves |
| Apple Intelligence | Gradientes vivos sobre lienzo limpio; halos de color como lenguaje de "inteligencia" |
| CHANEL — Les 4 Ombres Boutons | El producto como joya: macrotextura, oro contenido, ritmo lento de lujo |
| Bleu de CHANEL l'Exclusif | Oscuridad elegante para secciones de contraste (Invierno, autoridad) |
| Dolce&Gabbana Beauty Fresh Skin | Piel + luz + color como protagonistas fotográficos; frescura sin infantilizar |
| Urban Jürgensen | Serif editorial de altísimo nivel; artesanía + precisión técnica conviviendo |
| Modern Huntsman | Estructura de revista: spreads, columnas asimétricas, captions técnicos |
| Zoi Ice Tea | Bloques de color saturado con disciplina compositiva; color alegre sin perder elegancia |
| LEA WINERY | Storytelling de origen y método; lujo agrícola trasladable a "lujo cromático" |
| AVATR VISION XPECTRA | WebGL como capa de deseo tecnológico; cámara guiada por scroll |
| 100 Lost Species | Scrollytelling didáctico: el scroll enseña un sistema complejo paso a paso |
| The Missing Element / EchoWave | Partículas y materia digital con sobriedad; transiciones de estado |
| Abhishek Jha Folio '25 / Gen-02 SMSY | Microinteracciones memorables que no penalizan la conversión |
| Silver Pinewood Residences / R-Hotels | Inmobiliario/hotel de lujo: fotografía a sangre + tipografía mínima = percepción de precio alto |

(El análisis sistemático de las 30+ referencias con patrones por categoría es el entregable de la FASE 2.)

---

## B. ARQUITECTURA MODULAR (31 MÓDULOS)

Leyenda — **Mov:** nivel del sistema de movimiento (ver E.16) · **Pr:** prioridad (1 = imprescindible lanzamiento, 2 = lanzamiento deseable, 3 = post-lanzamiento) · Todo el contenido textual de todos los módulos es editable en Elementor; la columna "Código" indica qué sistema visual/JS lo acompaña.

| # | Módulo | Objetivo UX / CRO | Objetivo SEO / GEO | Mov | Código (CSS/JS) | Pr |
|---|--------|-------------------|--------------------|-----|------------------|----|
| 1 | Hero editorial inmersivo | Impacto en <3s; declarar categoría premium; primer CTA suave | H1 con keyword principal; LCP optimizado | 2 (+4 orbe) | `cc-hero.css` · `cc-color-orb.js` | 1 |
| 2 | Manifiesto Código Color | Conexión emocional; tono de marca | Bloque citable por IA (definición aspiracional) | 2 | `cc-manifesto.css` | 1 |
| 3 | El Problema | Identificación ("me pasa a mí"); retención | Long-tail "no sé qué colores me favorecen" | 2 | `cc-editorial.css` | 1 |
| 4 | La Solución | Giro narrativo; deseo | Entidad "análisis cromático personal" | 2 | `cc-editorial.css` | 1 |
| 5 | Qué es Código Color | Comprensión; confianza | **Definición citable nº1** ("Código Color es…"); snippet de párrafo | 1 | `cc-definition.css` | 1 |
| 6 | Diagnóstico cromático | Explicar el servicio central; CTA medio | Keyword "diagnóstico cromático" + "análisis de color" | 2 | `cc-service.css` | 1 |
| 7 | Experiencia interactiva de color | Memorabilidad; tiempo en página | Engagement signals; vocabulario técnico en HTML | 2-3 | `cc-palette-grid.css` · `cc-palette-interactive.js` | 2 |
| 8 | Método Código Color | Confianza por proceso; reducir incertidumbre | Snippet de lista ("pasos del análisis"); HowTo implícito | 2 | `cc-method.css` | 1 |
| 9 | Universo cromático estacional (hub) | Navegación visual de estaciones; asombro | Hub interno de las 4 estaciones; enlaces a satélites futuros | 2 (+4 si orbe se extiende) | `cc-universe.css` | 1 |
| 10 | Primavera | Identificación estacional | Keyword "colorimetría primavera"; enlace a satélite | 2 | `cc-season-card.css` | 1 |
| 11 | Verano | Identificación estacional | Keyword "colorimetría verano" | 2 | `cc-season-card.css` | 1 |
| 12 | Otoño | Identificación estacional | Keyword "colorimetría otoño" | 2 | `cc-season-card.css` | 1 |
| 13 | Invierno | Identificación estacional | Keyword "colorimetría invierno" | 2 | `cc-season-card.css` | 1 |
| 14 | Contraste, temperatura, saturación, luminosidad | Demostrar profundidad técnica | **Definiciones citables** de las 4 dimensiones; snippets | 2 | `cc-dimensions.css` | 1 |
| 15 | Beneficios | Traducir técnica a vida real; deseo | Long-tails de beneficio ("comprar mejor", "verse mejor") | 1-2 | `cc-benefits.css` | 1 |
| 16 | Color aplicado a ropa | Aplicabilidad; deseo | Keyword "paleta de colores ropa" | 2 | `cc-application.css` | 1 |
| 17 | Color aplicado a maquillaje | Aplicabilidad | Keyword "maquillaje según colorimetría" | 2 | `cc-application.css` | 1 |
| 18 | Color aplicado a cabello | Aplicabilidad | Keyword "color de pelo según colorimetría" | 2 | `cc-application.css` | 2 |
| 19 | Color aplicado a imagen profesional | Elevar ticket; audiencia profesional | Entidad "imagen profesional" + "marca personal" | 1 | `cc-application.css` | 2 |
| 20 | Antes y después conceptual | Visualizar la transformación sin inventar casos | Sin riesgo SEO (no claims) | 2 (scrub) | `cc-reveal.css` | 2 |
| 21 | Vídeo cinemático | Inmersión sensorial; percepción premium | Neutro (lazy, sin texto dependiente) | 3 | `cc-video-frame.css` | 2 |
| 22 | Cristina Barriga — dirección experta | Confianza; humanizar; autoridad | **E-E-A-T**; entidad Person; "quién dirige Código Color" | 1-2 | `cc-authority.css` | 1 |
| 23 | Jerarquía profesional y método | Criterio detrás del sistema | Refuerzo E-E-A-T; citabilidad de método | 1 | `cc-authority.css` | 2 |
| 24 | Para quién es | Autoselección; cualificar leads | Long-tails de audiencia ("colorimetría novias", "+40", etc.) | 1 | `cc-for-who.css` | 1 |
| 25 | Formación en colorimetría | Sembrar línea futura; autoridad docente | Keyword "formación colorimetría"; enlace a satélite futuro | 1 | `cc-training.css` | 3 |
| 26 | Cursos de asesoría de imagen | Sembrar línea futura | Keyword "curso asesoría de imagen" | 1 | `cc-training.css` | 3 |
| 27 | 100 FAQs técnicas organizadas | Resolver objeciones; permanencia | **Maquinaria principal GEO/AEO**: 100 unidades citables, PAA, long-tail | 1 | `cc-faq.css` (+ filtro JS opcional) | 1 |
| 28 | CTA principal | Conversión | Neutro | 1 | `cc-cta.css` | 1 |
| 29 | CTA final editorial | Cierre emocional; última conversión | Neutro | 2 | `cc-cta.css` | 1 |
| 30 | Sección de confianza | Credibilidad sin testimonios inventados | Señales de confianza verificables | 1 | `cc-trust.css` | 2 |
| 31 | Enlaces a futuras páginas satélite | Preparar ecosistema | Arquitectura de enlazado interno; flujo de autoridad | 1 | `cc-footer-links.css` | 1 |

### B.1 Asignaciones transversales

- **Vídeo:** módulos 1 (opcional como fallback/ambiente), 20 y 21. Especificación: WebM+MP4, loop, sin audio, `preload="metadata"`, póster optimizado, <4MB.
- **GSAP ScrollTrigger (nivel 2):** módulos 1-4, 6-14, 16-18, 20, 29. Patrón único reutilizable: revelados de texto, parallax suave de imágenes, pin + scrub solo en 1, 9 y 20.
- **Three.js (nivel 4):** SOLO módulo 1 (con extensión opcional al 9). Ver sección E.
- **Lottie/vídeo (nivel 3):** módulos 7 (microanimaciones de paleta exportadas) y 21.
- **100% editable sin código (contenido):** los 31 módulos. Sin excepciones: el JS y el CSS nunca contienen textos, precios ni imágenes.

---

## C. ESTRATEGIA SEO / GEO / AEO

### C.1 Entidad principal

- **Nombre:** Código Color
- **Tipo:** Organización / Marca (schema `Organization`, valorar `ProfessionalService` con datos locales confirmados)
- **Definición canónica (borrador citable, se pule en Fase 4):** "Código Color es un método de análisis de colorimetría personal y asesoría de imagen, dirigido por Cristina Barriga, que identifica mediante diagnóstico aplicado (subtono, contraste, intensidad y armonía) los colores que favorecen a cada persona en ropa, maquillaje y cabello."
- **Atributos:** método propio · diagnóstico aplicado al rostro real · colorimetría avanzada · visagismo · Madrid + online · dirección experta identificable · premium.
- **Relaciones:** `founder/director` → Cristina Barriga (Person) · `knowsAbout` → colorimetría, armocromía, análisis cromático, visagismo, asesoría de imagen · `areaServed` → Madrid, España (+ online) · `makesOffer` → diagnóstico cromático, packs, formación futura.

### C.2 Entidades secundarias (mapa)

| Entidad | Tipo | Relación con la principal |
|---------|------|---------------------------|
| Cristina Barriga | Person | Directora, autora del método, voz experta (E-E-A-T) |
| Colorimetría | Concepto | Campo principal de conocimiento |
| Análisis cromático personal | Servicio/Concepto | Servicio central |
| Armocromía | Concepto | Sinónimo/variante (puente con tendencia italiana/coreana) |
| Subtono, contraste, saturación, luminosidad, temperatura | Conceptos técnicos | Dimensiones del método |
| Estaciones cromáticas (primavera, verano, otoño, invierno + 16 subtipos) | Taxonomía | Sistema de clasificación |
| Drapeado / test de telas | Técnica | Procedimiento del diagnóstico |
| Visagismo | Concepto | Campo complementario diferenciador |
| Asesoría de imagen | Concepto | Campo complementario |
| Madrid / España | Lugar | Ámbito local de servicio |
| Formación en colorimetría / cursos | Servicio futuro | Línea estratégica |

### C.3 Clústeres temáticos (hub & spoke)

```
HUB CENTRAL: / (landing Código Color)
│
├── Clúster COLORIMETRÍA ········· /colorimetria-madrid/ (página de venta) + blog "qué colores me favorecen", "test colorimetría"
├── Clúster ESTACIONES ··········· /estaciones/ → 4 estaciones → 16 subtipos (fase 2 de contenido)
├── Clúster ANÁLISIS DE COLOR ···· método, comparativas (4 vs 12 vs 16 estaciones, presencial vs online, humano vs IA)
├── Clúster IMAGEN PERSONAL ······ ropa / maquillaje / cabello / marca personal por paleta
├── Clúster FORMACIÓN ············ /formacion-colorimetria/ + cursos (futuro)
├── Clúster ARMOCROMÍA ··········· puente de tendencia (TikTok, Corea, Italia) → redirige autoridad al método propio
└── Clúster AUTORIDAD ············ /cristina-barriga/ + /metodo-codigo-color/
```

### C.4 Arquitectura semántica (macro → meso → micro)

- **Macro:** colorimetría / análisis de color personal
- **Meso:** estaciones cromáticas · dimensiones del color (subtono, contraste, saturación, luminosidad) · aplicaciones (ropa, maquillaje, cabello, imagen profesional) · método y experiencia · formación
- **Micro:** cada FAQ, cada subtipo estacional, cada comparativa, cada término de glosario
- **Vocabulario nuclear preferente:** colorimetría, análisis cromático personal, paleta personal, subtono, estación cromática, diagnóstico cromático, Código Color, Cristina Barriga.
- **Variantes que deben aparecer de forma natural:** armocromía, análisis de color, test de color(imetría), estudio de color, qué colores me favorecen, asesoría de imagen, armonía cromática.

### C.5 Enlazado interno (flujo de autoridad)

- La landing es el hub: enlaza con anchor descriptivo a cada satélite futuro desde su módulo correspondiente (módulo 9→estaciones, 6→/colorimetria-madrid/, 22→/cristina-barriga/, 25-26→formación, 27→FAQs específicas de satélites).
- Cada satélite devuelve 1 enlace al hub + 2-3 enlaces laterales dentro de su clúster. Nunca enlaces masivos de footer como sustituto de enlazado editorial.
- Anchors recomendados (ejemplos): "análisis de colorimetría en Madrid", "estación cromática invierno", "método Código Color de Cristina Barriga", "qué es el subtono de la piel".
- Fuente de verdad: `seo/internal-linking-map.md` (se inaugura en Fase 4).

### C.6 Taxonomía futura

| Taxonomía | Valores |
|-----------|---------|
| Estación | primavera, verano, otoño, invierno (+16 subtipos: clara, suave, profunda, brillante…) |
| Subtono | cálido, frío, neutro, oliva |
| Contraste | alto, medio, bajo |
| Servicio | diagnóstico, color+imagen, transformación completa, experience, formación |
| Audiencia | mujeres profesionales, novias, +40, profesionales de la imagen, alumnas |
| Geografía | Madrid, online, (futuras ciudades) |
| Nivel de conocimiento | divulgación, práctico, técnico/profesional |

### C.7 Sistema de 100 FAQs — categorías para la landing (propuesta Fase 1)

Se adopta la estructura de 11 categorías del prompt maestro:

1. Fundamentos de la colorimetría (12) · 2. El análisis cromático: proceso y método (12) · 3. Estaciones y subtonos (12) · 4. Aplicada a ropa (10) · 5. Aplicada a maquillaje (10) · 6. Aplicada a cabello (8) · 7. Colorimetría vs armocromía vs otros métodos (8) · 8. La experiencia Código Color: reservas, sesión, resultados (10) · 9. Dirección experta y método de Cristina Barriga (8) · 10. Formación y cursos (6) · 11. Errores comunes y mitos (4).

**Criterio de asignación pregunta-URL para el ecosistema:** una pregunta = una URL (banco maestro `seo/faq-bank.md` con IDs `FAQ-0001…`); la landing responde lo general, los satélites lo específico; toda FAQ nueva se verifica contra el banco antes de publicarse. Redacción según anatomía: respuesta directa 40-60 palabras + expansión + microenlace.

### C.8 Schema markup recomendado

- `Organization` (Código Color) con `founder` → `Person`
- `Person` (Cristina Barriga) con `jobTitle`, `knowsAbout`, `sameAs` (pendiente de datos confirmados, ver D)
- `WebSite` + `BreadcrumbList`
- `Service` (Diagnóstico cromático / packs)
- `FAQPage` (selección priorizada de las 100; valor GEO aunque Google no muestre rich result)
- `LocalBusiness`/`ProfessionalService` solo cuando se confirmen dirección y datos locales
- Futuro: `Course` (formación), `Article` (blog)

### C.9 GEO / AEO / citabilidad por IA

- **Bloques citables marcados** (se redactan en Fase 4): definición de Código Color (módulo 5), definición de colorimetría, las 4 dimensiones (módulo 14), las 4 estaciones (9-13), el método paso a paso (8), quién dirige Código Color (22), cada una de las 100 FAQs.
- **Formato de extracción:** lenguaje definitorio ("X es…", "X consiste en…"), respuesta completa en los primeros 100 caracteres de cada sección, entidades con nombre completo (nunca "ella", "nuestro centro"), datos verificables, sin claims.
- **Featured snippets objetivo:** párrafo (definiciones), lista (método, pasos, "cómo saber qué colores me favorecen"), tabla (comparativa estaciones, cálido vs frío).
- **Preguntas que la página debe responder mejor que nadie en español:** las 14 del prompt maestro (qué es la colorimetría, qué es el análisis cromático personal, para qué sirve, cómo saber qué colores me favorecen, qué es la armocromía, cuáles son las estaciones, relación con asesoría de imagen, aplicación a ropa/maquillaje/cabello, qué se aprende en la formación, quién dirige Código Color, quién está detrás del método, por qué la dirección de Cristina Barriga aporta criterio, por qué la colorimetría mejora la imagen) — cada una tiene módulo asignado y formato de respuesta directa.
- **llms.txt** en la raíz del dominio: se redacta en Fase 4 con la definición canónica, entidades y URLs clave.

### C.10 Contenidos satélite futuros (plan de expansión, orden recomendado)

1. `/colorimetria-madrid/` (la página que vende — primera satélite tras la landing)
2. `/cristina-barriga/` (autoridad) y `/metodo-codigo-color/`
3. `/servicios/` con los 4 packs
4. 4 páginas de estaciones → después 16 subtipos
5. `/asesoria-de-imagen/` (SEO genérico) · 6. Blog (qué colores me favorecen, test, estaciones) · 7. Glosario 50+ términos · 8. Comparativas · 9. Formación/cursos · 10. Locales adicionales · 11. Lead magnets y test interactivo.

---

## D. JERARQUÍA EXPERTA — CRISTINA BARRIGA

### D.1 Papel como entidad de autoridad

Cristina Barriga es la **prueba de criterio** del método: Google y los LLMs deben entender que Código Color no es una web anónima de colorimetría sino un método con directora identificable. Se integra como: entidad `Person` enlazada por `founder/director` desde `Organization`; firma editorial en módulos 22-23; voz de las FAQs de categoría 9; futura página propia `/cristina-barriga/` y autora del blog y la formación.

### D.2 Representación visual (sin romper la estética)

- **Módulo 22** como *spread* editorial de revista: retrato fotográfico grande de dirección de arte (luz natural, fondo neutro, sin atrezo de "clínica"), titular serif con su nombre, claim de dirección ("Dirigido por Cristina Barriga"), 2-3 párrafos de visión del método y una cita en itálica Cormorant como pieza central.
- **Módulo 23**: "criterio experto" en formato columnas editoriales (cómo se supervisa cada diagnóstico, por qué hay método).
- Nunca: bio en tarjeta corporativa, iconos de LinkedIn azules, sello de "equipo médico".

### D.3 Señales E-E-A-T a construir

Nombre completo y consistente en toda la web · schema Person con `sameAs` hacia perfiles reales · autoría visible de método y FAQs técnicas · página propia enlazada desde el hub · contenido técnico que solo una experta puede firmar (categoría 7 de tipos de FAQ) · coherencia entidad-marca en Google Business Profile si existe.

### D.4 ⚠️ Información pendiente que DEBO recibir antes de redactar su sección (Fase 4)

> No se redactará la sección definitiva de Cristina Barriga sin estas confirmaciones. No se inventará nada.

1. Formación y titulaciones **confirmables** que se pueden citar
2. Años de experiencia y trayectoria profesional real (¿qué se puede contar públicamente?)
3. Relación pública con el INM: ¿se menciona como trayectoria personal o se omite por completo? (la marca es independiente; su biografía personal puede o no citarlo — decisión del cliente)
4. Perfiles para `sameAs`: Instagram, LinkedIn, otros (URLs exactas)
5. ¿Existe retrato fotográfico editorial de calidad o hay que producirlo?
6. Una frase de visión del método dicha por ella (o entrevista breve para extraerla)
7. Ciudad/modalidad de trabajo confirmada (¿Madrid presencial + online?)
8. Apariciones en medios, docencia o reconocimientos **reales y verificables**, si los hay

---

## E. ESTRATEGIA THREE.JS, WEBGL Y MOVIMIENTO PREMIUM

### E.1 ¿Recomiendo usar Three.js?

**Sí, con alcance quirúrgico y por fases.** Una única escena: el **Orbe Cromático** (elemento firma, A.5), implementada como *mejora progresiva*:

- **V1 (lanzamiento):** la página se lanza completa y premium con CSS + GSAP + gradientes animados; el hero usa la versión "halo de gradiente" del orbe (CSS/canvas 2D ligero). Cero dependencia de Three.js para lanzar.
- **V1.5 (2-4 semanas después):** se activa el módulo `cc-color-orb.js` (Three.js) sobre el mismo contenedor. Si rinde bien, se queda; si no, se desactiva con un atributo y nadie lo nota.

Esto cumple el criterio del prompt: tecnología al servicio de marca y conversión, nunca un bloqueo de lanzamiento.

### E.2 ¿En qué módulo exacto?

**Módulo 1 (Hero)**, con extensión opcional al **módulo 9 (Universo estacional)** en una sola escena persistente: el orbe del hero, al hacer scroll, viaja/se divide en los 4 halos estacionales. La extensión al módulo 9 solo se aborda si la métrica de rendimiento del hero lo permite. En ningún otro módulo habrá WebGL.

### E.3 ¿Qué experiencia visual?

Un volumen de luz esférico con shader de gradiente fluido (ruido orgánico lento, colores de la paleta de marca), borde fresnel sutil y bloom muy contenido, sobre el lienzo crudo. Interacciones: respira en idle; parallax mínimo con el cursor (desktop); con el scroll (scrub) se desplaza, cambia de temperatura de color y —en la versión extendida— se separa en cuatro halos que adoptan los hex estacionales y se posan junto a cada tarjeta de estación. Estética: lujo tecnológico tipo Apple Intelligence; prohibido cualquier acabado "gaming/metaverso".

### E.4 Integración con Elementor

El módulo 1 es un contenedor Elementor normal con H1, subtítulo y CTA como widgets editables. Dentro, un contenedor vacío con clase `cc-color-orb` y atributos de datos (`data-cc-orb="on"`, `data-cc-orb-colors="#C4A882,#D4A853,#8BA7C4,#C4622D,#2D3E5C"`). El JS inyecta el `<canvas>` detrás del contenido (z-index inferior). Resultado: el equipo edita textos y CTAs sin saber que existe Three.js, cambia los colores del orbe editando el atributo en Elementor, y lo apaga poniendo `data-cc-orb="off"`.

### E.5 Integración con GSAP ScrollTrigger

GSAP es la **única fuente de verdad del progreso de scroll**. Un timeline con `ScrollTrigger` (pin del hero + `scrub: true`) anima un objeto proxy `{progress: 0→1}`; en cada tick, el módulo Three.js lee ese progreso y actualiza uniforms del shader, posición de cámara y mezcla de colores. Three.js nunca escucha el scroll directamente: así una sola lógica gobierna textos (GSAP puro) y escena (Three.js), quedan sincronizados al frame y desactivar la escena no rompe el resto del timeline.

### E.6 Qué contenido queda editable (Elementor)

Todo el contenido real: H1, subtítulo, CTAs, textos de estaciones, imágenes, y los **colores del orbe** vía data-attribute. También el interruptor on/off.

### E.7 Qué queda en código (GitHub)

`cc-color-orb.js` (escena, shaders, geometría, materiales, timings, cámara), `cc-fallbacks.js` (detección WebGL/`prefers-reduced-motion`/dispositivo), `cc-motion-config.js` (constantes de movimiento), CSS del contenedor y del fallback.

### E.8 Fallback

Triple capa, automática: (1) sin WebGL o GPU débil → **gradiente CSS animado** (mismos colores, `background` animado con `@keyframes`, coste ~0); (2) `prefers-reduced-motion` → **versión estática** del halo (imagen/gradiente fijo); (3) error de carga del módulo → el contenedor conserva el gradiente CSS que ya estaba pintado debajo (el canvas solo se superpone cuando está listo: nunca hay hueco en blanco).

### E.9 Impacto en SEO

**Neutro si se respeta el diseño:** H1, textos y CTAs viven en HTML renderizado por Elementor; el canvas es decorativo (`aria-hidden="true"`). El LCP del hero será el H1 o la imagen de fondo, no el canvas (Three.js carga *después* del evento de LCP, diferido por IntersectionObserver + `requestIdleCallback`). Riesgo vigilado: INP en móviles débiles → mitigado con cap de DPR y detección de gama.

### E.10 Impacto en GEO

**Neutro-positivo.** Nada citable depende del canvas; los LLMs leen el HTML completo. Positivo indirecto: la memorabilidad de marca genera búsquedas de marca y menciones, señales que los motores generativos ponderan.

### E.11 Impacto en rendimiento (presupuesto)

| Métrica | Presupuesto |
|---------|-------------|
| JS adicional total (three.module + escena, min+gzip) | ≤ 180 KB, carga diferida post-LCP |
| LCP | < 2,5 s (sin cambio: el orbe no participa en LCP) |
| CLS | 0 aportado (canvas absolutamente posicionado sobre fallback ya pintado) |
| INP | < 200 ms (render loop pausado fuera de viewport vía IntersectionObserver) |
| FPS | 60 desktop / aceptar 30 estables en móvil medio; DPR cap 1,75 |
| Móvil | Geometría reducida, sin postprocesado, sin sombras; gama baja → fallback CSS directo |

Si tras medir en dispositivo real el hero no cumple, el orbe Three.js no se publica (queda el gradiente, que ya es premium).

### E.12 Impacto en mantenimiento

Bajo por diseño: un solo archivo de escena + un archivo de configuración; colores editables desde Elementor; interruptor on/off sin deploy; documentación obligatoria en `docs/MANTENIMIENTO.md` (qué archivo controla la escena, qué parámetros se cambian, cómo se desactiva, qué fallback aparece, flujo GitHub→SiteGround y purga Cloudflare según Fase 0). Riesgo real: dependencia de un perfil creative-dev para evoluciones de la escena → mitigado porque la web nunca depende de ella (E.1).

### E.13 Alternativa si Three.js no compensa

**Vídeo en loop renderizado offline (WebM+MP4, <3 MB) del mismo orbe + GSAP para el resto.** Da el 85-90% del impacto visual con coste técnico mínimo y cero riesgo de rendimiento JS; pierde la reactividad al cursor y el scrub fino. Segunda alternativa: canvas 2D con gradientes (sin librería). **Spline: descartado** para esta pieza (runtime pesado ~1MB+, menos control de shaders y de carga diferida, dependencia de plataforma); solo se reconsideraría para una pieza 3D secundaria editable por diseño. **Lottie: descartado** para el orbe (vectorial, no da volumen lumínico), válido para microanimaciones del módulo 7.

### E.14 Presupuesto técnico en complejidad

- Orbe hero solo (V1.5): **MEDIO**
- Orbe + transición a 4 estaciones con scroll-scrub (módulo 9): **ALTO**
- Resto del sistema de movimiento (GSAP + CSS): **BAJO-MEDIO**

### E.15 Qué debe hacer primero un desarrollador creative front-end

1. **Prototipo aislado** (HTML estático, fuera de WordPress) del orbe con shader de gradiente + GSAP ScrollTrigger scrub, con los hex de marca.
2. **Medir en dispositivos reales** (iPhone medio, Android de gama media): FPS, INP, batería, peso total.
3. Implementar **fallbacks primero** (gradiente CSS + reduced-motion): el fallback es el producto base, el orbe es la mejora.
4. Empaquetar como módulo `cc-color-orb.js` con la interfaz de data-attributes de E.4 y entregarlo con su documentación.
5. Solo entonces, integración en staging de WordPress y prueba con Elementor + cachés (Fase 0).

### E.16 Sistema de movimiento completo (niveles 1-5 por módulo)

| Nivel | Tecnología | Módulos | Uso |
|-------|-----------|---------|-----|
| 1 — CSS | transitions/keyframes | 5, 15, 19, 22-28, 30, 31 + todos los hovers | Microinteracciones, hover de CTAs y tarjetas, sombras, gradientes sutiles |
| 2 — GSAP ScrollTrigger | gsap + ScrollTrigger | 1-4, 6-14, 16-18, 20, 29 | Revelados de texto, parallax suave, pin+scrub en 1/9/20, aparición progresiva de paletas |
| 3 — Lottie / vídeo | lottie-web (solo si se usa) / `<video>` | 7, 21 | Microanimaciones de paleta exportadas; vídeo cinemático en loop |
| 4 — Three.js | three (module) | 1 (+9 opcional) | Orbe Cromático — única pieza WebGL |
| 5 — Spline | — | Ninguno | Descartado en esta fase (peso del runtime, menor control); reevaluable para piezas secundarias futuras |

Reglas globales: toda animación respeta `prefers-reduced-motion`; nada anima propiedades de layout (solo `transform`/`opacity`); ScrollTrigger se inicializa una vez y por `data-cc-module`; sin animación, la página debe seguir siendo perfectamente legible y bella.

---

## F. ANÁLISIS DE RIESGOS

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|:---:|:---:|------------|
| **Técnico:** actualización de Elementor rompe clases/estructura | Media | Medio | Clases propias `cc-*` (no IDs internos); staging antes de actualizar; child theme aislado |
| **Técnico:** conflicto minificación SiteGround con GSAP/Three | Media | Alto | Exclusión de `cc-*.js` ya definida en Fase 0; Rocket Loader OFF |
| **Rendimiento:** hero pesado degrada LCP/INP móvil | Media | Alto | Presupuesto E.11; orbe diferido post-LCP; fallback por gama de dispositivo; lanzar V1 sin Three.js |
| **SEO:** canibalización entre landing y satélites (sobre todo FAQs) | Alta sin protocolo | Alto | Banco maestro `faq-bank.md`, una pregunta = una URL; satélites más específicos que el hub |
| **SEO:** thin content en satélites tempranas | Media | Medio | No publicar satélites sin sus 100 FAQs propias y contenido editorial completo |
| **GEO:** cambios de algoritmo/criterios de citación de los LLMs | Alta (continua) | Medio | Apostar por fundamentos estables: definiciones autocontenidas, entidades claras, HTML real; revisar trimestralmente |
| **Autoridad:** sección de Cristina Barriga genérica o sin datos confirmados | Media | Alto | Lista D.4 obligatoria antes de Fase 4; sin datos confirmados no se publica el módulo 22 definitivo |
| **Autoridad:** mezcla de identidades con INM | Baja | Crítico | Restricción absoluta del prompt; revisión de copy en Fase 4 contra la regla |
| **Mantenimiento:** dependencia de creative-dev para la pieza WebGL | Media | Medio | La web nunca depende del orbe (E.1); interruptor off sin deploy; documentación E.12 |
| **CRO:** la espectacularidad entierra los CTAs | Media | Alto | Un CTA visible por viewport clave; wireframe de Fase 3 valida el camino de conversión antes de diseñar |

---

## G. RECOMENDACIÓN DE IMPLEMENTACIÓN

### G.1 Stack

- **Tema:** Hello Elementor + child theme `codigo-color-child` (Fase 0)
- **Constructor:** Elementor Pro 3.20+
- **SEO:** Rank Math (gestión de meta, breadcrumbs; el schema crítico va en PHP versionado para control total)
- **Caché:** SiteGround Speed Optimizer (único)
- **Imágenes:** ShortPixel o Imagify + WebP
- **Fuentes:** Cormorant Garamond + DM Sans servidas localmente
- **JS:** GSAP + ScrollTrigger (local, versionado en repo); Three.js solo como módulo del orbe (V1.5)
- **Evitar:** plugins de animación, addons de Elementor de terceros, page builders adicionales

### G.2 Orden de implementación

1. **Fundación:** tokens (`cc-variables.css`), tipografía, Global Colors/Fonts de Elementor → 2. **Esqueleto de conversión:** módulos 1 (sin orbe), 5, 6, 8, 28 → 3. **Narrativa:** 2, 3, 4, 9-14, 15 → 4. **Aplicaciones y autoridad:** 16-18, 22, 24 → 5. **FAQs (módulo 27) + schema** → 6. **Cierre:** 29, 30, 31, 20-21 → 7. **Movimiento nivel 2 (GSAP)** sobre lo construido → 8. **Lanzamiento V1** → 9. **V1.5:** orbe Three.js → 10. **Post:** 7 interactivo, 19, 23, 25-26.

### G.3 Complejidad estimada por bloque

| Bloque | Complejidad |
|--------|-------------|
| Tokens + tipografía + Elementor global | Baja |
| Módulos editoriales (2-6, 8, 10-19, 22-31) | Baja-Media |
| FAQs 100 + schema | Media (volumen, no dificultad) |
| GSAP nivel 2 transversal | Media |
| Hero con scrub + pin | Media-Alta |
| Orbe Three.js (V1.5) | Alta |

### G.4 Quick wins vs trabajo profundo

- **Quick wins (semana 1-2):** sistema de tokens, hero V1 con gradiente premium, módulo 5 citable, módulo 8 método, CTA principal, schema Organization+Person básico.
- **Trabajo profundo:** las 100 FAQs bien minadas y redactadas (el mayor ROI SEO/GEO de todo el proyecto), la narrativa estacional 9-14, y el orbe.

---

## CIERRE DE FASE 1 — QUÉ NECESITO DEL CLIENTE

1. **Aprobación explícita de esta Fase 1** (o ajustes módulo a módulo).
2. **Las 8 respuestas sobre Cristina Barriga** (D.4) — pueden llegar durante las Fases 2-3, pero son bloqueantes para la Fase 4.
3. Confirmación de la decisión Three.js por fases (V1 sin orbe, V1.5 con orbe) — o instrucción de cambiarla.

**Siguiente fase tras aprobación:** FASE 2 — Benchmark visual sistemático de las 30+ referencias (Apple + Awwwards) con patrones de hero, scroll, tipografía, color, movimiento, conversión y autoridad, y su traducción concreta a Código Color.
