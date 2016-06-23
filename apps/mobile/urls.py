# coding=utf-8
from django.conf.urls import patterns, url
from .views import GPSPointListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.mobile.views',
    url(r'^$', GPSPointListView.as_view(), name='list'),
)
