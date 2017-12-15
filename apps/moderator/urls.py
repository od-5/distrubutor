# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from apps.administrator.decorators import administrator_required
from .ajax import moderator_review_add, get_action_list, get_cost_by_action
from .views import ModeratorListView, ReviewListView, OrderListView, OrderDetailView, ModeratorCreateView,\
    ModeratorUserUpdateView, ModeratorDetailView, ModeratorCompanyUpdateView, AreaUpdateView, ReviewUpdateView,\
    PaymentListView, PaymentDetailView, CommissionListView, CommissionDetailView, moderator_action_update, area_add, \
    OrderCreateView, OrderUpdateView
from .decorators import blocked

__author__ = 'alexy'

urlpatterns = patterns(
    '',
    url(r'^$', login_required(ModeratorListView.as_view()), name='list'),
    url(r'^add/$', administrator_required(ModeratorCreateView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/$', login_required(ModeratorUserUpdateView.as_view()), name='update'),
    url(r'^(?P<pk>\d+)/detail/$', login_required(ModeratorDetailView.as_view()), name='detail'),
    url(r'^(?P<pk>\d+)/company/$', login_required(ModeratorCompanyUpdateView.as_view()), name='company'),
    url(r'^(?P<pk>\d+)/action/$', moderator_action_update, name='action'),

    url(r'review/add/$', moderator_review_add, name='review-add'),
    url(r'review/(?P<pk>\d+)/$', login_required(ReviewUpdateView.as_view()), name='review-update'),
    url(r'review/$', blocked(ReviewListView.as_view()), name='review-list'),

    url(r'^area-add/$', area_add, name='area-add'),
    url(r'^area/(?P<pk>\d+)/$', login_required(AreaUpdateView.as_view()), name='area-update'),

    url(r'^(?P<pk>\d+)/payment/$', login_required(PaymentListView.as_view()), name='payment-list'),
    url(r'^payment/(?P<pk>\d+)/$', login_required(PaymentDetailView.as_view()), name='payment-detail'),

    url(r'^(?P<pk>\d+)/commission/$', login_required(CommissionListView.as_view()), name='commission-list'),
    url(r'^commission/(?P<pk>\d+)/$', login_required(CommissionDetailView.as_view()), name='commission-detail'),

    url(r'^get_action_list/$', get_action_list, name='get_action_list'),
    url(r'^get_cost_by_action/$', get_cost_by_action, name='get_cost_by_action'),

    url(r'^order/$', administrator_required(OrderListView.as_view()), name='order-list'),
    url(r'^order/add/$', administrator_required(OrderCreateView.as_view()), name='order-add'),
    url(r'^order/(?P<pk>\d+)/update/$', administrator_required(OrderUpdateView.as_view()), name='order-update'),
    url(r'^order/(?P<pk>\d+)/$', administrator_required(OrderDetailView.as_view()), name='order-detail'),
)
