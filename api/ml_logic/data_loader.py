import os
import json
import pandas as pd
from django.conf import settings

def load_emails_from_folder(folder_name='raw_emails'):
    """
    Lee todos los archivos de una carpeta específica dentro del directorio 'data'
    y devuelve un DataFrame.
    """
    # Construir la ruta absoluta compatible con cualquier SO y Render
    data_path = os.path.join(settings.BASE_DIR, 'data', folder_name)
    
    all_data = []
    
    # Verificar si la carpeta existe
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"La carpeta {data_path} no existe. Asegúrate de crearla y subirla.")

    # Iterar sobre los archivos
    files = [f for f in os.listdir(data_path) if f.endswith('.json')] # Asumimos JSON por facilidad
    
    if not files:
        raise ValueError("La carpeta está vacía o no contiene archivos .json")

    print(f"Leyendo {len(files)} archivos desde {data_path}...")

    for filename in files:
        file_path = os.path.join(data_path, filename)
        try:
            with open(file_path, 'r') as f:
                # Leemos el contenido
                content = json.load(f)
                # Si el archivo tiene una estructura anidada, ajústalo aquí.
                # Asumimos que el JSON es un diccionario plano: {"src_bytes": 10, "protocol": "tcp"...}
                all_data.append(content)
        except Exception as e:
            print(f"Error leyendo {filename}: {e}")

    # Convertir lista de diccionarios a DataFrame
    df = pd.DataFrame(all_data)
    return df