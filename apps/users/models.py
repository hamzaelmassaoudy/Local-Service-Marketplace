import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"
        PROVIDER = "PROVIDER", "Service Provider"

    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    username = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.CUSTOMER)
    
    # Visuals - We added cover_image here
    profile_image = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default.png')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, default='covers/default_cover.jpg')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.username

    @property
    def is_provider(self):
        return self.role == self.Role.PROVIDER

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Customer Profile"

class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="provider_profile")
    business_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, default="I am a professional service provider.")
    is_verified = models.BooleanField(default=False)
    identity_document = models.ImageField(upload_to="provider_docs/", blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    num_reviews = models.IntegerField(default=0)
    years_experience = models.IntegerField(default=0)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    working_start = models.TimeField(default="09:00:00")
    working_end = models.TimeField(default="17:00:00")

    def __str__(self):
        return f"{self.user.username} - {self.business_name or 'Provider'}"