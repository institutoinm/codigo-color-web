// Claymation Science Studio · motor web
// three.js (GLB de Blender) + GSAP ScrollTrigger: scroll, toque, botones y cámara.
//
// Principios:
//  · Mejora progresiva: el HTML ya contiene textos, póster y vídeo; el 3D se añade encima.
//  · Stop motion real: la animación se cuantiza a 12 poses/s y la superficie "hierve".
//  · Rendimiento: carga diferida, GLB móvil más ligero, render bajo demanda, pausa fuera de pantalla.
//  · Accesibilidad: respeta prefers-reduced-motion y Save-Data; todo operable con teclado.
import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { MeshoptDecoder } from "three/addons/libs/meshopt_decoder.module.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { SCENES, HOTSPOTS } from "./scenes.js";

const { gsap, ScrollTrigger, ScrollToPlugin } = window;
gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);

const FPS = 24;
const POSE_STEP = 2; // "on twos"
const BOIL_MS = 1000 / 12;
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const saveData = navigator.connection?.saveData === true;
const isSmall = () => matchMedia("(max-width: 767px)").matches;
const lowEnd = (navigator.deviceMemory && navigator.deviceMemory <= 4) || (navigator.hardwareConcurrency || 8) <= 4;

const ACCENT = new THREE.Color(0x7fe3e0);
const UP = new THREE.Vector3(0, 1, 0);
const TMP_A = new THREE.Vector3();
const TMP_B = new THREE.Vector3();
const TMP_C = new THREE.Vector3();
const b2t = ([x, y, z]) => new THREE.Vector3(x, z, -y); // Blender (Z arriba) → glTF (Y arriba)
const smooth = (t) => t * t * (3 - 2 * t);

function webglAvailable() {
  try {
    const c = document.createElement("canvas");
    return !!(c.getContext("webgl2") || c.getContext("webgl"));
  } catch {
    return false;
  }
}

function track(event, detail = {}) {
  // Gancho de analítica (CRO). Conectar a GA4 / Matomo / Plausible si existe.
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event, ...detail });
}

class ClayStage {
  constructor(chapter) {
    this.chapter = chapter;
    this.slug = chapter.dataset.scene;
    this.cfg = SCENES[this.slug];
    this.stage = chapter.querySelector(".clay-stage");
    this.canvas = chapter.querySelector(".clay-canvas");
    this.tooltip = chapter.querySelector(".clay-tooltip");
    this.steps = [...chapter.querySelectorAll(".clay-step")];
    this.buttons = [...chapter.querySelectorAll("[data-goto-step]")];
    this.progress = 0;
    this.stepIndex = -1;
    this.camPos = new THREE.Vector3();
    this.camTarget = new THREE.Vector3();
    this.goalPos = new THREE.Vector3();
    this.goalTarget = new THREE.Vector3();
    this.yaw = 0;
    this.pitch = 0;
    this.yawGoal = 0;
    this.pitchGoal = 0;
    this.visible = false;
    this.ready = false;
    this.lastBoil = 0;
    this.dirty = true;
    this.bindUi();
  }

