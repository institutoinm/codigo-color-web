# Dirección artística · Plastilina científica

**Idea rectora:** escultura de taller de plastilina + laboratorio. Cada pieza parece hecha y movida a mano (huellas,
abolladuras, pose a pose), pero se ilumina y encuadra como un plano de cine, y lleva un único acento luminoso cian:
el «escáner ADN». No es infantil: los colores son minerales, el fondo es grafito y los movimientos son contenidos.

## 1. Material de plastilina (`clay_lib.clay_material`)

| Capa | Nodo | Valor | Para qué |
|---|---|---|---|
| Subsurface | Principled · Subsurface Weight | 0,18 · radio (1, 0,45, 0,25) · escala 0,035 | Translucidez de la cera: bordes cálidos y suaves |
| Rugosidad | Map Range por ruido | 0,46–0,66 | Zonas pulidas por el dedo y zonas mates |
| Variación tonal | Noise 2,2 → ColorRamp ±8 % | — | Amasado irregular, nunca un color plano |
| Poros | Noise 95, detalle 3 | 35 % de la altura | Micro-textura táctil |
| Abolladuras | Voronoi F1, escala 9 | 80 % de la altura | Presión de herramientas y yemas |
| Huellas dactilares | Wave «rings» 38, distorsión 7, enmascarada por ruido | Sólo en manchas | Huella visible a corta distancia |
| Relieve | Bump 0,32 / 0,012 | — | Suma de las tres alturas |
| Hervido | Nodo «ClayBoil» desplaza el espacio de ruido en cada pose | +0,37 por pose | Temblor de superficie del stop motion real |

Geometría: subdivisión + desplazamiento «Clouds» aplicados al mallado (`handmade`), con semillas deterministas
(`stable_seed`) para que el render, el .blend y el GLB sean idénticos.

Rendimiento: las texturas son 3D (no 4D) y Voronoi F1 (no Smooth F1); el material original en 4D tardaba 20 veces más.

## 2. Paleta (tokens en `PALETTE`)

| Token | Hex | Uso |
|---|---|---|
| grafito | `#2a2b2f` | Ciclorama |
| pizarra | `#3c4048` | Pedestales, dermógrafo |
| hueso / marfil | `#e8dfd0` / `#efe6d6` | Cadena de ADN, peanas |
| arcilla / terracota | `#b8644a` / `#a24f38` | Cadena de ADN, acentos cálidos |
| ocre · azul acero · ciruela · salvia | `#c4913f` · `#5b6f86` · `#6c4258` · `#8c9a7e` | Polos de las dimensiones del color |
| rosa piel · dermis · hipodermis | `#d9a596` · `#c77b72` · `#e3c48d` | Corte de piel |
| cian ADN | `#7fe3e0` | Único acento luminoso (escáner, franja objetivo, eje complementario) |

Los colores de marca definitivos se sustituyen en `PALETTE` y en los tokens CSS `--clay-*` (ver documento maestro).

## 3. Luz y cámara

- **Principal:** área de 5 m, cálida (#ffe7cf), arriba a la izquierda → sombras muy suaves.
- **Relleno:** área de 6 m, fría y al 18 %.
- **Contra:** área de 2 m, cian al 55 % → recorta la silueta y aporta el toque futurista.
- **Cenital:** suave al 15 %.
- **Fondo:** ciclorama de plastilina grafito, sin horizonte visible.
- **Color:** AgX «Medium High Contrast» en Blender; Neutral Tone Mapping en la web (respeta el color de la plastilina).
- **Cámaras:** 40–62 mm, f/4, enfoque en el sujeto, travelling lento con suavizado, siempre una versión 16:9 y otra 9:16.

## 4. Reglas de animación stop motion

1. Una pose nueva cada 2 fotogramas (24 fps → 12 poses/s), interpolación **constante**.
2. Micro-temblor de manipulación (±0,004 m, ±0,35°) en las piezas que «se tocan».
3. Squash & stretch con **shape keys** (Estirar, Aplastar, Difuminar) y entradas con rebote (`overshoot`).
4. Animación por **sustitución** cuando un objeto se transforma en otro (fusión de gotas).
5. La cámara sí se mueve con suavidad: el contraste entre cámara fluida y modelo a saltitos es la firma visual.

## 5. Las tres escenas

| # | Escena | Web | Concepto profesional | Duración |
|---|---|---|---|---|
| 01 | El ADN del color | CristinaBarriga.com | Subtono, valor, intensidad y contraste como pares de bases | 5 s (61 poses) |
| 02 | La profundidad exacta | Instituto Nacional de Micropigmentación | Capas de la piel, franja objetivo y migración por exceso de profundidad | 6 s (73 poses) |
| 03 | Neutralización del color | INM (y válida para Código Color) | Complementarios en el círculo cromático: azul + naranja = neutro | 5 s (61 poses) |

> **Revisión técnica pendiente:** los textos de la escena 02 son divulgativos y prudentes, pero deben validarlos
> los formadores del INM antes de publicarse.
