from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader

from .models import Ingredient


def index(request):
    ingredients = Ingredient.objects.all()[:20]
    context = RequestContext(request, {'ingredients': ingredients})
    return render(request, 'recipes_adviser/index.html', context)


def ingredients(request):
    cocktails = Ingredient.objects.order_by('abv')[:100]
    output = '\n'.join([str(item) for item in cocktails])
    return HttpResponse(output)


def ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    return render(request, 'recipes_adviser/detail.html',
                  {'ingredient': ingredient})


def search_form(request):
    return render_to_response('recipes_adviser/search_form.html')


def search(request):
    if 'q' in request.GET:
        message = 'Вы искали: %r' % request.GET['q']
    else:
        message = 'Вы отправили пустую форму.'
    return HttpResponse(message)
