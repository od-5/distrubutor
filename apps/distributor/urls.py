# coding=utf-8
from django.conf.urls import patterns, url
from apps.distributor.views import DistributorListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.distributor.views',
    url(r'^$', DistributorListView.as_view(), name='list'),
    url(r'^add/$', 'distributor_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'distributor_update', name='update'),
    #
    # url(r'^company/$', 'distributor_update', name='info'),
)
