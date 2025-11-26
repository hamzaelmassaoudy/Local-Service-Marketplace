from django.contrib import admin
from .models import ServiceCategory, Service

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'category', 'price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description')

admin.site.register(ServiceCategory)
admin.site.register(Service, ServiceAdmin)