# coding=utf-8
from django.views.generic import ListView, DetailView
from apps.moderator.models import Order

__author__ = 'alexy'


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'
