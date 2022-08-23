from rest_framework import serializers
from .models import Recipes, Tags, Ingredients

class TagsSerializer(serializers.ModelSerializer):

    class Meta():
        model = Tags
        fields = ('title', 'color', 'slug')
    

class IngredientsSerializer(serializers.ModelSerializer):
    pass