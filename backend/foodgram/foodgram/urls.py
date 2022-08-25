from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.authtoken')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('api.urls')),
    path('user/', include('user.urls')),
    path('admin/', admin.site.urls)
]