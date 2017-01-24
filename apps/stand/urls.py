# coding=utf-8
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

__author__ = 'alexy'

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='stand/stand.html'), name='index'),
    # url(r'^(?P<pk>\d+)/$', administrator_required(OrderDetailView.as_view()), name='detail'),
)
