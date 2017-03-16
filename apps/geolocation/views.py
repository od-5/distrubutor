# coding=utf-8
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView

from .models import City, Region, Country
from .forms import CityForm, RegionForm, CountryForm
from apps.moderator.forms import ModeratorAreaForm
from apps.moderator.models import ModeratorArea

__author__ = '2mitrij'


class CityListView(ListView):
    model = City
    template_name = 'geolocation/city_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = City.objects.select_related('moderator').all()
        elif user.type == 2:
            qs = user.moderator_user.city.all()
        elif user.type == 5:
            qs = user.manager_user.moderator.moderator_user.city.all()
        else:
            qs = None
        if self.request.GET.get('country') and int(self.request.GET.get('country')) != 0:
            qs = qs.filter(country=int(self.request.GET.get('country')))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(id=int(self.request.GET.get('city')))
        if self.request.GET.get('moderator'):
            qs = qs.filter(moderator__company__iexact=self.request.GET.get('moderator'))
        return qs

    @csrf_exempt
    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.type == 1:
            qs = City.objects.all()
            context.update({
                'country_list': Country.objects.all()
            })
        elif user.type == 2:
            qs = user.moderator_user.city.all()
        elif user.type == 5:
            qs = user.manager_user.moderator.moderator_user.city.all()
        else:
            qs = None
        context.update({
            'city_list': qs
        })
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            context.update({
                'r_city': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('country') and int(self.request.GET.get('country')) != 0:
            context.update({
                'r_country': int(self.request.GET.get('country'))
            })
        if self.request.GET.get('moderator'):
            context.update({
                'r_moderator': self.request.GET.get('moderator')
            })

        return context


class CityCreateView(CreateView):
    model = City
    form_class = CityForm
    template_name = 'geolocation/city_add.html'


class CityUpdateView(UpdateView):
    model = City
    form_class = CityForm
    template_name = 'geolocation/city_update.html'

    def get_context_data(self, **kwargs):
        context = super(CityUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.type != 1:
            if user.type == 2:
                moderator = user.moderator_user
            elif user.type == 5:
                moderator = user.manager_user.moderator.moderator_user
            else:
                moderator = None
            area_qs = ModeratorArea.objects.filter(city=self.object, moderator=moderator)
            initial = {
                'moderator': moderator,
                'city': self.object
            }
            areaform = ModeratorAreaForm(initial=initial)
            context.update({
                'areaform': areaform,
                'area_list': area_qs
            })
        else:
            context.update({
                'form': CityForm(instance=self.object)
            })
        return context


class RegionListView(ListView):
    model = Region
    template_name = 'geolocation/region_list.html'

    def get_queryset(self):
        qs = super(RegionListView, self).get_queryset()

        self.r_country = int(self.request.GET.get('country', 0))
        if self.r_country:
            qs = qs.filter(country=self.r_country)

        return qs

    def get_context_data(self, **kwargs):
        context = super(RegionListView, self).get_context_data(**kwargs)
        context['r_country'] = self.r_country
        context['country_list'] = Country.objects.all()
        return context


class RegionCreateView(CreateView):
    form_class = RegionForm
    template_name = 'geolocation/region_add.html'


class RegionUpdateView(UpdateView):
    model = Region
    form_class = RegionForm
    template_name = 'geolocation/region_update.html'


class CountryListView(ListView):
    model = Country
    template_name = 'geolocation/country_list.html'


class CountryCreateView(CreateView):
    model = Country
    form_class = CountryForm
    template_name = 'geolocation/country_add.html'


class CountryUpdateView(UpdateView):
    model = Country
    form_class = CountryForm
    template_name = 'geolocation/country_update.html'
