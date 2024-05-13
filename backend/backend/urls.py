"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from backend.profiles.views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, ActiveUserListAPIView, CurrentUserAPIView

urlpatterns = [
    path('api/register/', UserRegistrationAPIView.as_view(), name='register'),
    path('api/login/', UserLoginAPIView.as_view(), name='login'),
    path('api/logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/current-user/', CurrentUserAPIView.as_view(), name='current_user'),
    path('api/active-users/', ActiveUserListAPIView.as_view(), name='active_users'),
    path('', include('backend.file_management.urls'), name='file_management'),
]
