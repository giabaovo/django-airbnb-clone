from django.urls import path

from .api import (
    PropertyAPIView,
    UserFavoritePropertyAPIView,
    ToggleFavoritePropertyAPIView
)

urlpatterns = [
    path('', PropertyAPIView.as_view(), name='property'),
    path('wishlist/', UserFavoritePropertyAPIView.as_view(), name='wishlist'),
    path('<uuid:pk>/favorite/', ToggleFavoritePropertyAPIView.as_view(), name='toggle-favorite'),
]
