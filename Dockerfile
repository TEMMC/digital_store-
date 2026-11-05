FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir Flask==3.1.3 Flask-SQLAlchemy==3.1.1 gunicorn==23.0.0 psycopg[binary]==3.2.9
COPY app.py wsgi.py ./
COPY templates ./templates
COPY static ./static
ENV MT_BIND_HOST=0.0.0.0
EXPOSE 8000
CMD ["sh", "-c", "gunicorn --workers 2 --threads 8 --bind 0.0.0.0:${PORT:-8000} wsgi:app"]
