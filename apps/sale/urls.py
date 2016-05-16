# coding=utf-8
from django.conf.urls import patterns, url
from .models import Sale
from .views import SaleListView, JournalListView
from .ajax import get_client_coord_list

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.sale.views',
    url(r'^$', SaleListView.as_view(), name='list'),
    url(r'^add/$', 'sale_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'sale_view', name='update'),
    url(r'^update/$', 'sale_update', name='sale_update'),
    url(r'^(?P<pk>\d+)/maket/$', 'sale_maket', name='maket'),
    url(r'^maket/(?P<pk>\d+)/$', 'sale_maket_update', name='maket-update'),
    url(r'^(?P<pk>\d+)/order/$', 'sale_order', name='order'),
    url(r'^order/(?P<pk>\d+)/$', 'sale_order_update', name='order-update'),
    url(r'^journal/$', JournalListView.as_view(), name='journal'),
    url(r'export/$', 'address_export', name='address-export'),
    url(r'archive/$', 'get_files', name='download-archive'),
    # url(r'^add-surface/$', 'add_client_surface', name='add-client-surface'),
    #
    url(r'^get_coord_list/$', get_client_coord_list, name='get_cord_list'),
    # url(r'^get_order_address_list/$', get_client_order_address_list, name='get_order_address_list'),
    #
    #
    # url(r'^export/(?P<pk>\d+)/$', 'client_excel_export', name='excel_export'),
)
