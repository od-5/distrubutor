# coding=utf-8
from annoying.decorators import ajax_request
from django.views.decorators.csrf import csrf_exempt
from .models import City
from apps.moderator.models import Moderator

__author__ = 'alexy'


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
