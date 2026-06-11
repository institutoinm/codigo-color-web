# Código Color — Child Theme (V1)

Child theme ligero de **Hello Elementor** para [codigocolor.es](https://www.codigocolor.es).
Implementa la arquitectura D híbrida (Fase 0): sistema visual `cc-*` versionado + contenido 100% editable en Elementor.

## Estado: V1 (sin WebGL)
- ✅ Premium, rápido, mantenible, editable en Elementor.
- ✅ SEO/GEO/AEO: schema JSON-LD en PHP, contenido en HTML real.
- ✅ Arquitectura GSAP lista (degrada con elegancia si GSAP no está).
- ✅ Orbe Cromático **preparado pero desactivado** (fallback de gradiente CSS).
- ⏳ V1.5: activar Three.js / Orbe.

## Estructura
```
codigo-color-child/
├── style.css            # Cabecera del tema
├── functions.php        # Orquestador
├── inc/                 # enqueue, fonts, schema, helpers
├── assets/css/          # cc-tokens, cc-base, cc-fonts + 22 módulos cc-*
├── assets/js/           # motion-config, fallbacks, scroll-animations, palette, faq-filter
├── assets/fonts/        # (subir woff2 locales)
├── assets/vendor/       # (subir gsap.min.js, ScrollTrigger.min.js)
├── templates/elementor/ # respaldo JSON de plantillas
└── docs/MANTENIMIENTO.md
```

## Activación
Ver `docs/MANTENIMIENTO.md` §2.

## Requisitos
- WordPress ≥ 6.0 · PHP ≥ 7.4 · Hello Elementor · Elementor Pro 3.20+
