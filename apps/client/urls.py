# coding=utf-8
from django.conf.urls import patterns, url
from .views import ClientListView
# from .ajax import reassign_manager, get_available_manager_list, get_contact_list, get_incomingclient_info, \
#     ajax_task_add, get_incomingtask_info, ajax_task_update, ajax_client_add
from .ajax import reassign_manager, get_available_manager_list, get_contact_list

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.client.views',
    url(r'^$', ClientListView.as_view(), name='list'),
    url(r'^add/$', 'client_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'client_update', name='update'),
    url(r'^(?P<pk>\d+)/manager/history/$', 'clientmanager_history', name='history'),
    url(r'^(?P<pk>\d+)/contact/$', 'clientcontact_list', name='contact-list'),
    url(r'^(?P<pk>\d+)/contact/add/$', 'clientcontact_add', name='contact-add'),
    url(r'^contact/(?P<pk>\d+)/$', 'clientcontact_update', name='contact-update'),
    # url(r'^task/$', 'incomingtask_list', name='task-list'),
    # # url(r'^task/$', IncomingTaskListView.as_view(), name='task-list'),
    # url(r'^task/add/$', 'incomingtask_add', name='task-add'),
    # url(r'^task/ajax-add/$', ajax_task_add, name='ajax-task-add'),
    # url(r'^ajax-client-add/$', ajax_client_add, name='ajax-client-add'),
    # url(r'^task/ajax-update/$', ajax_task_update, name='ajax-task-update'),
    # url(r'^task/(?P<pk>\d+)/$', 'incomingtask_update', name='task-update'),
    url(r'^reassign-manager/$', reassign_manager, name='reassign-manager'),
    url(r'^get_available_manager_list/$', get_available_manager_list, name='get_available_manager_list'),
    url(r'^get_contact_list/$', get_contact_list, name='get_contact_list'),
    # url(r'^get_incomingclient_info/$', get_incomingclient_info, name='get_incomingclient_info'),
    # url(r'^get_incomingtask_info/$', get_incomingtask_info, name='get_incomingtask_info'),
)
