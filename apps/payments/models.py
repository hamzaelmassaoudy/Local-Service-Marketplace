from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.bookings.models import Booking

class Payment(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    stripe_checkout_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"Payment {self.id} for Booking {self.booking.id} - {self.status}"