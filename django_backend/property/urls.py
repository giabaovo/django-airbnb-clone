from django.urls import path

from .api import PropertyAPIView

urlpatterns = [
    path('', PropertyAPIView.as_view(), name='property'),
]
