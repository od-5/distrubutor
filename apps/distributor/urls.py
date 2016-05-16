# coding=utf-8
from django.conf.urls import patterns, url
from .ajax import distributor_payment_update, get_task_initial, get_task_cord_list, get_current_location
from .views import DistributorListView, DistributorTaskListView, DistributorTaskArchiveView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.distributor.views',
    url(r'^$', DistributorListView.as_view(), name='list'),
    url(r'^add/$', 'distributor_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'distributor_update', name='update'),
    url(r'^payment_update/$', distributor_payment_update, name='payment-update'),

    # tasks
    url(r'^tasks/$', DistributorTaskListView.as_view(), name='task-list'),
    url(r'^tasks/archive/$', DistributorTaskArchiveView.as_view(), name='task-archive'),
    url(r'^task/add/$', 'distributor_task_add', name='task-add'),
    url(r'^task/(?P<pk>\d+)/$', 'distributor_task_update', name='task-update'),

    # ajax
    url(r'^get_distr_and_area_for_sale/$', get_task_initial, name='get_task_initial'),
    url(r'^get_task_coord_list/$', get_task_cord_list, name='get_task_cord_list'),
    url(r'^get_current_location/$', get_current_location, name='get_current_location'),
)
