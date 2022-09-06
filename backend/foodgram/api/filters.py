from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet, filters
from user.models import User
from .models import Recipes, Tags

class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all()
    )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_in_favorite = filters.BooleanFilter(method='filter_favorite')
    is_in_shoping_cart = filters.BooleanFilter(method='filter_shoping_cart')

    def filter_favorite(self, queryset, name, value):
        if value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_shoping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shoping_cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipes
        fields = ('tags', 'author')