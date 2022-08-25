from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    USER = "user"
    ADMIN = "admin"
    GEST = "gest"

    user_type = [
        (USER, "user"),
        (GEST, "gest"),
        (ADMIN, "admin"),
    ]
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField('Почта', unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    password = models.CharField('Пароль', max_length=150)
    role = models.CharField('Уровень доступа', max_length=30, choices=user_type, default=USER)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    @property
    def is_gest(self):
        return self.role == self.GEST

    @property
    def is_user(self):
        return self.role == self.USER


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписка'
    )
    UniqueConstraint(fields=['user', 'author'], name='unic')

    class Meta:
        verbose_name_plural = 'Подписки'