# 06 — CÓDIGO (PLAN DE IMPLEMENTACIÓN)
## Código Color · Arquitectura del child theme, módulos CSS/JS, Orbe Three.js, schema PHP y orden de construcción

> **Estado:** Plan entregado, pendiente de aprobación del cliente. **Este documento aún no genera código de producción**: especifica qué se va a escribir, en qué archivo, con qué interfaz y en qué orden. La generación del tema se hace tras aprobar este plan.
> **Regla del código (Fase 0/Prompt):** prefijo `cc-` en todo; módulos independientes; CSS y JS separados; nada de contenido (textos/precios/imágenes) en el código; documentar dónde pega cada cosa; un módulo cada vez; no bloquear contenido SEO en JS.
> **Depende de:** FASE 0 (arquitectura D, despliegue, cachés), FASE 1 (módulos, movimiento, Orbe, presupuestos), FASE 3 (wireframe), FASE 4 (copy, schema, precios), FASE 5 (clases `cc-*`, frontera) y documento 08 (imágenes).
> **Rol asumido:** Arquitecto WordPress + Creative front-end (GSAP/Three.js) + Arquitecto SEO técnico.

---

## ÍNDICE

- **A.** Alcance y reglas del código
- **B.** Estructura del child theme (árbol de archivos)
- **C.** Capa PHP (`functions.php`, encolado condicional, schema)
- **D.** Capa CSS (`cc-*.css`: tokens + módulos)
- **E.** Capa JS (`cc-*.js`: módulos y fallbacks)
- **F.** El Orbe Cromático (especificación técnica)
- **G.** Schema JSON-LD en PHP (interfaz)
- **H.** Encolado condicional y presupuesto de rendimiento
- **I.** Frontera con Elementor (recordatorio operativo)
- **J.** Orden de implementación (sprints)
- **K.** Pruebas y criterios de aceptación
- **L.** Despliegue (enlace con Fase 0/7)
- **M.** Checklist y entregables para Fase 7

---

## A. ALCANCE Y REGLAS DEL CÓDIGO

### A.1 Qué se construye en Fase 6

1. **Child theme `codigo-color-child`** sobre Hello Elementor: `style.css` (cabecera), `functions.php`, assets.
2. **Sistema CSS `cc-*.css`**: tokens (variables) + un archivo por módulo (clases aplicadas en Elementor en Fase 5).
3. **Sistema JS `cc-*.js`**: Orbe Three.js, animaciones GSAP ScrollTrigger, interacción de paleta, filtro de FAQs, fallbacks y configuración de movimiento.
4. **Schema JSON-LD en PHP**: Organization, Person, Service (`OfferCatalog`), WebSite, BreadcrumbList, FAQPage (13 priorizadas).
5. **Fuentes locales**: Cormorant Garamond + DM Sans servidas desde el tema.
6. **`llms.txt`** desplegado en la raíz del dominio (artefacto Fase 4, ya redactado).

### A.2 Qué NO se construye aquí

- Contenido (vive en Elementor/BD).
- Plugins de terceros (solo se configuran: Elementor Pro, Rank Math, SG Optimizer — Fase 0).
- Nada que impida editar en Elementor.

### A.3 Principios no negociables (Fase 0/1)

- **Mejora progresiva:** la web se lanza completa y premium **sin** Three.js (V1); el Orbe Three.js se activa en V1.5 sobre el mismo contenedor. El fallback **es** el producto base.
- **SEO intacto:** ningún texto/FAQ/entidad depende de JS; todo en HTML real (Elementor). El canvas es decorativo (`aria-hidden`).
- **Presupuesto de rendimiento** (H) es un límite, no una aspiración.
- **`prefers-reduced-motion`** respetado en todo; animar solo `transform`/`opacity`.

---

## B. ESTRUCTURA DEL CHILD THEME (árbol propuesto)

