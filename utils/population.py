# utils/population.py
from typing import Optional, List, Dict, Any

# In the future, replace these stubs with your real providers:
# - Raster / tiles lookup (WorldPop/GHSL)
# - Vector aggregation (OSM/admin polygons)
# - Cached lookups by neighbourhood_id or slug

def estimate_population_point(lat: float, lng: float, radius_m: int) -> Dict[str, Any]:
    """
    Stub estimator for point+radius. Replace with real logic (raster sampling).
    """
    # TODO: sample population raster by buffered point
    return {
        "method": "point_buffer",
        "lat": lat,
        "lng": lng,
        "radius_m": radius_m,
        "population": None,     # put your computed integer here
        "confidence": 0.0,      # 0..1
        "notes": "Stub response. Plug real raster/tiles provider."
    }

def estimate_population_polygon(geojson: Dict[str, Any]) -> Dict[str, Any]:
    """
    Stub estimator for polygon GeoJSON. Replace with real logic (zonal stats).
    """
    # TODO: compute zonal statistics over polygon
    return {
        "method": "polygon",
        "population": None,
        "confidence": 0.0,
        "notes": "Stub response. Plug real zonal stats over population raster."
    }
