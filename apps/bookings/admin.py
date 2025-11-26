from django.contrib import admin
from .models import Booking, Review

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'provider', 'service', 'status', 'scheduled_date', 'price')
    list_filter = ('status', 'scheduled_date')
    search_fields = ('id', 'customer__email', 'provider__email')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'created_at')
    list_filter = ('rating',)

admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)