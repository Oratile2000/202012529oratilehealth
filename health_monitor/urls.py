from django.urls import path
from .views import HealthApiView, HealthDetailApiView

urlpatterns = [
    path('health_data/', HealthApiView.as_view()),
    path('health_data/<int:pk>/', HealthDetailApiView.as_view())
]