from django.contrib import admin


from .models import (
    Ingredients,
    Recipes,
    Tags,
    Favorite,
    Shoping_cart,
    Amount_of_ingredients)


class IngredientAdmin(admin.ModelAdmin):
    """Кастомная админка модели Ingredients."""
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_editable = ('name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-Нет значения-'


class IngredientAmountInline(admin.TabularInline):
    model = Amount_of_ingredients


class RecipeAdmin(admin.ModelAdmin):
    """Кастомная админка модели Recipes."""
    list_display = (
        'pk',
        'name',
        'author',
        'image',
        'count_added'
    )
    exclude = ('ingredients',)
    inlines = (IngredientAmountInline,)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('author__username', 'name', 'tags__name')
    empty_value_display = '-Нет значения-'

    def count_added(self, obj):
        return obj.favorite.count()


class TagAdmin(admin.ModelAdmin):
    """Кастомная админка модели Tags."""
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    list_editable = ('name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-Нет значения-'


class AmountOfIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount'
    )
    search_fields = ('recipe__name', 'ingredients__name')


class FavoriteShoppingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipes'
    )
    search_fields = ('user__username', 'recipes__name')


admin.site.register(Tags, TagAdmin)
admin.site.register(Recipes, RecipeAdmin)
admin.site.register(Ingredients, IngredientAdmin)
admin.site.register(Favorite, FavoriteShoppingAdmin)
admin.site.register(Shoping_cart, FavoriteShoppingAdmin)
admin.site.register(Amount_of_ingredients, AmountOfIngredientAdmin)
