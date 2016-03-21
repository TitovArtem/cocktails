from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ingredients/$', views.ingredients, name='ingredients'),
    url(r'^ingredient/(?P<ingredient_id>[0-9]+)/$',
        views.ingredient, name='ingredient_detail'),
    url(r'^search/$', views.search, name='search'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact/thanks/$', views.thanks, name='thanks'),
]