```
codigo-color-child/
├── style.css                      # Cabecera del tema (solo metadatos), nada más
├── functions.php                  # Orquestador: encola assets, registra fuentes, inyecta schema
├── screenshot.png
├── inc/
│   ├── enqueue.php                # Encolado condicional por página (CSS/JS)
│   ├── fonts.php                  # Registro de fuentes locales
│   ├── schema.php                 # Salida JSON-LD (Organization, Person, Service, …)
│   └── helpers.php                # Detección de página/plantilla, utilidades
├── assets/
│   ├── css/
│   │   ├── cc-tokens.css          # Variables: paleta, tipografía, espaciado, motion
│   │   ├── cc-base.css            # Reset suave, tipografía base, utilidades cc-*
│   │   ├── cc-hero.css
│   │   ├── cc-manifesto.css
│   │   ├── cc-editorial.css       # mods 3-4
│   │   ├── cc-definition.css      # mod 5
│   │   ├── cc-service.css         # mod 6
│   │   ├── cc-palette-grid.css    # mod 7
│   │   ├── cc-method.css          # mod 8
│   │   ├── cc-universe.css        # mod 9
│   │   ├── cc-season-card.css     # mods 10-13
│   │   ├── cc-dimensions.css      # mod 14
│   │   ├── cc-benefits.css        # mod 15
│   │   ├── cc-application.css     # mods 16-19
│   │   ├── cc-reveal.css          # mod 20
│   │   ├── cc-video-frame.css     # mod 21
│   │   ├── cc-authority.css       # mods 22-23
│   │   ├── cc-for-who.css         # mod 24
│   │   ├── cc-pricing.css         # mod S (precios)
│   │   ├── cc-training.css        # mods 25-26
│   │   ├── cc-faq.css             # mod 27
│   │   ├── cc-cta.css             # mods 28-29
│   │   ├── cc-trust.css           # mod 30
│   │   └── cc-footer-links.css    # mod 31
│   ├── js/
│   │   ├── cc-motion-config.js    # Constantes de movimiento (durations, easings, flags)
│   │   ├── cc-fallbacks.js        # Detección WebGL / reduced-motion / gama de dispositivo
│   │   ├── cc-scroll-animations.js# GSAP ScrollTrigger (revelados, parallax, scrub, pin)
│   │   ├── cc-color-orb.js        # Three.js: escena del Orbe (carga diferida)
│   │   ├── cc-palette-interactive.js # mod 7
│   │   └── cc-faq-filter.js       # mod 27 (filtro sobre HTML presente)
│   ├── fonts/                     # Cormorant Garamond + DM Sans (woff2 subset)
│   └── vendor/
│       ├── gsap.min.js            # GSAP + ScrollTrigger (local, versión fijada)
│       └── three.module.js        # Three.js (local, solo se carga donde hay Orbe)
├── templates/
│   └── elementor/                 # Export JSON de plantillas (respaldo, Fase 5 N)
└── docs/
    └── MANTENIMIENTO.md           # Guía no técnica (qué archivo controla qué, on/off, purga)
```

> El repo web contiene **derivados** (CSS/JS/fuentes optimizados). Los másters RAW de imagen viven fuera (doc 08 B.5). Lo que NO entra: uploads, wp-config, BD (Fase 0 `.gitignore`).

---

## C. CAPA PHP

### C.1 `functions.php` (orquestador, 3 responsabilidades — Fase 1 A.3)

1. Encolar el CSS versionado.
2. Encolar el JS modular **condicionalmente por página**.
3. Inyectar el schema JSON-LD.

No contiene lógica de presentación ni contenido. Delega en `inc/`.

### C.2 `inc/enqueue.php` (encolado condicional — patrón ilustrativo)

```php
// ILUSTRATIVO — no es el código final
function cc_assets() {
  $v = '1.0.0'; // cache busting (Fase 0); en build real, hash del archivo
  // Base siempre
  wp_enqueue_style('cc-tokens', CC_URI.'/assets/css/cc-tokens.css', [], $v);
  wp_enqueue_style('cc-base',   CC_URI.'/assets/css/cc-base.css', ['cc-tokens'], $v);

  if ( is_front_page() ) {
    foreach (['hero','manifesto','editorial','definition','service','palette-grid',
              'method','universe','season-card','dimensions','benefits','application',
              'reveal','video-frame','authority','for-who','pricing','training',
              'faq','cta','trust','footer-links'] as $m) {
      wp_enqueue_style("cc-$m", CC_URI."/assets/css/cc-$m.css", ['cc-base'], $v);
    }
    // JS diferido, post-LCP
    wp_enqueue_script('cc-motion-config', CC_URI.'/assets/js/cc-motion-config.js', [], $v, true);
    wp_enqueue_script('cc-fallbacks',     CC_URI.'/assets/js/cc-fallbacks.js', [], $v, true);
    wp_enqueue_script('cc-gsap',          CC_URI.'/assets/vendor/gsap.min.js', [], $v, true);
    wp_enqueue_script('cc-scroll',        CC_URI.'/assets/js/cc-scroll-animations.js', ['cc-gsap'], $v, true);
    // three + orbe se cargan dinámicamente por IntersectionObserver dentro de cc-scroll (no aquí)
  }
}
add_action('wp_enqueue_scripts', 'cc_assets');
```

