# coding=utf-8
from django.views.generic import UpdateView, ListView, CreateView
from .forms import PackageForm
from .models import Package

__author__ = 'alexy'


class PackageListView(ListView):
    model = Package
    template_name = 'payment/package_list.html'


class PackageAddView(CreateView):
    model = Package
    form_class = PackageForm
    template_name = 'payment/package_add.html'


class PackageUpdateView(UpdateView):
    model = Package
    form_class = PackageForm
    template_name = 'payment/package_update.html'

