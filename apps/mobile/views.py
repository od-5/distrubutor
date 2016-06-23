# coding=utf-8
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import date, datetime
from annoying.decorators import ajax_request
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from apps.distributor.models import PointPhoto

__author__ = 'alexy'


class GPSPointListView(ListView):
    model = PointPhoto
    template_name = 'mobile/point_list.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        qs = PointPhoto.objects.all()
        return qs
