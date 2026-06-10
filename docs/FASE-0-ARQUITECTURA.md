# FASE 0 — ARQUITECTURA TÉCNICA DE IMPLEMENTACIÓN Y DESPLIEGUE
## Código Color · WordPress · Elementor · SiteGround · Cloudflare · GitHub

> **Estado:** Entregado, pendiente de aprobación del cliente.
> **Regla:** Esta fase no genera código. Define cómo se construirá, versionará, desplegará y mantendrá todo lo que venga después.
> **Rol asumido:** CTO + Arquitecto WordPress senior + Arquitecto SEO/GEO.

---

## A. DECISIÓN DE ARQUITECTURA JUSTIFICADA

### A.1 Las cuatro opciones evaluadas

| Opción | Arquitectura | Resumen en una línea |
|--------|-------------|----------------------|
| **A** | Elementor + CSS personalizado | Todo vive en Elementor; el CSS se pega en el Customizer o en Site Settings |
| **B** | Tema hijo WordPress | Un child theme completo versionado en GitHub con CSS, PHP y assets |
| **C** | Plugin personalizado | Plugin propio "Código Color Core" con estilos, schema y funcionalidad |
| **D** | Arquitectura híbrida | Child theme **ligero** + Elementor editable + CSS global versionado + JS modular solo para animaciones premium (GSAP/Three.js) |

### A.2 Tabla puntuada (1 = malo · 5 = excelente)

Criterios en el orden de prioridad definido por el proyecto:

| # | Criterio | A: Elementor + CSS | B: Child theme | C: Plugin | D: Híbrida |
|---|----------|:---:|:---:|:---:|:---:|
| 1 | Facilidad de mantenimiento | 2 | 4 | 4 | **5** |
| 2 | Facilidad de despliegue | 3 | 4 | 4 | **5** |
| 3 | Edición para usuarios no técnicos | 5 | 4 | 3 | **5** |
| 4 | SEO | 3 | 4 | 4 | **5** |
| 5 | GEO | 3 | 4 | 4 | **5** |
| 6 | Rendimiento | 2 | 4 | 4 | **5** |
| 7 | Escalabilidad (cientos de URLs) | 1 | 3 | 4 | **5** |
| 8 | Compatibilidad futura | 3 | 3 | 4 | **4** |
| | **TOTAL** | **22** | **30** | **31** | **39** |

### A.3 Opción elegida: **D — Arquitectura híbrida**

**Composición exacta de la opción D para Código Color:**

1. **Child theme ligero** sobre **Hello Elementor** (el tema base oficial de Elementor: mínimo, rápido, mantenido por el mismo equipo que el constructor). El child theme contiene:
   - `style.css` mínimo (cabecera del tema, nada más)
   - `functions.php` que hace solo tres cosas: encolar los CSS versionados, encolar los JS modulares **de forma condicional por página**, e inyectar el schema JSON-LD
   - Carpeta `assets/` con CSS y JS compilados desde el repositorio
2. **Elementor** controla el 100% del contenido editable: textos, imágenes, vídeos, botones, formularios, FAQs, precios y CTAs. Las clases `cc-*` se aplican desde el campo "Clases CSS" de cada contenedor/widget de Elementor.
3. **CSS global versionado en GitHub**: el sistema visual completo (variables, tipografía, módulos `cc-*`) vive en archivos del repo, no en el Customizer. Elementor solo aplica clases; nunca define el sistema visual.
4. **JS modular solo para animaciones premium**: GSAP/ScrollTrigger y la eventual pieza Three.js (si la Fase 1 la aprueba) viven como módulos independientes (`cc-scroll-animations.js`, `cc-color-orb.js`…) que se cargan únicamente en las páginas que los usan, con detección de `prefers-reduced-motion` y fallback.

### A.4 Por qué gana D (justificación técnica)

