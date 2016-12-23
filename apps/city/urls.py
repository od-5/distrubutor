# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from apps.administrator.decorators import administrator_required
from .models import City
from .views import CityCreateView, CityUpdateView, CityListView
from .ajax import find_city, get_moderator_list

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.city.views',
    url(r'^$', login_required(CityListView.as_view(model=City)), name='list'),
    url(r'^add/$', administrator_required(CityCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', login_required(CityUpdateView.as_view()), name='update'),

    url(r'^find/$', find_city, name='find'),
    url(r'^get_moderator_list/$', get_moderator_list, name='get_moderator_list')
)
