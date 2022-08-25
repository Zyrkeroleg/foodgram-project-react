from rest_framework import serializers
from .models import Favorite, Recipes, Tags, Ingredients

class TagsSerializer(serializers.ModelSerializer):

    class Meta():
        model = Tags
        fields = (
            'title',
            'color', 
            'slug'
        )
    

class IngredientsSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Ingredients
        fields = (
            'name',
            'amount',
            'measurement_unit'
        )


class RecipesSerializer(serializers.ModelSerializer):

    class Meta():
        model = Recipes
        fields = (
            'author',
            'title',
            'image',
            'description',
            'ingredients',
            'cooking_time',
            'tags'
        )

class FavoriteSerializer(serializers.ModelField):
    favoriting = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Recipes.objects.all()
    )

    def validate_favoriting(self, recipe):
        if recipe in self.favorite:
            raise serializers.ValidationError('рецепт уже в избранном')
        return recipe


    class Meta():
        model = Favorite
        fields = '__all__'