- **Mantenimiento:** la frontera es nítida. Contenido → Elementor (sin tocar GitHub). Sistema visual y animaciones → GitHub (sin tocar Elementor). Nunca se pisan. Un cambio de texto jamás requiere un commit; un cambio de animación jamás rompe una página editada.
- **Despliegue:** se despliega **una sola carpeta** (el child theme) por SSH/rsync. No hay base de datos en juego, no hay riesgo de sobreescribir contenido. El despliegue es idempotente y reversible con `git revert`.
- **Edición no técnica:** idéntica a la opción A para el día a día. Cristina o su equipo editan todo desde Elementor. El código solo lo toca quien deba tocarlo.
- **SEO/GEO:** el schema JSON-LD (Organization, Person para Cristina Barriga, FAQPage, Service) vive en PHP versionado y auditable; el contenido SEO (100 FAQs, titulares, entidades) vive en HTML real renderizado por Elementor. Nada depende de JavaScript para existir en el DOM.
- **Rendimiento:** encolado condicional. La home no carga el JS de una página satélite y viceversa. GSAP/Three.js solo cargan donde se usan, con `defer` y carga diferida por IntersectionObserver. CSS versionado con cache busting automático.
- **Escalabilidad:** añadir 200 páginas satélite no cambia la arquitectura: son páginas Elementor que reutilizan las mismas clases `cc-*` y plantillas guardadas. El repo crece en módulos CSS, no en complejidad.

### A.5 Qué descarta cada opción no elegida y por qué

**Opción A (descartada como arquitectura, conservada como experiencia de edición):**
- El CSS en el Customizer no se versiona: sin historial, sin rollback, sin revisión. Con cientos de URLs futuras es ingobernable.
- No hay lugar limpio para GSAP/Three.js: habría que recurrir a plugins de "insertar código" o widgets HTML repetidos, que degradan rendimiento y mantenimiento.
- El CSS del Customizer se imprime inline en cada página: penaliza el HTML y no cachea como asset.
- **Lo que sí tomamos de A:** que el 100% del contenido sea editable desde Elementor.

**Opción B (descartada por acoplamiento excesivo):**
- Un child theme "completo" tiende a acumular funcionalidad (schema, shortcodes, lógica) que muere si algún día se cambia de tema.
- Mezcla presentación y funcionalidad en un solo paquete: cada despliegue toca más de lo necesario.
- **Lo que sí tomamos de B:** el child theme como vehículo de despliegue, pero deliberadamente *ligero*.

**Opción C (descartada por fricción sin beneficio neto a día de hoy):**
- Un plugin propio brilla cuando hay lógica de negocio (CPTs, APIs, lógica transaccional). Hoy Código Color necesita sistema visual + animaciones + schema: todo eso vive cómodamente en un child theme ligero.
- Añade una pieza más que actualizar, auditar y mantener compatible, sin resolver ningún problema que D no resuelva.
- **Punto de reevaluación documentado (ver F):** si en Fase 2 de negocio aparecen taxonomías personalizadas (16 estaciones como CPT, glosario como CPT), el schema y los CPTs migran a un plugin `codigo-color-core` y el child theme queda solo con presentación. La arquitectura D está diseñada para que esa migración sea un movimiento de archivos, no una reescritura.

---

## B. ARQUITECTURA DE REPOSITORIO GITHUB

### B.1 Estructura de carpetas del repositorio

