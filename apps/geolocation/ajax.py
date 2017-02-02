# coding=utf-8
from django.views.decorators.csrf import csrf_exempt

from annoying.decorators import ajax_request

from .models import City
from apps.moderator.models import Moderator

__author__ = '2mitrij'


@csrf_exempt
@ajax_request
def find_city(request):
    if request.GET.get('name_startsWith'):
        name_startsWith = request.GET.get('name_startsWith')
        city_list = []
        city_qs = City.objects.filter(name__icontains=name_startsWith)
        for city in city_qs:
            city_list.append({
                'name': city.name
            })
        return {
            'city_list': city_list
        }
    return {
        'success': True
    }


@ajax_request
def get_moderator_list(request):
    r_city = request.GET.get('city', '')
    if r_city and r_city.isdigit():
        moderator_qs = Moderator.objects.filter(city__id=int(r_city))
        return {
            'success': True,
            'moderator_list': [
                {
                    'id': item.id,
                    'name': item.company
                } for item in moderator_qs
            ]
        }

    return {
        'success': False
    }


@ajax_request
def get_city_list(request):
    r_country = request.GET.get('country') or ''
    city_list = []
    if r_country and r_country.isdigit():
        city_qs = City.objects.filter(country__id=int(r_country))
        for city in city_qs:
            city_list.append({
                'id': city.id,
                'name': city.name
            })
        return {
            'success': True,
            'city_list': city_list
        }
    return {
        'success': False
    }