  // ---------- UI y scroll (funcionan también sin WebGL) ----------
  bindUi() {
    this.buttons.forEach((btn) =>
      btn.addEventListener("click", () => {
        const i = Number(btn.dataset.gotoStep);
        const el = this.steps[i];
        if (!el) return;
        track("clay_step_button", { scene: this.slug, step: i });
        gsap.to(window, {
          // Con 3D: posición exacta del paso; en modo vídeo: la tarjeta de texto
          scrollTo: { y: this.isFallback() ? el : this.stepScroll(i), autoKill: true },
          duration: reduceMotion ? 0 : 1.1,
          ease: "power2.inOut",
        });
      }),
    );
    const play = this.chapter.querySelector("[data-clay-play]");
    play?.addEventListener("click", () => {
      track("clay_play", { scene: this.slug });
      const st = this.trigger;
      // autoKill: si la persona hace scroll o toca, la reproducción se detiene
      gsap.to(window, { scrollTo: { y: st.end - 2, autoKill: true }, duration: reduceMotion ? 0 : 9, ease: "none" });
    });

    this.trigger = ScrollTrigger.create({
      trigger: this.chapter,
      start: "top top",
      end: "bottom bottom",
      // Sin animación vinculada: el suavizado lo hace la cámara (lerp) en tick()
      onUpdate: (st) => {
        this.progress = st.progress;
        this.dirty = true;
        this.updateStep();
      },
    });
    this.steps.forEach((el, i) =>
      ScrollTrigger.create({
        trigger: el,
        start: "top 70%",
        end: "bottom 30%",
        toggleClass: "is-active",
        onEnter: () => track("clay_step_view", { scene: this.slug, step: i }),
      }),
    );
  }

  // El capítulo mide n pantallas y se desplaza (n−1): el paso i está centrado en progress = i/(n−1).
  stepPos() {
    const n = this.cfg.steps.length;
    const x = this.progress * (n - 1);
    const i = Math.min(n - 1, Math.round(x));
    return { n, i, local: THREE.MathUtils.clamp(x - i + 0.5, 0, 1) };
  }

  isFallback() {
    return document.documentElement.classList.contains("clay-fallback") || this.chapter.classList.contains("is-fallback");
  }

  stepScroll(i) {
    const st = this.trigger;
    return st.start + (i / (this.cfg.steps.length - 1)) * (st.end - st.start);
  }

  updateStep(force = false) {
    const { i } = this.stepPos();
    if (force || i !== this.stepIndex) {
      this.stepIndex = i;
      this.buttons.forEach((b) => b.setAttribute("aria-current", String(Number(b.dataset.gotoStep) === i)));
      this.applyHighlight(this.cfg.steps[i].highlight);
    }
  }

