from email.policy import default
from pickletools import read_long1
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=(
            'email',
            'username',
            'first_name',
            'last_name',
            'id'
        )


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate_following(self, user):
        if user == self.context['request'].user:
            raise serializers.ValidationError(
                'На себя подписаться не получится, хоть и очень хочется.'
                )
        return user


    class Meta():
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]