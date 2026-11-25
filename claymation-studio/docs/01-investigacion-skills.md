# Investigación de skills · Claymation Science Studio

Fecha: 25-11-2026 · Herramienta: skill **find-skills** (`npx skills find <consulta>`, registro público skills.sh).
Se lanzaron 21 búsquedas, una por cada capacidad pedida. Las cifras de instalaciones son las del registro el día de la búsqueda.

## Criterio de confianza

| Nivel | Regla |
|---|---|
| ✅ Fiable | Publicada por el fabricante oficial de la tecnología (GreenSock, Higgsfield, Vercel…) **o** con más de 5.000 instalaciones. |
| ⚠️ Revisar antes de usar | Entre 500 y 5.000 instalaciones, autor desconocido. |
| ⛔ Descartada | Menos de 500 instalaciones o autor sin trayectoria. Según la instrucción «no instalar herramientas de procedencia dudosa», no se instala. |

**No se ha instalado ninguna skill de terceros.** Las skills sólo aportan instrucciones; todo el trabajo se hizo con
herramientas oficiales: el módulo `bpy` 5.3 de la Blender Foundation (PyPI), el exportador glTF oficial de Blender,
`three` y `gsap` desde npm, `@gltf-transform/cli` (Don McCurdy, referencia del ecosistema glTF) y `gltf-validator` (Khronos).

## Resultados por capacidad

| Capacidad | Mejor resultado | Instalaciones | Valoración |
|---|---|---|---|
| Blender MCP | `vladmdgolam/agent-skills@blender-mcp` | 2,8K | ⚠️ Necesita Blender con interfaz abierto y el complemento MCP en el ordenador del usuario; aquí no aplica. Se sustituye por `bpy` sin interfaz, que hace lo mismo con scripts. |
| Blender Python / bpy | `freshtechbro/claudedesignskills@blender-web-pipeline` | 4,3K | ⚠️ Útil como referencia del flujo Blender→web; el resto (`blender-python-addon`, `bpy_skill`…) tiene < 120 instalaciones ⛔. |
| Claymation | `angrypenguinpng/blender-claymation-skill@blender-claymation` | 24 | ⛔ Muy poco usada. Las demás (`claymation-ad`) son plantillas de anuncios con IA, no Blender. |
| Stop motion | `arjun988/blender-skills@stop-motion-craft-style` | 698 | ⚠️ Autor desconocido. `papercraft-stop-motion-explainer` (MiniMax, 3,7K) es para vídeo IA de papel, no plastilina. |
| Materiales procedurales | `scottstts/...@threejs-procedural-materials` | 195 | ⛔ Poca adopción. El material de plastilina se ha programado desde cero. |
| Geometry Nodes | `scenario-labs/skills@scenario-blender-geometry-nodes` | 1,2K | ⚠️ |
| Escultura 3D | `scenario-labs/skills@scenario-blender-sculpting` | 1,3K | ⚠️ |
| Animación de personajes | `openmontageinc/openmontage@svg-character-animation` | 2,8K | ⚠️ Es SVG 2D, no Blender. |
| Shape keys | `el4cteo/blender-skills@blender-facial-shapekeys` | 782 | ⚠️ Orientada a caras; aquí las shape keys se generan por código. |
| Animación procedural | `scottstts/...@threejs-procedural-animation` | 187 | ⛔ |
| Three.js | `cloudai-x/threejs-skills` (animation, fundamentals, shaders, materials) | 23K–30K | ✅ |
| React Three Fiber | `cloudai-x/threejs-skills@threejs-react-three-fiber` | 9,3K | ✅ (también `vercel-labs/json-render@react-three-fiber`, 2,5K, oficial de Vercel) |
| GSAP / ScrollTrigger | `greensock/gsap-skills@gsap-scrolltrigger` | 93,5K | ✅ **Oficial de GreenSock.** También `gsap-core`, `gsap-timeline`, `gsap-performance`. |
| WebGL | `freshtechbro/claudedesignskills@threejs-webgl` | 5,5K | ✅ |
| GLB / glTF | `gamedev-skills/awesome-gamedev-agent-skills@threejs-gltf-loading` | 13,7K | ✅ |
| Higgsfield | `higgsfield-ai/skills@higgsfield-generate` (y otras) | 180K–265K | ✅ **Oficial.** Además, el conector Higgsfield ya está activo en esta cuenta. |
| After Effects | `iart-ai/motion-design-skills@after-effects` | 6,2K | ✅ por adopción, pero requiere After Effects instalado en el equipo del usuario. |
| Movimiento de cámara cinematográfico | `rfxlamia/flow@camera-movements` | 37 | ⛔ |
| Experiencias 3D web interactivas | `freshtechbro/claudedesignskills@web3d-integration-patterns` | 3,7K | ⚠️ |

## Qué permite automatizar realmente cada vía

| Necesidad | Cómo se ha resuelto aquí | Automatizable sin intervención |
|---|---|---|
| Modelos | `bpy` + `bmesh`: hélices, cápsulas, bloques biselados, esferas, ciclorama | Sí |
| Materiales de plastilina | Árbol de nodos procedural (SSS, poros, huellas, abolladuras, variación tonal) | Sí |
| Irregularidad «hecha a mano» | Subdivisión + desplazamiento de ruido aplicado al mallado | Sí |
| Iluminación | Luz principal grande y cálida, relleno frío, contra cian, cenital | Sí |
| Cámaras | 16:9 y 9:16 con profundidad de campo y travelling suavizado | Sí |
| Animación stop motion | Claves constantes cada 2 fotogramas (12 poses/s), micro-temblor, «hervido» de superficie | Sí |
| Shape keys | Generadas por código (gota: aplastar, estirar, expandir) → morph targets en GLB | Sí |
| Exportación | Horneado de color y normales → material glTF → GLB → optimización Meshopt + WebP | Sí |
| Render de secuencias | Cycles CPU, desenfoque de ruido OIDN, MP4 H.264 + WebM VP9 + pósteres | Sí |
| Blender MCP | Requiere el ordenador del usuario con Blender abierto | No en la nube |
| After Effects | Requiere licencia y equipo local | No en la nube |
| Higgsfield (Blender Studio 3D, vídeo IA) | Disponible por conector, pero **consume créditos de pago** | Pendiente de autorización |

## Recomendación

1. Usar Blender (`bpy`) como herramienta principal: todo el pipeline queda en scripts versionados y reproducibles.
2. Si se quiere instalar alguna skill para el día a día, las únicas que recomiendo son las oficiales de **GreenSock**
   (`npx skills add greensock/gsap-skills`) y **Higgsfield**, y como apoyo `cloudai-x/threejs-skills`.
3. Higgsfield puede añadir planos de vídeo IA en estilo plastilina a partir de los fotogramas de Blender
   (Cinema Studio / Genjutsu «Sculpted», «Soft 3D»), pero **sólo tras autorizar el gasto de créditos**.
