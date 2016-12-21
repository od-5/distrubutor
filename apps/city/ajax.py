# coding=utf-8
from annoying.decorators import ajax_request
from django.views.decorators.csrf import csrf_exempt
from .models import City

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



