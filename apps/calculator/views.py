# coding=utf-8
import os
import datetime
import re
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import HiddenInput
from django.utils.timezone import utc
from django.views.generic import TemplateView
from apps.geolocation.models import Country
from apps.distributor.models import GPSPoint, DistributorTask
from apps.moderator.forms import ReviewForm

__author__ = 'alexy'


class CalculatorTemplateView(TemplateView):
    template_name = 'calculator/calculator.html'

    def get_context_data(self, **kwargs):
        context = super(CalculatorTemplateView, self).get_context_data()
        context.update({
            'country_list': Country.objects.all()
        })
        return context
