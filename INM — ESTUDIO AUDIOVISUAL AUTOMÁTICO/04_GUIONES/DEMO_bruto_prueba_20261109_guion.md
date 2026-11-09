# GUION · DEMO_bruto_prueba_20261109

**Estado:** PENDIENTE DE APROBACIÓN  
**Bruto:** `01_BRUTOS/DEMO_bruto_prueba.mp4` (26.2 s) → montaje previsto **14.9 s** + cierre 2.8 s  
**Tema:** Así edita el estudio INM · **Para:** equipo INM · **Objetivo:** probar el editor · **Cierre/CTA:** AGENDA TU CITA

## Gancho (primeros 2 s, se entiende sin sonido)
«Así edita el estudio INM»

## Guion por momentos

| Nuevo | Original | Lo que digo | Lo que se ve | Efecto | Herramienta |
|---|---|---|---|---|---|
| 0.0–1.1 s | 0.0–1.1 s | Hola, | Cristina a cámara (9:16 centrado en rostro) | plano base; título gancho + pop | FFmpeg + ASS |
| 1.1–4.0 s | 1.4–4.4 s | esto es una prueba del editor automático del Instituto. | Cristina a cámara (9:16 centrado en rostro) | zoom alterno | FFmpeg + ASS |
| 4.0–7.9 s | 10.1–14.0 s | Hoy probamos cómo se cortan los silencios y las frases repetidas. | Cristina a cámara (9:16 centrado en rostro) | plano base | FFmpeg + ASS |
| 7.9–10.4 s | 15.4–18.0 s | Cuando digo pimiento, aparece un rópulo en pantalla. | Cristina a cámara (9:16 centrado en rostro) | zoom alterno | FFmpeg + ASS |
| 10.4–12.2 s | 18.7–20.4 s | Y cuando hablo de la piel también. | Cristina a cámara (9:16 centrado en rostro) | plano base; ★ rótulo «PIEL» + capas_piel + whoosh | FFmpeg + ASS |
| 12.2–14.9 s | 22.0–24.7 s | Al final, el cierre lleva la voz del Instituto. | Cristina a cámara (9:16 centrado en rostro) | zoom alterno | FFmpeg + ASS |
| final | — | — | Cierre institucional: INSTITUTO NACIONAL DE MICROPIGMENTACIÓN, web, email, «AGENDA TU CITA» | brillo | FFmpeg + ASS |

## Lista de cortes (lo que se quita y por qué)

| Original | Texto | Motivo |
|---|---|---|
| 5.1–5.3 s | Eh. | titubeo aislado (revisar) |
| 7.1–8.9 s | Hoy probamos cómo se cortan los silencios. | toma repetida (se queda la del 10.2 s) |
| — | (silencios) | 9 pausas detectadas; se comprimen las mayores de 0.32 s |

## Palabras con transcripción dudosa (revisa la ortografía)
«Hola,» (0.0 s), «la» (13.9 s), «voz» (14.0 s)

## Para aprobar
Si está bien, di «sí» o ejecuta: `python 12_AUTOMATIZACIONES/editar.py montar DEMO_bruto_prueba_20261109 --aprobar`
Si quieres cambios, dilo con el segundo: «en el 14 repito la frase, quédate con la segunda».
