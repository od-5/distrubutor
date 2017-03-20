# coding=utf-8
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import api_root, task_list, task_detail, gpspoint_add, confirm_address, gpspoint_comment, photo_add, \
    location_view, questionary_detail, questionary_completed, questionary_completed_answer, audio_add

__author__ = 'alexy'


urlpatterns = patterns(
    'api.views',
    url(r'^$', api_root, name='index'),
    url(r'^tasks/$', task_list, name='task_list'),
    url(r'^task/(?P<pk>[0-9]+)/$', task_detail, name='task_detail'),
    url(r'^questionary/(?P<pk>[0-9]+)/$', questionary_detail, name='questionary_detail'),
    url(r'^questionary/completed/$', questionary_completed, name='questionary_completed'),
    url(r'^questionary/completed/answer/$', questionary_completed_answer, name='questionary_completed_answer'),
    url(r'^point/$', gpspoint_add, name='point_add'),
    url(r'^point/confirm/$', confirm_address, name='confirm_address'),
    url(r'^point/(?P<pk>[0-9]+)/$', gpspoint_comment, name='point_comment'),
    url(r'^photo/$', photo_add, name='photo_add'),
    url(r'^audio/$', audio_add, name='audio_add'),
    url(r'^location/$', location_view, name='location'),

)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
