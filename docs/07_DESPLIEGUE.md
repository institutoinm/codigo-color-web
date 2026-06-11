# 07 — DESPLIEGUE A PRODUCCIÓN
## Código Color · Flujo GitHub → SiteGround → Cloudflare, staging, purga de cachés, rollback y verificación post-lanzamiento

> **Estado:** Plan/guía entregada, pendiente de aprobación. La **ejecución** (crear el workflow, dar de alta secrets, primer deploy) se hace tras aprobar este documento y con accesos confirmados.
> **Regla:** todo cambio de **código** pasa por GitHub → SiteGround. El **contenido** (textos, imágenes, precios, FAQs) se edita en Elementor y **no** pasa por este flujo.
> **Depende de:** FASE 0 (decisión de despliegue: GitHub Actions → SSH/rsync → SiteGround con staging y rollback; caché en cascada Cloudflare/SiteGround/Elementor), FASE 6 V1 (child theme `codigo-color-child`).
> **Rol asumido:** CTO + DevOps WordPress.
> **Objetivo:** que una persona poco técnica pueda desplegar siguiendo pasos, y que el sistema sea reversible.

---

## ÍNDICE

- **A.** Qué se despliega y qué no
- **B.** Estructura final en GitHub y versionado
- **C.** Método de despliegue (GitHub Actions → SSH/rsync)
- **D.** Conexión con WordPress (activación del tema)
- **E.** Cloudflare y SiteGround (configuración compatible)
- **F.** Purga de cachés (orden obligatorio)
- **G.** Uso del staging de SiteGround
- **H.** Checklist pre-lanzamiento
- **I.** Verificación post-despliegue
- **J.** Rollback (cómo deshacer)
- **K.** Cómo mantener Elementor editable y no romper la web
- **L.** Runbook resumido (la chuleta de una página)
- **M.** Entregables de ejecución y bloqueos

---

## A. QUÉ SE DESPLIEGA Y QUÉ NO

| ✅ Pasa por GitHub → SiteGround (código) | ⛔ NO pasa por este flujo |
|------------------------------------------|----------------------------|
| `codigo-color-child/` (tema: PHP, CSS, JS, fuentes, vendor) | Contenido de Elementor (vive en la base de datos) |
| `llms.txt` (raíz del dominio) | `wp-config.php`, uploads, base de datos |
| Plantillas Elementor exportadas (`templates/elementor/*.json`, respaldo) | Plugins (se instalan/configuran en WordPress) |

> **Regla de oro:** un cambio de texto/precio/FAQ se hace en Elementor y **no** requiere commit. Un cambio de `cc-*.css`/`cc-*.js`/schema sí pasa por este flujo.

---

## B. ESTRUCTURA FINAL EN GITHUB Y VERSIONADO

### B.1 Qué contiene el repo

```
/                          (raíz del repo)
├── codigo-color-child/    → se despliega a wp-content/themes/codigo-color-child/
├── llms.txt               → se despliega a la raíz pública del dominio
├── docs/                  → documentación del proyecto (NO se despliega)
├── seo/                   → faq-bank, mapas (NO se despliega; fuente de verdad)
└── .github/workflows/     → workflow de despliegue (al aprobar Fase 7)
```

> Solo se despliega lo «público»: el tema y `llms.txt`. `docs/` y `seo/` son documentación interna y **no** suben a producción.

### B.2 Ramas

- `main` → producción (lo que está vivo).
- `claude/codigo-color-web-review-57lqst` → rama de trabajo actual (esta fase).
- Flujo: trabajo en rama → revisión → merge a `main` → el merge dispara el deploy.

### B.3 Convención de commits (Fase 0)

`tipo(ámbito): descripción` — `feat`, `fix`, `docs`, `style`, `chore`. Ej.: `fix(theme): ajusta gap del módulo de precios en mobile`.

### B.4 Releases / versionado del tema

- Subir la versión en `style.css` (`Version:`) en cada cambio relevante del tema.
- Etiquetar releases (`v1.0.0`, `v1.1.0`…) para poder volver a una versión concreta (rollback, J).

### B.5 `.gitignore` (si se versiona más que el tema)

