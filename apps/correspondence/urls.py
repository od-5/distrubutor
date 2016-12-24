# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from apps.administrator.decorators import administrator_required
from .views import MessageListView, MessageCreateView, MessageDetailView, UserMessageListView, UserMessageDetailView
from .ajax import find_moderators

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.correspondence.views',
    url(r'^$', login_required(MessageListView.as_view()), name='list'),
    url(r'^add/$', administrator_required(MessageCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', login_required(MessageDetailView.as_view()), name='detail'),
    url(r'^messages/$', login_required(UserMessageListView.as_view()), name='usermessage-list'),
    url(r'^message/(?P<pk>\d+)/$', login_required(UserMessageDetailView.as_view()), name='usermessage-detail'),
    url(r'^find_moderators/$', find_moderators, name='find_moderators'),
)
