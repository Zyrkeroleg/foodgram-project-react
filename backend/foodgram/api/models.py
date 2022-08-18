from tabnanny import verbose
from django.contrib.auth import get_user_model
from django.db import models
from colorfield.fields import ColorField
from users.models import User


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


class Recipes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField('Название рецепта', max_length=200)
    image = models.ImageField(upload_to='.../', blank=True, null=True)
    description = models.TextField()
    # ingredients = models.ManyToManyField() # ???
    # tags = models.CharField(max_length=30, choices=...) # ??
    cooking_time = models.IntegerField()
    
    class Meta:
        verbose_name_plural = 'Рецепты'
    
    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField('Тег', max_length=20)
    color = ColorField(choices=COLOR_PALETTE)
    slug = models.SlugField(unique=True, max_length=20)


class Ingredients(models.Model):
    name = models.CharField('Ингредиент', max_length=200)
    amount = models.IntegerField(blank=False)
    measurement_unit = models.CharField('Еденица измерения',max_length=200, choices=UNITS)
