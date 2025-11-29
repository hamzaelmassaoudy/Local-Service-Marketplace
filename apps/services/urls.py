from django.urls import path
from .views import ServiceCategoryList, ServiceCreateView, ServiceListView, ServiceDetailView

urlpatterns = [
    path('categories/', ServiceCategoryList.as_view(), name='category-list'),
    path('create/', ServiceCreateView.as_view(), name='service-create'),
    path('search/', ServiceListView.as_view(), name='service-search'),
    
    # NEW: This URL allows deleting and editing specific services
    path('<uuid:pk>/', ServiceDetailView.as_view(), name='service-detail'),
]