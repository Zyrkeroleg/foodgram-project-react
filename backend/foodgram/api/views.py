from sqlite3 import IntegrityError
from urllib import request
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from user.models import User
from user.serializers import RecipesSimpleSerializer
from api.models import Favorite, Ingredients, Recipes, Tags 
from .serializers import FavoriteSerializer, TagsSerializer, RecipesSerializer, IngredientsSerializer
from .permissions import AuthorOrReadOnly

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = (TagsSerializer)


class IngregientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer




class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = (RecipesSerializer)

    @action(detail=True,
            url_path='recipes',
            methods={'post', 'get', 'delete'},
            permission_classes=[AuthorOrReadOnly, IsAuthenticatedOrReadOnly]
            )
    def get_and_create_recipes(self, request):
        author = request.user
        recipes = Recipes.objects.all()
        if request.method == "GET":
            serializer = RecipesSerializer(recipes)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'POST':
            serializer.save(author=self.request.user)

    def delete_recipes(self, request):
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipes, id=id)
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'],
            url_path='favorite',
            url_name='favorite')
    def favorite(self, request, pk=None):
        """Добавить и удалить рецепт в избранное."""
        user = request.user
        if request.method == "POST":
            recipes = get_object_or_404(Recipes, pk=pk)
            relation = Favorite.objects.filter(user=user, recipes=recipes)
            if relation.exists():
                return Response(
                    'Рецепт уже в избранном',
                    status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=user, recipes=recipes)
            serializer = RecipesSimpleSerializer(recipes)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            recipes = get_object_or_404(Recipes, pk=pk)
            relation = Favorite.objects.filter(user=user, recipes=recipes)
            if not relation.exists():
                return Response('Рецепт не в избранном', status=status.HTTP_400_BAD_REQUEST)
            relation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True,
            methods=['post', 'delete'],
            url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        user = request.user
        if request.method == 'POST':
            pass


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = (IngredientsSerializer)
