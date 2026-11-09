import {continueRender, delayRender} from 'remotion';
// Carga una fuente local (sin Google Fonts: funciona sin internet).
export const loadFont = (familia: string, url: string) => {
  if (typeof document === 'undefined') return;
  const h = delayRender(`fuente ${familia}`);
  const f = new FontFace(familia, `url('${url}')`);
  f.load().then((cargada) => { document.fonts.add(cargada); continueRender(h); }).catch(() => continueRender(h));
};
