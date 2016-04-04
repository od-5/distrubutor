# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from apps.moderator.views import ModeratorListView
from core.models import User

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.moderator.views',
    url(r'^$', ModeratorListView.as_view(), name='list'),
    url(r'^add/$', 'moderator_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'moderator_view', name='update'),

    url(r'^company/$', 'moderator_update', name='company'),
)
