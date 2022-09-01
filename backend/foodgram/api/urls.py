from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from user.views import CostomUserViewSet
from api.views import (
    TagsViewSet,
    RecipesViewSet,
    ShoppingCartViewSet,
    FavoriteViewSet,
    IngredientsViewSet,
    subscriptions,

)

app_name = 'api'
router = DefaultRouter()
router.register('users', CostomUserViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register(r'recipes/(?P<recipe_id>[^/.]+)/shopping_cart', ShoppingCartViewSet, basename='shopping_cart')
router.register(r'recipes/(?P<recipe_id>[^/.]+)/favorite', FavoriteViewSet, basename='favorite')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]