FROM python:3.13-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY collector/src/collector.c ./collector.c
RUN gcc -std=c11 -O2 -Wall -Wextra -Wpedantic -Wconversion -Werror collector.c -o /collector
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 SYSATLAS_DATABASE=/data/sysatlas.db SYSATLAS_COLLECTOR=/usr/local/bin/sysatlas-collector
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --system --uid 10001 appuser && mkdir -p /data && chown appuser:appuser /data
COPY app ./app
COPY --from=build /collector /usr/local/bin/sysatlas-collector
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=2)" || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
