# coding=utf-8
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView
from apps.city.forms import CityForm
from apps.city.models import City
from apps.moderator.forms import ModeratorAreaForm
from apps.moderator.models import ModeratorArea

__author__ = 'alexy'


class CityListView(ListView):
    model = City
    template_name = 'city/city_list.html'

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
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(id=int(self.request.GET.get('city')))
        if self.request.GET.get('moderator'):
            qs = qs.filter(moderator__company__iexact=self.request.GET.get('moderator'))
        return qs

    @csrf_exempt
    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data()
        user = self.request.user
        if user.type == 1:
            qs = City.objects.all()
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
        if self.request.GET.get('moderator'):
            context.update({
                'r_moderator': self.request.GET.get('moderator')
            })

        return context


class CityCreateView(CreateView):
    model = City
    form_class = CityForm
    template_name = 'city/city_add.html'


class CityUpdateView(UpdateView):
    model = City
    form_class = CityForm
    template_name = 'city/city_update.html'

    def get_context_data(self, **kwargs):
        context = super(CityUpdateView, self).get_context_data()
        user = self.request.user
        if user.type != 1:
            if user.type == 2:
                moderator = user.moderator_user

            elif user.type == 5:
                moderator = user.manager_user.moderator
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
        return context

