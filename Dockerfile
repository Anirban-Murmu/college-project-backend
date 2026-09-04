# ============================================================
# BUILD STAGE
# ============================================================

FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --prefix=/install \
    -r requirements.txt


# ============================================================
# PRODUCTION STAGE
# ============================================================

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ------------------------------------------------------------
# Create non-root application user
# ------------------------------------------------------------

RUN useradd --create-home appuser

WORKDIR /app

# ------------------------------------------------------------
# Copy installed Python packages
# ------------------------------------------------------------

COPY --from=builder /install /usr/local

# ------------------------------------------------------------
# Copy project files
# ------------------------------------------------------------

COPY --chown=appuser:appuser . .

# ------------------------------------------------------------
# Create static files directory
# ------------------------------------------------------------

RUN mkdir -p /app/staticfiles \
    && chown -R appuser:appuser /app/staticfiles

# ------------------------------------------------------------
# Run application as non-root user
# ------------------------------------------------------------

USER appuser

# ------------------------------------------------------------
# Port
# ------------------------------------------------------------

EXPOSE 8005

# ------------------------------------------------------------
# Startup
# ------------------------------------------------------------

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py create_admin && gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --workers 1 --bind 0.0.0.0:$PORT"]