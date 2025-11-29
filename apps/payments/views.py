from rest_framework import views, status, permissions
from rest_framework.response import Response
from apps.bookings.models import Booking
from .models import Payment

class InitiateCashPaymentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, customer=request.user)
            
            # Check if payment already exists
            if hasattr(booking, 'payment'):
                return Response({"message": "Payment method already selected"}, status=200)

            # Create the Cash Payment Record
            payment = Payment.objects.create(
                booking=booking,
                amount=booking.price,
                status=Payment.Status.PENDING,
                payment_method=Payment.Method.CASH
            )
            
            # Optionally update Booking status to 'ACCEPTED' or keep it 'REQUESTED' 
            # depending on if you want the Provider to manually accept first.
            # For COD, usually, we verify the intent, so let's keep Booking as REQUESTED 
            # until Provider accepts the job.

            return Response({
                "status": "success", 
                "message": "Cash payment selected. Please pay provider upon service delivery."
            })

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

class ConfirmPaymentReceivedView(views.APIView):
    """
    Allow the Provider to mark the payment as collected.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_id):
        try:
            # Only the Provider of this booking can confirm receipt
            booking = Booking.objects.get(id=booking_id, provider=request.user)
            
            if hasattr(booking, 'payment'):
                booking.payment.status = Payment.Status.COMPLETED
                booking.payment.save()
                
                # Also mark booking as completed if not already
                booking.status = Booking.Status.COMPLETED
                booking.save()
                
                return Response({"status": "success", "message": "Payment confirmed received."})
            else:
                return Response({"error": "No payment record found"}, status=404)

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found or access denied"}, status=404)