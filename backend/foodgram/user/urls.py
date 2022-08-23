from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )
from .views import UsersViewSet

router = SimpleRouter()
router.register(r'', UsersViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),
    # path('token/login/'),
    # path('subscriptions/', subscriptions, name='subscriptions'),
]