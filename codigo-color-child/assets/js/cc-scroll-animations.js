/* cc-scroll-animations.js — Arquitectura de movimiento (V1).
 *
 * - Si GSAP + ScrollTrigger están presentes y se permite movimiento:
 *   revelados, parallax y línea de progreso del método, gobernados por scroll.
 *   GSAP es la ÚNICA fuente de verdad del scroll (Fase 1 E.5).
 * - Si NO hay GSAP o hay prefers-reduced-motion: el contenido permanece
 *   visible (SEO-safe, sin FOUC) — nunca se oculta nada de forma permanente.
 *
 * El Orbe Cromático (Three.js) es V1.5: aquí queda el HOOK comentado, inactivo.
 */
(function (w, d) {
  'use strict';

  var caps = (w.CC && w.CC.capabilities) || { motion: true };
  var cfg = w.CC_MOTION || {};
  var gsap = w.gsap;
  var hasGSAP = !!gsap && !!(gsap.registerPlugin) && !!w.ScrollTrigger;

  function ready(fn) {
    if (d.readyState !== 'loading') fn();
    else d.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    // Sin GSAP o sin movimiento permitido: dejar todo visible y salir.
    if (!hasGSAP || !caps.motion) {
      return;
    }

    // A partir de aquí SÍ animamos: marcamos el body para que CSS oculte los
    // elementos de revelado antes de animarlos (evita FOUC; ya hay JS activo).
    d.body.classList.add('cc-anim');

    gsap.registerPlugin(w.ScrollTrigger);

    var R = cfg.reveal || {};
    // Revelados
    d.querySelectorAll(R.selector || '[data-cc-reveal]').forEach(function (el) {
      gsap.to(el, {
        opacity: 1,
        y: 0,
        duration: (cfg.durations && cfg.durations.base) || 0.6,
        ease: cfg.ease || 'power2.out',
        scrollTrigger: { trigger: el, start: (R.start || 'top 85%'), once: true },
        onStart: function () { el.classList.add('is-visible'); }
      });
    });

    // Parallax suave (solo transform)
    var P = cfg.parallax || {};
    d.querySelectorAll(P.selector || '[data-cc-parallax]').forEach(function (el) {
      gsap.to(el, {
        yPercent: -(P.amount ? P.amount / 6 : 6),
        ease: 'none',
        scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true }
      });
    });

    // Línea de progreso del método (mod 8) — si existe
    var progress = d.querySelector('.cc-method__progress');
    if (progress) {
      gsap.fromTo(progress, { scaleY: 0 }, {
        scaleY: 1, transformOrigin: 'top', ease: 'none',
        scrollTrigger: { trigger: '.cc-method', start: 'top center', end: 'bottom center', scrub: true }
      });
    }

    // --- HOOK ORBE CROMÁTICO (V1.5) — NO ACTIVO EN V1 ---
    // if (cfg.flags && cfg.flags.orb && caps.webgl) {
    //   import('./cc-color-orb.js').then(function (m) { m.initOrb(); });
    // }

    w.ScrollTrigger.refresh();
  });
})(window, document);
