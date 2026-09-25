FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN useradd --create-home appuser \
    && mkdir -p /app/staticfiles \
    && chown appuser:appuser /app/staticfiles

USER appuser

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]