# coding=utf-8
from django.db.models import Sum
from django.views.generic import ListView, DetailView
from apps.moderator.models import Order

__author__ = 'alexy'


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data()
        pay_qs = self.object_list.filter(pay=True)
        context.update({
            'total_sum': pay_qs.aggregate(Sum('cost'))['cost__sum']
        })
        return context


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'
