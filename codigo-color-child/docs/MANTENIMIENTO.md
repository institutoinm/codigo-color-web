# MANTENIMIENTO — Código Color Child (V1)

Guía no técnica del child theme. Qué controla cada cosa, cómo se activa, qué se edita en Elementor y qué no se toca.

---

## 1. Qué es este tema

Child theme ligero de **Hello Elementor**. Aporta el **sistema visual** (`cc-*.css`), la **arquitectura de animación** (GSAP, preparada) y el **schema SEO** (PHP). **No contiene contenido**: textos, imágenes, precios y FAQs se editan en Elementor.

**V1 (esta versión):** premium, rápida, sin WebGL.
**V1.5 (futuro):** se activará el Orbe Cromático (Three.js). Ya está preparado pero **desactivado**.

---

## 2. Activación (paso a paso)

1. Tener instalados y activos: **Hello Elementor** (tema padre) y **Elementor Pro**.
2. Subir la carpeta `codigo-color-child/` a `wp-content/themes/` (vía Git de SiteGround, SSH o SFTP — ver Fase 0/7).
3. En **Apariencia → Temas**, activar **«Código Color Child»**.
4. (Recomendado) Subir las fuentes locales a `assets/fonts/` (ver `assets/fonts/README.md`). Si no, la web usa Google Fonts automáticamente.
5. (Opcional, para animaciones) Subir `gsap.min.js` y `ScrollTrigger.min.js` a `assets/vendor/` (ver `assets/vendor/README.md`).
6. Construir las páginas en Elementor aplicando las clases `cc-*` según la Fase 5 (`docs/05_ELEMENTOR.md`).
7. Purga de cachés en orden: **Elementor → SiteGround → Cloudflare**.

> El tema funciona aunque falten fuentes locales y GSAP: degrada con elegancia y el contenido siempre es visible (SEO-safe).

---

## 3. Qué controla cada archivo

| Archivo | Controla |
|---------|----------|
| `style.css` | Cabecera del tema (no tocar para estilos) |
| `functions.php` | Carga `inc/*` |
| `inc/enqueue.php` | Qué CSS/JS se carga y en qué página |
| `inc/fonts.php` | Fuentes locales o puente Google Fonts |
| `inc/schema.php` | Schema JSON-LD (Organization, Person, Service+precios, FAQ) |
| `assets/css/cc-tokens.css` | Paleta, tipografía, espaciado, motion (variables) |
| `assets/css/cc-base.css` | Botones, placeholders, grids, fallback del Orbe, base |
| `assets/css/cc-<modulo>.css` | Estilo de cada módulo de la landing |
| `assets/js/cc-scroll-animations.js` | Animaciones de scroll (GSAP) |
| `assets/js/cc-fallbacks.js` | Detección de capacidades del dispositivo |
| `assets/js/cc-faq-filter.js` | Buscador de FAQs (sobre HTML existente) |

---

## 4. Cambios habituales

- **Cambiar un texto, precio, imagen o FAQ:** Elementor. **Nunca** toca este tema.
- **Cambiar un color de marca:** editar la variable en `assets/css/cc-tokens.css` → commit → desplegar → purgar cachés.
- **Ajustar el estilo de un módulo:** editar su `cc-<modulo>.css`.
- **Cambiar datos de schema (precios, perfiles):** `inc/schema.php`.

---

## 5. El Orbe Cromático (V1.5)

- En V1 el hero muestra un **gradiente CSS** animado (clase `.cc-color-orb`): es el fallback premium, no necesita WebGL.
- En V1.5 se añadirá `assets/js/cc-color-orb.js` (Three.js) y se pondrá `flags.orb = true` en `cc-motion-config.js`. El hook ya está en `cc-scroll-animations.js` (comentado).
- **Activar/desactivar** (cuando exista): atributo `data-cc-orb="on|off"` en el contenedor del hero, desde Elementor, sin desplegar.

---

## 6. Reglas de oro

- No renombrar las clases `cc-*` (son el contrato entre Elementor y el código).
- No meter contenido dentro del contenedor `.cc-color-orb`.
- Excluir `cc-*.js`, GSAP y Three de la minificación de SiteGround; Rocket Loader OFF en Cloudflare (Fase 0).
- Todo cambio de código pasa por GitHub → SiteGround. Nunca editar en producción.
