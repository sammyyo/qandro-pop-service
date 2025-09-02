from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from shapely.geometry import shape
import os
import json

app = FastAPI(title="Qandro Population Service")

# CORS — define once, no trailing slashes
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://qandro.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)

class SumReq(BaseModel):
    polygon_geojson: dict   # can be Feature or Geometry
    year: int = 2023

WORLDPOP = {
    2023: os.getenv("WORLDPOP_2023_PATH", "/data/worldpop_2023_region.tif")
}

# Optional simple token (if you want to enforce POP_SERVICE_TOKEN)
POP_TOKEN = os.getenv("POP_SERVICE_TOKEN", "")

@app.get("/health")
def health():
    tif_path = WORLDPOP.get(2023)
    return {"ok": True, "tif_exists": bool(tif_path and os.path.exists(tif_path))}

def _extract_geometry(obj: dict) -> dict:
    """Accept either a Geometry or a Feature and return the Geometry dict."""
    if not isinstance(obj, dict):
        raise HTTPException(status_code=400, detail="polygon_geojson must be a JSON object")
    t = obj.get("type")
    if t == "Feature":
        geom = obj.get("geometry")
        if not geom:
            raise HTTPException(status_code=400, detail="Feature missing geometry")
        return geom
    if t in ("Polygon", "MultiPolygon"):
        return obj
    raise HTTPException(status_code=400, detail=f"Unsupported GeoJSON type: {t}")

@app.post("/sum")
def sum_population(req: SumReq, authorization: str = Header(default="")):
    # Enforce token if configured
    if POP_TOKEN:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing bearer token")
        token = authorization.split(" ", 1)[1].strip()
        if token != POP_TOKEN:
            raise HTTPException(status_code=403, detail="Invalid token")

    try:
        import rasterio
        from rasterio.mask import mask
        import numpy as np
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Raster deps missing: {e}")

    tif_path = WORLDPOP.get(req.year)
    if not tif_path:
        raise HTTPException(status_code=400, detail=f"Unsupported year: {req.year}")
    if not os.path.exists(tif_path):
        raise HTTPException(status_code=500, detail=f"WorldPop file not found at {tif_path}")

    # Accept Feature or Geometry
    geom_dict = _extract_geometry(req.polygon_geojson)

    try:
        geom = shape(geom_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid polygon: {e}")

    if not geom.is_valid:
        raise HTTPException(status_code=400, detail="Invalid polygon geometry")

    try:
        import shapely.geometry as sgeom
        with rasterio.open(tif_path) as src:
            # Fast bounds check
            minx, miny, maxx, maxy = src.bounds
            raster_box = sgeom.box(minx, miny, maxx, maxy)
            if not geom.intersects(raster_box):
                raise HTTPException(status_code=400, detail="Polygon outside raster coverage")

            # WorldPop is EPSG:4326 (WGS84). Ensure your polygon is also WGS84.
            out, _ = mask(src, [geom.__geo_interface__], crop=True, filled=False)
            band = out[0]  # masked array

            if hasattr(band, "mask"):  # masked array
                pop_sum = float(band.sum())
                count = int(band.count())
            else:
                valid = band[band >= 0]
                pop_sum = float(valid.sum()) if valid.size else 0.0
                count = int(valid.size)

            return {
                "population": int(round(pop_sum)),
                "cells": count,
                "year": req.year,
                "source": "worldpop",
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Raster error: {e}")

@app.get("/sum")
def sum_help():
    return {"error": "Use POST /sum with JSON body { polygon_geojson, year }"}
