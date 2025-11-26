from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.users.models import ProviderProfile  # This import was failing before

class ServiceCategory(TimeStampedUUIDModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.ImageField(upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name

class Service(TimeStampedUUIDModel):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="services")
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, related_name="services")
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_hourly = models.BooleanField(default=False) # True = per hour, False = fixed price
    
    # Search & Filter
    location_lat = models.FloatField(blank=True, null=True)
    location_long = models.FloatField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.provider.user.username}"