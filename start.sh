#!/bin/sh

set -o errexit
set -o nounset

echo "----- RUNNING MIGRATIONS -----"
# python manage.py migrate --database=default
echo "----- FINISHED MIGRATIONS -----"

echo "----- STARTING WEB SERVER -----"
python manage.py runserver 0.0.0.0:8000