# BIBLIOTECA VFX DEL INM

Clasificación honesta de cada recurso: **LOCAL-HECHO** (implementado y probado en este estudio), **LOCAL-POSIBLE** (se puede hacer en local con herramientas instaladas o gratuitas, no automatizado aún), **GENERATIVO** (Higgsfield, Genjutsu, Kling, Runway… — de pago/cuenta), **APROBACIÓN** (requiere permiso, compra, cuenta, consentimiento o revisión clínica).
**2D/2,5D no es 3D real.** Un texto con sombra o una capa con paralaje no son un modelo 3D; el 3D real exige Blender (gratis, LOCAL-POSIBLE) o un servicio generativo.

| Recurso | Estado | Cómo | Notas |
|---|---|---|---|
| Texto detrás de Cristina | LOCAL-HECHO | `vfx.py texto-detras` (rembg u2net_human_seg) | Probado. El recorte incluye objetos que sujeta |
| Rotoscopia | LOCAL-HECHO | `vfx.Mascara` | Máscara a media resolución; bordes suaves |
| Duplicación / mini-Cristina | LOCAL-HECHO | `vfx.py mini` | Toma real reducida + sombra de contacto; rasgos sin alterar |
| Zoom cinematográfico / crash zoom | LOCAL-HECHO | `vfx.py crash-zoom`; zoom alterno/impacto en `editar.py` | Con desenfoque de movimiento |
| Pantalla dividida / comparativas A-B | LOCAL-HECHO | `vfx.py dividida` | Para técnicas, no para antes/después clínicos inventados |
| Partículas de pigmento | LOCAL-HECHO | `vfx.py particulas` y partículas vectoriales ASS en `editar.py` | Color de marca |
| Efectos sincronizados con palabras | LOCAL-HECHO | `editar.py` (`palabras_animables`) | Rótulo + partículas + SFX en la palabra exacta |
| Títulos animados / tipografía cinética | LOCAL-HECHO | ASS (FFmpeg), Remotion `TituloINM`, HyperFrames | Remotion: ver licencia |
| Contador / tarjeta con dato | LOCAL-HECHO | Remotion `Contador` | Solo con fuente verificada en pantalla |
| Transiciones (barrido, xfade) | LOCAL-HECHO | `prueba_5s.py`, Remotion | |
| Tracking de objetos (rótulo que sigue algo) | LOCAL-POSIBLE | OpenCV (CSRT/KCF) o `track.py` de reels-montage | Sin automatizar |
| Hologramas 2D (líneas, brillo, escaneo) | LOCAL-POSIBLE | Remotion/HyperFrames + capas | Se presentará como gráfico, no como 3D |
| Esquema de capas de piel (2D didáctico) | LOCAL-POSIBLE | Remotion | **APROBACIÓN** científica: epidermis/dermis/hipodermis sin profundidades inventadas |
| Escenarios cambiantes (fondo sustituido) | LOCAL-POSIBLE | rembg + fondo con licencia | Fondo de stock: licencia |
| Cámara virtual / paralaje 2,5D | LOCAL-POSIBLE | capas + zoompan / Remotion | |
| Títulos 3D reales, folículo 3D, piel 3D giratoria | LOCAL-POSIBLE (Blender) / GENERATIVO | Blender (gratuito) o Higgsfield 3D | Requiere modelado y **revisión anatómica** |
| Transiciones tipo Higgsfield (Crash/Dolly Zoom, Bullet Time, 360 Orbit, Through Object) | GENERATIVO | Higgsfield DoP / Camera Controls | Créditos de pago → **APROBACIÓN** |
| Genjutsu (restyle, sustitución de objetos, motion transfer) | GENERATIVO | Higgsfield Genjutsu | **APROBACIÓN**; no alterar rostro de Cristina |
| Mini-Cristina que camina sobre una ceja / entra en un frasco | GENERATIVO + composición | Higgsfield/Kling + rotoscopia local | **APROBACIÓN**; control de identidad y sombras |
| Simulación óptica de areolas (luz/volumen) | LOCAL-POSIBLE (esquema) | Remotion/Blender | **APROBACIÓN clínica**; nunca como resultado real; sin «discos luminosos» (doc. 05) |
| Música actual y efectos de stock | APROBACIÓN | Bibliotecas con licencia | Comprar no da derecho de sincronización |
| Voz generada | APROBACIÓN | — | Solo con autorización y en castellano peninsular |

## Las 50 escenas del documento «12 · MrBeast × Higgsfield × Hollywood»
- **Factibles ya en local** (con metraje adecuado): 7 (letras gigantes por detrás, con texto-detras), 10 y 31–33, 36 (duplicaciones/mini con la toma real), 20 (fondo congelado + objetos 2D), 22 (crash zoom hasta un macro real), 30 (texto atravesado, 2D), 37 (palabra → rótulo), 50 (cierre que se convierte en logo, cuando haya logo oficial).
- **Requieren Blender o generativo**: 1–6, 8–9, 11–19, 21, 23–29, 34–35, 38–49.
- **Requieren revisión científica antes de producir**: 41–49 (modelos de piel, folículo, colágeno, cicatriz, areola, células).

## Conectores disponibles en esta cuenta
Higgsfield aparece conectado como herramienta de Claude, pero **no se ha generado nada**: consume créditos y la norma exige aprobación expresa.
