# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import HangerMailListView, HangerMailCreateView, HangerMailUpdateView

__author__ = 'alexy'

urlpatterns = patterns(
    '',
    url(r'^$', login_required(HangerMailListView.as_view()), name='list'),
    url(r'^add/$', login_required(HangerMailCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', login_required(HangerMailUpdateView.as_view()), name='update'),
)
