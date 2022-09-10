from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from user.views import CustomPageNumberPagination

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientAmount, Recipes,
                     ShoppingCart, Tags)
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipePostSerializer,
                          ShoppingCartSerializer, TagSerializer)


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = CustomPageNumberPagination


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipes.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipePostSerializer
        return RecipeGetSerializer

    def create_ingredients(self, recipe, ingredients):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            IngredientAmount.objects.bulk_create([IngredientAmount(
                recipe=recipe, ingredient=ingredient_id, amount=amount)]
            )

    def create(self, request, *args, **kwargs):
        serializer = RecipePostSerializer(
            data=request.data,
            context={'request': request})
        try:
            serializer.is_valid()
            ingredients = serializer.validated_data.pop("ingredients")
            tags = serializer.validated_data.pop("tags")
            recipe = Recipes.objects.create(
                author=request.user, **serializer.validated_data)
            recipe.tags.set(tags)
            self.create_ingredients(recipe, ingredients)
            serializer = RecipeGetSerializer(
                instance=recipe, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = RecipePostSerializer(
            data=request.data, context={"request": request})
        try:
            serializer.is_valid()
            ingredients = serializer.validated_data.pop("ingredients")
            tags = serializer.validated_data.pop("tags")
            recipe = get_object_or_404(Recipes, id=kwargs["pk"])
            IngredientAmount.objects.filter(recipe=recipe).delete()
            recipe.tags.set(tags)
            self.create_ingredients(recipe, ingredients)
            Recipes.objects.filter(id=recipe.id).update(
                **serializer.validated_data)
            recipe = Recipes.objects.get(id=recipe.id)
            if serializer.validated_data.get("image"):
                recipe.image = serializer.validated_data["image"]
            recipe.save()
            serializer = RecipeGetSerializer(
                instance=recipe, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        context = super(RecipeViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipes, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite)

    @action(detail=True, methods=["POST"],
            url_path='shopping_cart', permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request, pk=None):
        ingredients = IngredientAmount.objects.filter(
            recipe__carts__user=request.user.id
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_cart = ['Список покупок:\n--------------']
        for position, ingredient in enumerate(ingredients, start=1):
            shopping_cart.append(
                f'\n{position}. {ingredient["ingredient__name"]}:'
                f' {ingredient["amount"]}'
                f'({ingredient["ingredient__measurement_unit"]})'
            )
        response = HttpResponse(shopping_cart, content_type='text')
        response['Content-Disposition'] = (
            'attachment;filename=shopping_cart.pdf'
        )
        return response
