from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.users.models import User
from apps.bookings.models import Booking

class ChatMessage(TimeStampedUUIDModel):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="chat_messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    text = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} in Booking {self.booking.id}"