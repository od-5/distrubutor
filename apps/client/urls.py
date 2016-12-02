# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from apps.client.data_import import client_list_import
from .views import ClientListView
from .ajax import reassign_manager, get_available_manager_list, get_contact_list, get_task_info, ajax_task_add, \
    get_client_info, ajax_sale_add, ajax_task_update

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.client.views',
    url(r'^$', login_required(ClientListView.as_view()), name='list'),
    url(r'^add/$', 'client_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'client_update', name='update'),
    url(r'^(?P<pk>\d+)/manager/history/$', 'clientmanager_history', name='history'),
    url(r'^(?P<pk>\d+)/contact/$', 'clientcontact_list', name='contact-list'),
    url(r'^(?P<pk>\d+)/contact/add/$', 'clientcontact_add', name='contact-add'),
    url(r'^contact/(?P<pk>\d+)/$', 'clientcontact_update', name='contact-update'),
    url(r'^task/$', 'task_list', name='task-list'),
    # # url(r'^task/$', IncomingTaskListView.as_view(), name='task-list'),
    url(r'^task/add/$', 'task_add', name='task-add'),
    url(r'^task/(?P<pk>\d+)/$', 'task_update', name='task-update'),
    url(r'^task/ajax-add/$', ajax_task_add, name='ajax-task-add'),
    url(r'^ajax-sale-add/$', ajax_sale_add, name='ajax-sale-add'),
    url(r'^task/ajax-update/$', ajax_task_update, name='ajax-task-update'),

    url(r'^reassign-manager/$', reassign_manager, name='reassign-manager'),
    url(r'^get_available_manager_list/$', get_available_manager_list, name='get_available_manager_list'),
    url(r'^get_contact_list/$', get_contact_list, name='get_contact_list'),
    url(r'^get_incomingclient_info/$', get_client_info, name='get_client_info'),
    url(r'^get_task_info/$', get_task_info, name='get_task_info'),

    url(r'^import/$', client_list_import, name='client_list_import'),

)
