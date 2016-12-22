# coding=utf-8
from django.views.generic import ListView, CreateView, UpdateView
from apps.country.forms import CountryForm
from apps.city.models import Country

__author__ = '2mitrij'


class CountryListView(ListView):
    model = Country
    template_name = 'country/country_list.html'


class CountryCreateView(CreateView):
    model = Country
    form_class = CountryForm
    template_name = 'country/country_add.html'


class CountryUpdateView(UpdateView):
    model = Country
    form_class = CountryForm
    template_name = 'country/country_update.html'
