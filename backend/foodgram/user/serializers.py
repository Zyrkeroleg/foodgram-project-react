from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    id=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=User
        fields=(
            'email',
            'username',
            'first_name',
            'last_name',
            'id'
        )
