from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.users.models import ProviderProfile

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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_hourly = models.BooleanField(default=False)
    
    # Location & Logistics
    location_lat = models.FloatField(blank=True, null=True)
    location_long = models.FloatField(blank=True, null=True)
    # NEW: Max distance the provider is willing to travel
    service_radius_km = models.FloatField(default=50.0, help_text="Maximum travel distance in km")
    
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.provider.user.username}"