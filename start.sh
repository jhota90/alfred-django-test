#!/bin/sh

set -o errexit
set -o nounset

echo "----- RUNNING MIGRATIONS -----"
python manage.py migrate --database=default
echo "----- FINISHED MIGRATIONS -----"

echo "----- ADD SUPERUSER -----"
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    print("Creando superusuario...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
else:
    print("Superuser already exist.")
EOF
echo "----- FINISHED SUPERUSER -----"

echo "----- ADD TEST DATA -----"
# Opcional: Sembrar datos de prueba solo si no existen conductores
python manage.py shell << EOF
from deliveries.models import Driver
if not Driver.objects.exists():
    from django.core.management import call_command
    call_command('seed')
EOF
echo "----- FINISHED TEST DATA -----"

echo "----- STARTING WEB SERVER -----"
# python manage.py runserver 0.0.0.0:8000
gunicorn app.wsgi:application --bind 0.0.0.0:8000