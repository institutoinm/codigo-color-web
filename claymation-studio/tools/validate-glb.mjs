// Valida todos los GLB con el validador oficial de Khronos.
import validator from "gltf-validator";
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

let failed = 0;
for (const dir of ["assets/glb/source", "assets/glb/web"]) {
  for (const f of readdirSync(dir).filter((x) => x.endsWith(".glb"))) {
    const report = await validator.validateBytes(new Uint8Array(readFileSync(join(dir, f))), {
      maxIssues: 50,
      externalResourceFunction: () => Promise.reject(new Error("sin recursos externos")),
    });
    const { numErrors, numWarnings } = report.issues;
    const i = report.info;
    console.log(`${numErrors ? "✖" : "✔"} ${dir}/${f}  errores=${numErrors} avisos=${numWarnings}  ` +
      `mallas=${i.drawCallCount} vértices=${i.totalVertexCount} animaciones=${i.animationCount} morph=${i.hasMorphTargets}`);
    if (numErrors) {
      failed++;
      report.issues.messages.filter((m) => m.severity === 0).slice(0, 5)
        .forEach((m) => console.log("   ", m.code, m.message, m.pointer));
    }
  }
}
process.exit(failed ? 1 : 0);
