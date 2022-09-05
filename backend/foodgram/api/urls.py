from django.urls import include, path
from rest_framework.routers import DefaultRouter
from user.views import CostomUserViewSet
from api.views import (
    TagsViewSet,
    RecipesViewSet,
    IngredientsViewSet,
)

app_name = 'api'
router = DefaultRouter()
router.register('users', CostomUserViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]