from django.urls import path
from .views import CreateCheckoutSessionView

urlpatterns = [
    path('create-session/<uuid:booking_id>/', CreateCheckoutSessionView.as_view(), name='create-checkout'),
]