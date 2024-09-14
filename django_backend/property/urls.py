from django.urls import path

from .api import (
    PropertyAPIView,
    PropertyByIdAPIView,
    UserFavoritePropertyAPIView,
    ToggleFavoritePropertyAPIView,
    ReservationByPropertyAPIView,
    ReservationByUserIdAPIView,
    ReservationAPIView,
    ReservationByAuthorAPIView,
    PropertyByUserAPIView
)

urlpatterns = [
    path('', PropertyAPIView.as_view(), name='property'),
    path('<uuid:pk>/', PropertyByIdAPIView.as_view(), name='property-by-id'),
    path('user-properties/', PropertyByUserAPIView.as_view(), name='property-by-user'),

    path('wishlist/', UserFavoritePropertyAPIView.as_view(), name='wishlist'),
    path('<uuid:pk>/favorite/', ToggleFavoritePropertyAPIView.as_view(), name='toggle-favorite'),

    path('<uuid:pk>/reservation/', ReservationByPropertyAPIView.as_view(), name='reservation-by-property'),
    path('user-reservation/', ReservationByUserIdAPIView.as_view(), name='reservation-by-user-id'),
    path('author-reservation/', ReservationByAuthorAPIView.as_view(), name='reservation-by-author'),
    path('reservation/<uuid:pk>/', ReservationAPIView.as_view(), name='reservation'),
]
