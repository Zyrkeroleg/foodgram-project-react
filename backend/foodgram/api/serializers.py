from rest_framework import serializers

from user.serializers import RecipesSimpleSerializer
from .models import Favorite, Recipes, Tags, Ingredients



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

class FavoriteSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    
    
    class Meta():
        model = Recipes
        fields = ('id', 'recipes')

    def get_recipes(self, object):
        recipes = object.recipes.all()
        return RecipesSimpleSerializer(recipes, many=True).data