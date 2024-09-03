from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('user_account.urls')),
    path('api/property/', include('property.urls')),
]
