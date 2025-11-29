from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from apps.bookings.models import Booking

class ChatHistoryView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        booking_id = self.kwargs['booking_id']
        user = self.request.user
        
        # --- FIX IS HERE ---
        # We must use 'booking__id' (UUID) instead of 'booking_id' (Internal Integer PK)
        return ChatMessage.objects.filter(
            booking__id=booking_id 
        ).filter(
            Q(booking__customer=user) | Q(booking__provider=user)
        ).order_by('created_at')

class SendMessageView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking_id = self.kwargs['booking_id']
        # This works correctly because it queries the Booking model by its UUID field 'id'
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Security Check: Ensure user belongs to this booking
        if self.request.user != booking.customer and self.request.user != booking.provider:
            raise permissions.PermissionDenied("You are not part of this booking.")

        serializer.save(sender=self.request.user, booking=booking)