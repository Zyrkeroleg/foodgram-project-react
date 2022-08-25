from django.contrib.auth import get_user_model
from django.db import models
from colorfield.fields import ColorField
from user.models import User


COLOR_PALETTE = [
        ("#FFFFFF", "белый",),
        ("#000000", "черный",),
        ("ff0000", "красный",),
        ("ff00fb", "розовый",),
        ("4000ff", "синий",),
        ("00ffee", "голубой",),
        ("00ff00", "зелёный",),
        ("e6ff00", "желтый",),
        ("ff6f00", "оранжевый",),
    ]

UNITS = [
    ('ч. л.', '1'),
    ('ст. л.', '2'),
    ('г', '3'),
    ('стакан', '4'),
    ('по вкусу', '5'),
    ('шт', '6'),
    ('капля', '7'),
    ('кг', '8'),
    ('мл', '9'),
    ('щепотка', '10'),
]

class Tags(models.Model):
    title = models.CharField('Тег', max_length=20, blank=False)
    color = ColorField(choices=COLOR_PALETTE, blank=False)
    slug = models.SlugField(unique=True, max_length=20, blank=False)

    class Meta:
        verbose_name_plural = 'Тэги'
    
    def __str__(self):
        return self.title


class Ingredients(models.Model):
    name = models.CharField('Ингредиент', max_length=200, blank=False)
    amount = models.IntegerField('Колличество', blank=False)
    measurement_unit = models.CharField('Еденица измерения',max_length=200, choices=UNITS, blank=False)

    class Meta:
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return self.name


class Recipes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    title = models.CharField('Название рецепта', max_length=200, blank=False)
    image = models.ImageField(upload_to='.../', blank=False, null=True)
    description = models.TextField('Описание', blank=False)
    ingredients = models.ManyToManyField(Ingredients, blank=False)
    tags = models.ManyToManyField(Tags, blank=False)
    cooking_time = models.IntegerField('Время приготовления. мин', blank=False)
    
    class Meta:
        verbose_name_plural = 'Рецепты'
    
    def __str__(self):
        return self.title

class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Избранное'
    )

    class Meta:
        verbose_name_plural = 'Избранное'


