from django.urls import path
from .views import BookingCreateView, BookingListView, BookingStatusUpdateView, CreateReviewView, VerifyBookingView

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('my-bookings/', BookingListView.as_view(), name='my-bookings'),
    path('<uuid:pk>/update-status/', BookingStatusUpdateView.as_view(), name='booking-update-status'),
    path('<uuid:booking_id>/review/', CreateReviewView.as_view(), name='create-review'),
    
    # NEW URL
    path('verify/', VerifyBookingView.as_view(), name='booking-verify'),
]