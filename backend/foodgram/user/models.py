from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AbstractUser
from django.db import models

USER = "user"
ADMIN = "admin"
GEST = "gest"

user_type = [
        (USER, "user"),
        (GEST, "gest"),
        (ADMIN, "admin"),
    ]

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField('Логин', max_length=150, unique=True)
    email = models.EmailField('Почта', unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    password = models.CharField('Пароль', max_length=150)
    role = models.CharField('Уровень доступа', max_length=30, choices=user_type, default=USER)
    token = models.CharField(max_length=200, blank=True)
    REQUIRED_FIELDS = ['email', ] 

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    @property
    def is_gest(self):
        return self.role == self.GEST

    @property
    def is_user(self):
        return self.role == self.USER


