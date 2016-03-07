from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ingredients/$', views.ingredients, name='ingredients'),
    url(r'^ingredient/(?P<ingredient_id>[0-9]+)/$',
        views.ingredient, name='detail'),
    url(r'^search-form/$', views.search_form),
    url(r'^search/$', views.search, name='search'),
]
