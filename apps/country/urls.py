# coding=utf-8
from django.conf.urls import patterns, url
from apps.administrator.decorators import administrator_required
from apps.city.models import Country
from .views import CountryListView, CountryCreateView, CountryUpdateView

__author__ = '2mitry'

urlpatterns = patterns(
    'apps.country.views',
    url(r'^$', administrator_required(CountryListView.as_view(model=Country)), name='list'),
    url(r'^add/$', administrator_required(CountryCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', administrator_required(CountryUpdateView.as_view()), name='update'),
)
