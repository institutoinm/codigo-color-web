# assets/fonts

Carpeta para las fuentes **locales** (estado final, Fase 0/1: servir local, no Google CDN).

Sube aquí los subsets **woff2** (latín + signos usados) con estos nombres exactos
para que `inc/fonts.php` active automáticamente `cc-fonts.css` y deje de cargar Google Fonts:

- `cormorant-garamond-400.woff2`
- `cormorant-garamond-500.woff2`
- `cormorant-garamond-400-italic.woff2`
- `dm-sans-400.woff2`
- `dm-sans-500.woff2`

Mientras estos archivos no existan, la web usa el **puente de Google Fonts** (V1, funcional y premium).
La detección es automática: en cuanto exista `cormorant-garamond-500.woff2`, se sirve local.
