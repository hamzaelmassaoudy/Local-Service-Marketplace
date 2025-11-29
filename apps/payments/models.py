from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.bookings.models import Booking

class Payment(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    class Method(models.TextChoices):
        CASH = 'CASH', 'Cash on Delivery'
        # You can add 'BANK_TRANSFER' etc. later

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(max_length=20, choices=Method.choices, default=Method.CASH)
    
    # We remove stripe_checkout_id or keep it optional for future use
    stripe_checkout_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.id} ({self.payment_method}) - {self.status}"