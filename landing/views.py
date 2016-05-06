# coding=utf-8
from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.conf import settings
from apps.city.models import City, Country
from apps.moderator.models import Moderator
from core.models import Setup

__author__ = 'alexy'


class LandingView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        # print self.request.META['LANG']
        try:
            # self.request.session['current_city']
            current_city = City.objects.get(pk=int(self.request.session['current_city']))
            moderator_qs = current_city.moderator_set.all()
        except:
            current_city = City.objects.first()
            moderator_qs = Moderator.objects.all()
            self.request.session['current_city'] = None
        # current_city = City.objects.get(pk=int(self.request.session['current_city']))
        setup = Setup.objects.first()
        context = {
            'country_list': Country.objects.select_related().all(),
            'city_list': City.objects.all(),
            'moderator_list': moderator_qs,
            # 'moderator_list': Moderator.objects.all(),
            'current_city': current_city,
            'SETUP': setup
        }
        return context


@csrf_exempt
@ajax_request
def set_current_city(request):
    if request.POST.get('city'):
        try:
            current_city = City.objects.get(name__iexact=request.POST.get('city'))
            request.session['current_city'] = current_city.id
        except:
            current_city = None
            request.session['current_city'] = None
    return {
        'success': True
    }


@csrf_exempt
def set_current_city_from_input(request):
    if request.POST.get('city'):
        try:
            current_city = City.objects.get(name__iexact=request.POST.get('city'))
            request.session['current_city'] = current_city.id
        except:
            pass
    return HttpResponseRedirect(reverse('landing:index'))
