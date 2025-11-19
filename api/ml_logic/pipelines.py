# api/ml_logic/pipelines.py
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd

def build_preprocessing_pipeline(X_sample):
    """
    Construye el pipeline completo basándose en las columnas del DataFrame de entrada.
    Replica la lógica final del Notebook 09.
    """
    # 1. Identificar columnas numéricas y categóricas
    num_attributes = list(X_sample.select_dtypes(exclude=['object']).columns)
    cat_attributes = list(X_sample.select_dtypes(include=['object']).columns)

    # 2. Pipeline Numérico (Imputación + Escalado)
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('rbst_scaler', RobustScaler())
    ])

    # 3. Pipeline Completo (ColumnTransformer)
    # Aplica OneHotEncoder a las categóricas y el num_pipeline a las numéricas
    full_pipeline = ColumnTransformer([
        ('num', num_pipeline, num_attributes),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_attributes)
    ])
    
    return full_pipeline