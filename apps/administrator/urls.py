# coding=utf-8
from django.conf.urls import patterns, url

from .views import AdministratorListView, AdministratorCreateView, AdministratorUpdateView
from .decorators import administrator_required

__author__ = 'alexy'

urlpatterns = patterns(
    '',
    url(r'^$', administrator_required(AdministratorListView.as_view()), name='list'),
    url(r'^add/$', administrator_required(AdministratorCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', administrator_required(AdministratorUpdateView.as_view()), name='update'),
)
