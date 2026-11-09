# AUTOMATIZACIONES (12_AUTOMATIZACIONES)

Todos los scripts usan rutas relativas a la carpeta del estudio (se puede mover), ejecutan los comandos sin shell y registran los fallos en `11_INFORMES/registro_errores.log`. Ninguno deja procesos en segundo plano ni publica nada.
Ejecutar siempre con el Python del entorno: `_HERRAMIENTAS/venv/bin/python` (Mac/Linux) o `_HERRAMIENTAS\venv\Scripts\python.exe` (Windows).

| Script | Qué hace | Comando | Probado |
|---|---|---|---|
| `comun.py` | Rutas, ffprobe, registro de errores, versiones `_vN`, colores ASS, audio 16 kHz | (librería) | Sí |
| `preparar.py` | Descarga modelos, clona guías, instala Remotion, plantilla HyperFrames; `--comprobar` solo revisa | `preparar.py [--comprobar]` | Sí: TODO LISTO |
| `sfx.py` | Crea whoosh, impacto, pop, brillo y tic por síntesis (material propio) | `sfx.py` | Sí |
| `prueba_5s.py` | Prueba real 5 s 1080×1920: título animado, transición, partículas, 3 SFX; verifica fotogramas y sincronía de SFX | `prueba_5s.py` | Sí: 150/150 fotogramas, SFX a 0,15/2,28/2,80 s, −14,0 LUFS |
| `editar.py` | Editor automático en 2 fases (analizar → guion; montar → vídeo + entregables + QC) | ver COMO-FUNCIONA.md | Sí, con bruto de prueba |
| `qc.py` | Control de calidad de cualquier MP4 | `qc.py VIDEO.mp4 [--plan plan.json]` | Sí |
| `vfx.py` | Biblioteca VFX local: texto-detras, mini, dividida, crash-zoom, particulas | `vfx.py <efecto> …` | Sí, los 5 |
| `remotion_render.py` | Renderiza composiciones Remotion y las normaliza (yuv420p, −14 LUFS) o con alfa (ProRes 4444) | `remotion_render.py TituloINM --salida …` | Sí |
| `estudiar_referencias.py` | Mide ritmo, cortes, paleta, LUFS, palabras/min y hace hoja de contactos de 02_REFERENCIAS | `estudiar_referencias.py` | Sí (con un vídeo propio de prueba) |
| `crear_bruto_prueba.py` | Bruto sintético con silencios, «eh» y toma repetida (voz Piper, foto NASA) | `crear_bruto_prueba.py` | Sí |

## Composiciones Remotion (`_HERRAMIENTAS/remotion-inm/src`)
- `TituloINM` (5 s): título con muelle y desenfoque, subtítulo, barrido diagonal a segunda escena, pop + whoosh.
- `TituloINMTransparente` (2,2 s): gancho con transparencia para superponer.
- `Contador` (2,5 s): cifra animada con **fuente obligatoria** en pantalla.
Fuentes Montserrat cargadas en local (sin Google Fonts). Colores inyectados desde `estilo_inm.json`.

## Plantilla HyperFrames (`_HERRAMIENTAS/hyperframes-inm`)
Proyecto vertical 1080×1920 con GSAP local. Render: `npx --yes hyperframes@0.9.26 render _HERRAMIENTAS/hyperframes-inm -o salida.mp4`.

## Prueba de extremo a extremo realizada (bruto DEMO)
| | Resultado medido |
|---|---|
| Bruto | 26,2 s, 1920×1080 horizontal, voz sintética con pausas, «eh» y frase repetida |
| Análisis | 53 palabras; cortes: «Eh.» (titubeo) y la primera toma de «Hoy probamos cómo se cortan los silencios»; 9 pausas comprimidas |
| Montaje | 17,7 s (14,9 s + cierre 2,8 s), 1080×1920, 30 fps, H.264 High yuv420p, AAC 48 kHz, 531 fotogramas sin errores |
| Sonido | −14,0 LUFS, −0,9 dBTP |
| Subtítulos | Re-transcripción del final: 24 coincidencias, desfase mediano 0,00 s, máximo 0,12 s |
| Composición | v1: **NO APTO** (texto sobre la cara por falsos positivos del detector) → corregido → v2: 0 conflictos |
| Entregables | MP4, portada JPG, SRT, ASS, EDL, plan.json, informe QC |
