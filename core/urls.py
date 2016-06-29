# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from .ajax import ajax_remove_item
from .views import UserUpdateView
from django.contrib.auth.decorators import login_required

__author__ = 'alexy'


urlpatterns = patterns(
    'core.views',
    url(r'^robots\.txt', 'get_robots_txt', name='robots'),
    url(r'^login/$', 'cms_login', name='login'),
    url(r'^login/moderator/$', 'cms_login', {'usertype': 2}, name='login-moderator'),
    url(r'^login/client/$', 'cms_login', {'usertype': 3},  name='login-client'),
    url(r'^login/distributor/$', 'cms_login', {'usertype': 4}, name='login-distributor'),
    url(r'^login/manager/$', 'cms_login', {'usertype': 5},  name='login-manager'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^profile/$', login_required(UserUpdateView.as_view()), name='profile'),
    url(r'^password_change/$', 'password_change', name='password_change'),

    url(r'^site_setup/$', 'setup_view', name='site-setup'),
    url(r'^ajax_remove/$', ajax_remove_item, name='ajax-remove'),

)
