from django.contrib import admin

from .models import Ingredients, Recipes, Tags

admin.site.register(Tags)
admin.site.register(Recipes)
admin.site.register(Ingredients)
