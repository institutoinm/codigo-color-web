# Claymation Science Studio

Animaciones 3D de plastilina (claymation / stop motion) creadas en **Blender** para
**CristinaBarriga.com** (Código Color) y el **Instituto Nacional de Micropigmentación**, con integración web
interactiva (three.js + GSAP ScrollTrigger) y contenido optimizado para SEO, GEO, AEO, CRO, SXO y AIO.

Todo el trabajo está en esta carpeta, **aislada del resto del repositorio**: no se ha modificado ningún archivo existente.

## Qué hay

| Carpeta | Contenido |
|---|---|
| `blender/clay_lib.py` | Librería bpy: material de plastilina procedural, estudio, luces, cámaras, stop motion, shape keys, horneado y exportación GLB |
| `blender/scenes/*.py` | Las tres escenas (reproducibles con un comando) |
| `blender/render.py`, `render_all.sh`, `encode.sh` | Render Cycles de secuencias 16:9 y 9:16 y codificación MP4/WebM/pósteres |
| `assets/blend/` | Archivos **.blend originales** (texturas empaquetadas) |
| `assets/glb/source/` | GLB exportados desde Blender (animación + morph targets) |
| `assets/glb/web/` | GLB optimizados para web: escritorio y `.mobile.glb` |
| `assets/video/` | Secuencias animadas: MP4 H.264 y WebM VP9, 16:9 (1280×720) y 9:16 (540×960) |
| `assets/posters/` | Pósteres WebP + JPEG por formato (y fotogramas de prueba) |
| `web/` | Motor `js/clay-stage.js`, estilos, páginas de ejemplo para ambas webs, librerías locales en `vendor/` |
| `contenido/` | Estrategia SEO/GEO/AEO/CRO/SXO/AIO, guiones, `llms.txt` de cada web |
| `docs/` | Investigación de skills, dirección artística, integración web y auditorías |
| `tools/` | Optimización y validación de GLB, copia de librerías, prueba de humo con Playwright |

## Escenas

| Escena | Web | Concepto |
|---|---|---|
| El ADN del color | CristinaBarriga.com | Subtono, valor, intensidad y contraste como pares de bases de una doble hélice |
| La profundidad exacta | INM | Capas de la piel, franja objetivo del pigmento y migración por exceso de profundidad |
| Neutralización del color | INM (y Código Color) | Complementarios: el gris azulado se corrige con naranja |

## Uso rápido

```bash
npm install
npm run vendor          # copia three.js y GSAP a web/vendor
npm run serve           # http://localhost:8080/web/
```

Regenerar desde Blender: ver `docs/03-integracion-web.md` → «Cómo regenerar todo».
Requisitos: Blender 5.x o el módulo oficial `bpy` 5.3 (`pip install bpy`, Python 3.13), ffmpeg y Node 20+.

## Pendiente del cliente

- **Documento maestro:** no estaba disponible en esta sesión. Antes de publicar hay que aplicar sus colores, tipografías,
  rutas, tono de voz y demás instrucciones (tokens `--clay-*` en `web/css/clay.css` y `PALETTE` en `clay_lib.py`).
- Validación técnica de los textos sanitarios del INM por sus formadores.
- Dominio, URL y CTA definitivos; conexión con la analítica real.
- **Higgsfield** (vídeo IA a partir de estos fotogramas) y **After Effects** no se han usado: el primero consume créditos
  de pago (requiere autorización) y el segundo exige licencia en el equipo local.
