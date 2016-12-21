# coding=utf-8
from django.conf.urls import patterns, url
from .views import LandingView

__author__ = 'alexy'


urlpatterns = patterns(
    'landing.views',
    url(r'^$', LandingView.as_view(), name='index'),
    url(r'^set_current_city/$', 'set_current_city', name='set_current_city'),
    url(r'^set_current_city_from_input/$', 'set_current_city_from_input', name='set_current_city_from_input'),
)
