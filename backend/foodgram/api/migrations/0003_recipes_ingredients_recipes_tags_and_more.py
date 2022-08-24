# Generated by Django 4.1 on 2022-08-24 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(to='api.ingredients'),
        ),
        migrations.AddField(
            model_name='recipes',
            name='tags',
            field=models.ManyToManyField(to='api.tags'),
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='amount',
            field=models.IntegerField(verbose_name='Колличество'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='cooking_time',
            field=models.IntegerField(verbose_name='Время приготовления. мин'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='image',
            field=models.ImageField(null=True, upload_to='.../'),
        ),
    ]
