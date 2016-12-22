# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

__author__ = 'alexy'

urlpatterns = patterns(
    '',
    url(r'^$', login_required(TemplateView.as_view(template_name='calculator/calculator.html')), name='index'),
)
