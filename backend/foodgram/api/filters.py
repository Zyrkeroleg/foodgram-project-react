from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from .models import Recipes, Tags


class RecipeFilter(FilterSet):
    """Фильтр рецептов."""
    Tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='uuid',
        queryset=Tags.objects.all(),
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipes
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(carts__user=self.request.user)
        return queryset


class IngredientSearchFilter(SearchFilter):
    """Фильтр поиска игредиентов."""
    search_param = 'name'
