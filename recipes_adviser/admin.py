from django.contrib import admin

from .models import Ingredient, Recipe, RecipeStage, CocktailComponent


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'liquid', 'abv', 'image')
    search_fields = ('name', )


class CocktailComponentAdmin(admin.ModelAdmin):
    raw_id_fields = ['ingredient']


class RecipeStageInline(admin.StackedInline):
    model = Recipe.stages.through
    verbose_name = 'Stage'
    verbose_name_plural = "Recipe stages"


class CocktailComponentInline(admin.StackedInline):
    model = Recipe.ingredients.through
    verbose_name = 'Component'
    verbose_name_plural = 'Cocktail components'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type',)
    fieldsets = [
        (None, {'fields': ['title', 'author', 'description',
                           'title_image', 'type']}),
    ]
    inlines = [RecipeStageInline, CocktailComponentInline]


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeStage)
admin.site.register(CocktailComponent, CocktailComponentAdmin)
