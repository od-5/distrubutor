# coding=utf-8
from django.conf.urls import patterns, url
from apps.manager.models import Manager
from apps.manager.views import ManagerListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.manager.views',
    url(r'^$', ManagerListView.as_view(), name='list'),
    url(r'^add/$', 'manager_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'manager_update', name='update'),
)
