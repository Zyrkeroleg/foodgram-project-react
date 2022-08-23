from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from user.models import User
from .permissions import AdminOnlyPermission
from .serializers import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "username",
    ]

    pass


def index(request):
    return HttpResponse("hi")