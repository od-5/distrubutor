# coding=utf-8
from annoying.decorators import ajax_request

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView
from django.views.generic.base import ContextMixin

from apps.geolocation.models import City, Country, Region
from core.models import Setup

__author__ = 'alexy'


class LandingMixin(ContextMixin):
    """
    Миксин добавляет настройки список стран, регионов, городов в контекст
    """
    def get_context_data(self, **kwargs):
        kwargs = super(LandingMixin, self).get_context_data(**kwargs)
        lang = get_language()
        if lang == 'ru':
            country_qs = Country.objects.select_related().all()
        else:
            country_qs = Country.objects.select_related().filter(code=lang)
        kwargs.update({
            'city_list': City.objects.all(),
            'country_list': country_qs,
            'region_list': Region.objects.all(),
            'SETUP': Setup.objects.first()
        })
        return kwargs


class LandingView(TemplateView, LandingMixin):
    template_name = 'landing/index.html'


class CityDetailView(DetailView, LandingMixin):
    model = City
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        context = super(CityDetailView, self).get_context_data(**kwargs)
        moderator_qs = self.object.moderator_set.filter(site_visible=False,  user__is_active=True,
                                                        superviser__isnull=True)
        context.update({
            'moderator_list': moderator_qs
        })
        return context


@csrf_exempt
def set_current_city_from_input(request):
    if request.POST.get('city'):
        try:
            current_city = City.objects.get(name__iexact=request.POST.get('city'))
            return HttpResponseRedirect(reverse('landing:city', args=(current_city.slug, )))
        except:
            pass
    return HttpResponseRedirect(reverse('landing:index'))
