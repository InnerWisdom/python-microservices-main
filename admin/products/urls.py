from django.urls import path

from .views import PredictionViewSet, UserAPIView

urlpatterns = [
    path('predictions', PredictionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('predictions/<str:pk>', PredictionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('user', UserAPIView.as_view())
]
