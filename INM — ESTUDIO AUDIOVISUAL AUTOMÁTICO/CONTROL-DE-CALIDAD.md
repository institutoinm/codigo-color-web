# CONTROL DE CALIDAD

Cada vídeo montado pasa `qc.py` automáticamente → `11_INFORMES/<id>_vN_QC.md` (+ `.json`).
Veredictos: **APTO**, **APTO CON AVISOS**, **NO APTO** (no se entrega hasta corregirlo). Estado siempre: **PENDIENTE DE APROBACIÓN DE CRISTINA**.

## Comprobaciones automáticas (medidas sobre el archivo final)
| Área | Comprobación | Criterio |
|---|---|---|
| Formato | 1080×1920, H.264, AAC, yuv420p | Exacto; si no, NO APTO |
| Reproducción | Decodificación completa con FFmpeg + conteo de fotogramas | Sin errores |
| Sincronía A/V | Duración vídeo vs audio | ≤ 0,07 s |
| Sonido | LUFS integrado y pico verdadero (EBU R128) | −14 ± 1,5 LUFS; ≤ −0,5 dBTP |
| Imagen | Tramos negros y congelados | Avisar |
| Composición | Rostros (YuNet, umbral 0,85) frente a cada caja de texto en su intervalo | 0 conflictos; si hay, NO APTO |
| Subtítulos | Re-transcripción del audio final y comparación con los tiempos de los subtítulos | Desfase mediano ≤ 0,12 s |
| Ortografía | Palabras con baja confianza o desconocidas | Lista para revisar |
| Marca | Colores, logo y teléfono verificados | Aviso si no |
| Licencias | Música con archivo `.licencia.txt` | Aviso si no hay música con licencia |
| Originalidad | Efecto estrella y efectos frente a los 5 vídeos anteriores aprobados | Aviso si similitud > 0,7 o mismo efecto estrella |
| Original intacto | SHA-256 del bruto antes/después | Registrar si cambia |

## Revisión humana obligatoria (no se puede automatizar con garantías)
- [ ] Sin sonido, en los dos primeros segundos se entiende de qué va.
- [ ] Subtítulos sin una falta, castellano de España, términos clínicos y nombres bien escritos.
- [ ] Nada tapa cara, **manos**, instrumentos ni zona de tratamiento.
- [ ] La voz se oye por encima de todo; sin cortes bruscos.
- [ ] Animaciones coherentes con lo que se dice; **precisión anatómica** revisada.
- [ ] Sin deformaciones en mini-Cristinas/duplicaciones; identidad de Cristina intacta.
- [ ] Ninguna simulación presentada como paciente real; ningún dato sin fuente.
- [ ] Música, imágenes y stock con licencia documentada.
- [ ] Identidad corporativa (logo/colores oficiales) correcta.
- [ ] Distinto de los cinco vídeos anteriores.
- [ ] Visto entero **en el móvil**.

## Informes ya generados (pruebas)
| Archivo | Veredicto | Notas |
|---|---|---|
| `PRUEBA_INM_5s_v1` (FFmpeg) | APTO CON AVISOS | 150/150 fotogramas, −14,0 LUFS, SFX en su sitio; avisos: marca sin verificar, sin música |
| `PRUEBA_INM_5s_REMOTION_v1` | APTO CON AVISOS | Igual; generado con Remotion |
| `DEMO_bruto_prueba_20261109_v1` | **NO APTO** | Texto sobre la cara en 17 muestras → corregido |
| `DEMO_bruto_prueba_20261109_v2` | APTO CON AVISOS | 0 conflictos, sincronía 0,00 s, −14,0 LUFS |
