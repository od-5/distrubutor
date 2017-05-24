# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from apps.administrator.decorators import administrator_required
from .views import SectionListView, SectionCreateView, SectionUpdateView, TopicListView, TopicCreateView,\
    TopicUpdateView, TopicDetailView, TopicNotifyListView, CommentUpdateView, CommentDeleteView, TopicDeleteView,\
    TopicCloseView
__author__ = 'alexy'

urlpatterns = patterns(
    '',
    url(r'^$', login_required(SectionListView.as_view()), name='list'),
    url(r'^add/$', administrator_required(SectionCreateView.as_view()), name='section-add'),
    url(r'^(?P<pk>\d+)/update/$', administrator_required(SectionUpdateView.as_view()), name='section-update'),
    url(r'^(?P<pk>\d+)/$', login_required(TopicListView.as_view()), name='topic-list'),
    url(r'^topic/add/$', login_required(TopicCreateView.as_view()), name='topic-add'),
    url(r'^topic/new/$', login_required(TopicNotifyListView.as_view()), name='topic-notify'),
    url(r'^topic/(?P<pk>\d+)/$', login_required(TopicDetailView.as_view()), name='topic-detail'),
    url(r'^topic/(?P<pk>\d+)/update/$', login_required(TopicUpdateView.as_view()), name='topic-update'),
    url(r'^topic/(?P<pk>\d+)/delete/$', login_required(TopicDeleteView.as_view()), name='topic-delete'),
    url(r'^topic/(?P<pk>\d+)/close/$', login_required(TopicCloseView.as_view()), name='topic-close'),
    url(r'^comment/(?P<pk>\d+)/update/$', login_required(CommentUpdateView.as_view()), name='comment-update'),
    url(r'^comment/(?P<pk>\d+)/delete/$', login_required(CommentDeleteView.as_view()), name='comment-delete'),
)
