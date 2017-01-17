# coding=utf-8
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from .views import LandingView

__author__ = 'alexy'


urlpatterns = patterns(
    'landing.views',
    url(r'^$', LandingView.as_view(), name='index'),
    url(r'^thnx/$', TemplateView.as_view(template_name='landing/ok.html'), name='thnx'),
    url(r'^set_current_city/$', 'set_current_city', name='set_current_city'),
    url(r'^set_current_city_from_input/$', 'set_current_city_from_input', name='set_current_city_from_input'),
)
