from posixpath import basename
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views
from user.views import UsersViewSet

from api.views import (
    TagsViewSet,
    RecipesViewSet,
    ShoppingCartViewSet,
    FavoriteViewSet,
    SubscribeViewSet,
    IngredientsViewSet,
    subscriptions,

)


router = SimpleRouter()
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'recipes/(?P<recipe_id>[^/.]+)/shopping_cart', ShoppingCartViewSet, basename='shopping_cart')
router.register(r'recipes/(?P<recipe_id>[^/.]+)/favorite', FavoriteViewSet, basename='favorite')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'users/(?P<users_id>[^/.]+)/subscribe/', SubscribeViewSet, basename='subscribe')


urlpatterns = [
    # path('recipes/download_shopping_cart/', ShoppingCartViewSet),
    path('', include(router.urls)),
    path('users/', include('djoser.urls')),
    path('users/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]