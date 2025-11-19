from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Importamos nuestra lógica modular
# Asegúrate de que los archivos transformers.py, pipelines.py y data_loader.py existan en api/ml_logic/
from .ml_logic.transformers import DeleteNanRows
from .ml_logic.pipelines import build_preprocessing_pipeline
from .ml_logic.data_loader import load_emails_from_folder

# ----------------------------------------------------------------
# VISTA 1: División del Dataset (Notebook 07)
# ----------------------------------------------------------------
class SplitDatasetView(APIView):
    def post(self, request):
        try:
            df = pd.DataFrame(request.data)
            if df.empty:
                return Response({"error": "Dataset vacío"}, status=status.HTTP_400_BAD_REQUEST)

            stratify_col = df['protocol_type'] if 'protocol_type' in df.columns else None
            
            train_set, test_set = train_test_split(
                df, test_size=0.4, random_state=42, stratify=stratify_col
            )
            
            # Segunda división para validación
            stratify_col_test = test_set['protocol_type'] if 'protocol_type' in test_set.columns else None
            val_set, final_test_set = train_test_split(
                test_set, test_size=0.5, random_state=42, stratify=stratify_col_test
            )

            return Response({
                "status": "success",
                "original_size": len(df),
                "splits": {
                    "train_set": len(train_set),
                    "validation_set": len(val_set),
                    "test_set": len(final_test_set)
                }
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------------
# VISTA 2: Preparación y Limpieza (Notebook 08)
# ----------------------------------------------------------------
class PrepareDatasetView(APIView):
    def post(self, request):
        try:
            df = pd.DataFrame(request.data)
            original_count = len(df)
            
            # Simulación de datos sucios para demostración
            if 'src_bytes' in df.columns:
                 df.loc[(df["src_bytes"] > 400) & (df["src_bytes"] < 800), "src_bytes"] = np.nan

            cleaner = DeleteNanRows()
            df_clean = cleaner.transform(df)

            return Response({
                "status": "success",
                "rows_before": original_count,
                "rows_after": len(df_clean),
                "dropped_rows": original_count - len(df_clean)
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------------
# VISTA 3: Pipeline Completo (Notebook 09)
# ----------------------------------------------------------------
class PipelineView(APIView):
    def post(self, request):
        try:
            df = pd.DataFrame(request.data)
            X = df.drop('class', axis=1) if 'class' in df.columns else df

            pipeline = build_preprocessing_pipeline(X)
            X_prep = pipeline.fit_transform(X)

            return Response({
                "status": "success",
                "input_shape": X.shape,
                "output_shape": X_prep.shape,
                "sample_data": X_prep[:2].tolist()
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------------
# VISTA 4: Entrenamiento Local (Batch Processing)
# ----------------------------------------------------------------
class TrainFromLocalFolderView(APIView):
    def post(self, request):
        try:
            print("Iniciando carga de archivos locales...")
            df = load_emails_from_folder('raw_emails') # Asegúrate que esta carpeta exista en data/
            
            total_loaded = len(df)
            
            # División
            stratify_col = df['protocol_type'] if 'protocol_type' in df.columns else None
            train_set, test_set = train_test_split(df, test_size=0.4, random_state=42, stratify=stratify_col)

            # Limpieza
            X_train = train_set.drop('class', axis=1) if 'class' in train_set.columns else train_set
            cleaner = DeleteNanRows()
            X_train_clean = cleaner.transform(X_train)

            # Pipeline
            full_pipeline = build_preprocessing_pipeline(X_train_clean)
            X_train_prepared = full_pipeline.fit_transform(X_train_clean)

            return Response({
                "status": "success",
                "message": f"Modelo entrenado con {total_loaded} archivos locales.",
                "details": {
                    "training_samples": len(X_train_clean),
                    "features": X_train_prepared.shape[1]
                }
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)