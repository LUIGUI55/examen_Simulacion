import os
from django.core.wsgi import get_wsgi_application

# IMPORTANTE: Asegúrate de que 'kdd_project' sea el nombre REAL de la carpeta 
# donde está settings.py. Si tu carpeta se llama 'my_ml_api', cámbialo aquí.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kdd_project.settings')

# Esta es la variable que Gunicorn está buscando y no encuentra:
application = get_wsgi_application()