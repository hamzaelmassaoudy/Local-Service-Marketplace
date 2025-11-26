from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'status', 'stripe_checkout_id')
    list_filter = ('status',)

admin.site.register(Payment, PaymentAdmin)