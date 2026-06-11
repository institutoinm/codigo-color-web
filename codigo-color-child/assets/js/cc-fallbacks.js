/* cc-fallbacks.js — Detección de capacidades. Sin dependencias.
 * Expone window.CC.capabilities y añade clases al <html> para que CSS/JS
 * decidan el nivel de experiencia. No carga librerías. */
(function (w, d) {
  'use strict';

  function hasWebGL() {
    try {
      var c = d.createElement('canvas');
      return !!(w.WebGLRenderingContext &&
        (c.getContext('webgl') || c.getContext('experimental-webgl')));
    } catch (e) {
      return false;
    }
  }

  function deviceTier() {
    var mem = w.navigator.deviceMemory || 4;
    var cores = w.navigator.hardwareConcurrency || 4;
    if (mem <= 2 || cores <= 2) return 'low';
    if (mem >= 8 && cores >= 8) return 'high';
    return 'mid';
  }

  var reduced = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var caps = {
    webgl: hasWebGL(),
    reducedMotion: !!reduced,
    tier: deviceTier(),
    // En V1 el movimiento "rico" se permite si no hay reduced-motion y el
    // dispositivo no es de gama baja. (El Orbe sigue desactivado por flag.)
    motion: !reduced
  };

  w.CC = w.CC || {};
  w.CC.capabilities = caps;

  var html = d.documentElement;
  html.classList.add(caps.webgl ? 'cc-webgl' : 'cc-no-webgl');
  html.classList.add('cc-tier-' + caps.tier);
  if (caps.reducedMotion) html.classList.add('cc-reduced-motion');
})(window, document);
