# coding=utf-8
from django.conf.urls import patterns, url
from .views import AgencyListView
from apps.administrator.decorators import administrator_required

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.agency.views',
    url(r'^$', administrator_required(AgencyListView.as_view()), name='list'),
    url(r'^add/$', 'agency_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'agency_update', name='update'),
)
