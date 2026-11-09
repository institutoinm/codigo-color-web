# CÓMO FUNCIONA · Estudio audiovisual automático del INM

> Si algún día falta algo, escribe a Claude: **«Lee COMO-FUNCIONA.md y déjalo todo listo»**.
> Claude ejecutará `python 12_AUTOMATIZACIONES/preparar.py`, que comprueba e instala lo que falte.

## La idea en una frase
Grabas, dejas el vídeo en **01_BRUTOS**, le escribes cuatro líneas a Claude y te devuelve un **guion con la lista de cortes**. Cuando dices «sí», monta el vídeo: cortado, reencuadrado en vertical, con color corregido, subtítulos palabra a palabra, rótulos animados en las palabras clave, efectos de sonido, cierre del INM, sonido a −14 LUFS, portada, subtítulos editables, proyecto editable e informe de calidad. **Nunca publica nada.**

## Para cada vídeo (texto 4 de la guía, adaptado)
```
Edita [nombre del vídeo / el último] siguiendo mis reglas de edición.
Va de [el tema en una frase] y es para [quién lo va a ver]. Lo quiero para [que me escriban / que me sigan / que pidan cita].
Que dure como mucho [segundos] y que acabe con [AGENDA TU CITA / comenta PALABRA / link en la bio].
Solo para este vídeo: [opcional: texto detrás de mí, mini-Cristina, sin música, zoom de impacto…]
```
Claude ejecutará, por debajo:

| Paso | Comando | Qué deja |
|---|---|---|
| 1. Analizar | `python 12_AUTOMATIZACIONES/editar.py analizar NOMBRE.mp4 --tema "…" --para "…" --objetivo "…" --cta "…" --max 60` | Copia en `06_PROYECTOS/<id>/`, transcripción, **guion en `04_GUIONES/`** |
| 2. Tú revisas | lees el guion | dices «sí» o corriges («en el 14 repito la frase…», «pone pimiento, es pigmento») |
| 3. Montar | `python 12_AUTOMATIZACIONES/editar.py montar <id> --aprobar [--corregir "pimiento=pigmento"]` | `08_FINALES/<id>_vN.mp4`, portada, SRT/ASS, EDL, informe QC |
| 4. Efectos extra | `python 12_AUTOMATIZACIONES/vfx.py texto-detras|mini|crash-zoom|particulas|dividida …` | `07_RENDERS/vfx/` |
| 5. Rótulos Remotion | `python 12_AUTOMATIZACIONES/remotion_render.py TituloINM --props '{"titulo":"…"}' --salida …` | MP4 o MOV con transparencia |

Atajo: `python 12_AUTOMATIZACIONES/editar.py ultimo` analiza el último vídeo que hayas dejado en 01_BRUTOS.

## Qué hace el editor por dentro (verificado con un bruto de prueba)
1. **No toca el original**: lo copia y comprueba su huella SHA-256 antes y después.
2. **Transcribe en local** con faster-whisper (sin internet, gratis), con el tiempo de cada palabra.
3. **Limpia**: silencios > 0,32 s, muletillas («eh», «em»… y «vale/pues/bueno» si van sueltas), titubeos aislados y **tomas repetidas** (se queda la última completa).
4. **Guion por momentos**: segundo nuevo, segundo original, lo que dices, lo que se ve, efecto y herramienta + lista de cortes y palabras dudosas. **No sigue sin tu «sí».**
5. **Imagen**: reencuadre 9:16 centrado en tu cara (detector YuNet), balance de blancos medido (máx. ±6 %), leve contraste/saturación, zoom alterno 1,07 entre cortes y zoom de impacto 1,14 en el momento estrella.
6. **Gráficos** (Montserrat): gancho en los 2 primeros segundos, subtítulos de ≤3 palabras con la palabra actual resaltada, rótulo + partículas cuando dices una palabra clave (pigmento, piel, cejas, areola, riesgo…). **Cada texto se coloca donde no hay cara**, medido fotograma a fotograma.
7. **Sonido**: voz con filtro de graves y compresión suave, whoosh/impacto/pop/brillo propios, música **solo si tiene archivo de licencia**, con *ducking* bajo tu voz, masterizado en 2 pasadas a −14 LUFS / −1 dBTP.
8. **Cierre institucional**: nombre del INM, web, correo y CTA. El teléfono **solo** si está verificado en la ficha.
9. **Entregables**: MP4 H.264/AAC 1080×1920, `09_PORTADAS/…_portada.jpg`, `10_SUBTITULOS/….srt` y `.ass`, `06_PROYECTOS/<id>/….edl` (se abre en Premiere/DaVinci), `plan.json`.
10. **Control de calidad** (`11_INFORMES/…_QC.md`): formato, decodificación completa, fotogramas, A/V, LUFS, negros/congelados, **texto sobre cara**, **sincronía de subtítulos re-transcribiendo el audio final**, palabras dudosas, marca, música y parecido con los 5 vídeos anteriores.
11. **Versiones**: cada corrección crea `_v2`, `_v3`… sin borrar la anterior.

## Carpetas
| Carpeta | Para qué |
|---|---|
| 01_BRUTOS | Tus vídeos tal cual. Nunca se modifican. |
| 02_REFERENCIAS | 3–6 vídeos que te gustan, para estudiar estilo (`estudiar_referencias.py`). |
| 03_ESTILO_INM | `estilo_inm.json` (lo que leen los scripts) y `BIBLIOTECA-VFX.md`. |
| 04_GUIONES | Guiones por momentos para aprobar. |
| 05_RECURSOS | Fuentes, efectos de sonido propios, logo oficial, música con licencia, VFX. |
| 06_PROYECTOS | Un proyecto por vídeo: copia, transcripción, plan, ASS, EDL, montaje intermedio. |
| 07_RENDERS | Renders intermedios y pruebas de VFX. |
| 08_FINALES | Vídeos terminados `_vN`, siempre **PENDIENTES DE APROBACIÓN**. |
| 09_PORTADAS | Portadas 1080×1920. |
| 10_SUBTITULOS | SRT y ASS editables. |
| 11_INFORMES | QC, estado de herramientas, registro de errores. |
| 12_AUTOMATIZACIONES | Los scripts. |
| _HERRAMIENTAS | Entorno Python, modelos, Remotion, HyperFrames, guías clonadas. No hace falta abrirla. |

## Lo que todavía necesita a Cristina
- **Colores HEX y logotipo oficiales** del INM (no estaban accesibles; no se inventan). Ver ESTILO-INM.md.
- **Teléfono oficial** verificado para el cierre.
- **Música con licencia** en `05_RECURSOS/musica` (o añadirla desde la biblioteca de Instagram al publicar).
- **3–6 vídeos de referencia** en `02_REFERENCIAS` y la entrevista de estilo.
- **Aprobar** cada guion y cada vídeo. Publicar es siempre decisión tuya.
