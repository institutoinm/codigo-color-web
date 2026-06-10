# Código Color — Web WordPress

Web oficial de Código Color · Colorimetría y asesoría de imagen · Dirigida por Cristina Barriga.

## Estado del proyecto

- Última actualización: 2026-06-10
- Fase actual: **FASE 1 — Dirección de arte y estrategia SEO/GEO** (entregada, pendiente de aprobación)
- Documentos: [`docs/FASE-0-ARQUITECTURA.md`](docs/FASE-0-ARQUITECTURA.md) (aprobada) · [`docs/FASE-1-DIRECCION-ARTE-SEO.md`](docs/FASE-1-DIRECCION-ARTE-SEO.md)

## Decisiones tomadas (Fase 0 — APROBADA)

- Arquitectura: **Opción D (híbrida)** — child theme ligero sobre Hello Elementor + Elementor para contenido + CSS/JS versionado + schema en PHP
- Despliegue: GitHub Actions → SSH/rsync a SiteGround (staging automático, producción manual con botón)
- Caché: SiteGround Speed Optimizer como único plugin de caché; Rocket Loader de Cloudflare OFF; purga Elementor → SiteGround → Cloudflare
- Frontera: contenido siempre editable en Elementor; sistema visual y animaciones siempre en GitHub

## Hoja de ruta por fases

- [x] FASE 0 — Arquitectura técnica de implementación y despliegue *(APROBADA)*
- [x] FASE 1 — Arquitectura modular, dirección de arte, estrategia SEO/GEO y estrategia Three.js/WebGL/movimiento premium *(pendiente de aprobación)*
- [ ] FASE 2 — Benchmark visual (30+ referencias Apple + Awwwards)
- [ ] FASE 3 — Wireframe editorial
- [ ] FASE 4 — Copy, SEO y GEO (100 FAQs + schema)
- [ ] FASE 5 — Diseño en Elementor
- [ ] FASE 6 — Código opcional (módulos cc-*)
- [ ] FASE 7 — Despliegue a producción
- [ ] FASE 8 — Modificaciones futuras

## Decisiones tomadas (Fase 1, pendientes de aprobación)

- Concepto: «Minimalismo Editorial Cromático Futurista» · narrativa «El Despertar del Color»
- Elemento firma: el Orbe Cromático (con versión estática de marca)
- Tipografía: Cormorant Garamond (display) + DM Sans (body), servidas localmente
- Three.js: SÍ, quirúrgico y por fases — V1 lanza sin Three.js (gradiente premium + GSAP); V1.5 activa el orbe como mejora progresiva solo en el hero
- Spline: descartado para esta fase
- 100 FAQs en 11 categorías; banco maestro anti-canibalización en `seo/faq-bank.md`

## Notas del cliente

- Fase 0 aprobada explícitamente el 2026-06-10

## Próximos pasos

1. Aprobación explícita de la Fase 1
2. Cliente: responder las 8 preguntas sobre Cristina Barriga (sección D.4 de Fase 1) — bloqueantes para Fase 4
3. Tras aprobación → FASE 2: benchmark visual de 30+ referencias
