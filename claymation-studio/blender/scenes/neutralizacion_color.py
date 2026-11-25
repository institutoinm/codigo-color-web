"""
Escena 03 · «Neutralización del color» — Colorimetría aplicada
(Instituto Nacional de Micropigmentación · también válida para Código Color)

Concepto profesional: los colores opuestos en el círculo cromático se
neutralizan. Un pigmento antiguo virado a gris azulado se corrige con un
modificador anaranjado: las dos gotas de plastilina viajan por el eje
complementario del círculo, se funden (animación por sustitución, como en el
stop motion clásico) y nace un marrón neutro y estable.

Shape keys: «Aplastar» y «Estirar» (squash & stretch) en las gotas.
"""
import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import bpy  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Vector  # noqa: E402
import clay_lib as C  # noqa: E402

SLUG = "neutralizacion-del-color"
END = 120
P = C.PALETTE

sc = C.reset_scene(END)
C.cyclorama()
C.cinematic_lighting(key_energy=950, target=(0, 0, 0.8))
root = C.link(bpy.data.objects.new("Rueda", None), "Rueda")

# Círculo cromático de plastilina: 12 cuñas con colores minerales
# índice 0 = naranja, índice 6 = azul: opuestos (complementarios) en la rueda
HUES = ["#c06f3c", "#c4913f", "#c9a640", "#a7a457", "#7f9a6a", "#5f8d7d",
        "#5b6f86", "#6a6390", "#7d5a86", "#94566e", "#a95546", "#b6603f"]
