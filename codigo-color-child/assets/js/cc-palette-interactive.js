/* cc-palette-interactive.js — Microinteracción de la grid de paleta (mod 7).
 * Degradación: en gama baja o sin JS, las muestras siguen siendo visibles. */
(function (w, d) {
  'use strict';
  d.addEventListener('DOMContentLoaded', function () {
    var grid = d.querySelector('.cc-palette-grid');
    if (!grid) return;

    var swatches = grid.querySelectorAll('.cc-palette-grid__swatch');
    if (!swatches.length) return;

    function activate(el) {
      swatches.forEach(function (s) { s.classList.remove('is-active'); });
      el.classList.add('is-active');
    }

    swatches.forEach(function (s) {
      s.addEventListener('mouseenter', function () { activate(s); });
      s.addEventListener('click', function () { activate(s); });
      s.addEventListener('focus', function () { activate(s); });
    });
  });
})(window, document);
