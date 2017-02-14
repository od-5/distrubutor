# coding=utf-8
from django.views.generic import TemplateView

from apps.geolocation.models import Country

__author__ = 'alexy'


class CalculatorTemplateView(TemplateView):
    template_name = 'calculator/calculator.html'

    def get_context_data(self, **kwargs):
        context = super(CalculatorTemplateView, self).get_context_data(**kwargs)
        context.update({
            'country_list': Country.objects.all()
        })
        return context
