# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from .ajax import ajax_remove_item
from .views import UserUpdateView

__author__ = 'alexy'


urlpatterns = patterns(
    'core.views',
    url(r'^robots\.txt', 'get_robots_txt', name='robots'),
    url(r'^login/$', 'cms_login', name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^profile/$', UserUpdateView.as_view(), name='profile'),
    url(r'^password_change/$', 'password_change', name='password_change'),

    # url(r'^block/example/add/$', 'block_example_add_view', name='block_example-add'),
    # url(r'^block/example/(?P<pk>\d+)/$', 'block_example_update_view', name='block_example-update'),
    # url(r'^block/example/$', 'block_example_view', name='block_example'),


    # url(r'^city-map/$', ymap, name='map'),
    # url(r'^surface-map/$', ymap_surface, name='map-surface'),
    url(r'^ajax_remove/$', ajax_remove_item, name='ajax-remove'),

    # url(r'^cabinet/login/$', 'cabinet_login', name='login'),
    # url(r'^cabinet/logout/$', logout, name='logout'),

)