- **Cache busting:** versión por hash del archivo (Fase 0); cambia el query string al desplegar para invalidar Cloudflare/SiteGround.
- **`defer`/footer:** todo el JS al final, sin bloquear el render. El LCP (H1 del hero) no depende de JS.
- **Exclusiones de minificación:** `cc-*.js`, GSAP y Three se excluyen de la minificación de SiteGround/Cloudflare Rocket Loader OFF (Fase 0, riesgo conocido).

### C.3 `inc/fonts.php`

Registra `@font-face` de Cormorant Garamond (400, 500, ital) y DM Sans (400, 500) en woff2 **subset** (latín + signos usados), con `font-display: swap`. Preload de las 2 fuentes críticas del above-the-fold (Cormorant 500, DM Sans 400).

### C.4 `inc/schema.php`

Imprime el `<script type="application/ld+json">` en `wp_head` con el `@graph` de Fase 4 §E (datos ya confirmados: dominio `www.codigocolor.es`, `sameAs` con LinkedIn y Amazon, `OfferCatalog` con los 3 precios). Ver G.

---

## D. CAPA CSS

### D.1 `cc-tokens.css` (fuente única de verdad del sistema visual)

Variables CSS con la paleta (Fase 1 / Fase 5 B), tipografía (presets fluidos `clamp`), espaciado, radios, sombras y constantes de motion. Ejemplo ilustrativo:

```css
:root{
  /* Paleta */
  --cc-blanco:#FFFFFF; --cc-crudo:#FAF8F5; --cc-gris:#F2F0ED;
  --cc-tinta:#1A1A1A; --cc-carbon:#2D2D2D;
  --cc-oro:#C4A882; --cc-oro-prof:#8B6F47; --cc-oro-claro:#E8D5B7;
  --cc-primavera:#D4A853; --cc-verano:#8BA7C4; --cc-otono:#C4622D; --cc-invierno:#2D3E5C;
  /* Tipografía */
  --cc-font-display:"Cormorant Garamond",serif; --cc-font-text:"DM Sans",sans-serif;
  --cc-hero:clamp(3rem,8vw,7rem);
  /* Espaciado */
  --cc-section-y:clamp(80px,12vh,200px); --cc-section-x:clamp(20px,6vw,120px);
  /* Motion */
  --cc-ease:cubic-bezier(.22,.61,.36,1); --cc-dur:.6s;
}
@media (prefers-reduced-motion:reduce){ :root{ --cc-dur:0s; } }
```

### D.2 Un archivo por módulo

Cada `cc-<modulo>.css` define **solo** lo que hacen las clases aplicadas en Elementor (Fase 5 F). Reglas:
- Nada de `!important` salvo para neutralizar un estilo de Elementor concreto y documentado.
- Animar solo `transform`/`opacity`; nada que provoque reflow.
- Mobile-first: estilos base = mobile, `min-width` para escalar.
- `cc-pricing.css` incluye el estado `--featured` (Signature) y el grid responsive (Fase 5 H).
- `cc-faq.css` estiliza el acordeón para que parezca editorial (no footer de soporte).

---

## E. CAPA JS

| Archivo | Responsabilidad | Notas |
|---------|-----------------|-------|
| `cc-motion-config.js` | Constantes: durations, easings, flags por módulo, breakpoints JS | Sin dependencias |
| `cc-fallbacks.js` | Detección de WebGL, `prefers-reduced-motion`, gama de dispositivo (DPR, memoria), decide nivel de experiencia | Devuelve un objeto de capacidades que el resto consume |
| `cc-scroll-animations.js` | GSAP ScrollTrigger: revelados de texto, parallax, pin+scrub (mods 1, 9, 20), línea de progreso (mod 8). **Única fuente de verdad del scroll** (Fase 1 E.5) | Inicializa por `data-cc-module`; carga el Orbe vía IntersectionObserver |
| `cc-color-orb.js` | Three.js: escena del Orbe (F). Se importa dinámicamente solo si `cc-fallbacks` lo permite y el hero entra en viewport | `import()` dinámico de `three.module.js` |
| `cc-palette-interactive.js` | Microinteracción de muestras de paleta (mod 7) | Degrada a estático en gama baja |
| `cc-faq-filter.js` | Filtro/búsqueda sobre las FAQs **ya presentes en el HTML** (mod 27) | Nunca carga FAQs por fetch |

