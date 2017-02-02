# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import StandListView, StandCreateView, StandUpdateView
from .ajax import update_standitem, delete_standitem

__author__ = 'alexy'

urlpatterns = patterns(
    '',
    url(r'^$', login_required(StandListView.as_view()), name='list'),
    url(r'^add/$', login_required(StandCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', login_required(StandUpdateView.as_view()), name='update'),
    # ajax
    url(r'^update_standitem/$', update_standitem, name='standitem'),
    url(r'^delete_standitem/$', delete_standitem, name='standitem-delete'),
)
