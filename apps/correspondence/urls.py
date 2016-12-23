# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from apps.administrator.decorators import administrator_required
from .views import MessageListView, MessageCreateView, MessageDetailView, MessageNotifyListView, MessageNotifyDetailView
from .ajax import find_moderators

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.correspondence.views',
    url(r'^$', login_required(MessageListView.as_view()), name='list'),
    url(r'^add/$', administrator_required(MessageCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', login_required(MessageDetailView.as_view()), name='detail'),
    url(r'^messages/$', login_required(MessageNotifyListView.as_view()), name='notify-list'),
    url(r'^message/(?P<pk>\d+)/$', login_required(MessageNotifyDetailView.as_view()), name='message-detail'),
    url(r'^find_moderators/$', find_moderators, name='find_moderators'),
)
