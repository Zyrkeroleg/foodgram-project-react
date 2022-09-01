from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UsersViewSet

router = SimpleRouter()
"""router.register(r'subscriptions/', SubcstiptionViewSet, basename='subscriptions')
router.register(r'<slug:user_slug>/subscribe', SubcstiptionViewSet, basename='subscribe')
"""
urlpatterns = [
    path('', include(router.urls)),
    

]