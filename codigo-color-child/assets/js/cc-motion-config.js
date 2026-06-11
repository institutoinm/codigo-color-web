/* cc-motion-config.js — Constantes de movimiento. Sin dependencias.
 * Expone window.CC_MOTION. No anima nada por sí mismo. */
(function (w) {
  'use strict';
  w.CC_MOTION = {
    durations: { fast: 0.25, base: 0.6, slow: 1.0 },
    ease: 'power2.out',
    reveal: {
      selector: '[data-cc-reveal]',
      y: 24,
      stagger: 0.08,
      start: 'top 85%'
    },
    parallax: { selector: '[data-cc-parallax]', amount: 40 },
    // Flags de funcionalidad. El Orbe queda preparado pero DESACTIVADO en V1.
    flags: { orb: false, orbVersion: '1.5' }
  };
})(window);