```
codigo-color-web/
├── README.md                        ← Estado del proyecto, decisiones, próximos pasos
├── CHANGELOG.md                     ← Registro de cambios por módulo
├── .gitignore
│
├── docs/                            ← Documentación de fases y operaciones
│   ├── FASE-0-ARQUITECTURA.md       ← Este documento
│   ├── DESPLIEGUE.md                ← Guía paso a paso para persona no técnica (se crea en Fase 7)
│   └── MANTENIMIENTO.md             ← Qué tocar, dónde y cómo (se crea en Fase 6/7)
│
├── wp-content/
│   └── themes/
│       └── codigo-color-child/      ← ÚNICA carpeta que se despliega a producción
│           ├── style.css            ← Cabecera del child theme (mínimo)
│           ├── functions.php        ← Encolado condicional de assets + schema
│           ├── screenshot.png
│           └── assets/
│               ├── css/
│               │   ├── cc-variables.css
│               │   ├── cc-reset.css
│               │   ├── cc-global.css
│               │   ├── cc-typography.css
│               │   ├── cc-animations.css
│               │   ├── cc-responsive.css
│               │   └── modules/     ← Un archivo por módulo cc-*
│               ├── js/
│               │   ├── vendor/      ← gsap.min.js, ScrollTrigger.min.js (decisión CDN vs local en Fase 1/6)
│               │   └── modules/     ← cc-motion-config.js, cc-scroll-animations.js, cc-fallbacks.js,
│               │                      cc-color-orb.js (solo si Fase 1 aprueba Three.js)
│               └── php/
│                   └── schema/      ← cc-schema-organization.php, cc-schema-person.php,
│                                      cc-schema-faqpage.php, cc-schema-service.php
│
├── elementor/                       ← Plantillas exportadas (backup versionado, NO se despliega)
│   ├── global-colors.json
│   ├── global-fonts.json
│   └── templates/                   ← cc-hero.json, cc-faq.json, etc.
│
└── seo/                             ← Activos SEO/GEO versionados (NO se despliegan; son fuente de verdad)
    ├── faq-bank.md                  ← Banco maestro de FAQs (regla anti-canibalización)
    ├── meta.md                      ← Metatítulos y descripciones por URL
    ├── schema-*.json                ← JSON-LD canónicos
    ├── sitemap-structure.md
    └── internal-linking-map.md
```

**Principio clave:** solo `wp-content/themes/codigo-color-child/` viaja a producción. `docs/`, `elementor/` y `seo/` son fuente de verdad y backup, nunca se suben al servidor.

### B.2 Estrategia de ramas (trunk-based simplificado)

Para un proyecto con un mantenedor principal y cambios de tamaño módulo, lo más simple que funciona:

```
main      ← SIEMPRE desplegable. Lo que hay en main es lo que hay (o puede haber) en producción.
feature/* ← Una rama corta por módulo o cambio: feature/cc-hero, feature/schema-person, fix/cc-faq-mobile
```

- No hay rama `develop`: añade ceremonia sin beneficio a esta escala.
- Toda rama `feature/*` se integra en `main` mediante Pull Request (aunque lo apruebe la misma persona: el PR deja registro y permite revisar el diff).
- **Releases:** cada despliegue a producción se etiqueta: `v1.0.0`, `v1.1.0`… (semver simplificado: mayor = rediseño, menor = módulo nuevo, parche = corrección). El tag es el punto de rollback.

### B.3 Convención de commits

Conventional Commits en español, con el módulo como ámbito:

```
feat(cc-hero): añade módulo hero editorial con animación de entrada
fix(cc-faq): corrige espaciado del acordeón en móvil
style(cc-variables): ajusta color acento a #C4A882
docs(despliegue): actualiza guía de purga de caché
seo(faq-bank): añade FAQ-0042 asignada a /codigo-color/
chore(release): v1.2.0
```

Regla del prompt maestro respetada: **un módulo = un commit conceptual**. Nunca dos módulos en el mismo commit.

### B.4 Qué entra y qué NO entra en el repositorio

**Entra:**
- Child theme completo (CSS, JS, PHP de schema)
- Documentación (`docs/`), activos SEO (`seo/`), plantillas Elementor exportadas (`elementor/`)

**NO entra (nunca):**
- `wp-config.php` ni ninguna credencial o salt
- `/wp-content/uploads/` (medios: viven en el servidor y en el backup de SiteGround)
- WordPress core, plugins, otros temas (se gestionan desde el panel de WP; versionarlos duplica responsabilidades y genera conflictos de actualización)
- Base de datos ni exports SQL (el contenido Elementor vive en la BD; su backup es el sistema de backups diarios de SiteGround + exports JSON puntuales en `elementor/`)
- Archivos de entorno local (`.env`, configs de IDE)

