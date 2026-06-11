# assets/vendor

Librerías de terceros **locales** (no CDN, por rendimiento y control — Fase 0).

## GSAP (animaciones, V1)
Sube aquí, con estos nombres, para activar el movimiento avanzado:

- `gsap.min.js`
- `ScrollTrigger.min.js`

`inc/enqueue.php` los detecta y los encola automáticamente. Si **no** están,
`cc-scroll-animations.js` degrada con elegancia: el contenido permanece visible
y legible (SEO-safe), simplemente sin las animaciones de scroll.

## Three.js (Orbe Cromático, V1.5 — NO en V1)
`three.module.js` se añadirá en V1.5 cuando se active el Orbe. En V1 **no** se incluye
ni se carga: el hero usa el fallback de gradiente CSS (`.cc-color-orb`).

> Recuerda excluir estos `.js` de la minificación de SiteGround y desactivar
> Rocket Loader en Cloudflare (Fase 0) para no romper GSAP.
