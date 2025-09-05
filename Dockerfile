FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates libstdc++6 && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code + data directory (ensure .dockerignore does not exclude it)
COPY . .

ENV WORLDPOP_2023_PATH=/app/data/worldpop_2023_region.tif
ENV PYTHONUNBUFFERED=1
CMD sh -c "uvicorn app:app --host 0.0.0.0 --port $PORT --proxy-headers"
