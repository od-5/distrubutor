# coding=utf-8
from django.conf.urls import patterns, url
from apps.administrator.decorators import administrator_required
from .views import PackageListView, PackageAddView, PackageUpdateView

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.packages.views',
    url(r'^$', administrator_required(PackageListView.as_view()), name='list'),
    url(r'^add/$', administrator_required(PackageAddView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', administrator_required(PackageUpdateView.as_view()), name='update'),
)
