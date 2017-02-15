# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import ManagerListView, ManagerReportView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.manager.views',
    url(r'^$', login_required(ManagerListView.as_view()), name='list'),
    url(r'^add/$', 'manager_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'manager_update', name='update'),
    url(r'^report/$', login_required(ManagerReportView.as_view()), name='report'),
    url(r'^report/excel/$', 'manager_report_excel', name='report-excel'),
    url(r'^report/detail/(?P<pk>\d+)/$', 'manager_detail_report_excel', name='report-detail'),
)