Si en el futuro se versiona `wp-content` completo, excluir: `/wp-config.php`, `/wp-content/uploads/`, `/wp-content/cache/`, `*.log`, `node_modules/`. En el estado actual el repo solo contiene el tema + artefactos, así que no aplica todavía.

---

## C. MÉTODO DE DESPLIEGUE (GitHub Actions → SSH/rsync)

> Decisión de Fase 0. Despliegue automático del tema por SSH al hacer merge a `main`. Una persona no técnica solo necesita **aprobar el merge**; el resto es automático.

### C.1 Cómo funciona

1. Merge (o push) a `main` que toque `codigo-color-child/**` o `llms.txt`.
2. GitHub Action arranca: hace checkout y **rsync** del tema al servidor de SiteGround por SSH.
3. Tras subir, ejecuta la **purga de cachés** (F) vía API/CLI.
4. Notifica el resultado (éxito/fallo).

### C.2 Secrets necesarios (GitHub → Settings → Secrets)

| Secret | Qué es |
|--------|--------|
| `SG_SSH_HOST` | Host SSH de SiteGround |
| `SG_SSH_PORT` | Puerto SSH (SiteGround suele usar 18765) |
| `SG_SSH_USER` | Usuario SSH |
| `SG_SSH_KEY` | Clave privada SSH (la pública se da de alta en SiteGround) |
| `SG_THEME_PATH` | Ruta destino: `.../wp-content/themes/codigo-color-child` |
| `CF_ZONE_ID` | Zona de Cloudflare (purga) |
| `CF_API_TOKEN` | Token de Cloudflare con permiso de purga |

### C.3 Workflow propuesto (ILUSTRATIVO — se crea al aprobar)

```yaml
# .github/workflows/deploy.yml  (BORRADOR — no activo todavía)
name: Deploy theme to SiteGround
on:
  push:
    branches: [ main ]
    paths: [ 'codigo-color-child/**', 'llms.txt' ]
  workflow_dispatch: {}          # permite lanzarlo a mano
concurrency: { group: deploy-prod, cancel-in-progress: false }
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Configurar SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SG_SSH_KEY }}" > ~/.ssh/id && chmod 600 ~/.ssh/id
          ssh-keyscan -p ${{ secrets.SG_SSH_PORT }} ${{ secrets.SG_SSH_HOST }} >> ~/.ssh/known_hosts
      - name: Rsync del tema
        run: |
          rsync -az --delete \
            -e "ssh -i ~/.ssh/id -p ${{ secrets.SG_SSH_PORT }}" \
            ./codigo-color-child/ \
            ${{ secrets.SG_SSH_USER }}@${{ secrets.SG_SSH_HOST }}:${{ secrets.SG_THEME_PATH }}/
      - name: Subir llms.txt (raíz pública)
        run: |
          rsync -az -e "ssh -i ~/.ssh/id -p ${{ secrets.SG_SSH_PORT }}" \
            ./llms.txt \
            ${{ secrets.SG_SSH_USER }}@${{ secrets.SG_SSH_HOST }}:${{ secrets.SG_THEME_PATH }}/../../../llms.txt
      - name: Purga Cloudflare
        run: |
          curl -s -X POST \
            "https://api.cloudflare.com/client/v4/zones/${{ secrets.CF_ZONE_ID }}/purge_cache" \
            -H "Authorization: Bearer ${{ secrets.CF_API_TOKEN }}" \
            -H "Content-Type: application/json" \
            --data '{"purge_everything":true}'
```

- `--delete` mantiene el servidor idéntico al repo (limpia archivos borrados). **No** afecta a uploads ni BD: solo a la carpeta del tema.
- `rsync` es idempotente: re-desplegar lo mismo no cambia nada.
- La ruta de `llms.txt` se ajustará a la raíz pública real de SiteGround en la ejecución.

### C.4 Alternativa manual documentada (sin Actions)

Si se prefiere empezar sin automatización: **SiteGround Git** (Site Tools → Git) o **SFTP**: subir `codigo-color-child/` a `wp-content/themes/` y `llms.txt` a la raíz, y purgar cachés a mano (F). Mismo resultado, más pasos manuales.

---

