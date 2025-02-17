from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    UserProfileUpdateView,
    UserProfileDeleteView,
    HomeView,
    EmailVerificationView,
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('profile/delete/', UserProfileDeleteView.as_view(), name='user_profile_delete'),
    path('home/', HomeView.as_view(), name='home'),
    path('verify-email/<uuid:token>/', EmailVerificationView.as_view(), name='verify_email'),
]
