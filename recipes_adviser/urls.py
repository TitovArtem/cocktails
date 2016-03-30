from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main_recipes_search, name='index'),
    url(r'^ingredients/$', views.ingredients, name='ingredients'),
    url(r'^ingredient/(?P<ingredient_id>[0-9]+)/$',
        views.ingredient, name='ingredient_detail'),
    url(r'^search/$', views.search, name='search'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact/thanks/$', views.thanks, name='thanks'),
    url(r'^recipe/(?P<recipe_id>[0-9]+)/$', views.recipe, name='recipe_detail'),
    url(r'^tool/(?P<tool_id>[0-9]+)/$', views.tool, name='tool_detail'),
]
