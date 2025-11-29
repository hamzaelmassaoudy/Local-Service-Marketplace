from django.urls import path
from .views import InitiateCashPaymentView, ConfirmPaymentReceivedView

urlpatterns = [
    # User selects Cash
    path('initiate-cash/<uuid:booking_id>/', InitiateCashPaymentView.as_view(), name='initiate-cash'),
    # Provider confirms Cash Received
    path('confirm-receipt/<uuid:booking_id>/', ConfirmPaymentReceivedView.as_view(), name='confirm-receipt'),
]