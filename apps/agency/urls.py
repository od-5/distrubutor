# coding=utf-8
from django.conf.urls import patterns, url

from apps.administrator.decorators import administrator_required
from .views import AgencyListView, AgencyCreateView, AgencyUpdateView

__author__ = 'alexy'

urlpatterns = patterns(
    '',
    url(r'^$', administrator_required(AgencyListView.as_view()), name='list'),
    url(r'^add/$', administrator_required(AgencyCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', administrator_required(AgencyUpdateView.as_view()), name='update'),
)
