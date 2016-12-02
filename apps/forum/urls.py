# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import SectionListView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.forum.views',
    url(r'^$', login_required(SectionListView.as_view()), name='list'),
    url(r'^add/$', 'section_add', name='section-add'),
    url(r'^(?P<pk>\d+)/update/$', 'section_update', name='section-update'),
    url(r'^(?P<pk>\d+)/$', 'topic_list', name='topic-list'),
    url(r'^topic/add/$', 'topic_add', name='topic-add'),
    url(r'^topic/new/$', 'topic_notify', name='topic-notify'),
    url(r'^topic/(?P<pk>\d+)/$', 'topic_detail', name='topic-detail'),
    url(r'^topic/(?P<pk>\d+)/update/$', 'topic_update', name='topic-update'),
    url(r'^comment/(?P<pk>\d+)/update/$', 'comment_update', name='comment-update'),
    url(r'^comment/(?P<pk>\d+)/delete/$', 'comment_delete', name='comment-delete'),


)
