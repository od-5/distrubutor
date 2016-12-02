# coding=utf-8
from django.conf.urls import patterns, url
from apps.administrator.decorators import administrator_required
from .views import OrderListView, OrderDetailView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.packages.views',
    url(r'^$', administrator_required(OrderListView.as_view()), name='list'),
    url(r'^(?P<pk>\d+)/$', administrator_required(OrderDetailView.as_view()), name='detail'),
)
