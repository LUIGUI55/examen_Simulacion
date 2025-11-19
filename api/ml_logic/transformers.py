# api/ml_logic/transformers.py
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import RobustScaler

class DeleteNanRows(BaseEstimator, TransformerMixin):
    """
    Transformador personalizado para eliminar filas con valores NaN.
    Equivalente a la lógica de limpieza del Notebook 08.
    """
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Se asume que X es un DataFrame
        return X.dropna()

class CustomScaler(BaseEstimator, TransformerMixin):
    """
    Transformador para escalar columnas específicas usando RobustScaler.
    """
    def __init__(self, attributes):
        self.attributes = attributes
        self.scaler_ = None

    def fit(self, X, y=None):
        self.scaler_ = RobustScaler()
        # Ajustamos solo sobre las columnas seleccionadas
        self.scaler_.fit(X[self.attributes])
        return self

    def transform(self, X, y=None):
        X_copy = X.copy()
        if self.scaler_:
            X_copy[self.attributes] = self.scaler_.transform(X_copy[self.attributes])
        return X_copy