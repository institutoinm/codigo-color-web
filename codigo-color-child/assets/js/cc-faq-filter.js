/* cc-faq-filter.js — Filtro/búsqueda de las 100 FAQs (mod 27).
 * Filtra SOLO el HTML ya presente en el DOM. Nunca carga FAQs por fetch
 * (requisito SEO/GEO: todo el contenido existe en el HTML). */
(function (w, d) {
  'use strict';
  d.addEventListener('DOMContentLoaded', function () {
    var input = d.querySelector('.cc-faq__search input, input.cc-faq__search');
    var items = d.querySelectorAll('.cc-faq__item');
    if (!input || !items.length) return;

    function norm(s) {
      return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    }

    input.addEventListener('input', function () {
      var q = norm(input.value.trim());
      items.forEach(function (item) {
        var text = norm(item.textContent);
        item.style.display = (!q || text.indexOf(q) !== -1) ? '' : 'none';
      });
      // Oculta categorías sin resultados visibles
      d.querySelectorAll('.cc-faq__category').forEach(function (cat) {
        var visible = cat.querySelectorAll('.cc-faq__item:not([style*="display: none"])').length;
        cat.style.display = visible ? '' : 'none';
      });
    });
  });
})(window, document);
