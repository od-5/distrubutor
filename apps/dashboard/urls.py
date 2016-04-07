# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.views.generic import ListView, UpdateView, CreateView, TemplateView
from core.models import User
from .views import DashboardView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.dashboard.views',
    url(r'^$', login_required(DashboardView.as_view()), name='index'),
)
