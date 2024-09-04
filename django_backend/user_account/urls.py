from django.urls import path

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from dj_rest_auth.jwt_auth import get_refresh_view

from rest_framework_simplejwt.views import TokenVerifyView

from .api import UserAPI

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('me/', UserAPI.as_view(), name='me'),
]