from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from djoser.views import UserViewSet
from user.models import User, Follow
from .serializers import SubscriptionSerializer


class CostomUserViewSet(UserViewSet):
    queryset = User.objects.all()

    @action(detail=False,
            url_path='subscriptions',
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Получаем список подписокю."""
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
             methods=['post', 'delete'],
             url_path='subscribe',
             permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        """Подписаться\отписаться от автора."""
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response('Нельзя подписаться на себя', status=status.HTTP_400_BAD_REQUEST)
        subscription = Follow.objects.filter(author=author, user=user)
        if request.method == 'POST':
            if subscription.exists():
                return Response('Вы уже подписаны', status=status.HTTP_400_BAD_REQUEST)
            queryset = Follow.objects.create(author=author, user=user)
            serializer = SubscriptionSerializer(queryset, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        if request.method == 'DELETE':
            if not subscription.exists():
                return Response('Вы не подписанны', status=status.HTTP_400_BAD_REQUEST)
            subscription.delete()
            return Response('Вы отписались', status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
