# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from django.contrib.admin.views.decorators import staff_member_required
from apps.administrator.views import AdministratorListView
from .views import OrderListView, OrderDetailView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.packages.views',
    url(r'^$', OrderListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', OrderDetailView.as_view(), name='detail'),
)
