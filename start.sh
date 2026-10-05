#!/bin/sh
set -e

echo "==> Creating database migrations if needed"
python manage.py makemigrations --noinput

echo "==> Applying database migrations"
python manage.py migrate --noinput

echo "==> Collecting static files"
python manage.py collectstatic --noinput

echo "==> Starting Gunicorn on port ${PORT:-8080}"
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers ${WEB_CONCURRENCY:-2} --timeout 120
