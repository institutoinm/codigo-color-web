"""
Escena 01 · «El ADN del color» — CristinaBarriga.com (Código Color)

Concepto profesional: el color personal se analiza con cuatro dimensiones
(subtono, valor, intensidad y contraste). Cada par de bases de la doble
hélice es una dimensión con sus dos polos; la hélice se ensambla pieza a
pieza en stop motion mientras un anillo de escaneo la recorre.

Ejecutar:  python adn_del_color.py   (con el módulo bpy)  ó
           blender -b -P adn_del_color.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import bpy  # noqa: E402
import bmesh  # noqa: E402
import clay_lib as C  # noqa: E402

SLUG = "adn-del-color"
END = 120
P = C.PALETTE

DIMENSIONES = [
    # (dimensión, polo A, color A, polo B, color B)
    ("subtono", "cálido", P["ocre"], "frío", P["azul_acero"]),
    ("valor", "claro", "#d9ccb7", "oscuro", P["ciruela"]),
    ("intensidad", "brillante", "#c5523a", "suave", P["salvia"]),
    ("contraste", "alto", P["pizarra"], "bajo", "#c9bba6"),
]

sc = C.reset_scene(END)
C.cyclorama()
C.cinematic_lighting(key_energy=950, target=(0, 0, 2.4))

root = C.link(bpy.data.objects.new("ADN", None), "ADN")
root.location = (0, 0, 0.55)

# Pedestal escultórico
bm = bmesh.new()
bmesh.ops.create_cone(bm, cap_ends=True, segments=64, radius1=1.9, radius2=1.75,
                      depth=0.5, calc_uvs=True)
ped = C.mesh_object("Pedestal", bm, C.clay_material("Pedestal_pizarra", P["pizarra"], roughness=0.7),
                    "ADN")
ped.location = (0, 0, 0.25)
C.handmade(ped, strength=0.04, scale=0.8, subdiv=1, seed=1)
ped["smart_uv"] = True  # el cono de bmesh sólo trae UV en las tapas

# Doble hélice
H, R, TURNS, N = 4.4, 1.15, 1.25, 160
mat_a = C.clay_material("Cadena_hueso", P["hueso"])
mat_b = C.clay_material("Cadena_arcilla", P["arcilla"])
for name, phase, mat in (("Cadena_A", 0.0, mat_a), ("Cadena_B", math.pi, mat_b)):
    pts = []
    for i in range(N + 1):
        t = i / N
        a = t * TURNS * 2 * math.pi + phase
        pts.append((R * math.cos(a), R * math.sin(a), 0.35 + t * H))
    tube = C.tube_along(name, pts, radius=0.17, sides=24, material=mat, collection="ADN")
    C.handmade(tube, strength=0.05, scale=0.35, subdiv=1, seed=C.stable_seed(name, 50))
    tube.parent = root

# Pares de bases: 12 peldaños, 3 por dimensión
rungs = []
mats_cache = {}
for i in range(12):
    dim, pa, ca, pb, cb = DIMENSIONES[i % 4]
    t = (i + 0.5) / 12
    a = t * TURNS * 2 * math.pi
    z = 0.35 + t * H
    for side, (polo, col, ang) in enumerate(((pa, ca, a), (pb, cb, a + math.pi))):
        key = f"{dim}_{polo}"
        if key not in mats_cache:
            mats_cache[key] = C.clay_material(f"Base_{key}", col)
        cap = C.capsule(f"Base_{i:02d}_{key}", radius=0.15, length=R * 0.98,
                        material=mats_cache[key], collection="ADN")
        C.handmade(cap, strength=0.03, scale=0.3, subdiv=1, seed=i * 2 + side)
        mid = R * 0.5
        cap.location = (mid * math.cos(ang), mid * math.sin(ang), z)
        cap.rotation_euler = (0, 0, ang)
        cap["dimension"] = dim
        cap["polo"] = polo
        cap.parent = root
        rungs.append((i, cap))

# Anillo de escaneo (futurismo ADN)
ring_pts = [(1.75 * math.cos(2 * math.pi * k / 96), 1.75 * math.sin(2 * math.pi * k / 96), 0)
            for k in range(97)]
ring = C.tube_along("Anillo_escaneo", ring_pts, radius=0.025, sides=10,
                    material=C.glow_material("Luz_escaneo", P["cian_adn"], 8.0), collection="ADN")
ring.parent = root

# Cámaras cinematográficas
C.camera("CAM_16x9", lens=40, location=(-7.5, -14.0, 4.2), target=(0, 0, 2.9), fstop=4.0)
C.camera("CAM_9x16", lens=62, location=(-6.5, -14.5, 3.8), target=(0, 0, 2.9), fstop=4.0)

# Texturas horneadas para la versión web (antes de animar escalas)
C.bake_web_materials([o for o in sc.objects if o.type == "MESH" and o.name != "Ciclorama"], size=512)

# ---------------- Animación stop motion (on twos) ----------------
for f in C.steps(0, END):
    root.rotation_euler = (0, 0, math.radians(-20 + 190 * C.ease(f / END)))
    root.keyframe_insert("rotation_euler", frame=f)

for name in ("Cadena_A", "Cadena_B"):
    o = sc.objects[name]
    for f in C.steps(0, 14):
        s = C.overshoot(f / 14, 1.08)
        o.scale = (1, 1, max(0.001, s))
        o.keyframe_insert("scale", frame=f)

for i, cap in rungs:
    start = 12 + i * 6
    for f in C.steps(0, END):
        t = (f - start) / 10
        if t <= 0:
            s = (0.001, 0.001, 0.001)
        else:
            sx = C.overshoot(t, 1.18)
            sq = 1 / math.sqrt(max(sx, 0.2)) if t < 1 else 1.0
            s = (max(0.001, sx), max(0.001, min(1.0, t * 1.4)) * sq, max(0.001, min(1.0, t * 1.4)) * sq)
        cap.scale = s
        cap.keyframe_insert("scale", frame=f)
        if f > start + 12:
            break

for f in C.steps(0, END):
    ring.location = (0, 0, 0.2 + 4.8 * C.ease((f - 20) / 90))
    ring.keyframe_insert("location", frame=f)

C.key_path(sc.objects["CAM_16x9"], [(0, (-7.5, -14.0, 4.2)), (END, (-4.2, -12.2, 3.4))])
C.key_path(sc.objects["CAM_9x16"], [(0, (-6.5, -14.5, 3.8)), (END, (-3.6, -13.0, 3.3))])
C.animate_boil([m for m in bpy.data.materials if m.node_tree and "ClayBoil" in m.node_tree.nodes
                and not m.name.endswith("_web") and "_web_" not in m.name], 0, END)

C.save_blend(os.path.join(C.ASSETS, "blend", f"{SLUG}.blend"))
C.export_glb(os.path.join(C.ASSETS, "glb", "source", f"{SLUG}.glb"))
print("OK", SLUG)
