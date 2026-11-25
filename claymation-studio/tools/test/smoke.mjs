// Prueba de humo: carga cada página, recorre el scroll y captura pantallas + errores.
// Uso: BASE=http://localhost:8765/web node tools/test/smoke.mjs
import { createRequire } from "node:module";
// Playwright viene preinstalado globalmente en el entorno (no se añade como dependencia).
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const BASE = process.env.BASE || "http://localhost:8765/web";
const OUT = process.env.OUT || "tools/test/out";
const ONLY = process.env.ONLY; // filtra páginas
const pages = ["cristinabarriga/adn-del-color.html", "inm/micropigmentacion-ciencia.html"]
  .filter((p) => !ONLY || p.includes(ONLY));
const viewports = {
  desktop: { width: 1366, height: 800 },
  mobile: { width: 390, height: 844, isMobile: true, hasTouch: true },
};
const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
let problems = 0;
for (const [vpName, vp] of Object.entries(viewports)) {
  for (const p of pages) {
    const ctx = await browser.newContext({
      viewport: { width: vp.width, height: vp.height },
      isMobile: !!vp.isMobile, hasTouch: !!vp.hasTouch, deviceScaleFactor: 1,
      reducedMotion: process.env.REDUCED ? "reduce" : "no-preference",
    });
    const page = await ctx.newPage();
    const errors = [];
    page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
    page.on("pageerror", (e) => errors.push(String(e)));
    page.on("response", (r) => r.status() >= 400 && errors.push(`${r.status()} ${r.url()}`));
    await page.goto(`${BASE}/${p}`, { waitUntil: "load" });
    const name = p.split("/").pop().replace(".html", "");
    const hScroll = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    if (hScroll) errors.push("scroll horizontal");
    const n = await page.locator(".clay-chapter").count();
    for (let c = 0; c < n; c++) {
      const top = await page.evaluate((i) => {
        const el = document.querySelectorAll(".clay-chapter")[i];
        return el.getBoundingClientRect().top + scrollY;
      }, c);
      const height = await page.evaluate((i) => document.querySelectorAll(".clay-chapter")[i].offsetHeight, c);
      await page.evaluate((y) => scrollTo(0, y), top);
      await page
        .waitForFunction(
          (i) => document.querySelectorAll(".clay-stage")[i].classList.contains("is-ready") ||
            document.documentElement.classList.contains("clay-fallback"),
          c, { timeout: 90000 })
        .catch(() => errors.push(`capítulo ${c} no listo`));
      // Comprobaciones funcionales: piezas tocables y resaltado activo en el paso 1
      const info = await page.evaluate(async (i) => {
        const s = window.__clayStages?.[i];
        if (!s || !s.ready) return null;
        window.scrollTo(0, s.stepScroll(1));
        await new Promise((r) => setTimeout(r, 800));
        let lit = 0;
        s.model.traverse((o) => { if (o.isMesh && o.material.emissiveIntensity > 0.1 && o.material.emissive.getHex() !== 0) lit++; });
        return { pickables: s.pickables.length, step: s.stepIndex, lit };
      }, c);
      if (info) {
        console.log(`   capítulo ${c}: tocables=${info.pickables} paso=${info.step} resaltadas=${info.lit}`);
        if (!info.pickables) errors.push(`capítulo ${c} sin piezas tocables`);
        if (info.step !== 1) errors.push(`capítulo ${c}: el botón del paso 1 no activa el paso 1`);
      }
      for (const f of [0.02, 0.5, 0.97]) {
        await page.evaluate((y) => scrollTo(0, y), top + (height - vp.height) * f);
        await page.waitForTimeout(2500);
        await page.screenshot({ path: `${OUT}/${vpName}_${name}_c${c}_${Math.round(f * 100)}.png` });
      }
    }
    console.log(`${errors.length ? "✖" : "✔"} ${vpName} ${p}`, errors.slice(0, 8));
    problems += errors.length;
    await ctx.close();
  }
}
await browser.close();
process.exit(problems ? 1 : 0);
