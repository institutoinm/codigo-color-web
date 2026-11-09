# Estudio audiovisual automático del INM — instrucciones para Claude

Esta carpeta es el estudio de edición de reels del Instituto Nacional de Micropigmentación (Cristina Barriga).

1. Antes de editar, lee `REGLAS-DE-EDICION.md` y `ESTILO-INM.md`. Si faltan herramientas: `COMO-FUNCIONA.md` → `12_AUTOMATIZACIONES/preparar.py`.
2. Flujo: `editar.py analizar` → enseña el guion de `04_GUIONES` → **espera el «sí» de Cristina** → `editar.py montar <id> --aprobar` → revisa el informe QC → cuéntale en 3 líneas qué has hecho.
3. Nunca modifiques `01_BRUTOS`, nunca borres ni sobrescribas (versiones `_vN`), nunca publiques, nunca inventes datos de marca, cifras ni resultados clínicos, nunca uses algo de pago o con cuenta sin preguntar.
4. Usa el Python del entorno: `_HERRAMIENTAS/venv/bin/python` (Windows: `_HERRAMIENTAS\venv\Scripts\python.exe`).
5. Habla con Cristina sin tecnicismos y en castellano de España.
