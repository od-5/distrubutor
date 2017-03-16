# coding=utf-8
from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from .views import CityCreateView, CityUpdateView, CityListView, CountryListView, CountryCreateView,\
    CountryUpdateView, RegionListView, RegionCreateView, RegionUpdateView
from .ajax import find_city, get_moderator_list, get_city_list
from apps.administrator.decorators import administrator_required

__author__ = '2mitrij'

city_urlpatterns = patterns(
    '',
    url(r'^$', login_required(CityListView.as_view()), name='list'),
    url(r'^add/$', administrator_required(CityCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', login_required(CityUpdateView.as_view()), name='update'),

    url(r'^find/$', find_city, name='find'),
    url(r'^get_moderator_list/$', get_moderator_list, name='get_moderator_list'),
)

country_urlpatterns = patterns(
    '',
    url(r'^$', administrator_required(CountryListView.as_view()), name='list'),
    url(r'^add/$', administrator_required(CountryCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', administrator_required(CountryUpdateView.as_view()), name='update'),
    url(r'^get_city_list/$', get_city_list, name='get_city_list'),
)

region_urlpatterns = patterns(
    '',
    url(r'^$', administrator_required(RegionListView.as_view()), name='list'),
    url(r'^add/$', administrator_required(RegionCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', administrator_required(RegionUpdateView.as_view()), name='update'),
)

urlpatterns = patterns(
    '',
    url(r'^city/', include(city_urlpatterns, 'city')),
    url(r'^region/', include(region_urlpatterns, 'region')),
    url(r'^country/', include(country_urlpatterns, 'country')),
)
