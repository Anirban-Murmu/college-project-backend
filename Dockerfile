# =========================
# Stage 1: Build
# =========================
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --prefix=/install \
    -r requirements.txt


# =========================
# Stage 2: Production
# =========================
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd --create-home appuser

WORKDIR /app

# Copy installed Python packages
COPY --from=builder /install /usr/local

# Copy project
COPY --chown=appuser:appuser . .

# Use non-root user
USER appuser

EXPOSE 8005

CMD ["sh", "-c", "python manage.py migrate && python manage.py create_admin && gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --workers 1 --bind 0.0.0.0:$PORT"]