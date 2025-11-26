from django.urls import path
from .views import PriceEstimationView

urlpatterns = [
    path('estimate-price/', PriceEstimationView.as_view(), name='ai-estimate'),
]