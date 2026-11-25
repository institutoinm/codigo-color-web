// Auditoría 2: SEO técnico + accesibilidad (axe-core, WCAG 2.1 AA).
// Uso: BASE=http://localhost:8765/web NODE_PATH=$(npm root -g) node tools/test/audit-seo-a11y.mjs
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const axeSource = readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");
const BASE = process.env.BASE || "http://localhost:8765/web";
const pages = ["cristinabarriga/adn-del-color.html", "inm/micropigmentacion-ciencia.html"];

const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
let fails = 0;
for (const p of pages) {
  const page = await browser.newPage({ viewport: { width: 1366, height: 800 } });
  await page.goto(`${BASE}/${p}`, { waitUntil: "load" });
  await page.waitForTimeout(1500);
  const seo = await page.evaluate(() => {
    const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => {
      try { return { ok: true, types: JSON.parse(s.textContent)["@graph"].map((g) => g["@type"]) }; }
      catch (e) { return { ok: false, error: String(e) }; }
    });
    const faqVisible = [...document.querySelectorAll(".faq summary")].map((s) => s.textContent.trim());
    const faqLd = [];
    document.querySelectorAll('script[type="application/ld+json"]').forEach((s) => {
      try {
        JSON.parse(s.textContent)["@graph"].filter((g) => g["@type"] === "FAQPage")
          .forEach((f) => f.mainEntity.forEach((q) => faqLd.push(q.name)));
      } catch {}
    });
    return {
      title: document.title, titleLen: document.title.length,
      desc: document.querySelector('meta[name="description"]')?.content.length,
      h1: document.querySelectorAll("h1").length,
      canonical: !!document.querySelector('link[rel="canonical"]'),
      lang: document.documentElement.lang,
      imgsNoAlt: [...document.images].filter((i) => !i.hasAttribute("alt")).length,
      ld, faqMatch: JSON.stringify(faqVisible) === JSON.stringify(faqLd), faqCount: faqVisible.length,
      headings: [...document.querySelectorAll("h1,h2,h3")].map((h) => h.tagName).join(""),
    };
  });
  await page.addScriptTag({ content: axeSource });
  const axe = await page.evaluate(async () => {
    const r = await window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21aa", "best-practice"] } });
    return r.violations.map((v) => ({ id: v.id, impact: v.impact, n: v.nodes.length, help: v.help, target: v.nodes[0]?.target.join(" ") }));
  });
  const checks = [
    ["título ≤ 65", seo.titleLen <= 65],
    ["descripción 120–160", seo.desc >= 120 && seo.desc <= 160],
    ["un solo h1", seo.h1 === 1],
    ["canonical", seo.canonical],
    ["lang=es", seo.lang === "es"],
    ["imágenes con alt", seo.imgsNoAlt === 0],
    ["JSON-LD válido", seo.ld.every((x) => x.ok)],
    ["FAQ visible = FAQPage", seo.faqMatch],
    ["axe sin violaciones serias", !axe.some((v) => ["serious", "critical"].includes(v.impact))],
  ];
  console.log(`\n## ${p}\n${seo.title} (${seo.titleLen}) · desc ${seo.desc} · JSON-LD: ${seo.ld.map((x) => x.types?.join(",")).join(" | ")}`);
  checks.forEach(([k, ok]) => { console.log(`${ok ? "✔" : "✖"} ${k}`); if (!ok) fails++; });
  axe.forEach((v) => console.log(`   axe ${v.impact} ${v.id} ×${v.n}: ${v.help} → ${v.target}`));
  await page.close();
}
await browser.close();
process.exit(fails ? 1 : 0);
