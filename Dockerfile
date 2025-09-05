FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates libstdc++6 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything, including seed/ and start.sh
COPY . .

# Ensure start.sh is executable
RUN chmod +x start.sh

# (Optional safety) Pre-create mount path; copy will no-op if seed is missing
RUN mkdir -p /app/data && cp ./seed/worldpop_2023_region.tif /app/data/ || true

ENV WORLDPOP_2023_PATH=/app/data/worldpop_2023_region.tif
ENV PYTHONUNBUFFERED=1

# Use shell form so $PORT expands on Railway
CMD sh -c "./start.sh"
