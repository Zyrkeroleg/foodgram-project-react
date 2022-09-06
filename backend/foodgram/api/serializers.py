from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from user.serializers import UserSerializer
from .models import Favorite, Recipes, Tags, Ingredients, Shoping_cart, Amount_of_ingredients
from . validators import validate_tags



class AmountOfIgredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')

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
            'name',
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
    author = UserSerializer(read_only=True)
    tags = TagsSerializer(read_only=True, many=True)
    ingredients = AmountOfIgredientsSerializer(
        read_only=True, many=True, source='amount_of_ingredients_set')
    image = Base64ImageField()
    is_in_favorite = serializers.SerializerMethodField()
    is_in_shoping_cart = serializers.SerializerMethodField()

    class Meta():
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'text',
            'ingredients',
            'cooking_time',
            'tags',
            'author',
            'is_in_shoping_cart',
            'is_in_favorite'
        )

    
    def get_is_in_shoping_cart(self, object):
        """Рецепт в карзине."""
        user_id = self.context.get('request').user.id
        return Shoping_cart.objects.filter(
            user=user_id, recipes=object.id).exists()

    def get_is_in_favorite(self, object):
        """Рецепт в избранном."""
        user_id = self.context.get('request').user.id
        return Favorite.objects.filter(
            user=user_id, recipes=object.id).exists()

    def create_ingredient_amount(self, valid_ingredients, recipe):
        """Колличество ингредиентов."""
        for ingredient_data in valid_ingredients:
            ingredient = get_object_or_404(
                Ingredients, id=ingredient_data.get('id'))
            Amount_of_ingredients.objects.create(
                recipes=recipe,
                ingredients=ingredient,
                amount=ingredient_data.get('amount'))

    def create_tags(self, data, recipe):
        """Создание тегов у рецепта"""
        valid_tags = validate_tags(data.get('tags'))
        tags = Tags.objects.filter(id__in=valid_tags)
        recipe.tags.set(tags)
    
    def update(self, instance, validated_data):
        instance.tags.clear()
        Amount_of_ingredients.objects.filter(recipe=instance).delete()
        self.create_tags(validated_data.pop('tags'), instance)
        self.create_ingredient_amount(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        """Создание рецепта - writable nested serializers."""
        valid_ingredients = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(**validated_data)
        self.create_tags(self.initial_data, recipe)
        self.create_ingredient_amount(valid_ingredients, recipe)
        return recipe

    