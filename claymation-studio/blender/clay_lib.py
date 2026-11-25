"""
Claymation Science Studio · librería Blender (bpy 5.x)
=======================================================

Utilidades reutilizables para construir escenas de plastilina escultórica
(claymation / stop motion) de forma 100 % procedural y reproducible:

* Material de plastilina auténtica (subsurface, rugosidad, huellas, poros,
  pequeñas abolladuras y variación tonal) con "hervido" de stop motion.
* Geometría con irregularidades aplicadas (bultos de modelado a mano).
* Estudio fotográfico: ciclorama, luz principal suave, relleno y contra.
* Cámaras cinematográficas 16:9 y 9:16 con profundidad de campo.
* Animación escalonada "on twos" (12 fps reales a 24 fps) con micro-jitter.
* Horneado (bake) de color y normales para materiales compatibles con glTF.
* Exportación GLB y guardado del .blend original.

Se ejecuta con el módulo oficial `bpy` (PyPI, Blender Foundation) o dentro de
Blender: `blender -b -P scenes/<escena>.py`.
"""
from __future__ import annotations

import math
import os
import random
from typing import Iterable

import bmesh
import bpy
from mathutils import Vector

# --------------------------------------------------------------------------
# Rutas
# --------------------------------------------------------------------------
STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(STUDIO_ROOT, "assets")
BAKE_DIR = os.path.join(STUDIO_ROOT, "assets", "glb", "_bake")

FPS = 24
STEP = 2  # stop motion "on twos": una pose nueva cada 2 fotogramas

# Paleta escultórica (no infantil): tonos minerales, piel, pigmento.
PALETTE = {
    "grafito": "#2a2b2f",
    "pizarra": "#3c4048",
    "hueso": "#e8dfd0",
    "marfil": "#efe6d6",
    "arcilla": "#b8644a",
    "terracota": "#a24f38",
    "salvia": "#8c9a7e",
    "azul_acero": "#5b6f86",
    "ocre": "#c4913f",
    "ciruela": "#6c4258",
    "rosa_piel": "#d9a596",
    "dermis": "#c77b72",
    "hipodermis": "#e3c48d",
    "cian_adn": "#7fe3e0",
}


def hex_to_rgba(h: str, alpha: float = 1.0):
    """Convierte #rrggbb (sRGB) a RGBA lineal para Blender."""
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    return (*lin, alpha)


# --------------------------------------------------------------------------
# Escena
# --------------------------------------------------------------------------
def reset_scene(frame_end: int = 96):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    prefs = bpy.context.preferences
    # Las claves nuevas son CONSTANTES: pose fija entre pasos = stop motion.
    prefs.edit.keyframe_new_interpolation_type = "CONSTANT"
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.frame_start = 0
    sc.frame_end = frame_end
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 32
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 4
    sc.cycles.adaptive_threshold = 0.03
    sc.view_settings.view_transform = "AgX"
    try:
        sc.view_settings.look = "AgX - Medium High Contrast"
    except TypeError:
        pass
    sc.render.film_transparent = False
    world = bpy.data.worlds.new("Mundo")
    sc.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = hex_to_rgba("#141518")
    bg.inputs["Strength"].default_value = 0.35
    random.seed(7)
    return sc


def link(obj, collection: str | None = None):
    sc = bpy.context.scene
    if collection:
        col = bpy.data.collections.get(collection)
        if col is None:
            col = bpy.data.collections.new(collection)
            sc.collection.children.link(col)
    else:
        col = sc.collection
    col.objects.link(obj)
    return obj


