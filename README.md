# Código Color — Web WordPress

Web oficial de Código Color · Colorimetría y asesoría de imagen · Dirigida por Cristina Barriga.

## Estado del proyecto

- Última actualización: 2026-06-10
- Fase actual: **FASE 0 — Arquitectura técnica** (entregada, pendiente de aprobación)
- Documento: [`docs/FASE-0-ARQUITECTURA.md`](docs/FASE-0-ARQUITECTURA.md)

## Decisiones tomadas (Fase 0, pendientes de aprobación)

- Arquitectura: **Opción D (híbrida)** — child theme ligero sobre Hello Elementor + Elementor para contenido + CSS/JS versionado + schema en PHP
- Despliegue: GitHub Actions → SSH/rsync a SiteGround (staging automático, producción manual con botón)
- Caché: SiteGround Speed Optimizer como único plugin de caché; Rocket Loader de Cloudflare OFF; purga Elementor → SiteGround → Cloudflare
- Frontera: contenido siempre editable en Elementor; sistema visual y animaciones siempre en GitHub

## Hoja de ruta por fases

- [x] FASE 0 — Arquitectura técnica de implementación y despliegue *(pendiente de aprobación)*
- [ ] FASE 1 — Arquitectura modular, dirección de arte, estrategia SEO/GEO y estrategia Three.js/WebGL/movimiento premium
- [ ] FASE 2 — Benchmark visual (30+ referencias Apple + Awwwards)
- [ ] FASE 3 — Wireframe editorial
- [ ] FASE 4 — Copy, SEO y GEO (100 FAQs + schema)
- [ ] FASE 5 — Diseño en Elementor
- [ ] FASE 6 — Código opcional (módulos cc-*)
- [ ] FASE 7 — Despliegue a producción
- [ ] FASE 8 — Modificaciones futuras

## Notas del cliente

- (Registrar aquí cualquier cambio solicitado)

## Próximos pasos

1. Aprobación explícita de la Fase 0
2. Iniciar Fase 1 (incluye la sección obligatoria "Estrategia Three.js, WebGL y movimiento premium" con sus 15 puntos)
