# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .models import Sale
from .views import SaleListView, JournalListView
from .ajax import get_client_coord_list, payment_add, get_material_residue, send_sms_notify, send_email_notify

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.sale.views',
    url(r'^$', login_required(SaleListView.as_view()), name='list'),
    url(r'^add/$', 'sale_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'sale_view', name='update'),
    url(r'^update/$', 'sale_update', name='sale_update'),
    url(r'^(?P<pk>\d+)/maket/$', 'sale_maket', name='maket'),
    url(r'^maket/(?P<pk>\d+)/$', 'sale_maket_update', name='maket-update'),
    url(r'^(?P<pk>\d+)/order/$', 'sale_order', name='order'),
    url(r'^order/(?P<pk>\d+)/$', 'sale_order_update', name='order-update'),
    url(r'^journal/$', login_required(JournalListView.as_view()), name='journal'),
    url(r'export/$', 'address_export', name='address-export'),
    url(r'archive/$', 'get_files', name='download-archive'),
    # url(r'^add-surface/$', 'add_client_surface', name='add-client-surface'),
    #
    url(r'^get_coord_list/$', get_client_coord_list, name='get_cord_list'),
    url(r'^get_material_residue/$', get_material_residue, name='get_material_residue'),
    # url(r'^get_order_address_list/$', get_client_order_address_list, name='get_order_address_list'),
    #
    #
    # url(r'^export/(?P<pk>\d+)/$', 'client_excel_export', name='excel_export'),
    url(r'(?P<pk>\d+)/payment/$', 'saleorderpayment_list', name='payment-list'),
    url(r'payment/add/$', payment_add, name='payment-add'),

    url(r'send/sms/$', send_sms_notify, name='sms-send'),
    url(r'send/email/$', send_email_notify, name='email-send'),
)