# --------------------------------------------------------------------------
# Material de plastilina
# --------------------------------------------------------------------------
def clay_material(name: str, color: str, *, roughness: float = 0.58,
                  sss: float = 0.18, fingerprints: float = 1.0,
                  emission: str | None = None, emission_strength: float = 0.0):
    """Plastilina auténtica: SSS suave, poros, abolladuras, huellas y "hervido".

    El nodo de valor "ClayBoil" desplaza el ruido 3D; animarlo paso a paso
    reproduce el temblor de superficie típico del stop motion real.
    """
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    N, L = nt.nodes, nt.links
    p = N["Principled BSDF"]
    base = hex_to_rgba(color)

    coord = N.new("ShaderNodeTexCoord")
    boil = N.new("ShaderNodeValue")
    boil.name = boil.label = "ClayBoil"
    boil.outputs[0].default_value = 0.0

    # "Hervido": desplaza el espacio de ruido 3D (barato) en cada pose
    comb = N.new("ShaderNodeCombineXYZ")
    for i, k in enumerate((1.0, 0.7, 1.3)):
        mulk = N.new("ShaderNodeMath"); mulk.operation = "MULTIPLY"
        mulk.inputs[1].default_value = k
        L.new(boil.outputs[0], mulk.inputs[0])
        L.new(mulk.outputs[0], comb.inputs[i])
    vec = N.new("ShaderNodeVectorMath"); vec.operation = "ADD"
    L.new(coord.outputs["Object"], vec.inputs[0])
    L.new(comb.outputs[0], vec.inputs[1])
    boiled = vec.outputs[0]

    # Variación tonal (amasado irregular)
    tone = N.new("ShaderNodeTexNoise")
    tone.inputs["Scale"].default_value = 2.2
    tone.inputs["Detail"].default_value = 2.0
    L.new(coord.outputs["Object"], tone.inputs["Vector"])
    ramp = N.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = tuple(c * 0.86 for c in base[:3]) + (1,)
    ramp.color_ramp.elements[1].color = tuple(min(1, c * 1.08) for c in base[:3]) + (1,)
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[1].position = 0.7
    L.new(tone.outputs["Factor"], ramp.inputs["Fac"])
    L.new(ramp.outputs["Color"], p.inputs["Base Color"])

    # Poros finos
    pores = N.new("ShaderNodeTexNoise")
    pores.inputs["Scale"].default_value = 95.0
    pores.inputs["Detail"].default_value = 3.0
    pores.inputs["Roughness"].default_value = 0.62
    L.new(boiled, pores.inputs["Vector"])

    # Abolladuras de herramienta / dedo
    dents = N.new("ShaderNodeTexVoronoi")
    dents.feature = "F1"
    dents.inputs["Scale"].default_value = 9.0
    L.new(boiled, dents.inputs["Vector"])

    # Huellas dactilares: anillos distorsionados, enmascarados por ruido
    warp = N.new("ShaderNodeTexWave")
    warp.wave_type = "RINGS"
    warp.inputs["Scale"].default_value = 38.0
    warp.inputs["Distortion"].default_value = 7.0
    warp.inputs["Detail"].default_value = 1.0
    L.new(coord.outputs["Object"], warp.inputs["Vector"])
    mask = N.new("ShaderNodeTexNoise")
    mask.inputs["Scale"].default_value = 3.5
    L.new(coord.outputs["Object"], mask.inputs["Vector"])
    mask_ramp = N.new("ShaderNodeMapRange")
    mask_ramp.inputs["From Min"].default_value = 0.55
    mask_ramp.inputs["From Max"].default_value = 0.7
    mask_ramp.inputs["To Max"].default_value = fingerprints
    L.new(mask.outputs["Factor"], mask_ramp.inputs["Value"])
    finger = N.new("ShaderNodeMath")
    finger.operation = "MULTIPLY"
    L.new(warp.outputs["Factor"], finger.inputs[0])
    L.new(mask_ramp.outputs["Result"], finger.inputs[1])

    # Suma de alturas
    h1 = N.new("ShaderNodeMath"); h1.operation = "MULTIPLY_ADD"
    L.new(pores.outputs["Factor"], h1.inputs[0]); h1.inputs[1].default_value = 0.35
    L.new(finger.outputs[0], h1.inputs[2])
    h2 = N.new("ShaderNodeMath"); h2.operation = "MULTIPLY_ADD"
    L.new(dents.outputs["Distance"], h2.inputs[0]); h2.inputs[1].default_value = 0.8
    L.new(h1.outputs[0], h2.inputs[2])

    bump = N.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.32
    bump.inputs["Distance"].default_value = 0.012
    L.new(h2.outputs[0], bump.inputs["Height"])
    L.new(bump.outputs["Normal"], p.inputs["Normal"])

    # Rugosidad modulada: zonas más pulidas por el dedo
    rough = N.new("ShaderNodeMapRange")
    rough.inputs["To Min"].default_value = roughness - 0.12
    rough.inputs["To Max"].default_value = roughness + 0.08
    L.new(mask.outputs["Factor"], rough.inputs["Value"])
    L.new(rough.outputs["Result"], p.inputs["Roughness"])

    p.inputs["Subsurface Weight"].default_value = sss
    p.inputs["Subsurface Radius"].default_value = (1.0, 0.45, 0.25)
    p.inputs["Subsurface Scale"].default_value = 0.035
    p.inputs["Sheen Weight"].default_value = 0.12
    p.inputs["Sheen Roughness"].default_value = 0.5
    p.inputs["Specular IOR Level"].default_value = 0.38
    if emission:
        p.inputs["Emission Color"].default_value = hex_to_rgba(emission)
        p.inputs["Emission Strength"].default_value = emission_strength

    mat["clay_color"] = color
    mat["clay_roughness"] = roughness
    return mat


