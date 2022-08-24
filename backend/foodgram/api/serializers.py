from dataclasses import fields
from rest_framework import serializers
from .models import Recipes, Tags, Ingredients

class TagsSerializer(serializers.ModelSerializer):

    class Meta():
        model = Tags
        fields = ('title', 'color', 'slug')
    

class IngredientsSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Ingredients
        fields = ('name', 'amount', 'measurement_unit')


class RecipesSerializer(serializers.ModelSerializer):

    class Meta():
        model = Recipes
        fields = ('author', 'title', 'image', 'description', 'ingredients', 'cooking_time', 'tags')