### B.5 `.gitignore`

```gitignore
# WordPress core y configuración — nunca versionar
wp-admin/
wp-includes/
wp-*.php
index.php
xmlrpc.php
license.txt
readme.html

# Contenido gestionado por WordPress
wp-content/uploads/
wp-content/upgrade/
wp-content/cache/
wp-content/backup*/
wp-content/plugins/
wp-content/themes/*
!wp-content/themes/codigo-color-child/

# Credenciales y entorno
wp-config.php
.env
.env.*
*.sql
*.sql.gz

# Sistema y herramientas
.DS_Store
Thumbs.db
.idea/
.vscode/
node_modules/
*.log
```

---

## C. FLUJO DE DESPLIEGUE GITHUB → SITEGROUND

### C.1 Método elegido: **GitHub Actions → SSH/rsync** (con plan B manual documentado)

**Comparativa rápida de los cuatro métodos posibles:**

| Método | Pros | Contras | Veredicto |
|--------|------|---------|-----------|
| SFTP manual | Cero configuración | Manual, propenso a error, sin registro | Solo como plan B documentado |
| SiteGround Git tool | Nativo | Limitado, requiere disciplina de rutas, herramienta poco mantenida | Descartado |
| SSH + `git pull` en servidor | Simple | Exige repo en servidor y SSH manual cada vez; una persona no técnica no lo hará | Descartado |
| **GitHub Actions → rsync** | **Automático, registrado, repetible, lo dispara un botón** | Configuración inicial (1 vez) | **Elegido** |

**Por qué:** el criterio decisivo es *"debe poder ejecutarlo una persona no técnica con una guía"*. Con GitHub Actions, desplegar es: fusionar el PR en `main` (o pulsar "Run workflow"). No hay clientes FTP, no hay terminal, no hay rutas que recordar. Cada despliegue queda registrado con quién, cuándo y qué.

### C.2 Pasos exactos del flujo

**Configuración inicial (una sola vez, la hace el desarrollador):**
1. En SiteGround (plan GrowBig/GoGeek): activar acceso SSH y generar par de claves.
2. En GitHub: guardar como *Secrets* del repositorio: `SG_HOST`, `SG_USER`, `SG_PORT`, `SG_SSH_KEY`, `SG_PATH_STAGING`, `SG_PATH_PROD`.
3. Crear el workflow `.github/workflows/deploy.yml` (se construye en Fase 7) con dos jobs: `deploy-staging` (automático al hacer merge en `main`) y `deploy-production` (manual, botón "Run workflow" con confirmación).
4. El workflow hace `rsync` **solo** de `wp-content/themes/codigo-color-child/` → ruta del tema en el servidor, con `--delete` limitado a esa carpeta.

**Flujo de cada cambio de código (rutina):**
```
1. Crear rama feature/cc-modulo
2. Hacer el cambio + commit
3. Abrir Pull Request → revisar diff → merge a main
4. GitHub Actions despliega AUTOMÁTICAMENTE al STAGING de SiteGround
5. Revisar en staging (móvil + desktop, checklist de Fase 7)
6. Pulsar "Run workflow → deploy-production" en GitHub
7. Purgar cachés en orden (ver D.4)
8. Verificar producción
9. Etiquetar release (vX.Y.Z)
```

### C.3 Uso del staging de SiteGround

- El staging de SiteGround (copia completa del sitio) se usa para **probar cambios de contenido/Elementor grandes** y actualizaciones de plugins/WordPress.
- Para **cambios de código del child theme**, el staging recibe el deploy automático del paso 4 antes de que nada toque producción.
- Regla: ningún cambio de código llega a producción sin haberse visto en staging. Los cambios de contenido en Elementor (textos, imágenes, FAQs) no necesitan staging: son reversibles con el historial de revisiones de Elementor.

