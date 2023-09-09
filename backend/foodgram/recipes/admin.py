from django.contrib import admin
from foodgram import settings
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    search_fields = (
        'name',
        'slug'
    )
    empty_value_display = settings.EMPTY_VALUE


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    list_filter = (
        'name',
    )
    empty_value_display = settings.EMPTY_VALUE


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'total_favorites'
    )
    list_filter = (
        'author',
        'name',
        'tags'
    )
    empty_value_display = settings.EMPTY_VALUE
    inlines = (RecipeIngredientInline, )

    def total_favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    total_favorites.short_description = 'Число добавлений рецепта в избранное'


@admin.register(RecipeIngredient)
class RecipeIngredient(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'ingredient',
        'amount'
    )
    empty_value_display = settings.EMPTY_VALUE


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    empty_value_display = settings.EMPTY_VALUE


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    empty_value_display = settings.EMPTY_VALUE
