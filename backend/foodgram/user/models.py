from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField('Почта', unique=True)
    username = models.CharField('Имя пользователя', max_length=150, unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    password = models.CharField('Пароль', max_length=150)

    class Meta:
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
    
    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name_plural = 'Подписки'
        constraints =(
            UniqueConstraint(
                fields=('user', 'author'),
                name='uniqoe_follow'
            ),
        )