  // ---------- 3D ----------
  async init() {
    const r = (this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: !lowEnd,
      alpha: true,
      powerPreference: "high-performance",
    }));
    r.setPixelRatio(Math.min(devicePixelRatio, isSmall() ? 1.5 : 1.75));
    r.outputColorSpace = THREE.SRGBColorSpace;
    r.toneMapping = THREE.NeutralToneMapping; // conserva los colores de la plastilina
    r.toneMappingExposure = 0.95;
    r.shadowMap.enabled = !lowEnd;
    r.shadowMap.type = THREE.PCFSoftShadowMap;

    const scene = (this.scene = new THREE.Scene());
    const pmrem = new THREE.PMREMGenerator(r);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 0.22;

    // Iluminación cinematográfica equivalente a la de Blender
    const key = new THREE.DirectionalLight(0xffe7cf, 1.9);
    key.position.copy(b2t([-4.5, -5.0, 6.0]));
    key.castShadow = !lowEnd;
    key.shadow.mapSize.set(1024, 1024);
    key.shadow.radius = 6;
    key.shadow.bias = -0.0005;
    Object.assign(key.shadow.camera, { left: -5, right: 5, top: 7, bottom: -3, near: 0.5, far: 25 });
    const rim = new THREE.DirectionalLight(0x7fe3e0, 1.3);
    rim.position.copy(b2t([2.5, 5.5, 5.0]));
    const fill = new THREE.HemisphereLight(0xd7e4ff, 0x2a2b2f, 0.35);
    scene.add(key, rim, fill);
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.ShadowMaterial({ opacity: 0.32 }));
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    this.camera = new THREE.PerspectiveCamera(this.cfg.fov, 1, 0.1, 100);

    const loader = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
    const base = this.chapter.dataset.glb;
    const url = isSmall() || lowEnd ? base.replace(/\.glb$/, ".mobile.glb") : base;
    const gltf = await loader.loadAsync(url);
    this.model = gltf.scene;
    this.pickables = [];
    this.model.traverse((o) => {
      if (!o.isMesh) return;
      o.castShadow = o.receiveShadow = !lowEnd;
      const m = o.material;
      if (m.normalMap) {
        m.normalMap = m.normalMap.clone(); // cada pieza "hierve" por separado
        m.normalMap.wrapS = m.normalMap.wrapT = THREE.MirroredRepeatWrapping;
        m.userData.baseNormalScale = m.normalScale.clone();
      }
      m.userData.baseEmissive = m.emissive.clone();
      m.userData.baseEmissiveIntensity = m.emissiveIntensity;
      // Los "extras" de Blender viven en el nodo padre (el objeto); la malla es su hijo.
      for (let n = o; n && n !== this.model; n = n.parent) {
        const u = n.userData;
        if (u.dimension || u.profundidad || u.papel) {
          o.userData.meta = u;
          this.pickables.push(o);
          break;
        }
      }
      // Nombres de la malla y sus antecesores (en GLTFLoader la malla puede ser el nodo o su hijo)
      const lineage = [];
      for (let n = o; n && n !== this.model; n = n.parent) lineage.push(n.name);
      o.userData.lineage = lineage;
    });
    scene.add(this.model);

    this.mixer = new THREE.AnimationMixer(this.model);
    this.actions = gltf.animations.map((clip) => {
      const a = this.mixer.clipAction(clip);
      a.setLoop(THREE.LoopOnce, 1);
      a.clampWhenFinished = true;
      a.play();
      return a;
    });

    this.bindPointer();
    this.resize();
    new ResizeObserver(() => this.resize()).observe(this.stage);
    this.updateStep(true); // reaplica el resaltado aunque el GLB cargue a mitad del capítulo
    this.updateCameraGoal(true);
    this.ready = true;
    this.stage.classList.add("is-ready");
    track("clay_scene_ready", { scene: this.slug, glb: url });
  }

  applyHighlight(h) {
    if (!this.model) return;
    this.model.traverse((o) => {
      if (!o.isMesh) return;
      const m = o.material;
      const meta = o.userData.meta || {};
      const lineage = o.userData.lineage || [o.name];
      const on = !!h && ((h.dimension && meta.dimension === h.dimension) || (h.names && h.names.some((n) => lineage.includes(n))));
      const glowBase = m.userData.baseEmissiveIntensity ?? 1;
      const isGlow = m.userData.baseEmissive && m.userData.baseEmissive.getHex() !== 0;
      // Resaltado "escáner ADN": un velo cian muy sutil sobre la plastilina
      if (!isGlow) m.emissive.copy(on ? ACCENT : m.userData.baseEmissive);
      gsap.to(m, {
        emissiveIntensity: on ? (isGlow ? glowBase * 2 : 0.16) : glowBase,
        duration: reduceMotion ? 0 : 0.5,
        onUpdate: () => (this.dirty = true),
      });
    });
  }

  bindPointer() {
    // Arrastre horizontal = girar la escena (el scroll vertical sigue libre: touch-action: pan-y).
    let dragging = false, sx = 0, sy = 0, moved = 0;
    const c = this.canvas;
    c.addEventListener("pointerdown", (e) => {
      dragging = true; moved = 0; sx = e.clientX; sy = e.clientY;
      c.setPointerCapture(e.pointerId);
    });
    c.addEventListener("pointermove", (e) => {
      if (!dragging) return;
      const dx = e.clientX - sx, dy = e.clientY - sy;
      moved += Math.abs(dx) + Math.abs(dy);
      sx = e.clientX; sy = e.clientY;
      this.yawGoal = THREE.MathUtils.clamp(this.yawGoal - dx * 0.006, -0.6, 0.6);
      this.pitchGoal = THREE.MathUtils.clamp(this.pitchGoal + dy * 0.003, -0.15, 0.25);
      this.dirty = true;
    });
    const end = (e) => {
      if (!dragging) return;
      dragging = false;
      if (moved < 6) this.pick(e);
      else track("clay_drag", { scene: this.slug });
    };
    c.addEventListener("pointerup", end);
    c.addEventListener("pointercancel", () => (dragging = false));
    c.addEventListener("dblclick", () => { this.yawGoal = 0; this.pitchGoal = 0; });
    c.addEventListener("keydown", (e) => {
      const k = { ArrowLeft: [-0.12, 0], ArrowRight: [0.12, 0], ArrowUp: [0, 0.05], ArrowDown: [0, -0.05] }[e.key];
      if (!k) return;
      e.preventDefault();
      this.yawGoal = THREE.MathUtils.clamp(this.yawGoal + k[0], -0.6, 0.6);
      this.pitchGoal = THREE.MathUtils.clamp(this.pitchGoal + k[1], -0.15, 0.25);
      this.dirty = true;
    });
  }

  pick(e) {
    if (!this.pickables.length) return;
    const rect = this.canvas.getBoundingClientRect();
    const ndc = new THREE.Vector2(((e.clientX - rect.left) / rect.width) * 2 - 1, -((e.clientY - rect.top) / rect.height) * 2 + 1);
    const ray = new THREE.Raycaster();
    ray.setFromCamera(ndc, this.camera);
    const hit = ray.intersectObjects(this.pickables, false)[0];
    if (!hit) return;
    const u = hit.object.userData.meta;
    const key = u.dimension || u.profundidad || u.papel;
    const text = HOTSPOTS[key] || key;
    // La región aria-live está siempre presente; sólo cambia su texto (así se anuncia)
    this.tooltip.textContent = u.polo ? `${text} Polo: ${u.polo}.` : text;
    this.tooltip.classList.add("is-visible");
    clearTimeout(this._tt);
    this._tt = setTimeout(() => {
      this.tooltip.classList.remove("is-visible");
      this.tooltip.textContent = "";
    }, 6000);
    track("clay_hotspot", { scene: this.slug, key });
  }

  resize() {
    if (!this.renderer) return;
    const { width, height } = this.stage.getBoundingClientRect();
    this.renderer.setSize(width, height, false);
    this.camera.aspect = width / Math.max(1, height);
    this.camera.updateProjectionMatrix();
    this.dirty = true;
  }

  // Cámara: interpolación suave entre los encuadres de cada paso.
  updateCameraGoal(snap = false) {
    const steps = this.cfg.steps;
    const { i, local } = this.stepPos();
    const prev = steps[Math.max(0, i - 1)];
    const cur = steps[i];
    const t = i === 0 ? 1 : smooth(Math.min(1, local / 0.45));
    this.goalPos.copy(b2t(prev.cam)).lerp(b2t(cur.cam), t);
    this.goalTarget.copy(b2t(prev.target)).lerp(b2t(cur.target), t);
    // En vertical (móvil) alejamos la cámara para que todo quepa
    if (this.camera.aspect < 1) {
      const k = Math.pow(1 / this.camera.aspect, 0.75);
      this.goalPos.sub(this.goalTarget).multiplyScalar(k).add(this.goalTarget);
    }
    const [f0, f1] = cur.frames;
    let frame = f0 + (f1 - f0) * smooth(local);
    frame = Math.round(frame / POSE_STEP) * POSE_STEP; // pose fija: stop motion
    this.frame = Math.min(frame, this.cfg.end);
    if (snap) {
      this.camPos.copy(this.goalPos);
      this.camTarget.copy(this.goalTarget);
    }
  }

  boil(now) {
    if (reduceMotion || now - this.lastBoil < BOIL_MS) return false;
    this.lastBoil = now;
    this.model.traverse((o) => {
      const m = o.isMesh && o.material;
      if (!m || !m.normalMap) return;
      m.normalMap.offset.set(Math.random() * 0.006, Math.random() * 0.006);
      const s = 0.85 + Math.random() * 0.3;
      m.normalScale.copy(m.userData.baseNormalScale).multiplyScalar(s);
    });
    return true;
  }

  tick(now) {
    if (!this.ready || !this.visible) return;
    this.updateCameraGoal();
    const k = reduceMotion ? 1 : 0.08;
    TMP_A.copy(this.camPos);
    this.camPos.lerp(this.goalPos, k);
    this.camTarget.lerp(this.goalTarget, k);
    this.yaw += (this.yawGoal - this.yaw) * 0.12;
    this.pitch += (this.pitchGoal - this.pitch) * 0.12;
    const moving = TMP_A.distanceToSquared(this.camPos) > 1e-7 ||
      Math.abs(this.yawGoal - this.yaw) > 1e-4 || Math.abs(this.pitchGoal - this.pitch) > 1e-4;

    // Órbita manual alrededor del objetivo (vectores reutilizados: sin basura por fotograma)
    const off = TMP_B.copy(this.camPos).sub(this.camTarget);
    off.applyAxisAngle(UP, this.yaw);
    const right = TMP_C.crossVectors(off, UP).normalize();
    off.applyAxisAngle(right, this.pitch);
    this.camera.position.copy(this.camTarget).add(off);
    this.camera.lookAt(this.camTarget);

    const frameChanged = this.frame !== this._lastFrame;
    if (frameChanged) {
      this._lastFrame = this.frame;
      // Scrub determinista (adelante y atrás): cada clip se fija a la pose exacta.
      const t = this.frame / FPS;
      this.actions.forEach((a) => {
        a.enabled = true;
        a.paused = false;
        a.time = Math.min(t, a.getClip().duration);
      });
      this.mixer.update(0);
    }
    const boiled = this.boil(now);
    if (moving || frameChanged || boiled || this.dirty) {
      this.renderer.render(this.scene, this.camera);
      this.dirty = false;
    }
  }
}

