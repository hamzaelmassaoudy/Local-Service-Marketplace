import stripe
from django.conf import settings
from rest_framework import views, status, permissions
from rest_framework.response import Response
from apps.bookings.models import Booking
from .models import Payment

# Dummy key to prevent errors on startup
stripe.api_key = "sk_test_placeholder" 

class CreateCheckoutSessionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, customer=request.user)
            
            # Create a dummy session link since we don't have a real Stripe account connected yet
            # In production, this would be stripe.checkout.Session.create(...)
            dummy_url = "https://checkout.stripe.com/pay/test_session"
            
            Payment.objects.create(
                booking=booking,
                stripe_checkout_id="sess_dummy_123",
                amount=booking.price,
                status=Payment.Status.PENDING
            )

            return Response({'url': dummy_url})

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)