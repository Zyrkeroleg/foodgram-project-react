from django.contrib import admin

from .models import Ingredients, Recipes, Tags, Favorite

admin.site.register(Tags)
admin.site.register(Recipes)
admin.site.register(Ingredients)
admin.site.register(Favorite)