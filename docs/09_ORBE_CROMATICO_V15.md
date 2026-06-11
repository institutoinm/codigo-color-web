# 09 — ORBE CROMÁTICO (V1.5)
## Código Color · Elemento firma WebGL: especificación, implementación, activación y protocolo de medición

> **Estado:** Implementado y versionado, **DESACTIVADO por defecto** (V1 sigue intacta). Se enciende tras medir en dispositivo real.
> **Regla (Fase 1 E.1):** mejora progresiva quirúrgica. La web es premium sin él; el Orbe es la guinda, nunca un bloqueo de lanzamiento. Si no cumple presupuesto, no se publica y queda el gradiente CSS.
> **Depende de:** FASE 1 §E (estrategia Three.js, fallbacks, presupuesto), FASE 5 §G (contenedor + data-attributes), FASE 6 (child theme V1).
> **Archivos:** `assets/js/cc-color-orb.js` (módulo), hook en `assets/js/cc-scroll-animations.js`, fallback en `assets/css/cc-base.css` (`.cc-color-orb`).

---

## A. QUÉ ES

Un volumen de luz esférico con shader de gradiente fluido (ruido orgánico) en los colores de marca, con borde fresnel sutil. Respira en reposo, reacciona al cursor (desktop) y, con el scroll, vira de temperatura (cálido → frío). Es la traducción visual del método: *el color se ordena en sistema*. Aparece en el hero (mód. 1) y, opcionalmente, en miniatura en el cierre (mód. 29).

---

## B. ESTADO ACTUAL (V1)

- **Flag `orb` = `false`** en `cc-motion-config.js` → el Orbe **no** se ejecuta en producción.
- En el hero se ve el **fallback de gradiente CSS** (`.cc-color-orb`, `cc-base.css`): animado, premium, coste ~0, sin WebGL.
- El módulo Three.js está escrito y versionado, listo para encenderse cuando se decida.

---

## C. ARQUITECTURA

```
cc-scroll-animations.js  (GSAP, gobierna el scroll)
   └─ si flags.orb && webgl && !reduced-motion && CC_THEME_URI:
        import dinámico → cc-color-orb.js  →  initOrb()
        GSAP ScrollTrigger (pin del hero, scrub) → api.setProgress(0..1)
cc-color-orb.js
   └─ import dinámico → /assets/vendor/three.module.js  (si falta → no-op, queda el gradiente)
```

- **GSAP es la única fuente de verdad del scroll** (Fase 1 E.5): anima un proxy `{p:0→1}` y se lo pasa al Orbe por `setProgress`. El Orbe nunca escucha el scroll directamente.
- **Three.js carga diferido** (import dinámico), post-LCP, solo si todo lo anterior se cumple.
- El contenedor `.cc-color-orb` se marca `aria-hidden` (decorativo, sin texto SEO).

---

## D. INTERFAZ Y EDICIÓN (Elementor)

En el contenedor del hero (Fase 5 §G):

| Atributo | Efecto |
|----------|--------|
| `data-cc-orb="on" \| "off"` | Enciende/apaga el Orbe sin desplegar |
| `data-cc-orb-colors="#C4A882,#D4A853,#8BA7C4,#C4622D,#2D3E5C"` | Colores (oro, primavera, verano, otoño, invierno), editables |

`initOrb()` devuelve `{ setProgress(p), destroy() }` o `null` si no procede.

---

## E. FALLBACK (triple, automático — Fase 1 E.8)

1. **Sin WebGL o gama baja** → gradiente CSS animado (mismos colores).
2. **`prefers-reduced-motion`** → halo estático (sin animación).
3. **Error de carga / falta `three.module.js`** → el gradiente CSS que ya estaba pintado debajo permanece. **Nunca hay hueco en blanco.**

---

## F. PRESUPUESTO DE RENDIMIENTO (Fase 1 E.11)

| Métrica | Límite | Cómo se cumple |
|---------|--------|----------------|
| JS extra (three + escena, min+gzip) | ≤ 180 KB | Carga diferida post-LCP |
| LCP | < 2,5 s | El Orbe no participa (LCP = H1) |
| CLS | 0 | Canvas absoluto sobre fallback ya pintado |
| INP | < 200 ms | Loop pausado fuera de viewport y con pestaña oculta |
| FPS | 60 desktop / ≥30 móvil medio | DPR cap 1,75, geometría por gama, sin postprocesado |

Optimizaciones ya incluidas en `cc-color-orb.js`: `IntersectionObserver` (pausa fuera de pantalla), `visibilitychange` (pausa con pestaña oculta), DPR cap 1,75, detalle de geometría por `tier`, antialias desactivado en gama baja, `dispose()` completo.

---

## G. CÓMO ACTIVARLO (V1.5)

1. **Subir Three.js local:** `assets/vendor/three.module.js` (versión fijada).
2. **Encender el flag:** en `assets/js/cc-motion-config.js`, `flags.orb = true`.
3. **(Opcional) colores:** ajustar `data-cc-orb-colors` en Elementor.
4. Desplegar (Fase 7) y **purgar cachés** (Elementor → SiteGround → Cloudflare).
5. **Verificar contra el protocolo H.** Si no cumple, volver a `flags.orb = false` (queda el gradiente, sin tocar nada más).

> Excluir `three.module.js` y `cc-*.js` de la minificación de SiteGround; Rocket Loader OFF en Cloudflare (Fase 0).

---

## H. PROTOCOLO DE MEDICIÓN ANTES DE PUBLICAR (Fase 1 E.15)

1. **Prototipo / staging:** activar en staging, no en producción.
2. **Medir en dispositivos reales:** iPhone medio y Android de gama media — FPS, INP, batería, peso total.
3. **Core Web Vitals (móvil):** LCP, CLS, INP dentro de F.
4. **Fallbacks:** probar sin WebGL, con reduced-motion y sin `three.module.js`.
5. **Decisión:** si cumple, se queda; si no, `flags.orb = false` y se publica solo el gradiente. **La web nunca depende del Orbe.**

---

## I. EXTENSIÓN FUTURA (opcional)

- **Módulo 9 (Universo):** el Orbe del hero podría viajar y separarse en 4 halos estacionales con scroll-scrub. Complejidad ALTA (Fase 1 E.14); solo si el hero cumple holgadamente el presupuesto.
- **Módulo 29 (cierre):** Orbe en miniatura como firma (ya hay contenedor `.cc-cta__orb` con fallback CSS).

---

## J. ALTERNATIVA SI NO COMPENSA (Fase 1 E.13)

Vídeo en loop renderizado offline del mismo Orbe (WebM+MP4, <3 MB) + GSAP: ~85-90 % del impacto, coste técnico mínimo, cero riesgo de JS. Spline y Lottie descartados para esta pieza.

---

## K. CHECKLIST

- [ ] `three.module.js` subido a `assets/vendor/`.
- [ ] `flags.orb = true`.
- [ ] Medido en iPhone y Android medios dentro de presupuesto (F/H).
- [ ] Fallbacks verificados (sin WebGL / reduced-motion / sin three).
- [ ] CWV móvil OK; si no → `flags.orb = false`.
- [ ] Cachés purgadas tras desplegar.

> El Orbe es lo único que puede esperar. Todo lo demás (V1) ya es premium sin él.
