# ESTILO INM · Ficha de estilo audiovisual

Fuentes leídas (Drive, carpeta de Instict): «05 · Prompt maestro permanente», «10 · Prompt maestro definitivo VFX» (5 nov 2026),
«11 · Vídeos reales + stock antes que IA», «12 · Norma permanente VFX» (8 nov 2026), «12 · MrBeast × Higgsfield × Hollywood»,
«INSTINCT · Música actual y rótulos sin tapar caras ni manos», «04 · Contexto maestro de Cristina Barriga».
La versión que leen los scripts es `03_ESTILO_INM/estilo_inm.json`.

> **Estado: PARCIAL.** Faltan datos de marca verificados y el estudio de 3–6 vídeos de referencia + entrevista.
> No se ha inventado ningún dato de marca: lo no verificado está marcado.

## 1. Identidad corporativa
| Elemento | Valor | Estado |
|---|---|---|
| Nombre | INSTITUTO NACIONAL DE MICROPIGMENTACIÓN (INM) | Verificado (documentos INM) |
| Web | institutonacionaldemicropigmentacion.es | Verificado (documentos INM) |
| Correo | info@institutonacionaldemicropigmentacion.es | Verificado (documentos INM) |
| Teléfono | — | **PENDIENTE**: no se muestra hasta verificarlo |
| CTA de cierre | «AGENDA TU CITA» | Del prompt maestro 05 |
| Logotipo oficial | — | **PENDIENTE**: hay «logo with tagline.png» y «Logo white version.png» en una carpeta mixta del Drive; sin confirmar que sean los oficiales. Colocar el bueno en `05_RECURSOS/logo/logo_inm.png` y marcar `logo_verificado: true` |
| Colores | «azules corporativos» + blanco | **PENDIENTE** de los HEX del manual. Provisionales (azul marino neutro): primario #0D2B4E, secundario #2F6DB5, resalte #8FC3FF, contorno #08182C. El QC avisa en cada vídeo mientras no se verifiquen |
| Tipografía | **Montserrat** (Black títulos, ExtraBold subtítulos, SemiBold textos) | Verificado en los prompts; instalada (OFL) |
| Conflicto de manuales | El documento 05 menciona «conflicto entre manuales» | Pendiente de resolver por Cristina |

## 2. Subtítulos (siempre, sin excepción)
- Castellano de España, fieles a la voz real; sin reformular. Revisión humana de ortografía y términos clínicos.
- Montserrat ExtraBold 76 px, blanco con contorno oscuro, **≤3 palabras / ≤22 caracteres por bloque**, máx. 2 líneas.
- La palabra que se está diciendo se resalta en el color de resalte (108 %). Entrada suave (86→100 % en 90 ms), nunca rebotes exagerados.
- Posición: banda baja (y≈1330) salvo que haya cara; se recoloca automáticamente. Zonas seguras: 250 px arriba, 420 abajo, 140 derecha.
- Entregar siempre SRT editable además del vídeo.

## 3. Ritmo
- Pausas > 0,32 s fuera; margen 0,06 s antes y 0,14 s después de cada frase.
- Zoom alterno 1,07 en cada corte (disimula los saltos) y **zoom de impacto 1,14** en el momento estrella.
- Estructura (doc. 05 y 12): gancho visual + pregunta en 0–3 s → problema → explicación con demostración → revelación → conclusión → cierre INM. 35–60 s.
- Comparar con los 5 vídeos anteriores: no repetir efecto estrella, fondo, transición ni estructura (el QC lo mide).

## 4. Animaciones y VFX
- Un **efecto protagonista** memorable por vídeo; los secundarios solo si explican.
- Efectos **ligados a palabras** (doc. 10 §5): duda→interrogación, pigmento→partículas, piel/profundidad→capas, folículo, cicatriz, color, volumen, riesgo→aviso, cejas, labios, areola. Máx. 2 rótulos cada 10 s, separados ≥3 s.
- Que entren con movimiento suave, nunca de golpe. Nada sobre cara, manos, instrumentos ni zona de tratamiento.
- Biblioteca y clasificación (local / generativo / requiere aprobación): `03_ESTILO_INM/BIBLIOTECA-VFX.md`.

## 5. Sonido
- La voz real de Cristina manda. Voces sintéticas solo con autorización expresa y en castellano peninsular.
- −14 LUFS integrados, −1 dBTP. Música a −24 dB bajo la voz con *ducking*; efectos a −16 dB.
- Música actual con licencia verificada (doc. INSTINCT): 5 candidatas con título, artista, fragmento, BPM, derechos. Si no hay licencia, se entrega sin música y con indicaciones para añadirla desde la biblioteca de Instagram.

## 6. Mini-Cristina y duplicaciones
- Se hacen con la toma real recortada (rotoscopia), sin alterar rasgos, con sombra de contacto y escala coherente.
- Variar el recurso entre vídeos. Mini-Cristina generada por IA solo con aprobación y control de identidad.

## 7. Portadas
- 1080×1920, fotograma real más nítido, degradado inferior, título en Montserrat Black, encabezado «INSTITUTO NACIONAL DE MICROPIGMENTACIÓN», logo oficial cuando esté verificado. Legible en miniatura.

## 8. Rigor científico y prohibiciones
- Nada de cifras, estudios, DOI, testimonios ni resultados inventados. Toda cifra en pantalla necesita fuente.
- Las animaciones son **esquemas didácticos**, no casos clínicos; nunca antes/después generados ni pacientes simulados presentados como reales.
- Distinguir efecto visual de regeneración biológica; no atribuir títulos médicos a Cristina.
- Lista completa en `estilo_inm.json → prohibiciones`.

## 9. Ejemplo: cómo editaría un vídeo de 30 s con esta ficha (para validar con Cristina)
| Momento | Qué pasa |
|---|---|
| 0,0–2,2 s | Gancho en Montserrat Black arriba («¿QUÉ HAY DENTRO DE UN PIGMENTO?») + pop; plano base |
| 2,2–8 s | Problema; subtítulos ≤3 palabras abajo; zoom alterno en cada corte |
| 8–9,6 s | Dice «pigmento» → **★ efecto estrella**: zoom de impacto + rótulo PIGMENTO + partículas + impacto sonoro (o texto detrás de ella) |
| 9,6–24 s | Explicación; 1–2 rótulos más ligados a palabras; respiraciones y silencios fuera |
| 24–27 s | Conclusión clara |
| 27–30 s | Cierre INM: nombre, web, correo, AGENDA TU CITA + brillo |

## Cómo se actualiza esta ficha
1. Mete 3–6 vídeos en `02_REFERENCIAS` y ejecuta `python 12_AUTOMATIZACIONES/estudiar_referencias.py`.
2. Pide a Claude la entrevista corta (una pregunta cada vez, con opciones y recomendación): subtítulos, movimiento, música, colores, arranque, cierre y lo que no soportas ver.
3. Actualiza esta ficha y `estilo_inm.json`. Lo que aparezca en un solo vídeo no cuenta como estilo.