R_OUT, R_IN, H = 2.6, 0.95, 0.28
for i, col in enumerate(HUES):
    a0 = 2 * math.pi * i / 12 + 0.035
    a1 = 2 * math.pi * (i + 1) / 12 - 0.035
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")
    segs = 10
    top, bot = [], []
    for r in (R_IN, R_OUT):
        for s in range(segs + 1):
            a = a0 + (a1 - a0) * s / segs
            top.append(bm.verts.new((r * math.cos(a), r * math.sin(a), H)))
            bot.append(bm.verts.new((r * math.cos(a), r * math.sin(a), 0)))
    n = segs + 1
    for s in range(segs):
        for ring in (top, bot):
            q = (ring[s], ring[s + 1], ring[n + s + 1], ring[n + s])
            bm.faces.new(q if ring is top else tuple(reversed(q)))
        for off in (0, n):  # bordes interior y exterior
            q = (bot[off + s], bot[off + s + 1], top[off + s + 1], top[off + s])
            bm.faces.new(q if off else tuple(reversed(q)))
    for idx in (0, segs):  # caras laterales
        q = (bot[idx], bot[n + idx], top[n + idx], top[idx])
        bm.faces.new(q if idx == 0 else tuple(reversed(q)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    w = C.mesh_object(f"Cuña_{i:02d}", bm, C.clay_material(f"Tono_{i:02d}", col, roughness=0.6), "Rueda")
    m = w.modifiers.new("Bevel", "BEVEL"); m.width = 0.06; m.segments = 3
    C.handmade(w, 0.025, 0.5, 2, seed=i + 60)
    w["smart_uv"] = True  # UV planas de la tapa superior para hornear
    w.parent = root

# Eje complementario luminoso (azul 6 ↔ naranja 0/11)
A_BLUE = 2 * math.pi * 6.5 / 12
A_ORNG = 2 * math.pi * 0.5 / 12
pts = [((1 - t) * (R_OUT + 0.2) * math.cos(A_BLUE) + t * (R_OUT + 0.2) * math.cos(A_ORNG),
        (1 - t) * (R_OUT + 0.2) * math.sin(A_BLUE) + t * (R_OUT + 0.2) * math.sin(A_ORNG), H + 0.05)
       for t in [k / 60 for k in range(61)]]
axis = C.tube_along("Eje_complementario", pts, radius=0.02, sides=8,
                    material=C.glow_material("Eje_luz", P["cian_adn"], 6.0), collection="Rueda")
axis.parent = root

# Gotas
def drop(name, color, loc, r=0.42):
    d = C.uv_sphere(name, r, 40, 20, C.clay_material(f"{name}_mat", color, roughness=0.56, sss=0.1), "Gotas")
    C.handmade(d, 0.03, 0.35, 1, seed=C.stable_seed(name, 90))
    C.add_shape_key(d, "Aplastar", lambda co: Vector((co.x * 1.3, co.y * 1.3, co.z * 0.6 - r * 0.2)))
    C.add_shape_key(d, "Estirar", lambda co: Vector((co.x * 0.8, co.y * 0.8, co.z * 1.45 + r * 0.2)))
    d.location = loc
    d.parent = root
    return d


z0 = H + 0.42
blue = drop("Gota_gris_azulada", "#5f6b7a", (2.0 * math.cos(A_BLUE), 2.0 * math.sin(A_BLUE), z0))
orng = drop("Gota_naranja", "#cf7a3a", (2.0 * math.cos(A_ORNG), 2.0 * math.sin(A_ORNG), z0))
neutral = drop("Gota_neutra", "#6e4a36", (0, 0, z0 + 0.12), r=0.55)
blue["papel"], orng["papel"], neutral["papel"] = "pigmento virado", "corrector", "resultado neutro"

# Peana central
bm = bmesh.new()
bm.loops.layers.uv.new("UVMap")
bmesh.ops.create_cone(bm, cap_ends=True, segments=48, radius1=0.8, radius2=0.72, depth=0.22, calc_uvs=True)
ped = C.mesh_object("Peana", bm, C.clay_material("Peana_hueso", "#cbbfac", roughness=0.65), "Rueda")
ped.location = (0, 0, 0.11)
C.handmade(ped, 0.02, 0.6, 1, seed=5)
ped["smart_uv"] = True
ped.parent = root

C.camera("CAM_16x9", lens=40, location=(0.0, -9.5, 5.6), target=(0, 0, 0.4), fstop=4.5)
C.camera("CAM_9x16", lens=40, location=(0.0, -11.5, 8.5), target=(0, 0.2, 0.3), fstop=5.0)

C.bake_web_materials([o for o in sc.objects if o.type == "MESH" and o.name != "Ciclorama"], size=512)

# ---------------- Animación ----------------
def hop(obj, start, end, a, b, hops=3):
    """Viaje a saltitos con squash & stretch: muy de plastilina."""
    kb = obj.data.shape_keys.key_blocks
    for f in C.steps(0, END):
        t = (f - start) / (end - start)
        tc = max(0.0, min(1.0, t))
        p = Vector(a).lerp(Vector(b), C.ease(tc))
        ph = (tc * hops) % 1.0
        lift = math.sin(ph * math.pi) * 0.35 if 0 < tc < 1 else 0
        obj.location = (p.x, p.y, p.z + lift)
        land = 0 < tc <= 1 and (ph < 0.12 or ph > 0.92)
        kb["Aplastar"].value = 0.7 if land else 0.0
        kb["Estirar"].value = 0.5 if (0 < tc < 1 and 0.2 < ph < 0.5) else 0.0
        obj.keyframe_insert("location", frame=f)
        kb["Aplastar"].keyframe_insert("value", frame=f)
        kb["Estirar"].keyframe_insert("value", frame=f)


MERGE = 70
hop(blue, 12, MERGE, blue.location.copy(), (-0.28, 0, z0 + 0.12))
hop(orng, 12, MERGE, orng.location.copy(), (0.28, 0, z0 + 0.12))

# Sustitución: las dos gotas desaparecen y nace la neutra (overshoot)
for f in C.steps(0, END):
    t = (f - MERGE) / 8
    s_out = 1.0 if t <= 0 else max(0.001, 1 - C.ease(t))
    for o in (blue, orng):
        o.scale = (s_out,) * 3
        o.keyframe_insert("scale", frame=f)
    t2 = (f - MERGE - 2) / 14
    s_in = 0.001 if t2 <= 0 else C.overshoot(t2, 1.2)
    neutral.scale = (max(0.001, s_in),) * 3
    neutral.keyframe_insert("scale", frame=f)
    kb = neutral.data.shape_keys.key_blocks
    kb["Aplastar"].value = 0.8 if 0 < t2 < 0.35 else (0.3 if 0.35 <= t2 < 0.6 else 0.0)
    kb["Aplastar"].keyframe_insert("value", frame=f)

for f in C.steps(0, END):
    root.rotation_euler = (0, 0, math.radians(-12 + 30 * C.ease(f / END)))
    root.keyframe_insert("rotation_euler", frame=f)
    axis.scale = (1, 1, 1) if f >= 6 else (0.001, 0.001, 0.001)
    axis.keyframe_insert("scale", frame=f)

C.key_path(sc.objects["CAM_16x9"], [(0, (0.0, -9.5, 5.6)), (END, (1.2, -7.6, 3.6))])
C.key_path(sc.objects["CAM_9x16"], [(0, (0.0, -11.5, 8.5)), (END, (0.8, -9.5, 6.2))])
C.animate_boil([m for m in bpy.data.materials if m.node_tree and "ClayBoil" in m.node_tree.nodes
                and "_web_" not in m.name], 0, END)

C.save_blend(os.path.join(C.ASSETS, "blend", f"{SLUG}.blend"))
C.export_glb(os.path.join(C.ASSETS, "glb", "source", f"{SLUG}.glb"))
print("OK", SLUG)
