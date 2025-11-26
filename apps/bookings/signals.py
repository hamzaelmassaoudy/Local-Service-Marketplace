from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review

@receiver(post_save, sender=Review)
def update_provider_rating(sender, instance, created, **kwargs):
    if created:
        # 1. Get the provider from the booking
        provider_profile = instance.booking.provider.provider_profile
        
        # 2. Calculate new average
        reviews = Review.objects.filter(booking__provider=instance.booking.provider)
        new_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        
        # 3. Update Profile
        provider_profile.rating = new_rating
        provider_profile.num_reviews = reviews.count()
        provider_profile.save()