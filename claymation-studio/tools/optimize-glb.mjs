// Optimiza los GLB originales de Blender para la web:
//  · resample: elimina claves redundantes (la animación es escalonada, 12 poses/s)
//  · simplify: reduce polígonos conservando la silueta (ratio por calidad)
//  · meshopt: compresión de geometría y animación (decodificador de 4 kB)
//  · webp + resize: texturas horneadas a 512 px como máximo
// Genera dos niveles: <slug>.glb (escritorio) y <slug>.mobile.glb (móvil).
import { execFileSync } from "node:child_process";
import { readdirSync, statSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const SRC = "assets/glb/source";
const OUT = "assets/glb/web";
mkdirSync(OUT, { recursive: true });
const cli = "node_modules/.bin/gltf-transform";

const levels = [
  { suffix: "", ratio: 0.5, size: 512 },
  { suffix: ".mobile", ratio: 0.25, size: 256 },
];

for (const file of readdirSync(SRC).filter((f) => f.endsWith(".glb"))) {
  const slug = file.replace(/\.glb$/, "");
  for (const { suffix, ratio, size } of levels) {
    const out = join(OUT, `${slug}${suffix}.glb`);
    execFileSync(cli, [
      "optimize", join(SRC, file), out,
      "--compress", "meshopt",
      "--texture-compress", "webp",
      "--texture-size", String(size),
      "--simplify", "true",
      "--simplify-ratio", String(ratio),
      "--simplify-error", "0.0008",
      "--instance", "false",
      "--join", "false",
      "--flatten", "false",
      "--palette", "false",
    ], { stdio: "inherit" });
    const kb = (statSync(out).size / 1024).toFixed(0);
    const srcKb = (statSync(join(SRC, file)).size / 1024).toFixed(0);
    console.log(`✔ ${out}  ${srcKb} kB → ${kb} kB`);
  }
}
