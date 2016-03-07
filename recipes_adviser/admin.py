from django.contrib import admin

from .models import Ingredient


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'liquid', 'abv')

admin.site.register(Ingredient, IngredientAdmin)
