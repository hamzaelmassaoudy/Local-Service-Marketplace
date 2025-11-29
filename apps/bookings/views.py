from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Booking, Review
from .serializers import BookingSerializer, ReviewSerializer
from apps.payments.models import Payment

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_provider:
            return Booking.objects.filter(provider=user).order_by('-created_at')
        else:
            return Booking.objects.filter(customer=user).order_by('-created_at')

class BookingStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, provider=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        new_status = request.data.get("status")
        booking.status = new_status
        booking.save()
        return Response({"status": "updated", "new_status": booking.status})

# --- NEW: Verify Booking Endpoint ---
class VerifyBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')
        
        # Find booking with this secret token
        booking = get_object_or_404(Booking, verification_token=token)
        
        # Ensure the logged-in user is the PROVIDER for this booking
        if booking.provider != request.user:
            return Response({"error": "You are not the provider for this job."}, status=403)
            
        # Mark as Completed
        booking.status = Booking.Status.COMPLETED
        booking.save()
        
        # Update Payment if exists
        if hasattr(booking, 'payment'):
            booking.payment.status = Payment.Status.COMPLETED
            booking.payment.save()
            
        return Response({"status": "success", "message": "Job Verified & Completed!"})
# ------------------------------------

class CreateReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()