## D. CONEXIÓN CON WORDPRESS

1. El deploy deja el tema en `wp-content/themes/codigo-color-child/`.
2. **Primera vez:** en **Apariencia → Temas**, activar «Código Color Child» (requiere Hello Elementor + Elementor Pro ya instalados).
3. Despliegues posteriores **no** requieren reactivar: rsync actualiza los archivos y la web usa la versión nueva tras la purga de cachés.
4. Verificar que el schema aparece (ver I) y que las clases `cc-*` pintan (CSS cargado).

---

## E. CLOUDFLARE Y SITEGROUND (configuración compatible — Fase 0)

| Plataforma | Ajuste | Valor |
|------------|--------|-------|
| **SiteGround** | Speed Optimizer | **Único** plugin de caché (no instalar otro) |
| SiteGround | Minificación JS | **Excluir** `cc-*.js`, `gsap.min.js`, `ScrollTrigger.min.js` |
| SiteGround | Staging | Activado para probar antes de producción (G) |
| **Cloudflare** | Auto Minify | Desactivado para JS (evita romper GSAP) |
| Cloudflare | **Rocket Loader** | **OFF** (rompe el JS de Elementor/GSAP) |
| Cloudflare | Caching | Standard; respeta cache-busting por `filemtime` del tema |
| Cloudflare | APO (opcional) | Solo si se valida que no sirve HTML cacheado problemático |

> Estos ajustes evitan los dos riesgos conocidos de Fase 1 (minificación que rompe GSAP, Rocket Loader que rompe Elementor).

---

## F. PURGA DE CACHÉS (orden obligatorio)

Tras **cada** despliegue de código, purgar **en este orden** (Fase 0):

```
1. Elementor   → Elementor → Herramientas → Regenerar CSS y datos
2. SiteGround  → SG Optimizer → Purgar caché (Dynamic + File-based)
3. Cloudflare  → Purge Everything (o por URL)
```

- El paso 3 lo hace el workflow automáticamente (C.3). Los pasos 1-2 se automatizan vía WP-CLI en la ejecución si hay acceso; si no, se hacen desde el panel.
- **Cache busting:** el tema versiona cada CSS/JS por `filemtime`, así que un archivo cambiado fuerza recarga aunque la caché no se purgue del todo. La purga acelera la propagación.

---

## G. USO DEL STAGING DE SITEGROUND

1. Crear/actualizar el **staging** desde Site Tools (copia de producción).
2. Desplegar el tema a **staging primero** (rama/entorno de staging o deploy manual).
3. Validar allí la checklist pre-lanzamiento (H) y la verificación (I).
4. Solo si pasa, llevar a **producción** (push del staging o merge a `main`).

> Nunca se prueba por primera vez en producción. El staging es obligatorio para cambios de código relevantes.

---

## H. CHECKLIST PRE-LANZAMIENTO

**Contenido y estructura**
- [ ] Todos los módulos de la landing montados en Elementor con sus clases `cc-*` (Fase 5).
- [ ] Copy de la Fase 4 colocado; precios correctos (180/590/1290 € + regalo).
- [ ] 100 FAQs presentes en el HTML (acordeón), con anclas e IDs.
- [ ] Imágenes con ALT y `srcset`; LCP del hero sin lazy (doc 08).
- [ ] Placeholders elegantes donde aún falten fotos; retrato de Cristina en puente tipográfico si no hay imagen.

**Técnico**
- [ ] Tema activo; CSS/JS cargando (sin 404 en consola).
- [ ] Schema válido (Rich Results Test) — Organization, Person, Service, FAQPage.
- [ ] `llms.txt` accesible en `https://www.codigocolor.es/llms.txt`.
- [ ] Sin JS: el contenido sigue visible (prueba con JS desactivado).
- [ ] `prefers-reduced-motion`: la web se ve bien sin animaciones.
- [ ] SiteGround/Cloudflare configurados según E.

**SEO**
- [ ] Meta título/descalción (Rank Math) correctos.
- [ ] `robots`/sitemap OK; indexación permitida (quitar «noindex» de desarrollo).
- [ ] Canonical correcto en `/`.

---

## I. VERIFICACIÓN POST-DESPLIEGUE

