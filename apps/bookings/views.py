from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking, Review
from .serializers import BookingSerializer, ReviewSerializer

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

class CreateReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()