from rest_framework import serializers
from api.models import Recipes
from .models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя."""
    password = serializers.CharField(write_only=True)

    
    class Meta:
        model=User
        fields=(
            'email',
            'username',
            'first_name',
            'last_name',
            'id',
            'password'
        )
        write_only_fields = ('password',)
    
    def create(self, validated_data):
        """Создание пользователя."""
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RecipesSimpleSerializer(serializers.ModelSerializer):
    """Отоброжение резептов у подписок."""

    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Получаем список подписок."""
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    email = serializers.ReadOnlyField(source='author.email')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')
    
    def get_is_subscribed(self, object):
        """Определение статуса подписки."""
        user = self.context.get('request').user
        return Follow.objects.filter(author=object.author, user=user).exists()
    
    def get_recipes(self, object):
        """Получаем список рецептов автора."""
        recipes = object.author.recipes.all()
        limit = self.context.get('request').GET.get('recipes_limit')
        if limit:
            recipes = recipes[:limit]
        serializer = RecipesSimpleSerializer(recipes, many=True)
        return serializer.data


    class Meta:
        model = Follow
        fields=(
            'email',
            'username',
            'first_name',
            'last_name',
            'id',
            'recipes',
            'recipes_count',
            'is_subscribed'
        )
