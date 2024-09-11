from django.urls import path

from .api import (
    PropertyAPIView,
    PropertyByIdAPIView,
    UserFavoritePropertyAPIView,
    ToggleFavoritePropertyAPIView,
    ReservationAPIView
)

urlpatterns = [
    path('', PropertyAPIView.as_view(), name='property'),
    path('<uuid:pk>/', PropertyByIdAPIView.as_view(), name='property-by-id'),

    path('wishlist/', UserFavoritePropertyAPIView.as_view(), name='wishlist'),
    path('<uuid:pk>/favorite/', ToggleFavoritePropertyAPIView.as_view(), name='toggle-favorite'),

    path('<uuid:pk>/reservation/', ReservationAPIView.as_view(), name='reservation'),
]
