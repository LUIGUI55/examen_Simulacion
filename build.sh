#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar estáticos (necesario para Django en producción)
python manage.py collectstatic --no-input

# Migrar base de datos (necesario para sesiones/auth)
python manage.py migrate