FROM python:3.11-slim

# Minimal runtime libraries only, no system GDAL to avoid conflicts
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates libstdc++6 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything into the container
COPY . .

# Set environment variables
ENV WORLDPOP_2023_PATH=/app/data/worldpop_2023_region.tif
ENV PYTHONUNBUFFERED=1

# Use shell form so Railway expands $PORT automatically
CMD sh -c "uvicorn app:app --host 0.0.0.0 --port $PORT --proxy-headers"
