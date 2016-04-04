# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.views.generic import ListView, UpdateView, CreateView, TemplateView
from core.models import User

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.dashboard.views',
    url(r'^$', login_required(TemplateView.as_view(template_name='dashboard/dashboard.html')), name='index'),
)
