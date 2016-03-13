from django.shortcuts import render, get_object_or_404, get_list_or_404, \
    render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.mail import send_mail

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
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Введите тему.')
        if not request.POST.get('message', ''):
            errors.append('Введите сообщение.')
        if request.POST.get('e-mail') and '@' not in request.POST['e-mail']:
            errors.append('Введите корректный e-mail адрес.')
        if not errors:
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST.get('e-mail', 'noreply@example.com'),
                ['pbi62007@yandex.ru'],
            )
        return HttpResponseRedirect('/recipes/contact/thanks/')
    return render(request, 'recipes_adviser/contact_form.html',
                  {'errors': errors})