### C.4 Plan de rollback

| Escenario | Acción | Tiempo |
|-----------|--------|--------|
| El último deploy de código rompe algo | En GitHub: "Run workflow" sobre el tag anterior (`vX.Y.Z-1`) → redeploy de la versión buena | ~2 min |
| Rotura grave o causa desconocida | Restaurar backup diario de SiteGround (panel → Backups) | ~10 min |
| Un cambio de Elementor rompe una página | Elementor → Historial de revisiones de la página → restaurar | ~1 min |
| Emergencia sin acceso a GitHub | Plan B documentado en `docs/DESPLIEGUE.md`: subir por SFTP la carpeta del child theme del último tag descargado de GitHub | ~10 min |

### C.5 Quién puede desplegar

- **Persona no técnica (Cristina/equipo):** cambios de contenido en Elementor (no tocan GitHub) y, con la guía `docs/DESPLIEGUE.md`, el botón "Run workflow" + purga de cachés.
- **Desarrollador:** cambios de código (ramas, PRs) y mantenimiento del workflow.
- Nunca se edita código directamente en producción (ni por el editor de archivos de WP ni por FTP). Todo cambio de código nace en GitHub.

---

## D. ESTRATEGIA DE CACHÉ EN CASCADA

La cadena real es: **Navegador → Cloudflare → SiteGround (NGINX/Dynamic cache) → WordPress/Elementor**. La regla de oro: **cada capa se purga de dentro hacia fuera**.

### D.1 Configuración recomendada de Cloudflare

| Ajuste | Valor | Motivo |
|--------|-------|--------|
| **Rocket Loader** | **OFF** | Rompe sistemáticamente el JS de Elementor y de GSAP/ScrollTrigger. Documentado como incompatible. Nuestro JS ya carga con `defer` propio |
| Auto Minify | N/A (retirado por Cloudflare en 2024) | La minificación la hace SiteGround Speed Optimizer |
| Caching level | Standard | |
| Browser Cache TTL | Respect Existing Headers | SiteGround ya envía cabeceras correctas |
| APO (Automatic Platform Optimization) | **No instalar por ahora** | Solapa con la caché dinámica de SiteGround; dos cachés de página = purgas impredecibles. Reevaluar solo si hay tráfico internacional significativo |
| Cache Rules | Bypass para `/wp-admin/*` y previews de Elementor (`?elementor-preview=*`) | Evita servir versiones cacheadas del editor |
| SSL | Full (Strict) | |

### D.2 Configuración recomendada de SiteGround Speed Optimizer

**Decisión: Speed Optimizer es el ÚNICO plugin de caché.** No instalar WP Rocket ni LiteSpeed (LiteSpeed además no aplica: SiteGround usa NGINX). Dos plugins de caché = la fuente número uno de bugs fantasma en WordPress.

- Dynamic Cache: ON · Memcached: ON si el plan lo incluye
- Minificación de CSS/JS: ON, **con exclusión explícita de los archivos `cc-*.js`** (GSAP/ScrollTrigger son sensibles a la re-minificación combinada; nuestros archivos ya llegan minificados desde el repo)
- "Combine CSS/JS": **OFF** (con HTTP/2 fragmentar es mejor que combinar, y combinar rompe el encolado condicional por página)
- Optimización de imágenes y WebP: ON
- Lazy load de imágenes: ON (excepto hero, que se marca como excluido)

### D.3 Caché interna de Elementor

- Elementor regenera su CSS por página/post. Tras cada despliegue de CSS del child theme: **Elementor → Herramientas → Regenerar CSS y datos**.
- Google Fonts: se cargarán localmente (decisión de Fase 5/6) para rendimiento y RGPD; Elementor → Ajustes → marcar fuentes locales.

### D.4 Orden de purga tras cada despliegue (memorizable)