- **GSAP gobierna; Three.js obedece** (Fase 1 E.5): un timeline con `ScrollTrigger` anima un proxy `{progress:0→1}`; el Orbe lee ese progreso. Desactivar el Orbe no rompe el resto.
- **Inicialización idempotente:** ScrollTrigger se inicializa una vez; refresh tras cargas diferidas.

---

## F. EL ORBE CROMÁTICO (especificación técnica)

> Una sola escena WebGL (Fase 1 E). Interfaz por data-attributes ya montada en Elementor (Fase 5 G).

| Aspecto | Especificación |
|---------|----------------|
| Geometría | Esfera de baja-media resolución; shader de gradiente fluido (ruido orgánico lento) con colores de marca |
| Materiales | Fresnel sutil, bloom muy contenido; nada metálico/gaming |
| Interacción | Respira en idle; parallax mínimo con cursor (desktop); con scroll (scrub) cambia temperatura; en mod 9 se separa en 4 halos estacionales |
| Carga | `import()` dinámico post-LCP, vía IntersectionObserver + `requestIdleCallback` |
| Entrada de color | `data-cc-orb-colors` (editable en Elementor) |
| Interruptor | `data-cc-orb="off"` desactiva sin deploy |
| Fallback (triple, Fase 1 E.8) | 1) sin WebGL/gama baja → gradiente CSS animado · 2) reduced-motion → halo estático · 3) error de carga → el gradiente CSS que ya estaba pintado debajo |
| Móvil | Geometría reducida, sin postprocesado, DPR cap 1.75; gama baja → fallback directo |
| Render loop | Pausado fuera de viewport (IntersectionObserver) para proteger INP/batería |
| Build alternativo (Fase 1 E.13) | Si no compensa: vídeo loop renderizado offline del orbe (<3MB) + GSAP. Spline y Lottie descartados para esta pieza |

---

## G. SCHEMA JSON-LD EN PHP (interfaz)

- **Origen del contenido:** Fase 4 §E (ya con datos confirmados).
- **Implementación:** `inc/schema.php` imprime el `@graph` en `wp_head`. Datos en constantes/array PHP; **no** en Elementor.
- **Piezas:** `Organization` (founder→Person), `Person` (Cristina Barriga, `sameAs`: web, bio, LinkedIn `/in/cristina-barriga/`, Amazon `/author/cristinabarriga`, `knowsAbout`), `Service` con `hasOfferCatalog` (180/590/1290 €), `WebSite`, `BreadcrumbList`, `FAQPage` (13 priorizadas, texto desde `faq-bank.md`).
- **Rank Math:** gestiona meta title/description y breadcrumbs; el schema crítico va a mano en PHP para control total (Fase 4).
- **Guardrails:** sin `MedicalBusiness`/`LocalBusiness` médico; INM **no** en `sameAs`.

---

## H. ENCOLADO CONDICIONAL Y PRESUPUESTO DE RENDIMIENTO

| Métrica (Fase 1 E.11) | Presupuesto |
|------------------------|-------------|
| JS adicional total (three + escena, min+gzip) | ≤ 180 KB, diferido post-LCP |
| LCP | < 2,5 s (el Orbe no participa: LCP = H1/fondo del hero) |
| CLS | 0 (canvas absolute sobre fallback ya pintado; imágenes con dimensiones) |
| INP | < 200 ms (render loop pausado fuera de viewport) |
| FPS | 60 desktop / ≥30 estable móvil medio; DPR cap 1,75 |
| Peso de imágenes | según doc 08 K.9 (hero ≤200KB AVIF, etc.) |

- **Carga por página:** la home encola sus módulos; los satélites futuros encolarán los suyos. Nada de cargar el JS de una página en otra.
- **Si el hero no cumple en dispositivo real:** no se publica el Orbe Three.js (queda el gradiente, que ya es premium).

---

## I. FRONTERA CON ELEMENTOR (recordatorio operativo)

- El código **define** lo que hacen las clases `cc-*`; Elementor solo las **aplica** (Fase 5 A).
- Cambiar un color del Orbe = editar `data-cc-orb-colors` en Elementor (sin deploy).
- Cambiar el sistema visual de un módulo = editar su `cc-*.css` (pasa por GitHub → SiteGround, con purga de cachés).
- Un cambio de texto/precio/FAQ nunca toca el repo.

---

## J. ORDEN DE IMPLEMENTACIÓN (sprints)

