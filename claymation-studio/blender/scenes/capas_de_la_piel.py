"""
Escena 02 · «La profundidad exacta» — Instituto Nacional de Micropigmentación

Concepto profesional: la piel tiene capas (epidermis, dermis, hipodermis) y el
pigmento debe quedar en la zona superficial correcta. En el corte de
plastilina, la aguja deposita tres gotas en la franja objetivo (línea cian);
una cuarta inserción demasiado profunda muestra cómo el pigmento se difumina y
vira a gris azulado (migración), el error que la formación enseña a evitar.

Shape keys de la gota: «Estirar», «Aplastar», «Difuminar» (morph targets en GLB).
"""
import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import clay_lib as C  # noqa: E402

SLUG = "capas-de-la-piel"
END = 144
P = C.PALETTE
W, D = 4.4, 2.2           # ancho y fondo del bloque
Z_HYPO, Z_DERM, Z_EPI = 1.0, 2.2, 2.5
Z_TARGET = 2.02           # franja objetivo (dermis superficial)


def wave(x, y):
    """Papilas dérmicas: ondulación de la unión dermo-epidérmica."""
    return 0.07 * math.sin(x * 5.5) * math.cos(y * 3.0) + 0.03 * math.sin(x * 13 + 1)


sc = C.reset_scene(END)
C.cyclorama()
C.cinematic_lighting(key_energy=1000, target=(0, 0, 1.6))
grp = C.link(bpy.data.objects.new("Corte_piel", None), "Piel")

# --- Capas ---
def layer(name, z0, z1, color, top_wave=False, bottom_wave=False, rough=0.6):
    h = z1 - z0
    ob = C.rounded_box(name, (W, D, h), bevel=0.06, material=C.clay_material(f"{name}_mat", color, roughness=rough),
                       collection="Piel")
    ob.location = (0, 0, z0 + h / 2)
    m = ob.modifiers.new("Sub", "SUBSURF"); m.levels = m.render_levels = 3
    C.apply_modifiers(ob)
    for v in ob.data.vertices:
        if top_wave and v.co.z > h / 2 - 0.02:
            v.co.z += wave(v.co.x, v.co.y)
        if bottom_wave and v.co.z < -h / 2 + 0.02:
            v.co.z += wave(v.co.x, v.co.y)
    C.handmade(ob, strength=0.03, scale=0.5, subdiv=0, seed=len(name))
    ob.parent = grp
    return ob


hypo = layer("Hipodermis", 0.0, Z_HYPO, P["hipodermis"], rough=0.66)
derm = layer("Dermis", Z_HYPO, Z_DERM, P["dermis"], top_wave=True)
epi = layer("Epidermis", Z_DERM, Z_EPI, P["rosa_piel"], bottom_wave=True, rough=0.5)

# Lóbulos de grasa asomando en el corte
fat = C.clay_material("Lobulo_mat", "#ecd3a2", roughness=0.62)
for i, (x, z, r) in enumerate([(-1.6, 0.45, 0.32), (-0.8, 0.35, 0.28), (0.1, 0.5, 0.34),
                               (0.95, 0.38, 0.3), (1.7, 0.5, 0.27)]):
    s = C.uv_sphere(f"Lobulo_{i}", r, 32, 16, fat, "Piel")
    s.location = (x, -D / 2 + r * 0.35, z)
    s.scale = (1.0, 0.6, 0.85)
    C.handmade(s, 0.02, 0.4, 1, seed=i + 20)
    s.parent = grp

# Fibras de colágeno en la dermis (frente del corte)
fib = C.clay_material("Colageno_mat", "#e0a08f", roughness=0.55)
for k, z in enumerate((1.3, 1.55, 1.8)):
    pts = [(-W / 2 + 0.25 + t * (W - 0.5) / 40, -D / 2 - 0.02, z + 0.06 * math.sin(t * 0.9 + k))
           for t in range(41)]
    f = C.tube_along(f"Colageno_{k}", pts, radius=0.035, sides=10, material=fib, collection="Piel")
    f.parent = grp

# Franja objetivo luminosa (futurismo ADN)
glow = C.glow_material("Franja_objetivo", P["cian_adn"], 7.0)
pts = [(-W / 2 - 0.15 + t * (W + 0.3) / 60, -D / 2 - 0.06, Z_TARGET) for t in range(61)]
guide = C.tube_along("Franja_objetivo", pts, radius=0.018, sides=8, material=glow, collection="Piel")
guide.parent = grp

# --- Dermógrafo (punta) ---
tool = C.link(bpy.data.objects.new("Dermografo", None), "Herramienta")
body = C.capsule("Dermografo_cuerpo", radius=0.22, length=2.2,
                 material=C.clay_material("Cuerpo_grafito", P["pizarra"], roughness=0.45), collection="Herramienta",
                 axis="Z")
body.location = (0, 0, 1.45)
C.handmade(body, 0.015, 0.5, 1, seed=3)
needle = C.uv_sphere("Dermografo_aguja", 0.06, 24, 12,
                     C.clay_material("Aguja_hueso", "#d8d4cc", roughness=0.35, sss=0.05), "Herramienta")