```
1. Elementor  → Herramientas → Regenerar CSS y datos
2. SiteGround → Speed Optimizer → Purge SG Cache
3. Cloudflare → Caching → Purge Everything (o por URL si el cambio es acotado)
4. Verificar en ventana de incógnito + móvil real
```

Este orden va impreso en `docs/DESPLIEGUE.md`. Purgar en orden inverso sirve versiones viejas re-cacheadas.

### D.5 Cache busting de CSS y JS versionados

- En `functions.php`, cada `wp_enqueue_style/script` usa `filemtime()` del archivo como número de versión: `cc-global.css?ver=1718031022`.
- Resultado: **el cache busting es automático en cada despliegue**. Cloudflare y los navegadores ven una URL nueva cuando (y solo cuando) el archivo cambia. Nadie tiene que recordar subir un número de versión a mano.

---

## E. FRONTERA CÓDIGO / ELEMENTOR

### E.1 Qué vive en código versionado en GitHub

| Pieza | Archivo | Cambia con |
|-------|---------|-----------|
| Sistema de variables (colores, tipos, espaciados) | `assets/css/cc-variables.css` | Commit + deploy |
| Sistema visual de cada módulo `cc-*` | `assets/css/modules/*.css` | Commit + deploy |
| Animaciones GSAP/ScrollTrigger | `assets/js/modules/*.js` | Commit + deploy |
| Pieza Three.js/WebGL (si Fase 1 la aprueba) + fallbacks | `assets/js/modules/cc-color-orb.js`, `cc-fallbacks.js` | Commit + deploy |
| Schema JSON-LD (Organization, Person, FAQPage, Service) | `assets/php/schema/*.php` | Commit + deploy |
| Encolado condicional de assets | `functions.php` | Commit + deploy |
| Banco maestro de FAQs y mapa de enlazado | `seo/` | Commit (sin deploy: es fuente de verdad) |

### E.2 Qué vive editable en Elementor (sin tocar GitHub jamás)

- Todos los textos: titulares, párrafos, manifiesto, microcopy
- Todas las imágenes y vídeos
- Botones y CTAs (texto, enlace, destino, WhatsApp)
- Formularios y sus campos
- Las 100 FAQs: pregunta y respuesta de cada una (widget acordeón, contenido en HTML real del DOM)
- Precios, packs y condiciones
- Orden de secciones dentro de una página
- Creación de páginas nuevas reutilizando plantillas guardadas

### E.3 Cómo se conectan sin pisarse

1. El código define **clases**, nunca contenido: `.cc-hero`, `.cc-faq__item`, `.cc-season-card--invierno`.
2. En Elementor, cada sección lleva su clase en el campo "Clases CSS" del contenedor. La plantilla guardada ya la trae puesta: quien duplica una sección hereda el sistema visual sin saberlo.
3. El JS se engancha por selectores `data-cc-module="..."` (atributo que también viene en la plantilla). Si el atributo no existe en la página, el módulo JS no hace nada y no falla.
4. **Protocolo anti-pisada:** el CSS del repo nunca usa selectores de IDs internos de Elementor (`.elementor-element-abc123`); Elementor nunca define estilos que el sistema ya cubre (se trabaja con Global Colors/Fonts sincronizados con `cc-variables.css`).

### E.4 Protocolo "un cambio de texto nunca toca GitHub"

Pregunta de triaje para cualquier cambio futuro (se documenta en `docs/MANTENIMIENTO.md`):

```
¿El cambio es de CONTENIDO (texto, imagen, precio, FAQ, CTA, vídeo)?
   → Elementor. Editar, actualizar, purgar Cloudflare de esa URL. Fin. GitHub no se entera.

¿El cambio es de SISTEMA (color de marca, tipografía, animación, schema, módulo nuevo)?
   → GitHub. Rama → PR → merge → staging → producción → purga en cascada.
```

---

## F. PLAN DE ESCALABILIDAD

### F.1 Cómo la arquitectura soporta crecer a cientos de URLs

