# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import DashboardView

__author__ = 'alexy'

urlpatterns = patterns(
    '',
    url(r'^$', login_required(DashboardView.as_view()), name='index'),
)
