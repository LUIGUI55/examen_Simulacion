from django.urls import path
from .views import SplitDatasetView, PrepareDatasetView, PipelineView, TrainFromLocalFolderView

urlpatterns = [
    # ... tus rutas anteriores ...
    path('split/', SplitDatasetView.as_view(), name='split'),
    path('prepare/', PrepareDatasetView.as_view(), name='prepare'),
    path('pipeline/', PipelineView.as_view(), name='pipeline'),
    
    # Nueva ruta para entrenamiento desde carpeta
    path('train-local/', TrainFromLocalFolderView.as_view(), name='train_local'),
]