needle.scale = (1, 1, 6.0)
needle.location = (0, 0, 0.2)
ring_band = C.capsule("Dermografo_anillo", radius=0.235, length=0.5,
                      material=C.clay_material("Anillo_ocre", P["ocre"], roughness=0.5), collection="Herramienta",
                      axis="Z")
ring_band.location = (0, 0, 0.62)
for o in (body, needle, ring_band):
    o.parent = tool

# --- Gotas de pigmento con shape keys ---
pig_ok = C.clay_material("Pigmento_estable", "#5a3b2c", roughness=0.4, sss=0.08)
pig_bad = C.clay_material("Pigmento_migrado", "#56606d", roughness=0.45, sss=0.08)
drops = []
for i, (x, z, mat) in enumerate([(-1.2, Z_TARGET, pig_ok), (-0.2, Z_TARGET, pig_ok),
                                 (0.8, Z_TARGET, pig_ok), (1.6, 1.3, pig_bad)]):
    d = C.uv_sphere(f"Gota_{i}", 0.13, 32, 16, mat, "Pigmento")
    C.handmade(d, 0.015, 0.3, 1, seed=40 + i)
    C.add_shape_key(d, "Estirar", lambda co: Vector((co.x * 0.75, co.y * 0.75, co.z * 1.7)))
    C.add_shape_key(d, "Aplastar", lambda co: Vector((co.x * 1.35, co.y * 1.35, co.z * 0.55)))
    C.add_shape_key(d, "Difuminar", lambda co: Vector((co.x * 2.6, co.y * 1.6, co.z * 0.7)))
    d.location = (x, -D / 2 + 0.05, z)
    d.parent = grp
    d["profundidad"] = "correcta" if i < 3 else "excesiva"
    drops.append(d)

C.camera("CAM_16x9", lens=42, location=(-3.6, -12.0, 5.2), target=(0, 0, 1.55), fstop=4.0)
C.camera("CAM_9x16", lens=50, location=(-2.6, -13.5, 5.6), target=(0, 0, 1.9), fstop=4.0)

C.bake_web_materials([o for o in sc.objects if o.type == "MESH" and o.name != "Ciclorama"], size=512)

# ---------------- Animación ----------------
# Inserciones: (inicio, x, profundidad del extremo de la aguja)
INS = [(10, -1.2, Z_TARGET), (38, -0.2, Z_TARGET), (66, 0.8, Z_TARGET), (96, 1.6, 1.3)]
TOP = Z_EPI + 0.9
# el extremo de la aguja está 0.16 por debajo del origen del dermógrafo
OFF = 0.16

def tool_pose(f):
    x, z = INS[0][1], TOP
    for k, (s, xi, zi) in enumerate(INS):
        if f < s:
            prev = INS[k - 1][1] if k else xi
            t = C.ease((f - (s - 10)) / 8) if k else 1
            x = prev + (xi - prev) * t
            z = TOP
            break
        if s <= f < s + 22:
            x = xi
            t = (f - s) / 22
            dive = math.sin(min(1, t * 1.6) * math.pi / 2) if t < 0.55 else 1 - C.ease((t - 0.55) / 0.45)
            z = TOP + (zi + OFF - TOP) * dive
            break
        x, z = xi, TOP
    return x, z

for f in C.steps(0, END):
    x, z = tool_pose(f)
    tool.location = (x, -D / 2 + 0.05, z)
    tool.rotation_euler = (math.radians(-6), math.radians(4 * math.sin(f * 0.3)), 0)
    tool.keyframe_insert("location", frame=f)
    tool.keyframe_insert("rotation_euler", frame=f)

for i, d in enumerate(drops):
    s0 = INS[i][0] + 10
    keys = d.data.shape_keys.key_blocks
    for f in C.steps(0, END):
        t = (f - s0) / 14
        sc_v = 0.001 if t <= 0 else min(1.0, C.overshoot(t, 1.12))
        d.scale = (sc_v, sc_v, sc_v)
        d.keyframe_insert("scale", frame=f)
        est = max(0.0, 1 - abs(t - 0.2) * 4) if t > 0 else 0
        apl = max(0.0, min(1, (t - 0.35) * 2.5)) * 0.45 if t > 0 else 0
        dif = 0.0
        if i == 3 and t > 0.6:
            dif = C.ease((f - s0 - 10) / 30)
        keys["Estirar"].value = est
        keys["Aplastar"].value = apl if i < 3 else apl * (1 - dif)
        keys["Difuminar"].value = dif
        for kb in ("Estirar", "Aplastar", "Difuminar"):
            keys[kb].keyframe_insert("value", frame=f)

C.jitter_keys(grp, 0, END, loc=0.003, rot=0.15)
C.key_path(sc.objects["CAM_16x9"], [(0, (-3.6, -12.0, 5.2)), (END, (-1.4, -10.6, 4.4))])
C.key_path(sc.objects["CAM_9x16"], [(0, (-2.6, -13.5, 5.6)), (END, (-1.0, -12.2, 4.8))])
C.animate_boil([m for m in bpy.data.materials if m.node_tree and "ClayBoil" in m.node_tree.nodes
                and "_web_" not in m.name], 0, END)

C.save_blend(os.path.join(C.ASSETS, "blend", f"{SLUG}.blend"))
C.export_glb(os.path.join(C.ASSETS, "glb", "source", f"{SLUG}.glb"))
print("OK", SLUG)
