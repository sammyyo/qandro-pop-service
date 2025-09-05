#!/bin/sh
set -e

mkdir -p /app/data

if [ ! -f /app/data/worldpop_2023_region.tif ]; then
  echo "[start] Seeding WorldPop TIFF..."
  cp ./seed/worldpop_2023_region.tif /app/data/ || true
else
  echo "[start] Using cached WorldPop TIFF from volume."
fi

exec uvicorn app:app --host 0.0.0.0 --port "$PORT" --proxy-headers
