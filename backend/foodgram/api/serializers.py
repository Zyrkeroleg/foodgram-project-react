from rest_framework import serializers
from .models import User, Recipes, Tags, Ingredients

class UserSerializer(serializers.ModelField):
    pass

class TagsSerializer(serializers.ModelField):
    pass

class IngredientsSerializer(serializers.ModelField):
    pass