> Mejora progresiva: primero la web premium sin WebGL; el Orbe al final.

**Sprint 1 — Cimientos**
1. Child theme (`style.css`, `functions.php`), `cc-tokens.css`, `cc-base.css`, fuentes locales.
2. `inc/enqueue.php` + `inc/fonts.php`. Verificar carga en staging.

**Sprint 2 — Sistema visual (CSS por módulo)**
3. `cc-*.css` de los módulos P1 (hero, definición, servicio, método, estaciones, dimensiones, beneficios, autoridad, precios, FAQ, CTA, enlaces).
4. Validar contra el montaje de Elementor (Fase 5) en staging.

**Sprint 3 — Schema y SEO técnico**
5. `inc/schema.php` (Fase 4 §E). Validar con Rich Results Test.
6. `llms.txt` a la raíz; metas con Rank Math.

**Sprint 4 — Movimiento base (sin WebGL)**
7. `cc-motion-config.js`, `cc-fallbacks.js`, `cc-scroll-animations.js` (GSAP): revelados, parallax, scrub, línea de método.
8. `cc-palette-interactive.js`, `cc-faq-filter.js`.
9. **Aquí la web ya es lanzable (V1).**

**Sprint 5 — Orbe (V1.5, opcional según métricas)**
10. Prototipo aislado del Orbe (HTML estático, fuera de WordPress) + medición en dispositivos reales (Fase 1 E.15).
11. `cc-color-orb.js` con la interfaz de data-attributes; fallbacks primero.
12. Integración en staging; si cumple presupuesto, se publica; si no, queda el gradiente.

---

## K. PRUEBAS Y CRITERIOS DE ACEPTACIÓN

- [ ] **Core Web Vitals** dentro de presupuesto (H) en móvil real, no solo Lighthouse de escritorio.
- [ ] **SEO sin JS:** desactivando JavaScript, todo el texto, FAQs y entidades siguen en el DOM.
- [ ] **Schema válido** (Rich Results Test) sin errores; `Person`, `Organization`, `Service`, `FAQPage`.
- [ ] **Fallback del Orbe:** sin WebGL y con `prefers-reduced-motion`, la web se ve premium y no hay hueco en blanco.
- [ ] **Idempotencia:** ScrollTrigger no duplica triggers tras cargas diferidas.
- [ ] **Edición Elementor intacta:** cambiar textos/precios/imágenes no rompe estilos ni animaciones.
- [ ] **Cachés:** tras desplegar, el cache busting sirve la versión nueva (purga Elementor→SiteGround→Cloudflare).
- [ ] **Accesibilidad:** foco visible, contraste, `aria-hidden` en decorativo, navegación por teclado en FAQs.

---

## L. DESPLIEGUE (enlace con Fase 0 / Fase 7)

- Flujo: commit → GitHub → (Action/SSH rsync) → SiteGround → purga de cachés en orden Elementor → SiteGround → Cloudflare (Fase 0 C/D).
- Probar siempre en **staging de SiteGround** antes de producción.
- Rollback con `git revert` (el child theme es idempotente; no hay BD en juego al desplegar código).
- La ejecución detallada del despliegue es la **Fase 7**.

---

## M. CHECKLIST Y ENTREGABLES PARA FASE 7

### M.1 Entregables de Fase 6 (cuando se apruebe y se ejecute)

- Child theme `codigo-color-child` completo y versionado.
- `cc-*.css` de todos los módulos + `cc-tokens.css`/`cc-base.css`.
- `cc-*.js` (movimiento base) y, si pasa métricas, `cc-color-orb.js`.
- `inc/schema.php` con el schema confirmado.
- `docs/MANTENIMIENTO.md` (guía no técnica: qué archivo controla qué, on/off del Orbe, purga de cachés).
- `templates/elementor/*.json` (respaldo de plantillas, Fase 5 N).

### M.2 Bloqueos

1. **Aprobación del cliente** de Fases 0-5 y de este plan (Fase 6).
2. **Assets fotográficos P1** (o placeholders) y **retrato de Cristina Barriga** para poblar módulos.
3. **Acceso de despliegue** confirmado (SiteGround Git/SSH, secrets de GitHub Actions) — preparación de Fase 7.
4. **Decisión Orbe:** confirmar si se aborda el Sprint 5 (V1.5) en este ciclo o tras lanzar V1.

> **Siguiente fase:** FASE 6 (ejecución del código) tras aprobar este plan → luego FASE 7 (despliegue a producción).
