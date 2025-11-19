import os
from django.core.wsgi import get_wsgi_application

# CAMBIA ESTO: 'nombre_de_tu_proyecto' por el nombre de la carpeta que tiene el settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nombre_de_tu_carpeta_principal.settings')

application = get_wsgi_application()