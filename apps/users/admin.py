from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CustomerProfile, ProviderProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active')
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'is_verified', 'rating')
    list_filter = ('is_verified',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(CustomerProfile)
admin.site.register(ProviderProfile, ProviderProfileAdmin)