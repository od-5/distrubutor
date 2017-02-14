# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .data_import import client_list_import
from .views import ClientListView, ClientCreateView, ClientUpdateView, ClientManagerHistory, ClientContactListView,\
    ClientContactCreateView, ClientContactUpdateView, ClientTaskListView, ClientTaskCreateView, ClientTaskUpdateView
from .ajax import reassign_manager, get_available_manager_list, get_contact_list, get_task_info, ajax_task_add, \
    get_client_info, ajax_sale_add, ajax_task_update

__author__ = 'alexy'

urlpatterns = patterns(
    '',
    url(r'^$', login_required(ClientListView.as_view()), name='list'),
    url(r'^add/$', login_required(ClientCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', login_required(ClientUpdateView.as_view()), name='update'),
    url(r'^(?P<pk>\d+)/manager/history/$', login_required(ClientManagerHistory.as_view()), name='history'),
    url(r'^(?P<pk>\d+)/contact/$', login_required(ClientContactListView.as_view()), name='contact-list'),
    url(r'^(?P<pk>\d+)/contact/add/$', login_required(ClientContactCreateView.as_view()), name='contact-add'),
    url(r'^contact/(?P<pk>\d+)/$', login_required(ClientContactUpdateView.as_view()), name='contact-update'),
    url(r'^task/$', login_required(ClientTaskListView.as_view()), name='task-list'),
    url(r'^task/add/$', login_required(ClientTaskCreateView.as_view()), name='task-add'),
    url(r'^task/(?P<pk>\d+)/$', login_required(ClientTaskUpdateView.as_view()), name='task-update'),
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
