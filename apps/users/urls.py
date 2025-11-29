from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterUserView, 
    CustomTokenObtainPairView, 
    UserProfileView, 
    BecomeProviderView, 
    PublicUserProfileView
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('become-provider/', BecomeProviderView.as_view(), name='become-provider'),
    
    # --- NEW: Public Profile Endpoint ---
    # This URL allows anyone to fetch profile data by username
    path('public/<str:username>/', PublicUserProfileView.as_view(), name='public-profile'),
]