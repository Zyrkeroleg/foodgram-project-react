from django.contrib import admin
from django.urls import include, path, re_path
from djoser import views

urlpatterns = [
    path('api/', include('api.urls')),
    path('user/', include('user.urls')),
    path('admin/', admin.site.urls)
]
