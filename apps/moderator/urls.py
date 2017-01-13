# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from .ajax import moderator_review_add, get_action_list, get_cost_by_action
from django.contrib.auth.decorators import login_required
from apps.administrator.decorators import administrator_required
from .views import ModeratorListView, ReviewListView
from core.models import User
from .decorators import blocked

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.moderator.views',
    url(r'^$', login_required(ModeratorListView.as_view()), name='list'),
    url(r'^add/$', 'moderator_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'moderator_user_update', name='update'),
    url(r'^(?P<pk>\d+)/detail/$', 'moderator_detail', name='detail'),
    url(r'^(?P<pk>\d+)/company/$', 'moderator_company_update', name='company'),
    url(r'^(?P<pk>\d+)/action/$', 'moderator_action_update', name='action'),

    # url(r'review/add/$', 'review_add', name='review-add'),
    url(r'review/add/$', moderator_review_add, name='review-add'),
    url(r'review/(?P<pk>\d+)/$', 'review_update', name='review-update'),
    url(r'review/$', blocked(ReviewListView.as_view()), name='review-list'),

    url(r'^area-add/$', 'area_add', name='area-add'),
    url(r'^area/(?P<pk>\d+)/$', 'area_update', name='area-update'),

    url(r'^(?P<pk>\d+)/payment/$', 'payment_list', name='payment-list'),
    url(r'^payment/(?P<pk>\d+)/$', 'payment_detail', name='payment-detail'),

    url(r'^(?P<pk>\d+)/commission/$', 'commission_list', name='commission-list'),
    url(r'^commission/(?P<pk>\d+)/$', 'commission_detail', name='commission-detail'),

    url(r'^get_action_list/$', get_action_list, name='get_action_list'),
    url(r'^get_cost_by_action/$', get_cost_by_action, name='get_cost_by_action'),
)
