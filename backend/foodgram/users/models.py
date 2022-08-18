from operator import truediv
from django.contrib.auth.models import AbstractUser
from django.db import models

USER = "user"
ADMIN = "admin"
MODERATOR = "moderator"

user_type = [
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    ]

class User(AbstractUser):
    username = models.CharField('Логин', max_length=150, unique=True)
    email = models.EmailField('Почта', unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    password = models.CharField('Пароль', max_length=150)
    role = models.CharField('Уровень доступа', max_length=30, choices=user_type, default=USER)


