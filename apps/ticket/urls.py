# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import TicketListView, TicketAgencyListView, TicketSaleListView, PreSaleListView
from .ajax import hanger_ticket, promo_ticket

__author__ = 'alexy'


urlpatterns = patterns(
    'apps.ticket.views',
    url(r'^$', 'ticket_send', name='send'),
    url(r'^list/$', login_required(TicketListView.as_view()), name='list'),
    url(r'^agency/$', login_required(TicketAgencyListView.as_view()), name='agency'),
    url(r'^sale/$', login_required(TicketSaleListView.as_view()), name='sale'),
    url(r'^add/$', 'ticket_add', name='add'),
    url(r'^presale/add/(?P<pk>\d+)/$', 'presale_add', name='presale-add'),
    url(r'^presale/(?P<pk>\d+)/$', 'presale_update', name='presale-update'),
    url(r'^presale/info/(?P<pk>\d+)/$', 'presale_detail', name='presale-detail'),
    url(r'^presale/$', login_required(PreSaleListView.as_view()), name='presale-list'),
    url(r'^(?P<pk>\d+)/$', 'ticket_detail', name='detail'),
    # hanger-reklama.com url
    url(r'^hanger/$', hanger_ticket, name='hanger'),
    url(r'^promo/$', promo_ticket, name='promo'),
)
