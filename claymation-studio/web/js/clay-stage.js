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
          scrollTo: { y: el, offsetY: innerHeight * 0.25 },
          duration: reduceMotion ? 0 : 1.1,
          ease: "power2.inOut",
        });
      }),
    );
    const play = this.chapter.querySelector("[data-clay-play]");
    play?.addEventListener("click", () => {
      track("clay_play", { scene: this.slug });
      const st = this.trigger;
      gsap.to(window, { scrollTo: st.end - 2, duration: reduceMotion ? 0 : 9, ease: "none" });
    });

    this.trigger = ScrollTrigger.create({
      trigger: this.chapter,
      start: "top top",
      end: "bottom bottom",
      scrub: reduceMotion ? true : 0.6,
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

  updateStep() {
    const n = this.cfg.steps.length;
    const i = Math.min(n - 1, Math.floor(this.progress * n));
    if (i !== this.stepIndex) {
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
    const url = isSmall() || saveData || lowEnd ? base.replace(/\.glb$/, ".mobile.glb") : base;
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
      const info = o.userData.dimension || o.userData.profundidad || o.userData.papel;
      if (info) this.pickables.push(o);
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
    this.updateStep();
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
      const on = h && ((h.dimension && o.userData.dimension === h.dimension) || (h.names && h.names.some((n) => o.name.startsWith(n))));
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
    const u = hit.object.userData;
    const key = u.dimension || u.profundidad || u.papel;
    const text = HOTSPOTS[key] || key;
    this.tooltip.textContent = u.polo ? `${text} Polo: ${u.polo}.` : text;
    this.tooltip.hidden = false;
    clearTimeout(this._tt);
    this._tt = setTimeout(() => (this.tooltip.hidden = true), 5000);
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
    const n = steps.length;
    const x = this.progress * n;
    const i = Math.min(n - 1, Math.floor(x));
    const local = Math.min(1, x - i);
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
    const before = this.camPos.clone();
    this.camPos.lerp(this.goalPos, k);
    this.camTarget.lerp(this.goalTarget, k);
    this.yaw += (this.yawGoal - this.yaw) * 0.12;
    this.pitch += (this.pitchGoal - this.pitch) * 0.12;
    const moving = before.distanceToSquared(this.camPos) > 1e-7 || Math.abs(this.yawGoal - this.yaw) > 1e-4;

    // Órbita manual alrededor del objetivo
    const off = this.camPos.clone().sub(this.camTarget);
    off.applyAxisAngle(new THREE.Vector3(0, 1, 0), this.yaw);
    const right = new THREE.Vector3().crossVectors(off, new THREE.Vector3(0, 1, 0)).normalize();
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
const chapters = [...document.querySelectorAll(".clay-chapter")];
const useFallback = reduceMotion || saveData || !webglAvailable();
document.documentElement.classList.toggle("clay-fallback", useFallback);

const stages = chapters.map((ch) => new ClayStage(ch));

if (!useFallback) {
  const io = new IntersectionObserver(
    (entries) =>
      entries.forEach((e) => {
        const s = stages.find((x) => x.chapter === e.target);
        s.visible = e.isIntersecting;
        if (e.isIntersecting && !s.loading) {
          s.loading = s.init().catch((err) => {
            console.error("Claymation:", err);
            s.chapter.classList.add("is-fallback");
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
  // Vídeo de respaldo: sólo se reproduce solo si el usuario no ha pedido reducir movimiento.
  document.querySelectorAll(".clay-video").forEach((v) => {
    v.controls = true;
    if (!reduceMotion && !saveData) {
      v.muted = true;
      v.play().catch(() => {});
    }
  });
}

// CTA visibles: medición de clics para CRO
document.querySelectorAll("[data-cta]").forEach((a) =>
  a.addEventListener("click", () => track("clay_cta_click", { cta: a.dataset.cta })),
);
