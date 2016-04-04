# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from django.contrib.admin.views.decorators import staff_member_required
from apps.administrator.views import AdministratorListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.administrator.views',
    url(r'^$', AdministratorListView.as_view(), name='list'),
    url(r'^add/$', 'administrator_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'administrator_update', name='update'),
)
