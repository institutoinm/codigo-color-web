/* cc-color-orb.js — Orbe Cromático (V1.5). Módulo ES, carga dinámica.
 *
 * Pieza firma WebGL (Three.js). Mejora progresiva y AISLADA:
 *  - Solo se ejecuta si lo invoca cc-scroll-animations.js con flags.orb = true.
 *  - Requiere WebGL, ausencia de prefers-reduced-motion y three.module.js presente.
 *  - Si falta cualquier requisito, NO hace nada: el fallback de gradiente CSS
 *    (.cc-color-orb en cc-base.css) permanece. Nunca hay hueco en blanco.
 *  - Es decorativo: marca el contenedor aria-hidden. No contiene texto SEO.
 *
 * Interfaz: initOrb() -> Promise<{ setProgress, destroy } | null>
 *  - setProgress(0..1): lo llama GSAP ScrollTrigger (GSAP gobierna el scroll).
 *  - destroy(): libera recursos.
 *
 * Presupuesto (Fase 1 E.11): DPR cap 1.75, sin postprocesado, loop pausado
 * fuera de viewport y con la pestaña oculta. Three.js carga aquí, post-LCP.
 */

let instance = null;

export async function initOrb() {
  if (instance) return instance;

  const host = document.querySelector('.cc-color-orb');
  if (!host) return null;
  if (host.getAttribute('data-cc-orb') === 'off') return null;

  const caps = (window.CC && window.CC.capabilities) || {};
  if (!caps.webgl || caps.reducedMotion) return null;

  // Three.js local (V1.5). Si no está, se conserva el fallback CSS.
  let THREE;
  try {
    THREE = await import(new URL('../vendor/three.module.js', import.meta.url).href);
  } catch (e) {
    return null;
  }

  // --- Colores de marca (editables en Elementor vía data-cc-orb-colors) ---
  const raw = (host.getAttribute('data-cc-orb-colors') ||
    '#C4A882,#D4A853,#8BA7C4,#C4622D,#2D3E5C').split(',').map((c) => c.trim());
  const col = raw.map((c) => new THREE.Color(c));
  const C = (i, fb) => col[i] || new THREE.Color(fb);

  // --- Render ---
  const dpr = Math.min(window.devicePixelRatio || 1, 1.75);
  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: caps.tier !== 'low' });
  renderer.setPixelRatio(dpr);
  const canvas = renderer.domElement;
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  canvas.style.display = 'block';
  host.setAttribute('aria-hidden', 'true');
  host.appendChild(canvas);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
  camera.position.z = 3.2;

  const detail = caps.tier === 'low' ? 4 : (caps.tier === 'high' ? 7 : 6);
  const geometry = new THREE.IcosahedronGeometry(1.2, detail);

  const uniforms = {
    uTime: { value: 0 },
    uProgress: { value: 0 },
    uColorA: { value: C(0, '#C4A882') },
    uColorB: { value: C(1, '#D4A853') },
    uColorC: { value: C(2, '#8BA7C4') },
    uWarm: { value: C(3, '#C4622D') },
    uCool: { value: C(4, '#2D3E5C') }
  };

  const material = new THREE.ShaderMaterial({
    uniforms,
    vertexShader: `
      varying vec3 vNormal; varying vec3 vView; varying vec3 vPos;
      void main(){
        vPos = position;
        vNormal = normalize(normalMatrix * normal);
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        vView = normalize(-mv.xyz);
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: `
      uniform float uTime; uniform float uProgress;
      uniform vec3 uColorA; uniform vec3 uColorB; uniform vec3 uColorC;
      uniform vec3 uWarm; uniform vec3 uCool;
      varying vec3 vNormal; varying vec3 vView; varying vec3 vPos;
      float hash(vec3 p){ p = fract(p*0.3183099 + 0.1); p *= 17.0;
        return fract(p.x*p.y*p.z*(p.x+p.y+p.z)); }
      float noise(vec3 x){ vec3 i=floor(x); vec3 f=fract(x); f=f*f*(3.0-2.0*f);
        return mix(mix(mix(hash(i+vec3(0,0,0)),hash(i+vec3(1,0,0)),f.x),
                       mix(hash(i+vec3(0,1,0)),hash(i+vec3(1,1,0)),f.x),f.y),
                   mix(mix(hash(i+vec3(0,0,1)),hash(i+vec3(1,0,1)),f.x),
                       mix(hash(i+vec3(0,1,1)),hash(i+vec3(1,1,1)),f.x),f.y), f.z); }
      void main(){
        float t = uTime * 0.08;
        float n = noise(vPos*1.6 + vec3(t, t*0.7, -t));
        n += 0.5 * noise(vPos*3.2 - vec3(t*0.6));
        n /= 1.5;
        vec3 base = mix(uColorA, uColorB, smoothstep(0.2, 0.8, n));
        base = mix(base, uColorC, smoothstep(0.5, 1.0, n) * 0.6);
        vec3 temp = mix(uWarm, uCool, uProgress);
        base = mix(base, temp, 0.25 * uProgress);
        float fres = pow(1.0 - max(dot(vNormal, vView), 0.0), 2.5);
        base += fres * 0.35;
        gl_FragColor = vec4(base, 1.0);
      }`,
    transparent: true
  });

  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);

  // --- Tamaño ---
  function resize() {
    const w = host.clientWidth || 1;
    const h = host.clientHeight || 1;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  resize();
  const ro = ('ResizeObserver' in window) ? new ResizeObserver(resize) : null;
  if (ro) ro.observe(host);

  // --- Estado e interacción ---
  let progress = 0;          // objetivo (lo fija GSAP)
  let progressLerp = 0;      // suavizado
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  function onPointer(e) {
    pointer.tx = (e.clientX / window.innerWidth - 0.5);
    pointer.ty = (e.clientY / window.innerHeight - 0.5);
  }
  if (caps.tier !== 'low') window.addEventListener('pointermove', onPointer, { passive: true });

  // --- Visibilidad: pausar fuera de viewport / pestaña oculta ---
  let inView = true;
  const io = ('IntersectionObserver' in window)
    ? new IntersectionObserver((es) => { inView = es[0].isIntersecting; if (inView) loop(); })
    : null;
  if (io) io.observe(host);
  document.addEventListener('visibilitychange', () => { if (!document.hidden && inView) loop(); });

  // --- Loop ---
  const clock = new THREE.Clock();
  let raf = 0;
  let running = false;
  function loop() {
    if (running) return;
    running = true;
    const tick = () => {
      if (!inView || document.hidden) { running = false; return; }
      uniforms.uTime.value += clock.getDelta();
      progressLerp += (progress - progressLerp) * 0.06;
      uniforms.uProgress.value = progressLerp;
      pointer.x += (pointer.tx - pointer.x) * 0.05;
      pointer.y += (pointer.ty - pointer.y) * 0.05;
      mesh.rotation.y = pointer.x * 0.4 + uniforms.uTime.value * 0.05;
      mesh.rotation.x = pointer.y * 0.3;
      const breathe = 1 + Math.sin(uniforms.uTime.value * 0.8) * 0.02;
      mesh.scale.setScalar(breathe);
      renderer.render(scene, camera);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
  }
  loop();

  instance = {
    setProgress(p) { progress = Math.max(0, Math.min(1, p)); if (!running && inView) loop(); },
    destroy() {
      cancelAnimationFrame(raf);
      window.removeEventListener('pointermove', onPointer);
      if (ro) ro.disconnect();
      if (io) io.disconnect();
      geometry.dispose();
      material.dispose();
      renderer.dispose();
      if (canvas.parentNode) canvas.parentNode.removeChild(canvas);
      instance = null;
    }
  };
  return instance;
}
