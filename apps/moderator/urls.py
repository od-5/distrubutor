# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from .ajax import moderator_review_add
from .views import ModeratorListView, ReviewListView
from core.models import User

__author__ = 'alexy'

urlpatterns = patterns(
    'apps.moderator.views',
    url(r'^$', ModeratorListView.as_view(), name='list'),
    url(r'^add/$', 'moderator_add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'moderator_user_update', name='update'),
    url(r'^(?P<pk>\d+)/company/$', 'moderator_company_update', name='company'),
    url(r'^(?P<pk>\d+)/action/$', 'moderator_action_update', name='action'),

    # url(r'review/add/$', 'review_add', name='review-add'),
    url(r'review/add/$', moderator_review_add, name='review-add'),
    url(r'review/(?P<pk>\d+)/$', 'review_update', name='review-update'),
    url(r'review/$', ReviewListView.as_view(), name='review-list'),

    url(r'^area-add/$', 'area_add', name='area-add'),
    url(r'^area/(?P<pk>\d+)/$', 'area_update', name='area-update'),

    url(r'^(?P<pk>\d+)/payment/$', 'payment_list', name='payment-list'),
    url(r'^payment/(?P<pk>\d+)/$', 'payment_detail', name='payment-detail'),
)
