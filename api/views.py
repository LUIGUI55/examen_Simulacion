from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sklearn.model_selection import train_test_split

# Importamos la nueva lógica
from .ml_logic.data_loader import load_emails_from_folder
from .ml_logic.transformers import DeleteNanRows
from .ml_logic.pipelines import build_preprocessing_pipeline

class TrainFromLocalFolderView(APIView):
    """
    Endpoint: /api/train-local/
    1. Lee 1000 archivos de la carpeta 'data/raw_emails'.
    2. Divide el dataset (Notebook 07).
    3. Limpia los datos (Notebook 08).
    4. Entrena el Pipeline completo (Notebook 09).
    """
    def post(self, request):
        try:
            # 1. CARGA DE DATOS (Desde la carpeta local)
            print("Iniciando carga de archivos locales...")
            df = load_emails_from_folder('raw_emails')
            
            total_loaded = len(df)
            
            # 2. DIVISIÓN (Lógica Notebook 07)
            # Asumimos que existe una columna 'class' o 'protocol_type' para estratificar
            stratify_col = df['protocol_type'] if 'protocol_type' in df.columns else None
            
            train_set, test_set = train_test_split(
                df, test_size=0.4, random_state=42, stratify=stratify_col
            )

            # 3. LIMPIEZA Y PREPARACIÓN (Lógica Notebook 08)
            # Separar Features (X) y Target (y) del conjunto de entrenamiento
            if 'class' in train_set.columns:
                X_train = train_set.drop('class', axis=1)
                y_train = train_set['class'].copy()
            else:
                X_train = train_set
            
            # Usar el transformador personalizado para limpiar nulos
            cleaner = DeleteNanRows()
            X_train_clean = cleaner.transform(X_train)

            # 4. PIPELINE (Lógica Notebook 09)
            # Construir pipeline basado en los datos limpios
            full_pipeline = build_preprocessing_pipeline(X_train_clean)
            
            # Entrenar el pipeline (Fit) y transformar
            X_train_prepared = full_pipeline.fit_transform(X_train_clean)

            return Response({
                "status": "success",
                "message": f"Modelo entrenado exitosamente usando {total_loaded} archivos locales.",
                "details": {
                    "files_loaded": total_loaded,
                    "training_samples": len(X_train_clean),
                    "features_processed": X_train_prepared.shape[1],
                    "pipeline_steps": list(full_pipeline.named_transformers_.keys())
                },
                # Mostramos una muestra de los datos procesados (convertido a lista para JSON)
                "sample_processed_data": X_train_prepared[:2].tolist()
            })

        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Captura errores generales (ej. columnas faltantes)
            return Response({"error": f"Error interno: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)