// ---------- Arranque ----------
// Vídeo de respaldo: con controles; sólo se reproduce solo si no se pidió reducir movimiento ni ahorrar datos.
function startVideos(root) {
  const vertical = matchMedia("(max-width: 767px)").matches;
  root.querySelectorAll(".clay-video").forEach((v) => {
    // El atributo poster no admite media queries: en móvil se usa el póster vertical del mismo vídeo.
    if (vertical && v.poster.includes("_16x9.")) v.poster = v.poster.replace("_16x9.", "_9x16.");
    v.controls = true;
    if (!reduceMotion && !saveData) {
      v.muted = true;
      v.play().catch(() => {});
    }
  });
}

const chapters = [...document.querySelectorAll(".clay-chapter")];
const useFallback = reduceMotion || saveData || !webglAvailable();
document.documentElement.classList.toggle("clay-fallback", useFallback);

const stages = chapters.map((ch) => new ClayStage(ch));
window.__clayStages = stages; // inspección en pruebas automáticas

if (!useFallback) {
  const io = new IntersectionObserver(
    (entries) =>
      entries.forEach((e) => {
        const s = stages.find((x) => x.chapter === e.target);
        s.visible = e.isIntersecting;
        if (e.isIntersecting && !s.loading) {
          s.loading = s.init().catch((err) => {
            console.error("Claymation:", err);
            s.ready = false;
            s.renderer?.dispose();
            s.chapter.classList.add("is-fallback");
            startVideos(s.chapter);
          });
        }
      }),
    { rootMargin: "300px 0px" },
  );
  chapters.forEach((c) => io.observe(c));
  const loop = (now) => {
    stages.forEach((s) => s.tick(now));
    requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);
} else {
  startVideos(document);
}

// CTA visibles: medición de clics para CRO
document.querySelectorAll("[data-cta]").forEach((a) =>
  a.addEventListener("click", () => track("clay_cta_click", { cta: a.dataset.cta })),
);
