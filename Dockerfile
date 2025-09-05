FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates libstdc++6 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# On first deploy, copy the TIFF from seed into the volume mount path
RUN mkdir -p /app/data && cp ./seed/worldpop_2023_region.tif /app/data/ || true

ENV WORLDPOP_2023_PATH=/app/data/worldpop_2023_region.tif
ENV PYTHONUNBUFFERED=1

CMD ["./start.sh"]
