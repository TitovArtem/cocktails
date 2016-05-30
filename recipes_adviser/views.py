from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse

from .models import Ingredient, Recipe, CocktailTool
from .forms import RecipeSearchForm


class RecipeSearchView(View):
    """ The view for index page with search form for cocktails. """

    RECIPE_PER_PAGE = 30

    def get(self, request):
        form = RecipeSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['query']
            if q:
                recipes = Recipe.objects.filter(title__icontains=q)
            else:
                recipes = Recipe.objects.all()

            if self.is_any_checkbox_pressed(form):
                recipes = self.filter_recipes_by_checkboxes(form, recipes)
        else:
            recipes = Recipe.objects.all()

        if request.is_ajax():
            recipes_num = request.GET.get('recipesNum')
            if not recipes_num:
                return HttpResponse(self.RECIPE_PER_PAGE)
            recipes_num = int(recipes_num)
            recipes = recipes[recipes_num:recipes_num + self.RECIPE_PER_PAGE]
            return render_to_response(
                'recipes_adviser/partials/_recipes_entry.html',
                {"recipes": recipes})

        context = {'recipes_search_form': form,
                   'recipes': recipes[:self.RECIPE_PER_PAGE]}
        return render_to_response('recipes_adviser/index.html', context)

    def is_any_checkbox_pressed(self, form):
        return (form.cleaned_data['is_long']
                or form.cleaned_data['is_shot']
                or form.cleaned_data['is_strong']
                or form.cleaned_data['is_non_alcoholic'])

    def filter_recipes_by_checkboxes(self, form, recipes):
        recipes = self._filter_by_cocktail_type(form, recipes)
        return self._filter_by_alcohol(form, recipes)

    def _filter_by_cocktail_type(self, form, recipes):
        is_long = form.cleaned_data['is_long']
        is_shot = form.cleaned_data['is_shot']
        if not (is_long ^ is_shot):  # xor - return if both checkboxes
            return recipes           # are pressed or both are unpressed
        result = []
        for recipe in recipes:
            if is_long and recipe.is_long():
                result.append(recipe)
            elif is_shot and recipe.is_shot():
                result.append(recipe)
        return result

    def _filter_by_alcohol(self, form, recipes):
        is_strong = form.cleaned_data['is_strong']
        is_non_alc = form.cleaned_data['is_non_alcoholic']
        if not (is_strong ^ is_non_alc):  # xor - return if both checkboxes
            return recipes                # are pressed or both are unpressed
        result = []
        for recipe in recipes:
            if is_strong and recipe.is_strong():
                result.append(recipe)
            elif is_non_alc and not recipe.is_alcoholic():
                result.append(recipe)
        return result


def ingredient(request, ingredient_id):
    ingredient_obj = get_object_or_404(Ingredient, id=ingredient_id)
    if not ingredient_obj.image:
        ingredient_obj.image = {'url': settings.DEFAULT_INGREDIENT_IMG_URL}
    return render_to_response('recipes_adviser/detail_page.html',
                              {'object': ingredient_obj})


def recipe(request, recipe_id):
    cocktail = get_object_or_404(Recipe, id=recipe_id)
    if not cocktail.title_image:
        cocktail.title_image = {'url': settings.DEFAULT_RECIPE_IMG_URL}
    rus_measures = {'ml': 'мл.', 'g': 'гр.', 'pcs': 'шт.'}
    return render_to_response('recipes_adviser/recipe_detail.html',
                              {'recipe': cocktail, 'measures': rus_measures})


def tool(request, tool_id):
    tool_obj = get_object_or_404(CocktailTool, id=tool_id)
    if not tool_obj.image:
        tool_obj.image = {"url": settings.DEFAULT_TOOL_IMG_URL}
    return render_to_response("recipes_adviser/detail_page.html",
                              {"object": tool_obj})


def about(request):
    return render_to_response("recipes_adviser/about.html")
