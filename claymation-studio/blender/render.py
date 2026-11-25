"""
Render de secuencias stop motion (12 poses/s) y fotogramas fijos.

Uso:
  python render.py <slug> <16x9|9x16> [--still FRAME] [--samples N] [--base PX]

Salida:
  assets/video/_frames/<slug>_<aspect>/####.png   (secuencia)
  assets/posters/<slug>_<aspect>_f<frame>.png      (fijo)
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
import clay_lib as C  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("slug")
ap.add_argument("aspect", choices=["16x9", "9x16"])
ap.add_argument("--still", type=int, default=None)
ap.add_argument("--samples", type=int, default=32)
ap.add_argument("--base", type=int, default=1280)
args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])

bpy.ops.wm.open_mainfile(filepath=os.path.join(C.ASSETS, "blend", f"{args.slug}.blend"))
sc = C.setup_render(args.aspect, samples=args.samples, base=args.base)

if args.still is not None:
    sc.frame_set(args.still)
    out = os.path.join(C.ASSETS, "posters", f"{args.slug}_{args.aspect}_f{args.still:03d}.png")
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
else:
    out_dir = os.path.join(C.ASSETS, "video", "_frames", f"{args.slug}_{args.aspect}")
    os.makedirs(out_dir, exist_ok=True)
    sc.render.filepath = os.path.join(out_dir, "")
    sc.render.use_overwrite = False   # reanudable: salta fotogramas ya hechos
    sc.render.use_placeholder = False
    bpy.ops.render.render(animation=True)
print("RENDER OK", args.slug, args.aspect)