- **Las páginas nuevas no son código nuevo.** Una página satélite (`/colorimetria-madrid/`, `/estacion-invierno-profundo/`…) se crea en WordPress + Elementor reutilizando plantillas guardadas y clases `cc-*` existentes. Coste marginal en el repo: cero.
- **El CSS es un sistema, no páginas.** Los módulos `cc-*` son agnósticos de la URL. 10 páginas o 300 páginas usan los mismos archivos, que cachean una sola vez.
- **El JS es condicional.** El encolado por página garantiza que el peso no crece con el número de URLs: cada página carga solo lo suyo.
- **El SEO escala desde `seo/`.** El banco maestro `faq-bank.md` (una pregunta = una URL) y `internal-linking-map.md` previenen canibalización y mantienen el flujo de autoridad hub→spoke cuando haya cientos de páginas.

### F.2 Qué cambia y qué no cambia al añadir servicios, cursos, estaciones, glosario y páginas locales

| | Cambia | No cambia |
|---|--------|-----------|
| Páginas de servicios/packs | Contenido en Elementor + entrada en `seo/meta.md` | Child theme, CSS, JS, flujo de deploy |
| 16 estaciones cromáticas | Quizá 1 módulo CSS nuevo (`cc-season-detail.css`) | Arquitectura, plantilla base |
| Glosario 50+ términos | Plantilla Elementor "término" + FAQs propias | Sistema visual |
| Páginas locales (Madrid, Barcelona…) | Contenido + schema LocalBusiness por ubicación | Todo lo demás |
| Blog | Se activa la plantilla de entrada del child theme | Arquitectura |

### F.3 Puntos de revisión de la arquitectura (cuándo reevaluar)

La arquitectura D se reevalúa **solo** si se cruza alguno de estos umbrales:

1. **Taxonomías reales:** si las 16 estaciones, el glosario o los cursos piden Custom Post Types con campos propios (ACF) → crear el plugin `codigo-color-core` y mover allí CPTs + schema. El child theme queda solo con presentación. (Migración prevista, no reescritura.)
2. **Multidioma:** si se lanza versión en inglés/italiano → decidir WPML vs Polylang y revisar hreflang en ese momento.
3. **E-commerce:** si los cursos se venden online → WooCommerce o plataforma externa; revisar caché (las páginas de carrito no se cachean).
4. **Tráfico internacional sostenido:** reevaluar Cloudflare APO.
5. **Más de ~300 URLs o varios editores simultáneos:** revisar gobernanza de contenido y staging.

Mientras no se cruce ningún umbral, la arquitectura no se toca.

---

## RESUMEN EJECUTIVO (para validación)

- **Arquitectura:** D — child theme ligero sobre Hello Elementor + Elementor para todo el contenido + CSS/JS versionado en GitHub + schema en PHP versionado.
- **Repositorio:** solo se despliega `wp-content/themes/codigo-color-child/`; `docs/`, `seo/` y `elementor/` son fuente de verdad.
- **Ramas:** `main` siempre desplegable + ramas `feature/*` cortas + tags de release como puntos de rollback.
- **Despliegue:** GitHub Actions → rsync por SSH; staging automático, producción con botón; plan B manual documentado.
- **Caché:** Speed Optimizer único plugin de caché; Rocket Loader OFF; purga siempre Elementor → SiteGround → Cloudflare; cache busting automático por `filemtime()`.
- **Frontera:** contenido = Elementor (nunca GitHub); sistema visual/animaciones/schema = GitHub (nunca editado en producción).
- **Escala:** páginas nuevas no generan código nuevo; umbral documentado para migrar a plugin si aparecen CPTs.

**Siguiente paso:** aprobación explícita de esta Fase 0 → arranque de **FASE 1** (concepto visual, arquitectura modular de 31 módulos, estrategia SEO/GEO/AEO, jerarquía experta de Cristina Barriga y la sección obligatoria "Estrategia Three.js, WebGL y movimiento premium" con sus 15 puntos).
