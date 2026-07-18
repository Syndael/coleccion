#!/bin/bash
# setup.sh — Instala y arranca el IG Publisher en el NAS
set -e
cd "$(dirname "$0")"

# Crear virtualenv si no existe
if [ ! -d venv ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install --prefer-binary requests "pydantic>=2.0" "Pillow>=9.2.0"
    pip install --no-deps instagrapi
else
    source venv/bin/activate
fi

echo "[OK] Entorno listo. Ejecutando publisher..."
exec python publisher.py
