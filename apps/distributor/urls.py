# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url

from .ajax import distributor_payment_update, get_task_initial, get_task_cord_list, get_current_location, \
    ajax_remove_photo
from .views import DistributorListView, DistributorTaskListView, DistributorTaskArchiveView,\
    DistributorTaskCreateView, DistributorTaskUpdateView, DistributorReportView, DistributorPromoTaskCreateView, \
    DistributorPromoTaskUpdateView, DistributorQuestTaskCreateView, DistributorQuestTaskUpdateView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.distributor.views',
    url(r'^$', login_required(DistributorListView.as_view()), name='list'),
    url(r'^add/$', 'distributor_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'distributor_update', name='update'),
    url(r'^payment_update/$', distributor_payment_update, name='payment-update'),
    # report
    url(r'^report/$', login_required(DistributorReportView.as_view()), name='report'),
    url(r'^report/excel/$', 'distributor_report_excel', name='report-excel'),
    url(r'^report/detail/(?P<pk>\d+)/$', 'distributor_detail_report_excel', name='report-detail'),
    # tasks
    url(r'^tasks/$', login_required(DistributorTaskListView.as_view()), name='task-list'),
    url(r'^tasks/archive/$', login_required(DistributorTaskArchiveView.as_view()), name='task-archive'),
    url(r'^task/add/$', login_required(DistributorTaskCreateView.as_view()), name='task-add'),
    url(r'^task/(?P<pk>\d+)/$', login_required(DistributorTaskUpdateView.as_view()), name='task-update'),

    url(r'^task/promo/add/$', login_required(DistributorPromoTaskCreateView.as_view()), name='task-promo-add'),
    url(r'^task/promo/(?P<pk>\d+)/$', login_required(DistributorPromoTaskUpdateView.as_view()),
        name='task-promo-update'),

    url(r'^task/quest/add/$', login_required(DistributorQuestTaskCreateView.as_view()), name='task-quest-add'),
    url(r'^task/quest/(?P<pk>\d+)/$', login_required(DistributorQuestTaskUpdateView.as_view()),
        name='task-quest-update'),

    url(r'^task/(?P<pk>\d+)/map/$', 'distributor_task_update_map', name='task-update-map'),
    url(r'^point/(?P<pk>\d+)/$', 'gps_point_update', name='gpspoint-update'),

    # ajax
    url(r'^get_distr_and_area_for_sale/$', get_task_initial, name='get_task_initial'),
    url(r'^get_task_coord_list/$', get_task_cord_list, name='get_task_cord_list'),
    url(r'^get_current_location/$', get_current_location, name='get_current_location'),
    url(r'^ajax_photo_delete/$', ajax_remove_photo, name='ajax_remove_photo'),
)
