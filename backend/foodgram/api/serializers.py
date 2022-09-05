from rest_framework import serializers

from .models import Favorite, Recipes, Tags, Ingredients, Shoping_cart, Amount_of_ingredients


class AmountOfIgredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = Amount_of_ingredients
        fields = (
            'id', 'name', 'measurement_unit', 'amount'
        )


class TagsSerializer(serializers.ModelSerializer):

    class Meta():
        model = Tags
        fields = (
            'id',
            'title',
            'color', 
            'slug'
        )
    

class IngredientsSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Ingredients
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class RecipesSerializer(serializers.ModelSerializer):

    class Meta():
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'text',
            'ingredients',
            'cooking_time',
            'tags'
        )
    
    def get_is_in_shopping_cart(self, obj):
        """Статус - рецепт в избранном или нет."""
        user_id = self.context.get('request').user.id
        return Shoping_cart.objects.filter(
            user=user_id, recipe=obj.id).exists()

    def get_is_favorited(self, obj):
        """Статус - рецепт в избранном или нет."""
        user_id = self.context.get('request').user.id
        return Favorite.objects.filter(
            user=user_id, recipe=obj.id).exists()

    