def glow_material(name: str, color: str, strength: float = 6.0):
    """Material luminoso para los acentos "futurismo ADN" (líneas de escaneo)."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    p = mat.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = hex_to_rgba(color)
    p.inputs["Emission Color"].default_value = hex_to_rgba(color)
    p.inputs["Emission Strength"].default_value = strength
    p.inputs["Roughness"].default_value = 0.3
    mat["clay_color"] = color
    mat["clay_roughness"] = 0.3
    mat["glow"] = strength
    return mat


def animate_boil(materials: Iterable, start: int, end: int, step: int = STEP):
    """Desplaza el ruido 3D en cada paso: superficie que "respira" a mano."""
    for mat in materials:
        node = mat.node_tree.nodes.get("ClayBoil")
        if not node:
            continue
        for i, f in enumerate(range(start, end + 1, step)):
            node.outputs[0].default_value = i * 0.37 + random.random() * 0.1
            node.outputs[0].keyframe_insert("default_value", frame=f)


# --------------------------------------------------------------------------
# Geometría
# --------------------------------------------------------------------------
def mesh_object(name: str, bm: bmesh.types.BMesh, material=None, collection=None):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for poly in me.polygons:
        poly.use_smooth = True
    obj = bpy.data.objects.new(name, me)
    if material:
        me.materials.append(material)
    return link(obj, collection)


def uv_sphere(name, radius=1.0, segments=48, rings=24, material=None, collection=None):
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")
    bmesh.ops.create_uvsphere(bm, u_segments=segments, v_segments=rings,
                              radius=radius, calc_uvs=True)
    return mesh_object(name, bm, material, collection)


def capsule(name, radius=0.2, length=1.0, material=None, collection=None, axis="X"):
    """Cápsula (churro de plastilina) a partir de una esfera estirada."""
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=20, radius=radius, calc_uvs=True)
    half = max(0.0, length / 2 - radius)
    for v in bm.verts:
        v.co.z += half if v.co.z > 1e-6 else (-half if v.co.z < -1e-6 else 0)
    if axis == "X":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0),
                         matrix=__import__("mathutils").Matrix.Rotation(math.pi / 2, 3, "Y"))
    return mesh_object(name, bm, material, collection)


def rounded_box(name, size=(1, 1, 1), bevel=0.08, material=None, collection=None):
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")
    bmesh.ops.create_cube(bm, size=1.0, calc_uvs=True)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=bevel,
                    segments=4, affect="EDGES", profile=0.5)
    return mesh_object(name, bm, material, collection)


def tube_along(name, points, radius=0.12, sides=20, material=None, collection=None,
               closed=False):
    """Barre un círculo a lo largo de una polilínea (con UVs)."""
    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")
    rings = []
    pts = [Vector(p) for p in points]
    n = len(pts)
    prev_side = None
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        up = Vector((0, 0, 1)) if abs(t.z) < 0.95 else Vector((1, 0, 0))
        side = t.cross(up).normalized() if prev_side is None else (prev_side - t * prev_side.dot(t)).normalized()
        prev_side = side
        up2 = side.cross(t).normalized()
        ring = []
        for s in range(sides):
            a = 2 * math.pi * s / sides
            ring.append(bm.verts.new(p + (side * math.cos(a) + up2 * math.sin(a)) * radius))
        rings.append(ring)
    for i in range(n - 1):
        for s in range(sides):
            s2 = (s + 1) % sides
            f = bm.faces.new((rings[i][s], rings[i][s2], rings[i + 1][s2], rings[i + 1][s]))
            for loop, (u, v) in zip(f.loops, ((s, i), (s + 1, i), (s + 1, i + 1), (s, i + 1))):
                loop[uv_layer].uv = (u / sides, v / (n - 1))
    # tapas redondeadas sencillas
    for ring, end in ((rings[0], pts[0] - (pts[1] - pts[0]).normalized() * radius * 0.6),
                      (rings[-1], pts[-1] + (pts[-1] - pts[-2]).normalized() * radius * 0.6)):
        c = bm.verts.new(end)
        for s in range(sides):
            bm.faces.new((ring[s], ring[(s + 1) % sides], c) if ring is rings[-1]
                         else (ring[(s + 1) % sides], ring[s], c))
    bm.normal_update()
    return mesh_object(name, bm, material, collection)


def apply_modifiers(obj):
    """Aplica modificadores vía depsgraph (sin operadores ni contexto UI)."""
    dg = bpy.context.evaluated_depsgraph_get()
    new_me = bpy.data.meshes.new_from_object(obj.evaluated_get(dg))
    old = obj.data
    obj.modifiers.clear()
    obj.data = new_me
    new_me.name = old.name
    if old.users == 0:
        bpy.data.meshes.remove(old)
    for poly in obj.data.polygons:
        poly.use_smooth = True


def handmade(obj, strength=0.025, scale=0.55, subdiv=1, seed=None):
    """Bultos de modelado manual: subdivisión + desplazamiento de ruido, aplicados.

    Se aplican al mallado para que sobrevivan a la exportación glTF y sean
    compatibles con shape keys (que se añaden después).
    """
    if subdiv:
        m = obj.modifiers.new("Sub", "SUBSURF")
        m.levels = m.render_levels = subdiv
    tex = bpy.data.textures.new(f"lumps_{obj.name}", "CLOUDS")
    tex.noise_scale = scale
    tex.noise_depth = 2
    d = obj.modifiers.new("Bultos", "DISPLACE")
    d.texture = tex
    d.texture_coords = "LOCAL"
    d.strength = strength
    d.mid_level = 0.5
    if seed is not None:
        # desplaza el espacio de ruido para que cada pieza sea única
        e = bpy.data.objects.new(f"seed_{obj.name}", None)
        e.location = (seed * 3.17, seed * 1.31, seed * 2.03)
        link(e)
        d.texture_coords = "OBJECT"
        d.texture_coords_object = e
        e.parent = obj
        e.matrix_parent_inverse = obj.matrix_world.inverted()
    apply_modifiers(obj)
    for c in list(obj.children):
        if c.type == "EMPTY" and c.name.startswith("seed_"):
            bpy.data.objects.remove(c)
    return obj


# --------------------------------------------------------------------------
# Estudio: ciclorama, luces, cámaras
# --------------------------------------------------------------------------
def cyclorama(color=PALETTE["grafito"], width=40.0, depth=26.0, height=14.0, radius=4.0, wall_y=6.0):
    # perfil: suelo recto + cuarto de círculo + pared
    prof =[(-depth + i * (depth - radius) / 7, 0.0) for i in range(8)]
    for i in range(1, 17):
        a = (math.pi / 2) * i / 16
        prof.append((-radius + radius * math.sin(a), radius - radius * math.cos(a)))
    prof.append((0.0, height))
    bm = bmesh.new()
    cols = 24
    grid = []
    for xi in range(cols + 1):
        x = -width / 2 + width * xi / cols
        grid.append([bm.verts.new((x, y + wall_y, z)) for (y, z) in prof])
    for xi in range(cols):
        for j in range(len(prof) - 1):
            bm.faces.new((grid[xi][j], grid[xi + 1][j], grid[xi + 1][j + 1], grid[xi][j + 1]))
    obj = mesh_object("Ciclorama", bm, clay_material("Fondo_grafito", color, roughness=0.8,
                                                     sss=0.0, fingerprints=0.25),
                      collection="Estudio")
    obj["web_export"] = False
    return obj


def area_light(name, location, target=(0, 0, 0), energy=500, size=4.0, color="#ffffff"):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy = energy
    ld.size = size
    ld.color = hex_to_rgba(color)[:3]
    ob = link(bpy.data.objects.new(name, ld), "Estudio")
    ob.location = location
    aim(ob, target)
    return ob


def aim(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def cinematic_lighting(key_energy=900, rim_color=PALETTE["cian_adn"], target=(0, 0, 1)):
    """Luz principal grande y cálida (sombras suaves), relleno frío, contra cian."""
    area_light("Luz_principal", (-4.5, -5.0, 6.0), target, key_energy, 5.0, "#ffe7cf")
    area_light("Luz_relleno", (6.0, -4.0, 2.5), target, key_energy * 0.18, 6.0, "#d7e4ff")
    area_light("Luz_contra", (2.5, 5.5, 5.0), target, key_energy * 0.55, 2.0, rim_color)
    area_light("Luz_cenital", (0, 0, 9), target, key_energy * 0.15, 8.0, "#ffffff")


def camera(name, lens=50, location=(0, -10, 2), target=(0, 0, 1), fstop=2.8, sensor=36):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = sensor
    cd.dof.use_dof = True
    cd.dof.aperture_fstop = fstop
    ob = link(bpy.data.objects.new(name, cd), "Camaras")
    ob.location = location
    tgt = link(bpy.data.objects.new(f"{name}_foco", None), "Camaras")
    tgt.location = target
    cd.dof.focus_object = tgt
    c = ob.constraints.new("TRACK_TO")
    c.target = tgt
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    return ob, tgt


def key_path(obj, keys):
    """keys = [(frame, (x,y,z)), ...]  · interpola suave y muestrea en pasos de 2.

    La cámara se mueve con suavizado cinematográfico (ease in-out), pero las
    claves se fijan cada STEP fotogramas, como en una mesa de stop motion.
    """
    keys = sorted(keys)
    f0, f1 = keys[0][0], keys[-1][0]
    for f in range(f0, f1 + 1, STEP):
        for (fa, pa), (fb, pb) in zip(keys, keys[1:]):
            if fa <= f <= fb:
                t = (f - fa) / max(1, fb - fa)
                t = t * t * (3 - 2 * t)
                obj.location = Vector(pa).lerp(Vector(pb), t)
                break
        obj.keyframe_insert("location", frame=f)


# --------------------------------------------------------------------------
# Animación stop motion
# --------------------------------------------------------------------------
def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def overshoot(t, amount=1.15):
    """0→1 con rebote suave (squash & stretch de plastilina)."""
    t = max(0.0, min(1.0, t))
    if t < 0.7:
        return ease(t / 0.7) * amount
    return amount + (1 - amount) * ease((t - 0.7) / 0.3)


def steps(start, end, step=STEP):
    return range(start, end + 1, step)


def jitter_keys(obj, start, end, loc=0.004, rot=0.35, scale_keys=False):
    """Micro-temblor de manipulación manual en cada pose (stop motion real)."""
    base_loc = obj.location.copy()
    base_rot = obj.rotation_euler.copy()
    for f in steps(start, end):
        obj.location = base_loc + Vector([random.uniform(-loc, loc) for _ in range(3)])
        obj.rotation_euler = [r + math.radians(random.uniform(-rot, rot)) for r in base_rot]
        obj.keyframe_insert("location", frame=f)
        obj.keyframe_insert("rotation_euler", frame=f)
    obj.location, obj.rotation_euler = base_loc, base_rot


def add_shape_key(obj, name, fn):
    """Crea una shape key moviendo cada vértice con fn(co) -> co nuevo."""
    if obj.data.shape_keys is None:
        obj.shape_key_add(name="Basis", from_mix=False)
    sk = obj.shape_key_add(name=name, from_mix=False)
    for i, v in enumerate(obj.data.vertices):
        sk.data[i].co = fn(v.co.copy())
    sk.value = 0.0
    return sk


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------
def setup_render(aspect="16x9", samples=32, base=1280):
    sc = bpy.context.scene
    cam = bpy.data.objects.get(f"CAM_{aspect}")
    if cam:
        sc.camera = cam
    if aspect == "16x9":
        sc.render.resolution_x, sc.render.resolution_y = base, int(base * 9 / 16)
    else:
        sc.render.resolution_x, sc.render.resolution_y = int(base * 9 / 16), base
    sc.render.resolution_percentage = 100
    sc.cycles.samples = samples
    sc.frame_step = STEP
    sc.render.image_settings.file_format = "PNG"
    return sc


# --------------------------------------------------------------------------
# Horneado y exportación web (glTF / GLB)
# --------------------------------------------------------------------------
def stable_seed(text: str, mod: int = 97) -> int:
    """Semilla determinista (hash() de Python cambia en cada ejecución)."""
    import zlib
    return zlib.crc32(text.encode("utf-8")) % mod


def cylinder_uv(obj):
    """UV cilíndricas para peanas/pedestales: laterales abajo, tapas arriba.

    El cono de bmesh sólo genera UV de las tapas y Smart UV Project no es
    fiable sin interfaz, así que se calcula a mano.
    """
    me = obj.data
    while me.uv_layers:
        me.uv_layers.remove(me.uv_layers[0])
    uv = me.uv_layers.new(name="UVMap").data
    rmax = max(math.hypot(v.co.x, v.co.y) for v in me.vertices) or 1.0
    zs = [v.co.z for v in me.vertices]
    z0, z1 = min(zs), max(zs)
    for poly in me.polygons:
        nz = poly.normal.z
        coords = []
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            if abs(nz) > 0.7:  # tapa superior (izq.) o inferior (dcha.)
                ox = 0.25 if nz > 0 else 0.75
                coords.append((ox + co.x / rmax * 0.24, 0.75 + co.y / rmax * 0.24))
            else:
                a = (math.atan2(co.y, co.x) / (2 * math.pi)) % 1.0
                coords.append((a, 0.02 + 0.46 * (co.z - z0) / max(1e-6, z1 - z0)))
        if abs(nz) <= 0.7:
            us = [c[0] for c in coords]
            if max(us) - min(us) > 0.5:  # cara que cruza la costura
                coords = [((u + 1.0) if u < 0.5 else u, v) for u, v in coords]
                coords = [(min(u, 0.999), v) for u, v in coords]
        for li, c in zip(poly.loop_indices, coords):
            uv[li].uv = c


def ensure_uv(obj, force=False):
    """Garantiza un mapa UV sin solapes (Smart UV Project) para hornear."""
    if obj.data.uv_layers and not force:
        return
    while obj.data.uv_layers:
        obj.data.uv_layers.remove(obj.data.uv_layers[0])
    obj.data.uv_layers.new(name="UVMap")
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")


def bake_web_materials(objects, size=512, samples=4):
    """Hornea color y normales de la plastilina procedural en texturas.

    glTF no admite nodos procedurales: cada objeto recibe un material
    "_web" (Principled + imagen de color + mapa de normales) que se asigna
    sólo durante la exportación. Debe llamarse antes de animar escalas a 0.
    """
    os.makedirs(BAKE_DIR, exist_ok=True)
    sc = bpy.context.scene
    prev_samples = sc.cycles.samples
    sc.cycles.samples = samples
    sc.render.bake.margin = 4
    hidden = {o: o.hide_render for o in sc.objects}
    for obj in objects:
        if obj.type != "MESH" or not obj.data.materials:
            continue
        if obj.get("smart_uv"):
            cylinder_uv(obj)
        else:
            ensure_uv(obj)
        for o in sc.objects:  # BVH mínimo: sólo el objeto que se hornea
            o.hide_render = (o is not obj) and o.type == "MESH"
        src = obj.data.materials[0]
        if src.get("glow"):
            obj["web_mat"] = src.name
            continue
        res = size if max(obj.dimensions) > 1.2 else max(128, size // 4)
        imgs = {}
        tmp = src.copy()
        tmp.name = f"{src.name}__bake_{obj.name}"
        obj.data.materials[0] = tmp
        node = tmp.node_tree.nodes.new("ShaderNodeTexImage")
        for kind in ("COLOR", "NORMAL"):
            img = bpy.data.images.new(f"{obj.name}_{kind.lower()}", res, res, alpha=False)
            if kind == "NORMAL":
                img.colorspace_settings.name = "Non-Color"
            node.image = img
            tmp.node_tree.nodes.active = node
            for o in bpy.context.view_layer.objects:
                o.select_set(False)
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            if kind == "COLOR":
                bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"}, use_clear=True)
            else:
                bpy.ops.object.bake(type="NORMAL", normal_space="TANGENT", use_clear=True)
            img.filepath_raw = os.path.join(BAKE_DIR, f"{obj.name}_{kind.lower()}.png")
            img.file_format = "PNG"
            img.save()
            imgs[kind] = img
        obj.data.materials[0] = src
        bpy.data.materials.remove(tmp)

        web = bpy.data.materials.new(f"{src.name}_web_{obj.name}")
        web.use_nodes = True
        nt = web.node_tree
        p = nt.nodes["Principled BSDF"]
        tc = nt.nodes.new("ShaderNodeTexImage"); tc.image = imgs["COLOR"]
        nc = nt.nodes.new("ShaderNodeTexImage"); nc.image = imgs["NORMAL"]
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nt.links.new(tc.outputs["Color"], p.inputs["Base Color"])
        nt.links.new(nc.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], p.inputs["Normal"])
        p.inputs["Roughness"].default_value = float(src.get("clay_roughness", 0.6))
        # Sin sheen en web: KHR_materials_sheen se ve como un velo blanco en three.js
        web.use_fake_user = True
        obj["web_mat"] = web.name
        print(f"[bake] {obj.name} {res}px", flush=True)
    for o, h in hidden.items():
        o.hide_render = h
    sc.cycles.samples = prev_samples


def export_glb(path, objects=None):
    """Exporta GLB con animación escalonada y morph targets (shape keys)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    objs = objects or [o for o in bpy.context.scene.objects
                       if o.type == "MESH" and o.get("web_export", True)]
    swapped = []
    for o in objs:
        wm = o.get("web_mat")
        if wm and wm in bpy.data.materials:
            swapped.append((o, o.data.materials[0]))
            o.data.materials[0] = bpy.data.materials[wm]
    for o in bpy.context.view_layer.objects:
        o.select_set(o in objs)
    bpy.context.scene.frame_set(bpy.context.scene.frame_start)
    bpy.ops.export_scene.gltf(
        filepath=path,
        export_format="GLB",
        use_selection=True,
        export_apply=False,
        export_yup=True,
        export_animations=True,
        export_animation_mode="SCENE",
        export_force_sampling=True,
        export_frame_step=1,
        export_morph=True,
        export_morph_normal=False,
        export_morph_animation=True,
        export_image_format="WEBP",
        export_image_quality=82,
        export_cameras=False,
        export_lights=False,
        export_extras=True,
    )
    for o, m in swapped:
        o.data.materials[0] = m


def save_blend(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Empaqueta las texturas horneadas: el .blend queda autocontenido y portable
    for img in bpy.data.images:
        if img.filepath_raw and os.path.exists(bpy.path.abspath(img.filepath_raw)) and not img.packed_file:
            img.pack()
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
