# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from django.contrib.admin.views.decorators import staff_member_required
from apps.administrator.views import AdministratorListView
from .views import PackageListView, PackageAddView, PackageUpdateView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.packages.views',
    url(r'^$', PackageListView.as_view(), name='list'),
    url(r'^add/$', PackageAddView.as_view(), name='add'),
    url(r'^(?P<pk>\d+)/$', PackageUpdateView.as_view(), name='update'),
)
