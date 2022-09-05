from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from fpdf import FPDF
from user.serializers import RecipesSimpleSerializer
from api.models import Favorite, Ingredients, Recipes, Shoping_cart, Tags 
from .serializers import TagsSerializer, RecipesSerializer, IngredientsSerializer
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
        return Response('Рецепт удален из избранного', status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True,
            methods=['post', 'delete'],
            url_path='Shoping_cart')
    def Shoping_cart(self, request, pk=None):
        """Добавление/удаление из карзины."""
        user = request.user
        if request.method == 'POST':
            recipes = get_object_or_404(Recipes, pk=pk)
            relation = Shoping_cart.objects.filter(user=user, recipes=recipes)
            if relation.exists():
                return Response(
                    'Рецепт уже в корзине',
                    status=status.HTTP_400_BAD_REQUEST)
            Shoping_cart.objects.create(user=user, recipes=recipes)
            serializer = RecipesSimpleSerializer(recipes)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            recipes = get_object_or_404(Recipes, pk=pk)
            relation = Shoping_cart.objects.filter(user=user, recipes=recipes)
            if not relation.exists():
                return Response('Рецепта нет в карзине', status=status.HTTP_400_BAD_REQUEST)
            relation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('Рецепт удален из карзины', status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['get'], detail=False, url_path='download_shopping_cart',
            url_name='download_shopping_cart')
    def download_cart(self, request):
        """Формирование и скачивание списка покупок."""
        user = request.user
        ingredients = Ingredients.objects.filter(
            recipe__shhopping_cart__user=user).values(
                'ingredient__name', 'ingredient__measurement_unit').annotate(
                    Sum('amount', distinct=True))
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=12)
        pdf.cell(200, 10, txt='Список покупок', center=True)
        pdf.ln(8)
        for i, ingredient in enumerate(ingredients):
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['amount__sum']
            pdf.cell(40, 10, f'{i + 1}) {name} - {amount} {unit}')
            pdf.ln()
        file = pdf.output(dest='S')
        response = HttpResponse(
            content_type='application/pdf', status=status.HTTP_200_OK)
        response['Content-Disposition'] = (
            'attachment; filename="Shoping_cart.pdf"')
        response.write(bytes(file))
        return response


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = (IngredientsSerializer)