1. **Core Web Vitals** (PageSpeed Insights, **móvil**): LCP < 2,5 s · CLS 0 · INP < 200 ms (presupuesto Fase 1 E.11).
2. **Rich Results Test**: el JSON-LD se detecta sin errores.
3. **Render real en móvil**: animaciones suaves (si GSAP está) o degradación limpia; nada de saltos.
4. **Search Console**: enviar sitemap, comprobar cobertura e «Inspeccionar URL» de la home.
5. **Consola del navegador**: sin errores 404 ni JS.
6. **Lighthouse**: sin alertas críticas de imágenes (formato, dimensionado, lazy).
7. **Cross-browser/dispositivo**: Chrome, Safari, Firefox; iPhone y Android medios.
8. **Formularios/CTAs**: reserva y WhatsApp funcionan; enlaces internos correctos.

---

## J. ROLLBACK (cómo deshacer)

Como el despliegue es solo de **código de tema** (sin BD), revertir es seguro:

1. **Vía Git (recomendado):** `git revert <commit>` en `main` → el workflow redepliega la versión anterior automáticamente. O `git checkout` de una etiqueta previa (`v1.0.0`) y push.
2. **Vía release:** redeploy de la última etiqueta estable con `workflow_dispatch`.
3. **Vía staging:** si SiteGround tiene copia previa, restaurar.
4. **Inmediato:** desactivar el tema y volver al anterior desde Apariencia → Temas (medida de emergencia).
5. Tras el rollback, **purgar cachés** (F).

> El contenido de Elementor no se ve afectado por un rollback de código (vive en la BD). Por eso el rollback es de bajo riesgo.

---

## K. CÓMO MANTENER ELEMENTOR EDITABLE Y NO ROMPER LA WEB

- **Nunca** editar código directamente en producción: siempre GitHub → SiteGround.
- **No** renombrar clases `cc-*` (rompen el vínculo CSS/JS — Fase 5 O).
- Cambios de **contenido** = Elementor (sin deploy). Cambios de **código** = repo (con deploy + purga).
- Antes de actualizar Elementor/plugins: probar en **staging** (riesgo Fase 1: una actualización puede alterar estructura).
- Mantener `docs/MANTENIMIENTO.md` del tema al día para el equipo no técnico.

---

## L. RUNBOOK RESUMIDO (chuleta de una página)

**Para un cambio de código:**
1. Rama → editar `codigo-color-child/...` → commit → push.
2. Probar en **staging**.
3. Merge a `main` → el deploy es automático.
4. Purga: Elementor → SiteGround → Cloudflare (Cloudflare lo hace el workflow).
5. Verificar (I). Si algo falla → `git revert` (J).

**Para un cambio de contenido:** editar en Elementor → guardar → (si hace falta) purgar caché de SiteGround/Cloudflare. **Sin tocar GitHub.**

---

## M. ENTREGABLES DE EJECUCIÓN Y BLOQUEOS

### M.1 Qué se crea al aprobar la ejecución de la Fase 7

- `.github/workflows/deploy.yml` (a partir del borrador C.3, ajustado a rutas reales).
- `.gitignore` raíz (si se decide versionar más que el tema).
- Alta de **secrets** en GitHub (C.2).
- Primer deploy a **staging** y luego a producción.
- Automatización opcional de purga Elementor/SiteGround vía WP-CLI.

### M.2 Bloqueos (datos/accesos que necesito)

1. **Accesos SSH de SiteGround** (host, puerto, usuario) y alta de la **clave pública**.
2. **Ruta exacta** del tema y de la raíz pública en el servidor.
3. **Cloudflare:** `Zone ID` + **API Token** con permiso de purga.
4. **Confirmación** de plan SiteGround con SSH/Git (GrowBig/GoGeek).
5. **Hello Elementor + Elementor Pro** instalados en el WordPress destino.
6. Decisión: ¿empezar con **GitHub Actions** (C.3) o con **subida manual** (C.4) en el primer lanzamiento?

> **Siguiente paso tras aprobar:** crear el workflow y ejecutar el primer deploy a staging. Y, en paralelo, **V1.5** (Orbe Three.js) cuando se decida.
