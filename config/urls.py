from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- Frontend Pages ---
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    
    # Provider Pages
    path('provider/', TemplateView.as_view(template_name='provider.html'), name='provider'),
    path('provider/orders/', TemplateView.as_view(template_name='provider_orders.html'), name='provider-orders'),
    
    # User Profile Pages
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('public-profile.html', TemplateView.as_view(template_name='public_profile.html'), name='public-profile-page'),

    # --- NEW: Messages Page ---
    path('messages/', TemplateView.as_view(template_name='messages.html'), name='messages'),

    # --- API Routes ---
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/services/', include('apps.services.urls')),
    path('api/v1/bookings/', include('apps.bookings.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/ai/', include('apps.ai_engine.urls')),
    path('api/v1/chat/', include('apps.communication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)