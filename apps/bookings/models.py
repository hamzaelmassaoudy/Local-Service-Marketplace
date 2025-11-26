from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel
from apps.users.models import User
from apps.services.models import Service

class Booking(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        DISPUTED = 'DISPUTED', 'Disputed'

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings_as_customer")
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings_as_provider")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    
    # Scheduling
    scheduled_date = models.DateTimeField()
    
    # Location
    address = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, help_text="Details about the issue")

    def __str__(self):
        return f"Booking {self.id} - {self.status}"

class Review(TimeStampedUUIDModel):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="review")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) # 1-5 Stars
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.rating} Stars for Booking {self.booking.id}"