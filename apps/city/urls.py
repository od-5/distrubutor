# coding=utf-8
from django.conf.urls import patterns, url
from .models import City
from .views import CityCreateView, CityUpdateView, CityListView
from .ajax import find_city

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.city.views',
    url(r'^$', CityListView.as_view(model=City), name='list'),
    url(r'^add/$', CityCreateView.as_view(), name='add'),
    url(r'^(?P<pk>\d+)/$', CityUpdateView.as_view(), name='update'),

    url(r'^find/$', find_city, name='find'),
)
