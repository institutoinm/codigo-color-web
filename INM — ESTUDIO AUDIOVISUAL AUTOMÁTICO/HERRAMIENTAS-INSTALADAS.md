# HERRAMIENTAS INSTALADAS Y VERIFICADAS (09/11/2026, contenedor Linux de pruebas)

«Verificada» = se ha ejecutado aquí y ha producido un resultado comprobado, no solo instalada.

| Herramienta | Versión | Licencia | Para qué | Verificación real |
|---|---|---|---|---|
| FFmpeg / FFprobe | 6.1.1 | LGPL/GPL | Cortes, color, subtítulos, mezcla, exportación | Prueba 5 s y montaje DEMO completos |
| Node.js | 22.23.4 | MIT | Remotion e HyperFrames | — |
| Python | 3.13 (venv aislado) | PSF | Scripts del estudio | Todos los scripts ejecutados |
| faster-whisper | 1.2.1 (modelo `small`, int8, CPU) | MIT (modelo Whisper: MIT) | Transcripción local palabra a palabra | 53 palabras con tiempos; re-transcripción del final: desfase mediano 0,00 s |
| rembg | 2.0.87 + `u2net_human_seg` | MIT | Rotoscopia: texto detrás, mini-Cristina | `vfx.py texto-detras` y `mini` renderizados |
| OpenCV + YuNet | 5.0.0.93 / 2023mar | Apache 2.0 / MIT | Localizar caras (no identifica) para no taparlas | Detectó el falso positivo de los parches y se corrigió el umbral a 0,85 |
| Remotion | 4.0.542 (+ React 18.3.1) | **Remotion License** | Rótulos, contadores, transiciones con código | `TituloINM` 1080×1920 renderizado, normalizado y QC apto |
| Remotion skills | repo clonado | MIT | Guías para Claude | Leídas (incl. `remotion-license`) |
| HyperFrames | 0.9.26 (npx) | Apache 2.0 | Rótulos/gráficos en HTML → vídeo | Render 1080×1920 10 s (`07_RENDERS/PRUEBA_hyperframes_10s.mp4`) |
| Media Use (skill de HyperFrames) | en el repo | Apache 2.0 | Música/SFX/voz/imágenes | **No activado**: el catálogo HeyGen exige iniciar sesión (cuenta) → requiere aprobación |
| reels-montage / IT Reelsmaker | repo clonado (plugin `it-reelsmaker`) | MIT | Guía de montaje que inspiró el flujo | Leído; ver «Instrucciones desactualizadas» |
| yt-dlp | 2026.10.26 | Unlicense | Bajar referencias para estudiar estilo | `--version` OK; descargas no probadas (red del contenedor) |
| Montserrat | 5 pesos TTF | SIL OFL 1.1 | Tipografía INM | Ñ, tildes, ¿¡ comprobados |
| pyspellchecker | 0.9.1 | MIT | Lista orientativa de palabras dudosas | — |
| Piper + voz es_ES «davefx» | 1.8.0 | GPL / CC (ver ficha del modelo) | **Solo** para crear el bruto de prueba | No se usa en vídeos del INM |
| scikit-image | 0.26.0 | BSD | Imagen de prueba (foto NASA, dominio público) | — |

## Licencia de Remotion (importante)
Gratis para particulares, entidades sin ánimo de lucro y **empresas de hasta 3 empleados**. Con **4 o más personas** en total hace falta *Company License* (remotion.pro). **Pendiente de que Cristina confirme** el tamaño del INM. Si hiciera falta licencia y no se compra, el estudio funciona igual: todo lo esencial (subtítulos, rótulos, partículas, cierre) está hecho con FFmpeg + ASS; Remotion es opcional (`remotion_render.py`).

## Instrucciones desactualizadas de la guía (PDF «Deja de editar tus reels») y alternativa aplicada
| La guía dice | Realidad hoy | Qué se ha hecho |
|---|---|---|
| reels-montage «no es un programa, es una guía en ruso» | Ahora es un *marketplace* de plugins de Claude Code (`it-reelsmaker`), README en inglés (y ruso), con scripts y Remotion | Se ha clonado y leído; el estudio implementa su flujo (corte por voz, plan de cortes aprobado antes de cortar, caras sin tapar, −14 LUFS) en scripts propios en castellano |
| «Cowork hace todo; la web no sirve» | El propio plugin dice que Cowork sin acceso al ordenador no puede ejecutarlo; hace falta Claude Code o Cowork con carpeta conectada | Instaladores para Windows/Mac + `CLAUDE.md` en la carpeta |
| «Remotion: licencia si sois 4 o más» | Correcto (gratis hasta 3 empleados) | Documentado arriba |
| «Media Use viene con HyperFrames» | Es una *skill* del repo; su catálogo musical pide cuenta HeyGen | No se ha creado cuenta |
| HyperFrames carga GSAP desde CDN | En redes restringidas falla el render | GSAP servido en local desde npm |
| faster-whisper + PyAV recientes | `TypeError: metadata_errors` al abrir audio | Audio decodificado con FFmpeg (ver SOLUCION-DE-ERRORES.md) |
| «todo gratis» | Cierto para lo instalado; Higgsfield/Genjutsu, stock y música comercial son de pago o requieren cuenta | Marcado como «requiere aprobación» en BIBLIOTECA-VFX.md |
