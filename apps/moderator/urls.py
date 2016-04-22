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
    url(r'^(?P<pk>\d+)/$', 'moderator_user_update', name='update'),
    url(r'^(?P<pk>\d+)/company/$', 'moderator_company_update', name='company'),
    url(r'^(?P<pk>\d+)/action/$', 'moderator_action_update', name='action'),
    # url(r'^(?P<pk>\d+)/$', 'moderator_view', name='update'),


    # url(r'^task-type/$', 'task_type_update', name='task-type'),

    url(r'^area-add/$', 'area_add', name='area-add'),
    url(r'^area/(?P<pk>\d+)/$', 'area_update', name='area-update'),
)
