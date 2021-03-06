from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings

from .models import Ingredient, Recipe, CocktailTool
from .forms import ContactForm


IMG_SIZE = {'height': 250, 'width': 250}


def ingredients(request):
    cocktails = Ingredient.objects.order_by('abv')[:100]
    output = '\n'.join([str(item) for item in cocktails])
    return HttpResponse(output)


def ingredient(request, ingredient_id):
    ingredient_obj = get_object_or_404(Ingredient, id=ingredient_id)
    if not ingredient_obj.image:
        ingredient_obj.image = {'url': settings.DEFAULT_INGREDIENT_IMG_URL}
    return render_to_response('recipes_adviser/ingredient_detail.html',
                              {'ingredient': ingredient_obj,
                               'img_size': IMG_SIZE})


def recipe(request, recipe_id):
    cocktail = get_object_or_404(Recipe, id=recipe_id)
    if not cocktail.title_image:
        cocktail.title_image = {'url': settings.DEFAULT_RECIPE_IMG_URL}
    rus_measures = {'ml': 'мл.', 'g': 'гр.', 'pcs': 'шт.'}
    return render_to_response('recipes_adviser/recipe_detail.html',
                              {'recipe': cocktail, 'img_size': IMG_SIZE,
                               'measures': rus_measures})


def tool(request, tool_id):
    tool_obj = get_object_or_404(CocktailTool, id=tool_id)
    if not tool_obj.image:
        tool_obj.image = {'url': settings.DEFAULT_TOOL_IMG_URL}
    return render_to_response('recipes_adviser/tool_detail.html',
                              {'tool': tool_obj, 'img_size': IMG_SIZE})


def index(request):
    errors = []
    recipes = Recipe.objects.all()[:20]
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Поисковой запрос не был задан.')
        elif len(q) > 20:
            errors.append('Максимальный размер запроса 20 символов.')
        else:
            recipes = Recipe.objects.filter(title__icontains=q)

    if 'cocktails-checkbox' in request.GET:
        checkboxes = {'long': False, 'shot': False,
                      'strong': False, 'non-alcoholic': False}
        for val in request.GET.getlist('cocktails-checkbox'):
            checkboxes[val] = True

        if checkboxes['long']:
            recipes = [recipe for recipe in recipes if recipe.is_long()]
        if checkboxes['shot']:
            shots = [recipe for recipe in recipes if recipe.is_shot()]
            if checkboxes['long']:
                recipes += shots
            else:
                recipes = shots
        if checkboxes['non-alcoholic'] and not checkboxes['strong']:
            recipes = [recipe for recipe in recipes
                       if not recipe.is_alcoholic()]
        if checkboxes['strong'] and not checkboxes['non-alcoholic']:
            recipes = [recipe for recipe in recipes if recipe.is_strong()]

    return render_to_response('recipes_adviser/index.html',
                              {'errors': errors, 'recipes': recipes})


def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Поисковой запрос не был задан.')
        elif len(q) > 20:
            errors.append('Максимальный размер запроса 20 символов.')
        else:
            ingredients = Ingredient.objects.filter(name__icontains=q)
            return render_to_response('recipes_adviser/search_results.html',
                                      {'ingredients': ingredients, 'query': q})
    return render_to_response('recipes_adviser/search_form.html',
                              {'errors': errors})


def thanks(request):
    return render(request, 'recipes_adviser/thanks.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('e-mail', 'pbi62007@yandex.ru'),
                ['pbi62007@yandex.ru'],
            )
            return HttpResponseRedirect('/recipes/contact/thanks/')
    else:
        form = ContactForm()
    return render_to_response('recipes_adviser/contact_form.html',
                              {'form': form})

