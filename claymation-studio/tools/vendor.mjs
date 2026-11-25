// Copia a web/vendor sólo los módulos necesarios (sin CDN externos: privacidad,
// rendimiento y control de versiones). three@0.180.0 · gsap@3.13.0 (MIT / licencia GSAP estándar).
import { cpSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const files = {
  "three/build/three.module.js": "three/three.module.js",
  "three/build/three.core.js": "three/three.core.js",
  "three/examples/jsm/loaders/GLTFLoader.js": "three/addons/loaders/GLTFLoader.js",
  "three/examples/jsm/utils/BufferGeometryUtils.js": "three/addons/utils/BufferGeometryUtils.js",
  "three/examples/jsm/libs/meshopt_decoder.module.js": "three/addons/libs/meshopt_decoder.module.js",
  "three/examples/jsm/environments/RoomEnvironment.js": "three/addons/environments/RoomEnvironment.js",
  "three/LICENSE": "three/LICENSE",
  "gsap/dist/gsap.min.js": "gsap/gsap.min.js",
  "gsap/dist/ScrollTrigger.min.js": "gsap/ScrollTrigger.min.js",
  "gsap/dist/ScrollToPlugin.min.js": "gsap/ScrollToPlugin.min.js",
};
for (const [src, dst] of Object.entries(files)) {
  const out = join("web/vendor", dst);
  mkdirSync(dirname(out), { recursive: true });
  cpSync(join("node_modules", src), out);
}
const v = (p) => JSON.parse(readFileSync(`node_modules/${p}/package.json`)).version;
writeFileSync("web/vendor/VERSIONS.txt", `three ${v("three")}\ngsap ${v("gsap")}\n`);
console.log("vendor OK", v("three"), v("gsap"));
