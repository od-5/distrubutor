# coding=utf-8
from annoying.decorators import ajax_request
from apps.city.models import City

__author__ = 'alexy'


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