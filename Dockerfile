# qandro-pop-service/Dockerfile
FROM python:3.11-slim

# System deps for rasterio/GDAL
# NOTE: remove 'libgdal32' (not present on this base)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin libgdal-dev proj-bin libproj-dev ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# (Usually not needed if rasterio wheel bundles GDAL, but harmless)
ENV GDAL_DATA=/usr/share/gdal
ENV PROJ_LIB=/usr/share/proj

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code + raster
COPY app.py ./app.py
COPY data ./data

# Point app at the raster inside the image
ENV WORLDPOP_2023_PATH=/app/data/worldpop_2023_region.tif

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
