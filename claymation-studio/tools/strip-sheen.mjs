// Elimina KHR_materials_sheen de los GLB web (three.js lo renderiza como un velo blanquecino
// que apaga los colores de la plastilina). Se ejecuta tras optimize-glb.mjs.
import { NodeIO } from "@gltf-transform/core";
import { ALL_EXTENSIONS } from "@gltf-transform/extensions";
import { MeshoptDecoder, MeshoptEncoder } from "meshoptimizer";
import { readdirSync } from "node:fs";

await MeshoptDecoder.ready;
await MeshoptEncoder.ready;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({
  "meshopt.decoder": MeshoptDecoder,
  "meshopt.encoder": MeshoptEncoder,
});
for (const f of readdirSync("assets/glb/web").filter((x) => x.endsWith(".glb"))) {
  const path = `assets/glb/web/${f}`;
  const doc = await io.read(path);
  const ext = doc.getRoot().listExtensionsUsed().find((e) => e.extensionName === "KHR_materials_sheen");
  if (ext) {
    ext.dispose();
    await io.write(path, doc);
    console.log("sheen eliminado:", f);
  }
}
