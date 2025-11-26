from django.urls import path
from .views import ServiceCategoryList, ServiceCreateView, ServiceListView

urlpatterns = [
    path('categories/', ServiceCategoryList.as_view(), name='category-list'),
    path('create/', ServiceCreateView.as_view(), name='service-create'),
    path('search/', ServiceListView.as_view(), name='service-search'),
]