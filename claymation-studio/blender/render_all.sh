#!/usr/bin/env bash
# Renderiza todas las secuencias (reanudable: salta fotogramas existentes) y las codifica.
# 16:9 → 1280×720 (escritorio) · 9:16 → 540×960 (móvil)
set -euo pipefail
cd "$(dirname "$0")"
PY=${BPY_PYTHON:-/opt/blenv/bin/python}
for slug in adn-del-color capas-de-la-piel neutralizacion-del-color; do
  "$PY" render.py "$slug" 16x9 --samples 8 --base 1280 2>&1 | grep -E "RENDER|Error" || true
done
for slug in adn-del-color capas-de-la-piel neutralizacion-del-color; do
  "$PY" render.py "$slug" 9x16 --samples 8 --base 960 2>&1 | grep -E "RENDER|Error" || true
done
bash encode.sh
