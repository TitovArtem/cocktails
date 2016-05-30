from django.conf.urls import url

from . import views


app_name = 'recipes_adviser'

urlpatterns = [
    url(r'^$', views.RecipeSearchView.as_view(), name='index'),
    url(r'^ingredient/(?P<ingredient_id>[0-9]+)/$',
        views.ingredient, name='ingredient_detail'),
    url(r'^recipe/(?P<recipe_id>[0-9]+)/$', views.recipe, name='recipe_detail'),
    url(r'^tool/(?P<tool_id>[0-9]+)/$', views.tool, name='tool_detail'),
    url(r'about/$', views.about, name='about')
]
