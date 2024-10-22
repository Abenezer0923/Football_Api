from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # For django-allauth
    path('', include('users.urls')),  # Your app's URLs
]
