# coding=utf-8
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

__author__ = 'alexy'


urlpatterns = patterns(
    'api.views',
    url(r'^$', 'api_root', name='index'),
    url(r'^tasks/$', 'task_list', name='task_list'),
    url(r'^task/(?P<pk>[0-9]+)/$', 'task_detail', name='task_detail'),
    # url(r'^porch/(?P<pk>[0-9]+)/$', 'porch_update', name='porch_update'),
    url(r'^point/$', 'gpspoint_add', name='point_add'),
    url(r'^point/(?P<pk>[0-9]+)/$', 'gpspoint_comment', name='point_comment'),
    url(r'^photo/$', 'photo_add', name='photo_add'),
    url(r'^location/$', 'location_view', name='location'),

)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
