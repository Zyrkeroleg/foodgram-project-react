from posixpath import basename
from django.urls import include, path
from rest_framework import SimpleRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import (
    UsersViewSet,
    TagsViewSet,
    RecipesViewSet,
    ShoppingCartViewSet,
    FavoriteViewSet,
    SubscribeViewSet,
    IngredientsViewSet,
    subscriptions,

)


router = SimpleRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'recipes/(?P<recipe_id>[^/.]+)/shopping_cart', ShoppingCartViewSet, basename='shopping_cart')
router.registe(r'recipes/(?P<recipe_id>[^/.]+)/favorite', FavoriteViewSet, basename='favorite')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'users/(?P<users_id>[^/.]+)/subscribe/', SubscribeViewSet, basename='subscribe')


urlpatterns = [
    path('recipes/download_shopping_cart/', ShoppingCartViewSet.as_view(),),
    path('users/subscriptions/', subscriptions, name='subscriptions'),
    path('auth/', views.obtain_auth_tocken),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]