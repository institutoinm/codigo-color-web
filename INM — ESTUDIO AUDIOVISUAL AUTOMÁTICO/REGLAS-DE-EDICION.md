# REGLAS DE EDICIÓN (texto 3 de la guía, adaptado al INM)

Síguelas enteras cada vez que Cristina pida editar un vídeo.

## Antes de tocar nada
- Lee `ESTILO-INM.md` y `03_ESTILO_INM/estilo_inm.json`. Si no están, para y avisa.
- Coge el vídeo de `01_BRUTOS` que diga, o el último si no dice cuál. **Nunca lo modifiques**: `editar.py` trabaja con una copia y comprueba la huella.
- Si falta algo para decidir, como mucho **3 preguntas**, con opciones y la que tú elegirías.

## El guion, antes de editar
- `python 12_AUTOMATIZACIONES/editar.py analizar <vídeo> --tema … --para … --objetivo … --cta … --max …`
- Enseña a Cristina `04_GUIONES/<id>_guion.md`: momentos, lo que dice, lo que se ve, efecto, herramienta y **lista de cortes**.
- **No sigas hasta que diga «sí».** Si corrige palabras: `--corregir "mal=bien"`.

## Cómo editas
1. Limpieza: silencios, huecos, muletillas («eh», «em»; «vale/pues» si van sueltas) y tomas repetidas (se queda la última completa).
2. Imagen: luz y color sin que se note; vertical 1080×1920 centrado en la cara.
3. Subtítulos palabra a palabra, sin una falta, respetando nombres y marcas, **sin tapar cara ni manos**.
4. Animaciones (FFmpeg/ASS, Remotion o HyperFrames) y recortes (rembg) solo cuando refuercen lo que dice. Entrada suave.
5. Sonido: música con licencia por debajo de la voz, efecto discreto en cada animación, −14 LUFS.
6. Un efecto estrella por vídeo, distinto de los 5 anteriores.

## Lo que nunca haces
- Inventar datos, cifras, estudios, DOI, testimonios o resultados clínicos.
- Presentar simulaciones o imágenes generadas como pacientes reales o antes/después.
- Meter logos o material de otros; usar música o stock sin licencia verificada.
- Usar algo de pago, crear cuentas o introducir credenciales sin preguntar.
- Borrar o sobrescribir archivos (cada corrección es una versión nueva).
- **Publicar.** Siempre lo decide Cristina.

## Antes de dármelo
- El QC se ejecuta solo (`11_INFORMES/<id>_vN_QC.md`). Si dice **NO APTO**, se corrige antes de entregar.
- Comprueba duración, resolución, subtítulos a tiempo, volumen, que nada tape la cara y que en los dos primeros segundos se entienda de qué va **sin sonido**.
- Guarda en `08_FINALES` con `_v1`, `_v2`… sin borrar la anterior.
- Cuéntale en tres líneas qué has hecho y qué ajustarías tú.

## Correcciones habituales (lo que puede decir Cristina → qué haces)
| Dice | Haces |
|---|---|
| «Los subtítulos van medio segundo tarde» | Mira la sincronía del QC; re-transcribe o desplaza y monta `_vN+1` |
| «En el segundo 14 repito la frase, quédate con la segunda» | Marca la primera toma como cortada en `plan.json` (o re-analiza) y monta |
| «La música no deja oír la voz» | Baja `musica_db_bajo_voz` (p. ej. −28) y monta |
| «Queda recargado» | Sube `min_separacion_rotulos_s` o baja `max_rotulos_por_10s` |
| «El texto tapa la cara o las manos» | Sube los subtítulos a la banda alta para ese vídeo; revisa manos a ojo (el detector solo mide caras) |
| «No se parece a mi estilo» | Relee ESTILO-INM.md y di qué partes no se han aplicado |
