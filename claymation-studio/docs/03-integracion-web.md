# Integración web · scroll, toque, botones y cámara

## Arquitectura

```
Blender (bpy) ──► .blend (original, materiales procedurales)
      │
      ├─► GLB fuente (texturas horneadas: color + normales, animación escalonada, shape keys)
      │       └─► gltf-transform: resample · simplify · meshopt · WebP → GLB web + GLB móvil
      │
      └─► Cycles: secuencias PNG 16:9 y 9:16 ──► MP4 H.264 + WebM VP9 + pósteres WebP/JPEG
                                                   (respaldo sin WebGL, movimiento reducido, redes sociales)

Página HTML (textos, póster, vídeo)  ──►  clay-stage.js (three.js + GSAP ScrollTrigger) añade el 3D encima
```

## Interacciones

| Interacción | Implementación | Por qué |
|---|---|---|
| **Scroll** | `ScrollTrigger` sobre cada capítulo (n pantallas de alto, n−1 de recorrido). El paso *i* está centrado en progress = i/(n−1), alineado con su tarjeta de texto; cada paso tiene su rango de fotogramas y su encuadre (`web/js/scenes.js`). El suavizado lo aporta la cámara. | El usuario controla el ritmo de la explicación. |
| **Pose a pose** | El fotograma se redondea a múltiplos de 2 → 12 poses/s también en la web. | Coherencia con el stop motion de Blender. |
| **Hervido** | Cada 1/12 s se desplaza ligeramente el mapa de normales y su intensidad. | La plastilina «respira» incluso en pausa. |
| **Cámara cinematográfica** | Interpolación suave entre encuadres; en vertical se aleja automáticamente para que todo quepa. | Movimiento fluido frente al modelo a saltitos. |
| **Toque / arrastre** | Pointer Events con `touch-action: pan-y`: el arrastre horizontal gira la escena (±34°) y el vertical sigue haciendo scroll. Doble clic: recentrar. | Funciona igual con ratón, dedo y lápiz. |
| **Tocar una pieza** | Raycaster sobre las piezas con datos `extras` exportados desde Blender (`dimension`, `polo`, `profundidad`, `papel`). Panel `aria-live`. | Explicación a demanda, sin saturar la pantalla. |
| **Botones de capítulo** | `ScrollToPlugin` lleva al paso; `aria-current` marca el activo. | Atajos para quien no quiere hacer scroll. |
| **«Ver completa»** | Desplaza la página hasta el final del capítulo en 9 s; se interrumpe en cuanto la persona hace scroll (`autoKill`). | Modo «reproducir» sin perder la sincronía ni el control. |
| **Teclado** | El lienzo es enfocable; flechas para girar. | Accesibilidad (WCAG 2.1.1). |

## Matriz de respaldo

| Situación | Qué se muestra |
|---|---|
| WebGL disponible | Póster inmediato → GLB al acercarse al capítulo (`IntersectionObserver`, 300 px) → fundido al 3D |
| Móvil o dispositivo modesto (≤ 4 GB / ≤ 4 núcleos) | GLB `.mobile.glb` (mitad de polígonos, texturas 256 px), sin antialias ni sombras en gama baja |
| `prefers-reduced-motion` | Sin 3D: vídeo con controles, en pausa, y textos debajo (se evalúa al cargar la página) |
| Save-Data | Sin 3D: vídeo con controles, sin reproducción automática |
| Error al cargar el GLB | Ese capítulo pasa a vídeo con controles y se libera el contexto WebGL |
| Sin WebGL | Vídeo silenciado en bucle (o en pausa si Save-Data) con controles |
| Sin JavaScript | Póster `<picture>` 16:9 / 9:16 y todos los textos (el contenido nunca depende del 3D) |

## Presupuesto de rendimiento

| Recurso | Escritorio | Móvil |
|---|---|---|
| GLB por escena | 0,56–0,87 MB | 0,39–0,67 MB |
| three.js + GLTFLoader + meshopt (sin minificar / gzip) | ≈ 1,3 MB / ≈ 300 kB | igual |
| GSAP + ScrollTrigger + ScrollTo | ≈ 115 kB / 45 kB | igual |
| Render | Sólo cuando cambia la cámara o la pose, y a 12 fps en reposo por el «hervido»; nada fuera de pantalla | DPR máx. 1,5 |

Para producción se recomienda empaquetar con Vite (tree-shaking de three.js) y servir con Brotli.

## Despliegue

1. Copiar `web/` y `assets/glb/web`, `assets/video/*.mp4|webm`, `assets/posters/*.webp|jpg` manteniendo la relación de rutas
   (o ajustar las rutas `../../assets/` de las páginas).
2. Servir `.glb` como `model/gltf-binary` y `.webm` como `video/webm`.
3. Cabeceras: `Cache-Control: public, max-age=31536000, immutable` para GLB, vídeo y pósteres (cambiar el nombre al actualizarlos).
4. Conectar `window.dataLayer` (eventos `clay_*`) con la analítica existente.

## Alternativa React Three Fiber

Si alguna web usa React, la misma escena se monta así (la lógica de scroll sigue en GSAP):

```jsx
import { Canvas, useFrame } from "@react-three/fiber";
import { useGLTF, useAnimations } from "@react-three/drei";

function Clay({ url, progress, end }) {
  const { scene, animations } = useGLTF(url, false, true); // meshopt activado
  const { mixer, actions } = useAnimations(animations, scene);
  useFrame(() => {
    const frame = Math.round((progress.current * end) / 2) * 2; // 12 poses/s
    Object.values(actions).forEach((a) => { a.play(); a.paused = true; a.time = frame / 24; });
    mixer.update(0);
  });
  return <primitive object={scene} />;
}
```

## Cómo regenerar todo

```bash
# 1. Blender (módulo oficial bpy 5.3 o Blender 5.x: blender -b -P <script>)
python blender/scenes/adn_del_color.py
python blender/scenes/capas_de_la_piel.py
python blender/scenes/neutralizacion_color.py
# 2. Vídeos y pósteres (reanudable)
bash blender/render_all.sh
# 3. Web
npm install && npm run vendor && npm run glb:web && npm run glb:validate
npm run serve   # http://localhost:8080/web/
npm test        # prueba de humo con Playwright
```
