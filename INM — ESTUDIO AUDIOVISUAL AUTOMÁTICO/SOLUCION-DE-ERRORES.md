# SOLUCIÓN DE ERRORES

Registro automático: `11_INFORMES/registro_errores.log` (fecha · contexto · error · recuperación).

## Errores encontrados al construir el estudio y cómo se resolvieron
| Problema | Causa | Solución aplicada |
|---|---|---|
| faster-whisper no descargaba el modelo | La red del entorno bloqueaba Hugging Face (y su CDN `us.aws.cdn.hf.co`) | Se permitieron esos hosts en el entorno; `HF_HUB_DISABLE_XET=1` |
| `TypeError: open() got an unexpected keyword argument 'metadata_errors'` | PyAV 19 rompe `faster_whisper.decode_audio` | `comun.audio_16k()` decodifica con FFmpeg y pasa el array |
| La escena 2 de la prueba salía morada | `blend` de FFmpeg mezclaba en YUV | Mezcla en `gbrp` |
| Prueba a −10,9 LUFS | Efectos sin normalizar | Ajuste de ganancia; QC lo vigila (±1,5 LU) |
| El bruto de prueba no terminaba | `-shortest` no corta con `-loop 1` + `filter_complex` | Duración explícita `-t` |
| Texto sobre la cara (QC NO APTO en v1) | YuNet detectaba parches redondos como caras (0,71–0,79) y se unían todas en una caja | Umbral 0,85 y comprobación cara a cara |
| `Object of type bool is not JSON serializable` | Valores numpy en el informe | Serializador `_js` |
| Remotion entregaba `yuvj420p` y −12,6 LUFS | Rango completo y sin normalizar | `remotion_render.py` convierte a yuv420p y normaliza en 2 pasadas |
| HyperFrames: `ERR_TUNNEL_CONNECTION_FAILED` gsap | CDN jsdelivr bloqueado | GSAP local desde npm |
| El QC no leía la duración del vídeo | `ffprobe` devolvía «5.000000,» | Parseo robusto; si no puede medir, falla en vez de aprobar |
| Vocabulario como *hotwords* empeoró la transcripción | Sesgo del modelo («Eh.» → «Ed.») | Solo `initial_prompt`; titubeos aislados se cortan por regla |

## Lo que puede pasar al usarlo
| Lo que ves | Qué escribir a Claude |
|---|---|
| Se atasca instalando | «Explícame qué falla sin tecnicismos y prueba otra forma» (mira `registro_errores.log`) |
| `ffmpeg no se reconoce` (Windows) | Cierra y vuelve a abrir la terminal tras instalar; o reinstala con `winget install Gyan.FFmpeg` |
| Palabras mal transcritas | Corrige en el guion: `montar <id> --aprobar --corregir "pimiento=pigmento"`; o analiza con `--modelo medium` |
| Subtítulos desfasados | «Van medio segundo tarde: vuelve a sincronizarlos con la transcripción» |
| Toma repetida que se escapó | «En el segundo 14 repito la frase: quédate con la segunda» |
| La música tapa la voz | «La voz tiene que oírse clarísima: baja la música» |
| El texto tapa cara o manos | «Pasa los subtítulos arriba en todo el vídeo» |
| Recargado | «Quita la mitad de las animaciones» |
| Remotion falla al renderizar | Primera vez: necesita internet para su navegador; en Windows puede tardar |
| rembg recorta también objetos que sujetas | Limitación del modelo: usa la versión «ventana» o graba sobre fondo liso |
| Se acaba el uso de Claude a mitad | Normal en vídeo: los scripts hacen el trabajo pesado; retoma con «sigue con <id>» |
| Empiezas otra tarea y no encuentra nada | «Lee COMO-FUNCIONA.md y déjalo todo listo» |

## Errores pendientes / limitaciones conocidas
- **Manos**: el QC solo detecta caras. Las manos e instrumentos se revisan a ojo (lista de revisión humana).
- **Ortografía**: lista orientativa; el diccionario automático no conoce todos los tecnicismos.
- **Colores y logo oficiales**: sin verificar → aviso en cada QC.
- **Transcripción**: probada con voz sintética; con la voz real de Cristina conviene validar el modelo `small` frente a `medium` en el primer vídeo.
- **HyperFrames** envía telemetría de uso por defecto; desactivar con `DO_NOT_TRACK=1`.
- **Equipo Windows**: los instaladores no se han podido ejecutar en el portátil desde la nube (la carpeta de Remote Control no estaba disponible para sesiones en la nube).
