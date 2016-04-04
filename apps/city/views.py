# coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView
from apps.city.forms import CityForm
from apps.city.models import City

__author__ = 'alexy'


class CityListView(ListView):
    model = City
    template_name = 'city/city_list.html'

    def get_queryset(self):
        user = self.request.user
        qs = City.objects.all()
        # if user.type == 1:
        #     qs = City.objects.all()
        # elif user.type == 2:
        #     qs = City.objects.filter(moderator=user)
        # elif self.request.user.is_leader_manager():
        #     manager = Manager.objects.get(user=self.request.user)
        #     qs = City.objects.filter(moderator=manager.moderator)
        # else:
        #     qs = None
        # if self.request.GET.get('moderator'):
        #     qs = qs.filter(moderator__email=self.request.GET.get('moderator'))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(id=int(self.request.GET.get('city')))
        return qs

    @csrf_exempt
    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data()
        qs = City.objects.all()
        # if self.request.user.type == 1:
        #     qs = City.objects.all()
        # elif self.request.user.type == 2:
        #     qs = City.objects.filter(moderator=self.request.user.id)
        # else:
        #     qs = None
        context.update({
            'city_list': qs
        })
        # if self.request.GET.get('moderator'):
        #     context.update({
        #         'r_moderator': self.request.GET.get('moderator')
        #     })
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            context.update({
                'r_city': int(self.request.GET.get('city'))
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

