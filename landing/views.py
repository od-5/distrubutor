# coding=utf-8
from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.conf import settings
from apps.geolocation.models import City, Country
from apps.moderator.models import Moderator
from core.models import Setup

__author__ = 'alexy'


class LandingView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        # print self.request.META['LANG']
        lang = get_language()
        if lang == 'ru':
            country_qs = Country.objects.select_related().all()
        else:
            country_qs = Country.objects.select_related().filter(code=lang)
        try:
            # self.request.session['current_city']
            current_city = City.objects.get(pk=int(self.request.session['current_city']))
            if lang != 'ru':
                if current_city.country.code != lang:
                    current_city = None
                    self.request.session['current_city'] = None
                    moderator_qs = None
                else:
                    # fixme: пока не наберётся команда стабильно работающих исполнителей - показывать всё равно
                    # неоплативших на сайте. Заказами займётся рекламное агенство. Продумать как автоматизировать
                    # moderator_qs = current_city.moderator_set.filter(
                    #     site_visible=False, deny_access=False, user__is_active=True, superviser__isnull=True)
                    moderator_qs = current_city.moderator_set.filter(
                        site_visible=False, user__is_active=True, superviser__isnull=True)
            else:
                # fixme: пока не наберётся команда стабильно работающих исполнителей - показывать всё равно
                # неоплативших на сайте. Заказами займётся рекламное агенство. Продумать как автоматизировать
                moderator_qs = current_city.moderator_set.filter(
                    site_visible=False,  user__is_active=True, superviser__isnull=True)
                # moderator_qs = current_city.moderator_set.filter(
                #     site_visible=False, deny_access=False, user__is_active=True, superviser__isnull=True)
        except:
            current_city = None
            moderator_qs = None
            self.request.session['current_city'] = None
        # current_city = City.objects.get(pk=int(self.request.session['current_city']))
        setup = Setup.objects.first()
        context = {
            'country_list': country_qs,
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
